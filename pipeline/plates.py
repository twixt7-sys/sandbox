"""Background plates: AI stills (and optional image-to-video clips) for each shot's `imagePrompt`.

Dry-run by default: prints what would be generated and the estimated cost, spends nothing.

  python pipeline/plates.py ep01                      # quote only
  python pipeline/plates.py ep01 --yes                # generate stills (Runway gen4_image, ~$0.08 each)
  python pipeline/plates.py ep01 --yes --video hook,lanterns   # + 5 s gen4_turbo clips for those shots
  python pipeline/plates.py ep01 --register           # you dropped PNG/JPG/MP4 files in episodes/<ep>/plates/ by hand
                                                      # (e.g. stills made with Figma generate_image or any other tool)

Needs RUNWAYML_API_SECRET for generation. Writes episodes/<ep>/plates.json (shot id -> file).
Shots without a plate keep their procedural scene, so partial plates are fine.
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import os
import time
import urllib.request

from common import ROOT, load_episode, load_series, out_dir

API = "https://api.dev.runwayml.com/v1"
HEADERS = {"X-Runway-Version": "2024-11-06", "Content-Type": "application/json"}
# Published API prices (docs.dev.runwayml.com/guides/pricing, checked 2026-10-19): $0.01/credit.
COST = {"gen4_image": 0.08, "gen4_turbo_per_sec": 0.05}
TIMEOUT = 600


def _req(method, path, body=None):
    key = os.environ.get("RUNWAYML_API_SECRET")
    if not key:
        raise SystemExit("RUNWAYML_API_SECRET is not set (Runway developer portal -> API keys).")
    req = urllib.request.Request(f"{API}{path}", method=method, data=json.dumps(body).encode() if body else None,
                                 headers={**HEADERS, "Authorization": f"Bearer {key}"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(2 ** (attempt + 2))
                continue
            raise SystemExit(f"Runway {method} {path} -> {e.code}: {e.read().decode()[:400]}")


def _wait(task_id):
    t0 = time.time()
    while time.time() - t0 < TIMEOUT:
        task = _req("GET", f"/tasks/{task_id}")
        if task["status"] == "SUCCEEDED":
            return task["output"][0]
        if task["status"] in ("FAILED", "CANCELLED"):
            raise SystemExit(f"task {task_id} {task['status']}: {task.get('failure')}")
        time.sleep(5)
    raise SystemExit(f"task {task_id} timed out after {TIMEOUT}s")


def _download(url, dest):
    with urllib.request.urlopen(url, timeout=120) as r:  # output URLs are short-lived: fetch immediately
        dest.write_bytes(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--yes", action="store_true", help="actually call the paid API")
    ap.add_argument("--video", default="", help="comma-separated shot ids to animate with image-to-video")
    ap.add_argument("--only", default="", help="comma-separated shot ids to (re)generate")
    ap.add_argument("--register", action="store_true", help="index files already in episodes/<ep>/plates/")
    args = ap.parse_args()

    ep = load_episode(args.episode)
    series = load_series()
    pdir = ROOT / "episodes" / ep["id"] / "plates"  # committed with the episode; build.sh copies to public/
    pdir.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT / "episodes" / ep["id"] / "plates.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    if args.register:
        for f in sorted(pdir.iterdir()):
            if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".mp4"):
                manifest[f.stem] = f"plates/{f.name}"
        manifest_path.write_text(json.dumps(manifest, indent=1))
        print(json.dumps(manifest, indent=1))
        return

    only = set(filter(None, args.only.split(",")))
    video = set(filter(None, args.video.split(",")))
    todo = [s for s in ep["shots"] if s.get("imagePrompt") and s.get("plate", True) and (not only or s["id"] in only)]
    # Clips must cover the whole shot (plus its transition-in), so size them from the narration timing.
    tpath = out_dir(ep["id"]) / "timing.json"
    spans = {s["id"]: s for s in json.loads(tpath.read_text())["shots"]} if tpath.exists() else {}

    def clip_seconds(shot_id):
        span = spans.get(shot_id)
        return 5 if not span else max(2, min(10, math.ceil(span["end"] - span["start"] + 1.0)))

    cost = len(todo) * COST["gen4_image"] + sum(clip_seconds(s["id"]) * COST["gen4_turbo_per_sec"] for s in todo if s["id"] in video)
    print(f"[plates] {len(todo)} stills, {len(video)} clips -> estimated ${cost:.2f}")
    for s in todo:
        print(f"  {s['id']:<9} {'still+clip' if s['id'] in video else 'still'}")
    if not args.yes:
        print("Dry run. Re-run with --yes to generate.")
        return

    for s in todo:
        prompt = f"{s['imagePrompt']}. {series['visualStyleSuffix']}"[:1000]
        url = _wait(_req("POST", "/text_to_image", {"model": "gen4_image", "promptText": prompt, "ratio": "1080:1920"})["id"])
        still = pdir / f"{s['id']}.png"
        _download(url, still)
        manifest[s["id"]] = f"plates/{still.name}"
        print(f"  still {s['id']} ok")
        if s["id"] in video and s.get("videoPrompt"):
            data_uri = "data:image/png;base64," + base64.b64encode(still.read_bytes()).decode()
            vurl = _wait(_req("POST", "/image_to_video", {"model": "gen4_turbo", "promptImage": data_uri, "promptText": s["videoPrompt"][:1000],
                                                         "ratio": "720:1280", "duration": clip_seconds(s["id"])})["id"])
            clip = pdir / f"{s['id']}.mp4"
            _download(vurl, clip)
            manifest[s["id"]] = f"plates/{clip.name}"
            print(f"  clip  {s['id']} ok")
        manifest_path.write_text(json.dumps(manifest, indent=1))
    print(f"[plates] wrote {manifest_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
