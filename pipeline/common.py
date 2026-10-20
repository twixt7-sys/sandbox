"""Shared helpers: paths, episode loading, cue resolution."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SR = 48000


def load_series() -> dict:
    return json.loads((ROOT / "series" / "series.json").read_text())


def load_episode(ep_id: str) -> dict:
    return json.loads((ROOT / "episodes" / ep_id / "episode.json").read_text())


def out_dir(ep_id: str) -> Path:
    d = ROOT / "public" / ep_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def norm(word: str) -> str:
    return re.sub(r"[^a-z0-9']", "", word.lower())


def resolve_cue(cue: dict, timing: dict) -> float:
    """Resolve {"line","word","nth","offset"} or {"shot","offset"} to seconds (nth: 1-based repeat of the word)."""
    offset = cue.get("offset", 0.0)
    if "shot" in cue:
        shot = next(s for s in timing["shots"] if s["id"] == cue["shot"])
        return shot["start"] + offset
    line = next(l for l in timing["lines"] if l["id"] == cue["line"])
    if "word" not in cue:
        return line["start"] + offset
    target = norm(cue["word"])
    hits = [w for w in line["words"] if norm(w["text"]) == target]
    if len(hits) >= cue.get("nth", 1):
        return hits[cue.get("nth", 1) - 1]["start"] + offset
    raise KeyError(f"word {cue['word']!r} not found in line {cue['line']}")
