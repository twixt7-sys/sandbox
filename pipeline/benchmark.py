"""Retention scorecard for a Season 2 episode: measures the script and the timeline against the short-form patterns
recorded in docs/SEASON2_RESEARCH.md §7 (hook, pace, how often the picture changes, where the story beats land, the
ending formula, the loop). The targets are directional (creator consensus, not platform rules); the point is to make
every episode measurable the same way and to catch a slow hook or a static stretch before rendering.

Usage: python pipeline/benchmark.py ep31 [ep30 ...] [--json out/ep31_benchmark.json]
Needs episodes/<ep>/episode.json and public/<ep>/timing.json (pipeline/build.sh <ep>).
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path

from common import resolve_cue

ROOT = Path(__file__).resolve().parent.parent


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if s.strip()]


def events(ep: dict, timing: dict) -> list[float]:
    """Times at which the picture visibly changes: camera keys, overlays arriving, kinetic words popping, checklist
    rows ticking, veils and stamps, and hard changes in the world's own keys. Merged within 0.2 s."""
    shots = {s["id"]: s for s in timing["shots"]}
    ts: list[float] = []
    for k in ep["world"].get("camera", []):
        ts.append(resolve_cue(k["at"], timing))
    for sh in ep["shots"]:
        for g in sh.get("graphics", []):
            ts.append(resolve_cue(g["start"], timing) if g.get("start") else shots[sh["id"]]["start"])
            for key in ("at", "revealAt", "pressAt", "dietAt", "subtitleAt", "motiveAt", "hideAt", "fillAt", "runAt", "blinkAt", "withAt"):
                v = g.get(key)
                for c in v if isinstance(v, list) else [v]:
                    if isinstance(c, dict):  # a cue (a pin's `at` is a world position, not a cue)
                        ts.append(resolve_cue(c, timing))
            for p in (g.get("parts", []) or []) + (g.get("choices", []) or []):
                for key in ("at", "pulseAt"):
                    if isinstance(p, dict) and p.get(key):
                        ts.append(resolve_cue(p[key], timing))
            for p in g.get("pulses", []) or []:
                ts.append(resolve_cue(p[0], timing))
            for r in g.get("rows", []) or []:
                if isinstance(r, dict):
                    for key in ("at", "unlockAt"):
                        if r.get(key):
                            ts.append(resolve_cue(r[key], timing))
                    for side in ("left", "right"):
                        for k in r.get(side, []) or []:
                            ts.append(resolve_cue(k[0], timing))
            for v in g.get("verdicts", []) or []:
                ts.append(resolve_cue(v[0], timing))
    for l in ep["world"].get("light", []):
        ts.append(resolve_cue(l["at"], timing))
    dur = timing["duration"]
    ts = sorted(t for t in ts if 0 <= t <= dur)
    merged: list[float] = []
    for t in ts:
        if not merged or t - merged[-1] > 0.2:
            merged.append(t)
    return merged


