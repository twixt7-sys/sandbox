"""Subtitle file from the verified word timings. Usage: python pipeline/srt.py ep05 [--burned-only]

Groups words exactly like the burned-in captions (src/captions/Captions.tsx: buildGroups): at most
20 characters per line, a new group after a pause > 0.28 s or a phrase-ending comma/period, and
each group held until the next begins. Two consecutive groups from the same sentence share a cue as a
two-line subtitle (each line is exactly one burned-in caption), so cues stay on screen long enough to read.

By default every line is included, also those spoken over a shot with `"captions": false` (the CTA card
shows that line as type instead of captions), so the SRT carries the complete narration.
`--burned-only` matches the burned-in captions exactly. Writes out/<ep>.srt.
"""
import json
import re
import sys
from pathlib import Path

from common import load_episode, out_dir

MAX_CHARS = 20
ROOT = Path(__file__).resolve().parent.parent


def groups(timing: dict, ep: dict, burned_only: bool) -> list[dict]:
    off = {s["id"] for s in ep["shots"] if s.get("captions") is False} if burned_only else set()
    replace = ep.get("captionReplace", {})
    out = []
    for line in timing["lines"]:
        if line["shot"] in off:
            continue
        cur: list[dict] = []

        def flush():
            if cur:
                out.append({"words": list(cur), "start": cur[0]["start"], "end": cur[-1]["end"]})
                cur.clear()

        for i, w in enumerate(line["words"]):
            bare = re.sub(r"[.,;:]+$", "", w["text"])
            text = replace.get(bare.lower(), bare)
            length = sum(len(c["text"]) + 1 for c in cur)
            gap = w["start"] - cur[-1]["end"] if cur else 0
            if cur and (length + len(text) > MAX_CHARS or gap > 0.28):
                flush()
            # Subtitles keep the spoken punctuation that the burned-in captions drop.
            cur.append({"text": text, "full": w["text"], "start": w["start"], "end": w["end"]})
            if re.search(r"[.,;:!?]$", w["text"]) and i < len(line["words"]) - 1:
                flush()
        flush()
    for i, g in enumerate(out):
        nxt = out[i + 1] if i + 1 < len(out) else None
        g["hold"] = nxt["start"] - 0.03 if nxt and nxt["start"] - g["end"] < 0.6 else g["end"] + 0.35
        g["start"] = max(0.0, g["start"] - 0.08)
    return out


def stamp(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    ep_id = sys.argv[1]
    burned_only = "--burned-only" in sys.argv
    ep = load_episode(ep_id)
    timing = json.loads((out_dir(ep_id) / "timing.json").read_text())
    gs = groups(timing, ep, burned_only)
    # Pair groups into two-line cues within a sentence (never across . ? !).
    pairs, i = [], 0
    while i < len(gs):
        a = gs[i]
        b = gs[i + 1] if i + 1 < len(gs) else None
        if b and not re.search(r"[.?!]$", a["words"][-1]["full"]) and b["hold"] - a["start"] <= 3.5:
            pairs.append({"lines": [a, b], "start": a["start"], "end": b["hold"]})
            i += 2
        else:
            pairs.append({"lines": [a], "start": a["start"], "end": a["hold"]})
            i += 1
    cues = []
    for n, c in enumerate(pairs, 1):
        nxt = pairs[n] if n < len(pairs) else None
        end = min(c["end"], nxt["start"] - 0.02 if nxt else timing["duration"], timing["duration"])
        text = "\n".join(" ".join(w["full"] for w in g["words"]) for g in c["lines"])
        cues.append(f"{n}\n{stamp(c['start'])} --> {stamp(end)}\n{text}\n")
    dest = ROOT / "out" / f"{ep_id}.srt"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text("\n".join(cues), encoding="utf-8")
    print(f"[srt] {len(cues)} cues -> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
