"""Automated QA on a rendered MP4. Exits non-zero if a critical check fails.

Usage: python pipeline/qa.py out/ep01.mp4 [--sheet out/ep01_sheet.jpg]

Checks: container plays end-to-end (full decode), 1080x1920 @ 30 fps, duration in the episode's window
(episode.json -> format.qa {min, max}, e.g. 55-62 s for Season 2; 27-33 s when absent, as for EP01-EP25),
audio present, integrated loudness and true peak, no black gaps, no frozen video,
no audio dropouts mid-narration. Writes a JSON report next to the video and an
optional contact sheet of representative frames (incl. the last frame) for visual review.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def episode_id(v: Path):
    m = re.search(r"(ep\d+)", v.name)
    return m.group(1) if m else None


def window(ep_id):
    """Duration window from the episode (format.qa); 27-33 s when the episode doesn't set one (EP01-EP25)."""
    if ep_id:
        f = Path(__file__).resolve().parent.parent / "episodes" / ep_id / "episode.json"
        if f.exists():
            q = json.loads(f.read_text()).get("format", {}).get("qa", {})
            return float(q.get("min", 27.0)), float(q.get("max", 33.0))
    return 27.0, 33.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--sheet")
    ap.add_argument("--min", type=float, default=None)
    ap.add_argument("--max", type=float, default=None)
    ap.add_argument("--episode", help="episode id for the duration window (default: from the file name, e.g. out/ep26_compat.mp4)")
    args = ap.parse_args()
    v = Path(args.video)
    checks = {}
    lo, hi = window(args.episode or episode_id(v))
    args.min = lo if args.min is None else args.min
    args.max = hi if args.max is None else args.max

    probe = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(v)]).stdout)
    vs = next(s for s in probe["streams"] if s["codec_type"] == "video")
    aud = [s for s in probe["streams"] if s["codec_type"] == "audio"]
    dur = float(probe["format"]["duration"])
    num, den = map(int, vs["r_frame_rate"].split("/"))
    checks["resolution_1080x1920"] = (vs["width"], vs["height"]) == (1080, 1920)
    checks["fps_30"] = abs(num / den - 30) < 0.01
    checks["duration_ok"] = args.min <= dur <= args.max
    checks["h264_yuv420p"] = vs["codec_name"] == "h264" and vs.get("pix_fmt") == "yuv420p"
    checks["audio_present"] = bool(aud) and aud[0]["codec_name"] == "aac"

    decode = run(["ffmpeg", "-v", "error", "-i", str(v), "-f", "null", "-"])
    checks["decodes_without_errors"] = decode.returncode == 0 and not decode.stderr.strip()

    black = run(["ffmpeg", "-i", str(v), "-vf", "blackdetect=d=0.25:pix_th=0.06", "-an", "-f", "null", "-"]).stderr
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", black)
    checks["no_black_gaps"] = not blacks

    freeze = run(["ffmpeg", "-i", str(v), "-vf", "freezedetect=n=0.0005:d=1.2", "-an", "-f", "null", "-"]).stderr
    freezes = re.findall(r"freeze_start: ([\d.]+)", freeze)
    checks["no_frozen_video"] = not freezes

    loud = run(["ffmpeg", "-i", str(v), "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"]).stderr
    summary = loud[loud.rfind("Summary:"):]
    lufs = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary).group(1))
    checks["loudness_-16_to_-12_lufs"] = -16 <= lufs <= -12
    checks["true_peak_below_-1db"] = tp <= -1.0

    silence = run(["ffmpeg", "-i", str(v), "-af", "silencedetect=n=-45dB:d=1.2", "-vn", "-f", "null", "-"]).stderr
    silences = [(float(a), float(b)) for a, b in re.findall(r"silence_start: ([\d.]+).*?silence_end: ([\d.]+)", silence, re.S)]
    # Only the very end may go quiet (loop fade); a long silence before that means a dropout.
    checks["no_audio_dropouts"] = all(s >= dur - 2.0 for s, _ in silences)

    report = {"file": str(v), "durationWindow": [args.min, args.max], "durationSec": round(dur, 3), "integratedLufs": lufs, "truePeakDb": tp,
              "blackSegments": blacks, "freezeStarts": freezes, "silences": silences, "checks": checks,
              "passed": all(checks.values())}
    v.with_suffix(".qa.json").write_text(json.dumps(report, indent=1))

    if args.sheet:
        times = [0.5, 2.5, 4.8, 8.0, 11.5, 14.5, 17.3, 19.8, 23.0, 26.5, dur - 1.2, None]
        if dur > 40:  # longer formats (Season 2): spread the first ten tiles evenly instead
            times = [0.5] + [round(dur * k / 10, 2) for k in range(1, 10)] + [dur - 1.2, None]
        tiles = []
        for i, t in enumerate(times):
            f = v.parent / f".sheet_{i}.jpg"
            # None = the very last frame (seek from the end; seeking to dur-ε can return nothing).
            seek = ["-sseof", "-0.2"] if t is None else ["-ss", f"{t:.2f}"]
            keep = ["-update", "1"] if t is None else ["-frames:v", "1"]  # last frame: keep overwriting until EOF
            run(["ffmpeg", "-y", "-v", "error", *seek, "-i", str(v), *keep, "-vf", "scale=360:-1", str(f)])
            tiles.append(f)
        inputs = sum((["-i", str(f)] for f in tiles), [])
        grid = "".join(f"[{i}]" for i in range(len(tiles))) + f"xstack=inputs={len(tiles)}:layout=" + "|".join(f"{(i % 6) * 360}_{(i // 6) * 640}" for i in range(len(tiles)))
        res = run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", grid, args.sheet])
        if res.returncode:
            print(f"[qa] contact sheet failed: {res.stderr.strip()[:300]}")
        for f in tiles:
            f.unlink(missing_ok=True)

    for k, ok in checks.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {k}")
    print(f"[qa] {dur:.2f}s, {lufs} LUFS, TP {tp} dB -> {'PASSED' if report['passed'] else 'FAILED'}")
    sys.exit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
