"""Mix narration + music + sfx: gain-stage by loudness, duck music under the voice,
then two-pass EBU R128 normalisation with ffmpeg to the series target (-14 LUFS, -1.5 dBTP).

Usage: python pipeline/mix.py ep01  ->  public/<ep>/mix.wav + public/<ep>/mix_report.json
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import butter, sosfilt

from common import SR, load_series, out_dir

VOICE_LUFS = -18.0
MUSIC_LUFS = -31.0   # before ducking; ~13 LU under the voice
SFX_LUFS = -30.0
DUCK_DB = -7.0       # extra music reduction while the narrator speaks


def stereo(x):
    return np.stack([x, x], axis=1) if x.ndim == 1 else x


def gain_to(x, target, meter):
    return x * 10 ** ((target - meter.integrated_loudness(x)) / 20)


def duck_curve(voice, attack=0.04, release=0.45):
    """Smoothed 0..1 'voice present' envelope -> per-sample music gain."""
    mono = np.abs(voice).mean(axis=1)
    sos = butter(2, 12, "low", fs=SR, output="sos")
    level = sosfilt(sos, mono)
    present = (level > level.max() * 0.04).astype(float)
    out = np.zeros_like(present)
    a, r = np.exp(-1 / (attack * SR)), np.exp(-1 / (release * SR))
    prev = 0.0
    for i, p in enumerate(present):
        coef = a if p > prev else r
        prev = coef * prev + (1 - coef) * p
        out[i] = prev
    return 10 ** (DUCK_DB * out / 20)


def ffmpeg_loudnorm(src, dst, target, tp):
    base = f"loudnorm=I={target}:TP={tp}:LRA=11"
    probe = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af", base + ":print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True, check=True).stderr
    m = json.loads(re.search(r"\{[^{}]+\}", probe[probe.rfind("[Parsed_loudnorm"):], re.S).group(0))
    second = (f"{base}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
              f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src), "-af", second,
                    "-ar", str(SR), "-c:a", "pcm_s16le", str(dst)], check=True)
    return m


def main():
    ep_id = sys.argv[1]
    d = out_dir(ep_id)
    audio_cfg = load_series()["audio"]
    meter = pyln.Meter(SR)

    voice, _ = sf.read(d / "narration.wav")
    music, _ = sf.read(d / "music.wav")
    sfx, _ = sf.read(d / "sfx.wav")
    n = len(voice)
    voice = stereo(voice)
    music, sfx = (np.pad(x[:n], ((0, max(0, n - len(x))), (0, 0))) for x in (music, sfx))

    voice = gain_to(voice, VOICE_LUFS, meter)
    music = gain_to(music, MUSIC_LUFS, meter) * duck_curve(voice)[:, None]
    sfx = gain_to(sfx, SFX_LUFS, meter)
    premix = voice + music + sfx
    sf.write(d / "premix.wav", premix.astype(np.float32), SR, subtype="FLOAT")

    measured = ffmpeg_loudnorm(d / "premix.wav", d / "mix.wav", audio_cfg["targetLufs"], audio_cfg["truePeak"])
    (d / "premix.wav").unlink()

    final, _ = sf.read(d / "mix.wav")
    report = {
        "integratedLufs": round(meter.integrated_loudness(final), 2),
        "samplePeakDb": round(20 * np.log10(np.abs(final).max() + 1e-12), 2),
        "voiceOverMusicLu": round(meter.integrated_loudness(voice) - meter.integrated_loudness(music), 1),
        "durationSec": round(len(final) / SR, 3),
        "ffmpegFirstPass": measured,
    }
    (d / "mix_report.json").write_text(json.dumps(report, indent=1))
    print(f"[mix] {report['integratedLufs']} LUFS, peak {report['samplePeakDb']} dBFS, voice/music {report['voiceOverMusicLu']} LU")


if __name__ == "__main__":
    main()
