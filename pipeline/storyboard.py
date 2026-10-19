"""Render episodes/<ep>/STORYBOARD.md from episode.json + the measured timing.json.

Usage: python pipeline/storyboard.py ep01
"""
from __future__ import annotations

import json
import sys

from common import ROOT, load_episode, load_series, out_dir


def fmt(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:05.2f}"


def main():
    ep = load_episode(sys.argv[1])
    series = load_series()
    timing = json.loads((out_dir(ep["id"]) / "timing.json").read_text())
    spans = {s["id"]: s for s in timing["shots"]}
    words = sum(len(l["words"]) for l in timing["lines"])
    md = [f"# {ep['title']}", "", f"**Series:** {series['name']} · Episode {ep['number']:02d}  ",
          f"**Lesson:** {ep['lesson']}  ",
          f"**Measured runtime:** {timing['duration']:.2f} s · {words} spoken words · voice `{timing['provider']}`", "",
          "## Narration (exactly as spoken)", ""]
    for l in timing["lines"]:
        md.append(f"- `{fmt(l['start'])}–{fmt(l['end'])}` {l['text']}")
    md += ["", f"**Voice direction:** {ep['voice']['direction']}", "", "## Shots", ""]
    for i, s in enumerate(ep["shots"], 1):
        sp = spans[s["id"]]
        lines = [l for l in timing["lines"] if l["shot"] == s["id"]]
        md += [f"### {i}. `{s['id']}` · {fmt(sp['start'])} → {fmt(sp['end'])} ({sp['end'] - sp['start']:.1f} s)", "",
               f"**Purpose:** {s['purpose']}", "",
               "**Narration:** " + (" ".join(f"“{l['text']}”" for l in lines) or "—"), "",
               f"**Visual:** {s['visual']}", "",
               f"**Camera:** {s['camera']}", "",
               f"**Layers:** foreground: {s['layers']['foreground']}; midground: {s['layers']['midground']}; background: {s['layers']['background']}", "",
               f"**Light / palette / composition:** {s['lighting']}", ""]
        if s.get("imagePrompt") and s.get("plate", True):
            md += ["**Image prompt** (series style suffix appended automatically):", "", f"> {s['imagePrompt']}", ""]
        if s.get("videoPrompt"):
            md += ["**Image-to-video prompt:**", "", f"> {s['videoPrompt']}", ""]
        md += [f"**On-screen text:** {s['onScreenText']}", "",
               "**Motion graphics:** " + ", ".join(f"`{g['type']}`" for g in s["graphics"]), "",
               f"**Captions:** {'off (text is on screen verbatim)' if s.get('captions') is False else 'word-timed, emphasis: ' + ', '.join(w for l in lines for w in l['emphasis'])}", "",
               f"**Transition out:** {s['transition']}", "",
               "**Sound:** " + "; ".join(f"{c['sound']} ({c.get('gain', -18)} dB)" for c in s.get("sfx", [])) + f". Music: {s['music']}", ""]
    md += ["## Platform metadata", ""]
    for k, v in ep["metadata"].items():
        if isinstance(v, dict):
            md.append(f"### {k.capitalize()}")
            for kk, vv in v.items():
                md.append(f"- **{kk}:** {' '.join(vv) if isinstance(vv, list) else vv}")
            md.append("")
        else:
            md += [f"**{k}:** {v}", ""]
    path = ROOT / "episodes" / ep["id"] / "STORYBOARD.md"
    path.write_text("\n".join(md))
    print(f"[storyboard] {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
