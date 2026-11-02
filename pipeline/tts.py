"""Narration: synthesize each line, trim, assemble with scripted pauses, emit word timings.

Providers
  kokoro      Kokoro-82M (Apache-2.0), runs on CPU in the cloud runner. No key needed.
  elevenlabs  ElevenLabs /with-timestamps endpoint. Needs ELEVENLABS_API_KEY.

Usage: python pipeline/tts.py ep01 [--provider elevenlabs]
Outputs public/<ep>/narration.wav (48 kHz mono) and public/<ep>/timing.json.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import time
import urllib.request

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

from common import SR, load_episode, out_dir, resolve_cue

TRIM_DB = -42.0
PAD_IN, PAD_OUT = 0.03, 0.07


def _words_from_spans(spans: list[tuple[str, float, float]]) -> list[dict]:
    """Merge punctuation-only spans into the preceding word."""
    words: list[dict] = []
    for text, start, end in spans:
        if not re.search(r"[A-Za-z0-9]", text):
            if words:
                words[-1]["text"] += text
            continue
        words.append({"text": text, "start": float(start), "end": float(end)})
    return words


def synth_kokoro(lines: list[dict], cfg: dict):
    from kokoro import KPipeline  # heavy import, only when used

    pipe = KPipeline(lang_code=cfg.get("lang", "a"), repo_id="hexgrad/Kokoro-82M")
    for line in lines:
        chunks, spans, t0 = [], [], 0.0
        for r in pipe(line["text"], voice=cfg["voice"], speed=cfg.get("speed", 1.0)):
            audio = r.audio.numpy().astype(np.float32)
            for tok in r.tokens:
                if tok.start_ts is None:
                    continue
                spans.append((tok.text, t0 + tok.start_ts, t0 + (tok.end_ts or tok.start_ts)))
            chunks.append(audio)
            t0 += len(audio) / 24000
        audio = resample_poly(np.concatenate(chunks), 2, 1).astype(np.float32)
        yield audio, _words_from_spans(spans)


def synth_elevenlabs(lines: list[dict], cfg: dict):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set. Add it as an environment secret, or use --provider kokoro.")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voiceId']}/with-timestamps?output_format=pcm_24000"
    for i, line in enumerate(lines):
        body = {
            "text": line["text"],
            "model_id": cfg.get("model", "eleven_multilingual_v2"),
            "voice_settings": cfg.get("settings", {}),
            # Neighbouring lines keep prosody continuous across separately generated lines.
            "previous_text": lines[i - 1]["text"] if i else None,
            "next_text": lines[i + 1]["text"] if i + 1 < len(lines) else None,
        }
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                     headers={"xi-api-key": key, "Content-Type": "application/json"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read())
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2 ** (attempt + 1))
        pcm = np.frombuffer(base64.b64decode(data["audio_base64"]), dtype=np.int16).astype(np.float32) / 32768
        al = data["alignment"]
        spans, cur, cs = [], "", None
        for ch, s, e in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
            if ch.isspace():
                if cur:
                    spans.append((cur, cs, prev_e))
                cur, cs = "", None
                continue
            if cs is None:
                cs = s
            cur += ch
            prev_e = e
        if cur:
            spans.append((cur, cs, prev_e))
        yield resample_poly(pcm, 2, 1).astype(np.float32), _words_from_spans(spans)


def trim(audio: np.ndarray, words: list[dict]):
    level = 20 * np.log10(np.abs(audio) + 1e-9)
    idx = np.where(level > TRIM_DB)[0]
    a = max(0, idx[0] - int(PAD_IN * SR))
    b = min(len(audio), idx[-1] + int(PAD_OUT * SR))
    shift = a / SR
    for w in words:
        w["start"] = max(0.0, w["start"] - shift)
        w["end"] = max(w["start"], w["end"] - shift)
    return audio[a:b], words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--provider")
    args = ap.parse_args()

    ep = load_episode(args.episode)
    provider = args.provider or ep["voice"]["provider"]
    lines = ep["lines"]
    gen = synth_kokoro(lines, ep["voice"]["kokoro"]) if provider == "kokoro" else synth_elevenlabs(lines, ep["voice"]["elevenlabs"])

    tm = ep["timing"]
    out = [np.zeros(int(tm["leadIn"] * SR), np.float32)]
    t = tm["leadIn"]
    timed_lines = []
    for line, (audio, words) in zip(lines, gen):
        audio, words = trim(audio, words)
        for w in words:
            w["start"] = round(t + w["start"], 3)
            w["end"] = round(t + w["end"], 3)
        dur = len(audio) / SR
        timed_lines.append({"id": line["id"], "shot": line["shot"], "text": line["text"],
                            "start": round(t, 3), "end": round(t + dur, 3), "words": words,
                            "emphasis": line.get("emphasis", [])})
        out.append(audio)
        pause = line.get("pauseAfter", 0.3)
        out.append(np.zeros(int(pause * SR), np.float32))
        t += dur + pause
    out.append(np.zeros(int(tm["tail"] * SR), np.float32))
    narration = np.concatenate(out)
    total = len(narration) / SR

    # Shots start a beat before their first line so the picture cuts ahead of the voice.
    # `startAt` (a word cue) cuts mid-line instead, e.g. from the wide town to a close-up on "to make it believable".
    shots = []
    for s in ep["shots"]:
        first = next((l for l in timed_lines if l["shot"] == s["id"]), None)
        if s.get("startAt"):
            start = max(0.0, resolve_cue(s["startAt"], {"lines": timed_lines, "shots": []}) - tm["shotLead"])
        else:
            start = 0.0 if not shots else max(0.0, first["start"] - tm["shotLead"])
        shots.append({"id": s["id"], "start": round(start, 3)})
    for i, s in enumerate(shots):
        s["end"] = shots[i + 1]["start"] if i + 1 < len(shots) else round(total, 3)

    d = out_dir(ep["id"])
    sf.write(d / "narration.wav", narration, SR, subtype="PCM_16")
    timing = {"episode": ep["id"], "provider": provider, "duration": round(total, 3),
              "lines": timed_lines, "shots": shots}
    (d / "timing.json").write_text(json.dumps(timing, indent=1))
    speech = sum(l["end"] - l["start"] for l in timed_lines)
    words = sum(len(l["words"]) for l in timed_lines)
    print(f"[tts] {provider}: {words} words, speech {speech:.2f}s, total {total:.2f}s")
    for s in shots:
        print(f"  {s['id']:<9} {s['start']:6.2f} -> {s['end']:6.2f}")


if __name__ == "__main__":
    main()