def card(ep_id: str) -> dict:
    ep = json.loads((ROOT / "episodes" / ep_id / "episode.json").read_text())
    timing = json.loads((ROOT / "public" / ep_id / "timing.json").read_text())
    dur = timing["duration"]
    lines = timing["lines"]
    words = [w for l in lines for w in l["words"]]
    text = " ".join(l["text"] for l in lines)
    sents = sentences(text)
    slen = [len(s.split()) for s in sents]
    shot_start = {s["id"]: s["start"] for s in timing["shots"]}
    hook_line = lines[0]
    ev = events(ep, timing)
    gaps = [b - a for a, b in zip(ev, ev[1:])] + ([dur - ev[-1]] if ev else [])
    # where the standard beats land (shot ids are the series' own: rehook, twist, lesson, cta, next)
    first = lambda sid: next((l["start"] for l in lines if l["shot"] == sid), None)
    twist_word = next((w["start"] for l in lines for w in l["words"] if l["shot"] == "rehook" and w["text"].lower().startswith("twist")), None)
    last = lines[-1]["text"]
    n = ep.get("number", 0)
    formula = bool(re.match(rf"Part {n} of 50\. Follow for part {n + 1}: .+", last))
    hook_g = [g for g in ep["shots"][0].get("graphics", []) if g.get("type") == "kinetic" and g.get("preShow")]
    loop_g = [g for g in ep["shots"][-1].get("graphics", []) if g.get("type") == "kinetic" and g.get("preShow")]
    cta = next((l["text"] for l in lines if l["shot"] == "cta"), "")
    silences = [b["start"] - a["end"] for a, b in zip(lines, lines[1:])]
    # how long the lesson line (the full card's serif subtitle) can be read before the card leaves
    lesson_read = None
    for i, sh in enumerate(ep["shots"]):
        for g in sh.get("graphics", []):
            if g.get("type") == "fieldCard" and g.get("mode") == "full" and g.get("subtitle"):
                a = resolve_cue(g.get("subtitleAt") or g["start"], timing)
                b = resolve_cue(g["end"], timing) if g.get("end") else (timing["shots"][i + 1]["start"] if i + 1 < len(timing["shots"]) else dur)
                lesson_read = b - a
    qa = ep.get("format", {}).get("qa", {"min": 27.0, "max": 33.0})

    rows = [
        # (group, metric, value, display, target text, pass)
        ("Hook", "First spoken word starts", words[0]["start"], f"{words[0]['start']:.2f} s", "≤ 0.5 s", words[0]["start"] <= 0.5),
        ("Hook", "Spoken hook ends", hook_line["end"], f"{hook_line['end']:.2f} s", "≤ 4.0 s", hook_line["end"] <= 4.0),
        ("Hook", "Hook length", len(hook_line["text"].split()), f"{len(hook_line['text'].split())} words", "≤ 12 words", len(hook_line["text"].split()) <= 12),
        ("Hook", "Words heard in the first 3 s", sum(1 for w in words if w["end"] <= 3.0), f"{sum(1 for w in words if w['end'] <= 3.0)}", "≥ 7", sum(1 for w in words if w["end"] <= 3.0) >= 7),
        ("Hook", "Title on screen at frame 0", len(hook_g), "yes" if hook_g else "no", "yes", bool(hook_g)),
        ("Hook", "First change of picture after the hook", min((t for t in ev if t > 1.6), default=dur), f"{min((t for t in ev if t > 1.6), default=dur):.2f} s", "≤ 4.5 s", min((t for t in ev if t > 1.6), default=dur) <= 4.5),
        ("Pace", "Narration", len(words), f"{len(words)} words", "140–170", 140 <= len(words) <= 170),
        ("Pace", "Speaking rate", len(words) / dur * 60, f"{len(words) / dur * 60:.0f} wpm", "150–175 wpm", 150 <= len(words) / dur * 60 <= 175),
        ("Pace", "Average sentence", statistics.mean(slen), f"{statistics.mean(slen):.1f} words", "≤ 6.0", statistics.mean(slen) <= 6.0),
        ("Pace", "Longest sentence", max(slen), f"{max(slen)} words", "≤ 12", max(slen) <= 12),
        ("Pace", "Longest pause between lines", max(silences), f"{max(silences):.2f} s", "≤ 0.45 s", max(silences) <= 0.45),
        ("Picture", "Changes of picture", len(ev), f"{len(ev)} ({len(ev) / dur * 60:.0f} a minute)", "≥ 40 a minute", len(ev) / dur * 60 >= 40),
        ("Picture", "Longest stretch without a change", max(gaps), f"{max(gaps):.2f} s", "≤ 2.5 s", max(gaps) <= 2.5),
        ("Picture", "Median stretch", statistics.median(gaps), f"{statistics.median(gaps):.2f} s", "≤ 1.0 s", statistics.median(gaps) <= 1.0),
        ("Story", "Run 1 starts", first("run1"), f"{first('run1'):.1f} s", "≤ 12 s", first("run1") <= 12),
        ("Story", "The drop (naive design fails)", first("drop"), f"{first('drop'):.1f} s", "13–19 s", 13 <= first("drop") <= 19),
        ("Story", "Re-hook ('the twist' promised)", twist_word, f"{twist_word:.1f} s" if twist_word else "missing", "18–25 s", bool(twist_word) and 18 <= twist_word <= 25),
        ("Story", "The twist", first("twist"), f"{first('twist'):.1f} s", "36–47 s", 36 <= first("twist") <= 47),
        ("Story", "Payoff line (the lesson)", first("lesson"), f"{first('lesson'):.1f} s", "after the twist, ≥ 45 s", first("lesson") >= 45),
        ("Story", "Lesson line stays on screen", lesson_read, f"{lesson_read:.2f} s" if lesson_read is not None else "missing", "≥ 1.2 s", lesson_read is not None and lesson_read >= 1.2),
        ("Ending", "CTA", len(cta.split()), f"{len(cta.split())} words", "≤ 10 words, one ask", 0 < len(cta.split()) <= 10),
        ("Ending", "Ending formula (part, follow, tease)", formula, "yes" if formula else "no", "yes", formula),
        ("Ending", "Follow ask in the last", dur - first("next"), f"{dur - first('next'):.1f} s", "final 3–7 s", 3 <= dur - first("next") <= 7),
        ("Ending", "Hook title returns for the loop", len(loop_g), "yes" if loop_g else "no", "yes", bool(loop_g)),
        ("Format", "Duration", dur, f"{dur:.2f} s", f"{qa['min']:.0f}–{qa['max']:.0f} s", qa["min"] <= dur <= qa["max"]),
    ]
    return {"episode": ep_id, "title": ep.get("title"), "duration": dur,
            "rows": [{"group": g, "metric": m, "value": (round(v, 3) if isinstance(v, float) else v), "display": d, "target": t, "pass": bool(p)} for g, m, v, d, t, p in rows],
            "passed": sum(1 for r in rows if r[5]), "total": len(rows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="+")
    ap.add_argument("--json")
    args = ap.parse_args()
    cards = [card(e) for e in args.episodes]
    head = cards[0]
    w = max(len(r["metric"]) for r in head["rows"])
    print(f"{'':10} {'metric':{w}}  {'target':24} " + " ".join(f"{c['episode']:>22}" for c in cards))
    for i, r in enumerate(head["rows"]):
        cells = " ".join(f"{('✓ ' if c['rows'][i]['pass'] else '✗ ') + c['rows'][i]['display']:>22}" for c in cards)
        print(f"{r['group']:10} {r['metric']:{w}}  {r['target']:24} {cells}")
    print(f"{'':10} {'score':{w}}  {'':24} " + " ".join(f"{str(c['passed']) + '/' + str(c['total']):>22}" for c in cards))
    if args.json:
        Path(args.json).write_text(json.dumps(cards if len(cards) > 1 else cards[0], indent=1))
        print(f"[benchmark] wrote {args.json}")


if __name__ == "__main__":
    main()
