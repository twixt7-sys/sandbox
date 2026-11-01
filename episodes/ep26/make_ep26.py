"""Generate episodes/ep26/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep26/make_ep26.py
The world timeline (camera, populations, terrain layers, HUD) is written here in Python, so the population curves
can be computed (e.g. the predator-prey cycle) instead of typed by hand.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def cue(line, word=None, offset=0.0, nth=None):
    c = {"line": line}
    if word:
        c["word"] = word
    if nth:
        c["nth"] = nth
    if offset:
        c["offset"] = round(offset, 3)
    return c


LINES = [
    ("L1", "hook", "If your giant predator eats everything, why hasn't everything gone extinct?", 0.45, ["everything,", "extinct?"]),
    ("L2", "setup", "Let's test it. This is the Grimmaw. It eats anything that moves.", 0.25, ["grimmaw.", "anything"]),
    ("L3", "setup", "Press run.", 0.3, ["run."]),
    ("L4", "run1", "Year one: mossbacks everywhere. Year three: thinning. Year five: gone.", 0.35, ["mossbacks", "gone."]),
    ("L5", "starve", "With nothing left to hunt, the Grimmaw starves too.", 0.3, ["starves"]),
    ("L6", "ends", "A monster that eats everything doesn't rule your world. It ends it.", 0.7, ["rule", "ends"]),
    ("L7", "rehook", "Real predators live inside limits. Four are easy. The fifth is the twist.", 0.35, ["limits.", "twist."]),
    ("L8", "prey", "One: prey that breeds faster than it's eaten.", 0.2, ["breeds", "faster"]),
    ("L9", "range", "Two: territory. One Grimmaw needs a whole valley.", 0.2, ["territory.", "valley."]),
    ("L10", "energy", "Three: energy. A body this big hunts rarely and sleeps a lot.", 0.2, ["energy.", "rarely"]),
    ("L11", "breed", "Four: slow breeding. One cub every few winters.", 0.35, ["slow", "cub"]),
    ("L12", "run2", "Run it again.", 0.25, ["again."]),
    ("L13", "run2", "Now the numbers rise and fall, but nothing vanishes.", 0.45, ["nothing", "vanishes."]),
    ("L14", "twist", "Rule five? Delete the monster.", 0.3, ["delete"]),
    ("L15", "twist", "The mossbacks boom, strip the meadow bare, then starve.", 0.35, ["boom,", "starve."]),
    ("L16", "role", "Rule five is its job. The Grimmaw holds the island together.", 0.45, ["job.", "together."]),
    ("L17", "lesson", "Don't design a monster. Design its place in the world.", 0.4, ["monster.", "place"]),
    ("L18", "cta", "Share this with someone designing fantasy monsters.", 0.3, ["share"]),
]

SHOTS = ["hook", "setup", "run1", "starve", "ends", "rehook", "prey", "range", "energy", "breed", "run2", "twist", "role", "lesson", "cta"]


# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle (world units; see src/s2/world/island.ts and the map in BRIEF.md).
G1_HOME = (8.0, -1.0)
DEN = (1.0, -5.5)
RING_A = (11.0, -2.0, 7.5)
RING_B = (4.0, -14.0, 6.5)
RING_C = (10.0, 12.0, 6.0)
HERD_CENTERS = [[13, -6], [15, 3], [6, -12], [3, -16], [17, -2], [9, -9], [14, 9]]


def cam(at, az, el, dist, target, fov=24, dur=1.4, drift=0.0, cut=False):
    c = {"at": at, "az": az, "el": el, "dist": dist, "target": list(target), "fov": fov, "dur": dur, "drift": drift}
    if cut:
        c["cut"] = True
    return c


def pk(at, x, z, state="idle", face=None, dur=0.0):
    k = {"at": at, "x": x, "z": z, "state": state}
    if face is not None:
        k["face"] = face
    if dur:
        k["dur"] = dur
    return k


def lv_keys(start_line, start_word, t_offsets, values):
    return [[cue(start_line, start_word, o), v] for o, v in zip(t_offsets, values)]


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": off} if off else {})}
    roam = [(11, -6), (6, -11), (3, -15), (9, -9), (13, 0), (10, 6), (14, 3), (8, -3)]
    g1 = [pk(shot("hook"), *G1_HOME, face=10)]
    g1.append(pk(cue("L2", "This"), 9.6, -1.8, "walk", dur=2.2))
    g1.append(pk(cue("L2", "moves.", 0.4), 9.6, -1.8, "idle", face=200))
    for k, (x, z) in enumerate(roam):
        g1.append(pk(cue("L3", "run.", 0.15 + k * 0.58), x, z, "walk", dur=0.55))
    g1 += [
        pk(cue("L5", "With", -0.1), 7.0, -5.0, "walk", dur=1.5),
        pk(cue("L5", "starves"), 7.0, -5.0, "lie"),
        pk(cue("L6", "A", 0.15), 7.0, -5.0, "dissolve"),
        pk(cue("L6", "rule", 0.0), 7.0, -5.0, "hidden"),
        pk(cue("L6", "it.", 0.45), *G1_HOME, "appear", face=10),
        pk(cue("L7", "Real", 0.2), *G1_HOME, "idle", face=10),
        pk(cue("L9", "Two:", -0.2), 10.5, -2.2, "walk", dur=1.1),
        pk(cue("L9", "valley.", 0.1), 10.5, -2.2, "idle", face=160),
        pk(cue("L10", "energy.", 0.1), DEN[0], DEN[1], "walk", dur=2.0),
        pk(cue("L10", "sleeps"), DEN[0], DEN[1], "sleep", face=70),
    ]
    roam2 = [(12, -4), (9, -6), (13, 1), (10, -1), (14, -3), (9, 1)]
    g1.append(pk(cue("L12", "Run", 0.1), DEN[0], DEN[1], "idle", face=70))
    for k, (x, z) in enumerate(roam2):
        g1.append(pk(cue("L12", "Run", 0.25 + k * 0.62), x, z, "walk", dur=0.58))
    g1 += [
        pk(cue("L14", "Rule", 0.0), 10.0, -1.0, "walk", dur=0.6),
        pk(cue("L14", "Delete", 0.1), 10.0, -1.0, "dissolve"),
        pk(cue("L14", "monster.", 0.6), 10.0, -1.0, "hidden"),
        pk(cue("L16", "Grimmaw"), 11.0, -2.0, "appear", face=200),
        pk(cue("L16", "together.", 0.2), 11.0, -2.0, "idle", face=200),
        pk(cue("L17", "Design", 0.0), 9.0, -1.5, "walk", dur=2.5),
        pk({"shot": "cta", "offset": 3.2}, *G1_HOME, "idle", face=10),
    ]
    g2 = [
        pk(cue("L9", "One", 0.1), RING_B[0], RING_B[1], "hidden"),
        pk(cue("L9", "Grimmaw", 0.1), RING_B[0], RING_B[1], "appear", face=300),
        pk(cue("L9", "needs", 0.4), RING_B[0], RING_B[1], "idle", face=300),
    ]
    for k, (dx, dz) in enumerate([(2, 2), (-2, 1), (1, -2), (-1, -1), (2, 0), (0, 2)]):
        g2.append(pk(cue("L12", "Run", 0.3 + k * 0.6), RING_B[0] + dx, RING_B[1] + dz, "walk", dur=0.55))
    g2 += [
        pk(cue("L14", "Delete", 0.22), RING_B[0], RING_B[1] + 2, "dissolve"),
        pk(cue("L14", "monster.", 0.7), RING_B[0], RING_B[1] + 2, "hidden"),
        pk(cue("L16", "Grimmaw", 0.15), RING_B[0], RING_B[1], "appear", face=250),
        pk(cue("L16", "together.", 0.3), RING_B[0], RING_B[1], "idle", face=250),
        pk({"shot": "cta", "offset": 3.2}, RING_B[0], RING_B[1], "hidden"),
    ]
    g3 = [
        pk(cue("L9", "One", 0.1), RING_C[0], RING_C[1], "hidden"),
        pk(cue("L9", "whole", 0.0), RING_C[0], RING_C[1], "appear", face=120),
        pk(cue("L9", "valley.", 0.5), RING_C[0], RING_C[1], "idle", face=120),
    ]
    for k, (dx, dz) in enumerate([(-2, -1), (1, 2), (2, -1)]):
        g3.append(pk(cue("L12", "Run", 0.3 + k * 0.55), RING_C[0] + dx, RING_C[1] + dz, "walk", dur=0.5))
    g3 += [
        pk(cue("L13", "and", 0.0), RING_C[0] + 2, RING_C[1] - 1, "despawn"),
        pk(cue("L13", "but", 0.1), RING_C[0], RING_C[1], "spawn", face=90),
        pk(cue("L13", "vanishes.", 0.2), RING_C[0] - 1, RING_C[1] + 1, "walk", dur=0.6),
        pk(cue("L14", "Delete", 0.34), RING_C[0] - 1, RING_C[1] + 1, "dissolve"),
        pk(cue("L14", "monster.", 0.8), RING_C[0] - 1, RING_C[1] + 1, "hidden"),
        pk(cue("L16", "Grimmaw", 0.3), RING_C[0], RING_C[1], "appear", face=150),
        pk(cue("L16", "together.", 0.4), RING_C[0], RING_C[1], "idle", face=150),
        pk({"shot": "cta", "offset": 3.2}, RING_C[0], RING_C[1], "hidden"),
    ]
    cub = [
        pk(cue("L11", "One", 0.0), DEN[0] + 1.6, DEN[1] + 1.4, "hidden"),
        pk(cue("L11", "cub", -0.05), DEN[0] + 1.6, DEN[1] + 1.4, "spawn", face=40),
        pk(cue("L11", "winters.", 0.3), DEN[0] + 1.6, DEN[1] + 1.4, "idle", face=40),
        pk(cue("L12", "Run", 0.15), DEN[0] + 1.6, DEN[1] + 1.4, "despawn"),
        pk(cue("L12", "again.", 0.3), DEN[0] + 1.6, DEN[1] + 1.4, "hidden"),
    ]

    herd = [
        [shot("hook"), 120],
        [cue("L3", "run."), 120],
        [cue("L4", "everywhere.", 0.35), 116],
        [cue("L4", "three:", 0.3), 64, "linear"],
        [cue("L4", "five:", 0.15), 9, "linear"],
        [cue("L4", "gone.", 0.1), 0, "linear"],
        [cue("L6", "it.", 0.4), 0],
        [cue("L7", "Real", 0.15), 120, "out"],
        [cue("L8", "breeds"), 120],
        [cue("L8", "eaten.", 0.3), 175, "out"],
        [cue("L12", "Run", 0.2), 175],
    ]
    # Run two: a damped predator-prey cycle (prey leads, predators lag), two waves in about 4 s.
    run2_t = [0.6, 1.1, 1.6, 2.1, 2.6, 3.1, 3.6, 4.1]
    run2_v = [150, 122, 118, 142, 186, 196, 172, 158]
    herd += lv_keys("L12", "Run", run2_t, run2_v)
    herd += [
        [cue("L15", "The"), 160],
        [cue("L15", "boom,", 0.35), 380, "out"],
        [cue("L15", "bare,", 0.2), 372],
        [cue("L15", "starve.", 0.35), 28, "in"],
        [cue("L16", "Grimmaw"), 28],
        [cue("L16", "together.", 0.2), 150, "out"],
        [cue("L18", "Share", 0.6), 150],
        [{"shot": "cta", "offset": 3.0}, 120, "linear"],
    ]
    pred = [
        [shot("hook"), 1],
        [cue("L5", "starves", 0.3), 1],
        [cue("L5", "starves", 0.5), 0, "step"],
        [cue("L6", "it.", 0.45), 0],
        [cue("L6", "it.", 0.55), 1, "step"],
        [cue("L9", "Grimmaw", 0.1), 1],
        [cue("L9", "Grimmaw", 0.2), 2, "step"],
        [cue("L9", "whole", 0.0), 2],
        [cue("L9", "whole", 0.1), 3, "step"],
        [cue("L11", "cub", -0.05), 3],
        [cue("L11", "cub", 0.05), 4, "step"],
        [cue("L12", "Run", 0.15), 4],
        [cue("L12", "Run", 0.25), 3, "step"],
        [cue("L13", "and", 0.0), 3],
        [cue("L13", "and", 0.1), 2, "step"],
        [cue("L13", "but", 0.1), 2],
        [cue("L13", "but", 0.2), 3, "step"],
        [cue("L14", "Delete", 0.1), 3],
        [cue("L14", "Delete", 0.5), 0, "linear"],
        [cue("L16", "Grimmaw"), 0],
        [cue("L16", "Grimmaw", 0.35), 3, "linear"],
    ]
    clock = [
        [shot("hook"), 0],
        [cue("L3", "run."), 0],
        [cue("L4", "one:", 0.2), 1, "linear"],
        [cue("L4", "three:", 0.25), 3, "linear"],
        [cue("L4", "five:", 0.2), 5, "linear"],
        [cue("L6", "it.", 0.4), 5],
        [cue("L7", "Real", 0.15), 0, "linear"],
        [cue("L11", "slow"), 0],
        [cue("L11", "winters.", 0.4), 3, "linear"],
        [cue("L12", "Run", 0.1), 3],
        [cue("L13", "vanishes.", 0.7), 23, "linear"],
        [cue("L15", "The"), 23],
        [cue("L15", "starve.", 0.4), 31, "linear"],
    ]
    speed = [
        [shot("hook"), 1],
        [cue("L3", "run."), 1],
        [cue("L3", "run.", 0.35), 9],
        [cue("L4", "gone.", 0.2), 9],
        [cue("L5", "With", -0.1), 1],
        [cue("L6", "it.", 0.35), 1],
        [cue("L6", "it.", 0.55), -10],
        [cue("L7", "Real", 0.1), -10],
        [cue("L7", "Real", 0.3), 1],
        [cue("L12", "Run", 0.1), 1],
        [cue("L12", "Run", 0.4), 9],
        [cue("L13", "vanishes.", 0.6), 9],
        [cue("L14", "Rule", 0.0), 1],
        [cue("L15", "The", -0.1), 1],
        [cue("L15", "The", 0.2), 9],
        [cue("L15", "starve.", 0.4), 9],
        [cue("L16", "Rule", 0.0), 1],
    ]
    graze = [
        [shot("hook"), 0],
        [cue("L15", "strip", -0.3), 0],
        [cue("L15", "bare,", 0.25), 1, "linear"],
        [cue("L16", "Grimmaw"), 1],
        [cue("L16", "together.", 0.1), 0, "linear"],
    ]
    forest = [
        [shot("hook"), 1],
        [cue("L15", "meadow", -0.2), 1],
        [cue("L15", "starve.", 0.2), 0.3, "linear"],
        [cue("L16", "Grimmaw"), 0.3],
        [cue("L16", "together.", 0.2), 1, "linear"],
    ]
    snow = [
        [shot("hook"), 0],
        [cue("L11", "slow", -0.2), 0],
        [cue("L11", "breeding.", 0.2), 0.95, "linear"],
        [cue("L11", "winters.", 0.4), 0.95],
        [cue("L12", "Run", -0.2), 0, "linear"],
    ]
    # Run two: winters flicker past while the years count up.
    for k, base in enumerate([0.9, 2.0, 3.1]):
        snow += [[cue("L12", "Run", base), 0], [cue("L12", "Run", base + 0.25), 0.6, "linear"], [cue("L12", "Run", base + 0.55), 0, "linear"]]
    rings = [
        {"x": RING_A[0], "z": RING_A[1], "r": RING_A[2], "on": cue("L9", "territory."), "off": cue("L10", "Three:", -0.1), "color": "#f4c46e"},
        {"x": RING_B[0], "z": RING_B[1], "r": RING_B[2], "on": cue("L9", "Grimmaw", 0.1), "off": cue("L10", "Three:", -0.1), "color": "#f08a4b"},
        {"x": RING_C[0], "z": RING_C[1], "r": RING_C[2], "on": cue("L9", "whole"), "off": cue("L10", "Three:", -0.1), "color": "#f08a4b"},
    ]
    ripple = [shot("hook", 0.05), cue("L3", "run."), cue("L12", "Run"), cue("L15", "The"), cue("L16", "together.")]

    # Long lens (fov 16.5 from 54 units): less perspective, so the predator towers over its herd. Chosen over a 22° / 40-unit variant.
    hook_pose = dict(az=24, el=8, dist=54, target=(8.9, 6.9, -1.2), fov=16.5)
    camera = [
        cam(shot("hook"), drift=1.2, **hook_pose),
        cam(cue("L2", "Let's", -0.2), 8, 12, 40, (9.6, 9.4, -1.8), fov=22, dur=1.8, drift=2.0),
        cam(cue("L3", "run.", 0.05), 30, 44, 192, (2.0, 10.5, 0.0), fov=26, dur=1.3, drift=2.0),
        cam(cue("L5", "With", -0.25), 140, 15, 32, (6.6, 7.4, -4.6), fov=22, dur=1.3, drift=3.0),
        cam(cue("L6", "A", 0.0), 165, 34, 200, (1.0, 5.0, 0.0), fov=26, dur=2.6, drift=2.0),
        cam(cue("L6", "it.", 0.45), 40, 30, 92, (7.0, 9.5, -2.0), fov=24, dur=0.9, drift=2.0),
        cam(cue("L8", "One:", -0.2), 64, 24, 46, (15.0, 6.4, 3.0), fov=22, dur=1.1, drift=1.0),
        cam(cue("L9", "Two:", -0.15), 25, 66, 182, (5.0, 13.0, -1.0), fov=26, dur=1.1, drift=1.5),
        cam(cue("L10", "Three:", -0.15), 12, 18, 40, (4.0, 11.0, -4.4), fov=22, dur=1.3, drift=2.0),
        cam(cue("L11", "Four:", -0.1), 108, 22, 34, (2.4, 10.6, -4.4), fov=22, dur=1.3, drift=2.0),
        cam(cue("L12", "Run", -0.05), 35, 44, 196, (2.0, 13.0, 0.0), fov=26, dur=1.0, drift=3.0),
        cam(cue("L14", "Rule", -0.1), 50, 42, 170, (4.0, 12.0, -1.0), fov=26, dur=0.8, drift=1.0),
        cam(cue("L16", "Rule", -0.1), 30, 36, 170, (3.0, 13.5, -1.0), fov=26, dur=1.4, drift=1.5),
        cam(cue("L17", "Don't", -0.25), 15, 30, 190, (2.0, 2.0, 0.0), fov=26, dur=1.6, drift=3.0),
        cam({"shot": "cta", "offset": 3.6}, hook_pose["az"] - 1.2 * 2.1, hook_pose["el"], hook_pose["dist"], hook_pose["target"], fov=hook_pose["fov"], cut=True, drift=1.2),
    ]
    light = [
        {"at": shot("hook"), "mood": "day"},
        {"at": cue("L5", "With", -0.2), "mood": "dusk", "dur": 1.0},
        {"at": cue("L5", "starves"), "mood": "gloom", "dur": 1.8},
        {"at": cue("L6", "it.", 0.45), "mood": "day", "dur": 0.8},
        {"at": cue("L11", "slow", -0.2), "mood": "winter", "dur": 0.8},
        {"at": cue("L12", "Run", -0.2), "mood": "day", "dur": 0.6},
        {"at": cue("L15", "bare,"), "mood": "gloom", "dur": 0.8},
        {"at": cue("L16", "Grimmaw"), "mood": "day", "dur": 0.9},
        {"at": cue("L17", "Don't"), "mood": "dusk", "dur": 2.0},
        {"at": {"shot": "cta", "offset": 3.6}, "mood": "day", "dur": 0.1},
    ]
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": herd, "max": 380, "base": 120, "centers": HERD_CENTERS},
        "pred": pred,
        "predators": [
            {"id": "g1", "keys": g1},
            {"id": "g2", "keys": g2},
            {"id": "g3", "keys": g3},
            {"id": "cub", "scale": 0.45, "keys": cub},
        ],
        "layers": {"graze": graze, "forest": forest, "snow": snow, "rings": rings, "ripple": ripple},
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "PREY", "text": "breeds faster than it's eaten", "at": cue("L8", "prey")},
    {"n": 2, "label": "RANGE", "text": "one valley per Grimmaw", "at": cue("L9", "territory.")},
    {"n": 3, "label": "ENERGY", "text": "hunts rarely, sleeps a lot", "at": cue("L10", "energy.")},
    {"n": 4, "label": "BREEDING", "text": "one cub, every few winters", "at": cue("L11", "slow")},
    {"n": 5, "label": "ROLE", "text": "keeps the grazers in check", "at": cue("L7", "limits."), "locked": True, "unlockAt": cue("L16", "job.")},
]


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "IF IT EATS"}, {"text": "EVERYTHING", "color": "ember"}]
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 100, "start": {"shot": "hook"}, "end": cue("L1", "why", -0.08), "preShow": True},
        {"type": "kinetic", "parts": [{"text": "WHY ISN'T", "at": cue("L1", "why")}, {"text": "EVERYTHING", "at": cue("L1", "everything", nth=2)}, {"text": "EXTINCT?", "at": cue("L1", "extinct?"), "color": "rust", "size": 132}],
         "y": 452, "size": 100, "start": cue("L1", "why", -0.02), "end": cue("L2", "Let's", -0.1)},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 26 · CREATURES", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
    ]
    G["setup"] += [
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "This", -0.1), "end": cue("L3", "Press", -0.1), "dietAt": cue("L2", "eats"),
         "kicker": "FIELD CARD · NO. 001", "kind": "APEX PREDATOR", "name": "GRIMMAW", "diet": "anything that moves", "sprite": "ep26/grimmaw_sprite.png"},
        {"type": "simBar", "start": cue("L3", "Press", -0.15), "end": cue("L17", "Don't", -0.3), "runAt": [cue("L3", "run."), cue("L12", "Run"), cue("L15", "The")]},
    ]
    G["run1"] += [
        {"type": "simGraph", "y": 456, "h": 214, "from": cue("L3", "run."), "to": cue("L4", "gone.", 0.4), "start": cue("L4", "Year", -0.15), "end": cue("L5", "With", -0.1), "caption": "YEARS 0–5",
         "series": [{"key": "herd", "color": "#9bd16a", "max": 130, "label": "MOSSBACKS"}, {"key": "pred", "color": "#f08a4b", "max": 2, "label": "GRIMMAW"}]},
    ]
    G["starve"] += [
        {"type": "pin", "pred": "g1", "kicker": "FOOD IN RANGE", "text": "NONE", "color": "rust", "lift": 120, "start": cue("L5", "nothing"), "end": cue("L5", "starves", 0.2)},
    ]
    G["ends"] += [
        {"type": "stamp", "text": "EXTINCT", "sub": "EVERYTHING · YEAR 5", "color": "rust", "y": 560, "start": cue("L6", "eats"), "end": cue("L6", "It", -0.1)},
        {"type": "kinetic", "parts": [{"text": "IT ENDS IT.", "at": cue("L6", "It"), "color": "rust"}], "font": "pixel", "size": 100, "y": 1180, "start": cue("L6", "It", -0.02), "end": cue("L6", "it.", 0.55)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "it.", 0.5), "end": cue("L7", "Real", 0.25)},
        {"type": "blockWipe", "at": cue("L6", "it.", 0.48), "dur": 0.34},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "limits.", -0.1), "end": cue("L17", "Don't", -0.3),
         "kicker": "DESIGN CHECK", "title": "GRIMMAW", "blinkAt": cue("L7", "twist."), "lockedText": "the twist",
         "collapse": [[cue("L9", "territory.", 0.5), 0], [cue("L9", "territory.", 0.85), 1], [cue("L10", "Three:", -0.25), 1], [cue("L10", "Three:", 0.1), 0],
                      [cue("L12", "Run", -0.2), 0], [cue("L12", "Run", 0.15), 1], [cue("L16", "Rule", -0.3), 1], [cue("L16", "Rule", 0.05), 0]]},
    ]
    G["prey"] += [
        {"type": "pin", "at": [15, 4.5, 3], "kicker": "SPRING", "text": "+55 BORN", "color": "prey", "lift": 130, "start": cue("L8", "breeds"), "end": cue("L9", "Two:", -0.1)},
    ]
    G["range"] += [
        {"type": "pin", "at": [RING_A[0], None, RING_A[1]], "kicker": "TERRITORY", "text": "1 VALLEY EACH", "color": "ember", "lift": 70, "start": cue("L9", "territory.", 0.1), "end": cue("L10", "Three:", -0.15)},
    ]
    G["energy"] += [
        {"type": "pin", "pred": "g1", "kicker": "BIG BODY", "text": "HUNTS RARELY", "color": "sky", "lift": 120, "start": cue("L10", "hunts", -0.1), "end": cue("L10", "sleeps", -0.05)},
        {"type": "zzz", "pred": "g1", "start": cue("L10", "sleeps", 0.3), "end": cue("L12", "Run")},
    ]
    G["breed"] += [
        {"type": "pin", "pred": "cub", "dy": 3.0, "kicker": "EVERY FEW WINTERS", "text": "1 CUB", "color": "ember", "lift": 90, "start": cue("L11", "cub", 0.1), "end": cue("L12", "Run", -0.1)},
    ]
    G["run2"] += [
        {"type": "simGraph", "y": 566, "h": 214, "from": cue("L12", "Run"), "to": cue("L13", "vanishes.", 0.6), "start": cue("L12", "Run", 0.1), "end": cue("L14", "Rule", -0.1), "caption": "YEARS 3–23",
         "series": [{"key": "herd", "color": "#9bd16a", "max": 230, "label": "MOSSBACKS"}, {"key": "pred", "color": "#f08a4b", "max": 5, "label": "GRIMMAW"}]},
        {"type": "stamp", "text": "STABLE", "sub": "NOTHING VANISHES", "color": "stable", "rotate": -4, "y": 900, "size": 92, "start": cue("L13", "nothing"), "end": cue("L14", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L14", "Rule"), "color": "ember"}], "size": 150, "y": 640, "start": cue("L14", "Rule", -0.02), "end": cue("L14", "Delete", -0.08)},
        {"type": "deleteFx", "preds": ["g1", "g2", "g3"], "y": 640, "start": cue("L14", "Delete", -0.05), "end": cue("L14", "monster.", 0.45)},
        {"type": "simGraph", "y": 566, "h": 214, "from": cue("L15", "The"), "to": cue("L15", "starve.", 0.45), "start": cue("L15", "The", 0.05), "end": cue("L16", "Rule", -0.05), "caption": "NO PREDATOR",
         "series": [{"key": "herd", "color": "#9bd16a", "max": 400, "label": "MOSSBACKS"}]},
        {"type": "pin", "at": [12, None, -6], "kicker": "MEADOW", "text": "STRIPPED BARE", "color": "rust", "lift": 140, "start": cue("L15", "bare,", -0.1), "end": cue("L16", "Rule", -0.1)},
    ]
    G["role"] += []
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L17", "Don't", -0.3), **({"unlockAt": cue("L17", "Don't", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L17", "Don't", -0.3), "end": cue("L18", "Share", -0.25), "kicker": "BEFORE YOU DESIGN A MONSTER", "title": "GRIMMAW",
         "subtitle": "Design its place in the world.", "subtitleAt": cue("L17", "Design")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": cue("L18", "Share", -0.3), "dur": 0.34},
        {"type": "endCardS2", "start": cue("L18", "Share", -0.3), "end": {"shot": "cta", "offset": 4.85}, "fadeOut": 0.3, "kicker": "EPISODE 26 / 50",
         "title": "Don't Design a Monster. Design an Ecosystem.", "cta": "SHARE THIS", "with": "with someone designing fantasy monsters"},
        # The loop: the hook's opening words fade back in as the end card lifts, matching frame 0.
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 100, "start": {"shot": "cta", "offset": 5.1}, "fadeIn": 0.4, "preShow": True},
    ]
    return G


LESSON = "A creature becomes believable when it has a place in its environment: prey that out-breeds it, a territory, an energy budget, slow breeding, and a job the ecosystem needs it for."

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Stop the scroll on a question with the answer already on screen: a giant predator among its prey.",
             "The Grimmaw in profile on the meadow of the Isle, mossbacks grazing around it; WORLD ENGINE boots top-right as the island ripples.",
             "Long-lens hero shot (fov 16.5 from dist 54, el 8, az 24), slow drift; the last 0.7 s returns to this exact pose.", ("kinetic question", "the Grimmaw and herd", "the Isle's peak and the void"),
             "Day mood; warm key from the south-east, hard pixel shadows.", "IF IT EATS / EVERYTHING then WHY ISN'T / EVERYTHING / EXTINCT?",
             "Continuous camera into the setup.", "Hook: Dm–Bb, pad + 8th arp."),
    "setup": ("Meet the subject and its one dangerous claim, then press RUN.",
              "Field card intro (sprite x3, GRIMMAW, APEX PREDATOR, DIET anything that moves) over the Grimmaw walking in profile; the sim bar slides in and RUN is pressed.",
              "Hero close orbit (az 8), then rise to wide on 'run'.", ("field card, sim bar", "the Grimmaw walking", "herd and lake"),
              "Day.", "Field card; RUN.", "Ripple + rise to the wide on 'run'.", "Adds bass and a heartbeat kick."),
    "run1": ("The naive design runs and fails, in numbers.", "The whole Isle; clock 0→5, MOSSBACKS 120→0 while the graph falls; herds thin everywhere.",
             "Wide (dist 192, el 44).", ("sim bar + graph", "the thinning herds", "the island in the void"), "Day.", "YEAR 01..05; counters; graph YEARS 0–5.",
             "Swoop down to the lone predator.", "Run: 16th arp, four-on-the-floor, claps."),
    "starve": ("Hunger shown as an empty range, never a kill.", "The Grimmaw walks an empty meadow at dusk, then lies down and greys. Pin: FOOD IN RANGE / NONE.",
               "Close (dist 32, az 140).", ("pin", "the Grimmaw", "empty meadow"), "Dusk to gloom.", "FOOD IN RANGE: NONE", "Pull back.", "Drop: drone and heartbeat."),
    "ends": ("The punchline of the failure.", "The whole island desaturated and empty; EXTINCT stamp; 'IT ENDS IT.' in rust.",
             "Long pull back (dist 200).", ("stamp, kinetic", "empty island", "void"), "Gloom (saturation 0.35).", "EXTINCT · EVERYTHING · YEAR 5; IT ENDS IT.",
             "Rewind + block wipe.", "Near silence, drone; duck on 'It ends it'."),
    "rehook": ("Re-hook: rewind the world and open a loop (four easy rules, one locked twist).", "REWIND chip and scanlines; clock and herd run back; the checklist card with a blinking locked row 5.",
               "Medium (dist 92).", ("rewind, checklist card", "herd returning", "island"), "Back to day.", "DESIGN CHECK 0/5, row 5 '??? the twist'.", "Cut on 'One'.", "Arp returns: Dm–C–Bb–A."),
    "prey": ("Rule 1: prey that breeds faster than it is eaten.", "Close on a herd; lambs pop in small and grow; pin SPRING +55 BORN; row 1 ticks.",
             "Close on the herd (dist 46).", ("pin", "herd and lambs", "meadow"), "Day.", "1 PREY · breeds faster than it's eaten", "Rise to top-down.", "Bass joins."),
    "range": ("Rule 2: territory; the island only fits three.", "Top-down Isle; three territory rings painted on the voxels (outside dimmed); two more Grimmaws appear, one per valley; card folds.",
              "Near top-down wide (el 66, dist 182).", ("pin, folded card", "three rings", "island"), "Day.", "2 RANGE · one valley per Grimmaw; TERRITORY / 1 VALLEY EACH", "Down to the den.", "Kick joins."),
    "energy": ("Rule 3: a big body hunts rarely and sleeps a lot.", "The Grimmaw walks to its den at the foot of the peak and lies down to sleep; Zs.",
               "Close profile (dist 40).", ("pin, Zs", "sleeping Grimmaw", "rock face"), "Day.", "3 ENERGY · hunts rarely, sleeps a lot; BIG BODY / HUNTS RARELY", "Orbit.", "Hats join."),
    "breed": ("Rule 4: slow breeding.", "Winter falls over the den (snow on voxels and trees); one cub pops in beside the sleeping Grimmaw.",
              "Close (dist 34, az 108).", ("pin", "cub and parent", "snowy rocks"), "Winter mood.", "4 BREEDING · one cub, every few winters; 1 CUB", "Rise to the wide on 'Run'.", "Bells join."),
    "run2": ("The fixed world runs: it cycles instead of collapsing.", "Wide Isle, winters flicker past, years 3→23; graph shows prey and predators rising and falling; STABLE stamp.",
             "Wide (dist 196).", ("folded card, graph, stamp", "herds and three predators", "island"), "Day.", "YEARS 3–23; STABLE · NOTHING VANISHES", "Hold the wide.", "Full groove in F."),
    "twist": ("The locked rule, as an experiment: delete the monster.", "RULE 5? then selection brackets + DEL: the three Grimmaws fly apart into voxels; mossbacks boom to 380, strip the meadow to dirt, the forest thins, then the herd crashes.",
              "Wide (dist 170).", ("kinetic, DEL, graph, pin", "boom and bare earth", "island"), "Gloom on 'bare'.", "RULE 5?; DEL; NO PREDATOR graph; MEADOW / STRIPPED BARE",
              "Restore.", "Dark minor, filter down; drone on the crash."),
    "role": ("Unlock rule 5: its job.", "Row 5 unlocks (ROLE · keeps the grazers in check); the Grimmaws re-appear, the meadow and forest heal, the island ripples on 'together'.",
             "Medium-wide (dist 170).", ("unlocked card", "healing island", "void"), "Day.", "5/5", "Card goes full.", "Resolution to D major, bells."),
    "lesson": ("The takeaway: the full design check, screenshot-able.", "The complete field card (BEFORE YOU DESIGN A MONSTER / GRIMMAW / 5 rows ticked) with 'Design its place in the world.' in serif italic.",
               "Wide orbit (dist 190).", ("full card", "island at dusk", "stars"), "Dusk.", "Full card.", "Block wipe to the end card.", "D–G–Bm–A, warm."),
    "cta": ("Share CTA, then loop to frame 0.", "End card: logo, EPISODE 26 / 50, title, SHARE THIS with someone designing fantasy monsters; it lifts to reveal the hook frame and title again.",
            "Cut (under the card) to the hook pose.", ("end card", "the Isle", "void"), "Day for the loop frame.", "End card; then the hook title.", "Loop.", "G–D outro, faded to silence by 59.7 s."),
}


def build():
    ep = {
        "id": "ep26",
        "number": 26,
        "season": 2,
        "title": "Don't Design a Monster. Design an Ecosystem.",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.05},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "A curious lab-host energy: brisk, warm, a little playful. The hook is a genuine puzzle. 'Press run' is a small grin. "
                         "The year count is a quick, flat countdown. 'It ends it' lands low and slow. 'The fifth is the twist' teases. "
                         "Rules one to four are crisp list beats. 'Rule five? Delete the monster' is mischievous; the lesson is sure and warm.",
        },
        "timing": {"leadIn": 0.2, "tail": 2.4, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L6", "from": "It"}, {"line": "L14", "from": "Rule", "to": "Delete"}],
        "lines": [{"id": i, "shot": s, "text": t, "pauseAfter": p, "emphasis": em} for i, s, t, p, em in LINES],
        "shots": [],
        "world": world(),
    }
    G = overlays()
    for s in SHOTS:
        n = NOTES[s]
        shot = {"id": s, "scene": "world", "purpose": n[0], "visual": n[1], "camera": n[2],
                "layers": {"foreground": n[3][0], "midground": n[3][1], "background": n[3][2]}, "lighting": n[4],
                "onScreenText": n[5], "transition": n[6], "music": n[7], "graphics": G[s], "sfx": SFX.get(s, [])}
        if s in ("hook", "lesson", "cta"):
            shot["captions"] = False
        if s == "cta":
            shot["hideLogoBug"] = True
            shot["hideLogoBugUntil"] = {"shot": "cta", "offset": 4.95}
        ep["shots"].append(shot)
    ep["music"] = MUSIC
    ep["mix"] = {"musicLufs": -28.0, "duckDb": -6.0, "sfxLufs": -29.0}
    ep["metadata"] = METADATA
    return ep


# ---------------------------------------------------------------- sound (pipeline/score_s2.py palette)

def hit(sound, at, gain):
    return {"sound": sound, "at": at, "gain": gain}


def bed(sound, a, b, gain):
    return {"sound": sound, "from": a, "to": b, "gain": gain}


SFX = {
    "hook": [hit("sting", {"shot": "hook"}, -9), hit("worldRipple", {"shot": "hook", "offset": 0.05}, -17)],
    "setup": [bed("stomp", cue("L2", "This"), cue("L2", "This", 2.2), -17), hit("cardSlide", cue("L2", "This", -0.1), -17),
              hit("check", cue("L2", "eats"), -20), hit("runPress", cue("L3", "run."), -11), hit("worldRipple", cue("L3", "run."), -16)],
    "run1": [bed("simTicks", cue("L3", "run.", 0.3), cue("L4", "gone.", 0.2), -21), bed("losses", cue("L4", "everywhere.", 0.35), cue("L4", "gone."), -23)],
    "starve": [bed("stomp", cue("L5", "With", -0.1), cue("L5", "With", 1.4), -18), hit("crash", cue("L5", "starves", 0.1), -19)],
    "ends": [hit("stamp", cue("L6", "eats"), -10)],
    "rehook": [hit("rewind", cue("L6", "it.", 0.45), -11), hit("cardSlide", cue("L7", "limits.", -0.1), -17)],
    "prey": [hit("check", cue("L8", "prey"), -13), bed("births", cue("L8", "breeds"), cue("L8", "eaten.", 0.3), -20)],
    "range": [hit("check", cue("L9", "territory."), -13), hit("ringOn", cue("L9", "territory."), -15), hit("ringOn", cue("L9", "Grimmaw", 0.1), -19),
              hit("ringOn", cue("L9", "whole"), -19)],
    "energy": [hit("check", cue("L10", "energy."), -13), bed("stomp", cue("L10", "energy.", 0.1), cue("L10", "energy.", 2.0), -18),
               hit("sleepZ", cue("L10", "sleeps", 0.3), -14), hit("sleepZ", cue("L10", "lot.", 0.6), -18)],
    "breed": [hit("check", cue("L11", "slow"), -13), hit("snowAir", cue("L11", "slow", -0.2), -15), hit("cubPop", cue("L11", "cub"), -12)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L13", "vanishes.", 0.6), -21),
             hit("stamp", cue("L13", "nothing"), -13)],
    "twist": [hit("delete", cue("L14", "Delete", 0.05), -9), hit("runPress", cue("L15", "The"), -14), hit("boomPop", cue("L15", "boom,"), -13),
              bed("simTicks", cue("L15", "The", 0.2), cue("L15", "starve.", 0.4), -22), bed("losses", cue("L15", "then"), cue("L15", "starve.", 0.5), -20),
              hit("crash", cue("L15", "starve."), -15)],
    "role": [hit("unlock", cue("L16", "job."), -10), hit("restore", cue("L16", "Grimmaw"), -12), hit("worldRipple", cue("L16", "together."), -14)],
    "lesson": [hit("cardSlide", cue("L17", "Don't", -0.3), -18)],
    "cta": [hit("restore", cue("L18", "Share", -0.3), -21)],
}

Dm, Bb, F, C, A, Gm = ["D3", "F3", "A3", "D4"], ["Bb2", "D3", "F3", "Bb3"], ["F3", "A3", "C4", "F4"], ["C3", "E3", "G3", "C4"], ["A2", "C#3", "E3", "A3"], ["G2", "Bb2", "D3", "G3"]
D, G, Bm = ["D3", "F#3", "A3", "D4"], ["G2", "B2", "D3", "G3"], ["B2", "D3", "F#3", "B3"]
LOW = ["D2", "A2", "D3", "F3"]


def sec(at, chords, layers, level, bpc=4, **kw):
    return {"from": at, "chords": chords, "beatsPerChord": bpc, "layers": layers, "level": level, **kw}


MUSIC = {
    "engine": "s2",
    "key": "D minor, resolving to D major",
    "bpm": 100,
    "sections": [
        sec({"shot": "hook"}, [Dm, Bb], {"pad": 0.6, "arp": 0.7, "arpRate": 8}, 0.5),
        sec(cue("L2", "Let's", -0.1), [Dm, Bb, F, C], {"pad": 0.5, "arp": 0.8, "arpRate": 8, "bass": 0.6, "kick": "heart"}, 0.55),
        sec(cue("L3", "run."), [Dm, Dm, Bb, A], {"pad": 0.3, "arp": 1.0, "arpRate": 16, "bass": 1.0, "bassEighths": True, "kick": "four", "hats": 16, "clap": 0.6}, 0.66, bpc=2, bright=1.3),
        sec(cue("L5", "With", -0.2), [LOW], {"pad": 0.6, "kick": "heart"}, 0.42, bpc=8, dark=True),
        sec(cue("L6", "A"), [["D2", "A2", "D3"]], {"pad": 0.4}, 0.3, bpc=8, dark=True),
        sec(cue("L7", "Real", -0.1), [Dm, C, Bb, A], {"pad": 0.5, "arp": 0.7, "arpRate": 8}, 0.5, bpc=2),
        sec(cue("L8", "One:"), [F, C, Dm, Bb], {"pad": 0.5, "arp": 0.7, "arpRate": 8, "bass": 0.7}, 0.55),
        sec(cue("L9", "Two:"), [F, C, Dm, Bb], {"pad": 0.5, "arp": 0.7, "arpRate": 8, "bass": 0.7, "kick": "half"}, 0.56),
        sec(cue("L10", "Three:"), [F, C, Dm, Bb], {"pad": 0.5, "arp": 0.8, "arpRate": 8, "bass": 0.7, "kick": "half", "hats": 8}, 0.58),
        sec(cue("L11", "Four:"), [F, C, Dm, Bb], {"pad": 0.6, "arp": 0.8, "arpRate": 8, "bass": 0.7, "kick": "half", "hats": 8, "bells": 0.8}, 0.6),
        sec(cue("L12", "Run"), [F, C, Bb, F], {"pad": 0.35, "arp": 1.0, "arpRate": 16, "bass": 1.0, "bassEighths": True, "kick": "four", "hats": 16, "clap": 0.8}, 0.7, bpc=2, bright=1.4),
        sec(cue("L14", "Rule", -0.1), [Dm, Bb, Gm, A], {"pad": 0.4, "arp": 0.8, "arpRate": 16, "bass": 0.8, "kick": "one"}, 0.58, bpc=2, bright=0.6, dark=True),
        sec(cue("L15", "starve.", -0.3), [LOW], {"pad": 0.5, "kick": "heart"}, 0.4, bpc=8, dark=True),
        sec(cue("L16", "Rule"), [Bb, F, C, D], {"pad": 0.5, "arp": 0.8, "arpRate": 8, "bass": 0.7, "kick": "half", "bells": 0.8}, 0.6, bpc=2),
        sec(cue("L17", "Don't", -0.2), [D, G, Bm, A], {"pad": 0.6, "arp": 0.6, "arpRate": 8, "bass": 0.5, "bells": 0.5}, 0.55),
        sec(cue("L18", "Share"), [G, D], {"pad": 0.6, "arp": 0.5, "arpRate": 8, "bells": 0.4}, 0.5),
    ],
    "drones": [{"from": cue("L5", "With", -0.2), "to": cue("L7", "Real"), "notes": ["D1", "A1"], "level": 1.0}],
    "events": [
        {"type": "duck", "at": cue("L6", "It"), "pre": 0.2, "dur": 1.4, "gain": 0.4},
        {"type": "duck", "at": cue("L14", "Delete"), "pre": 0.15, "dur": 1.0, "gain": 0.5},
    ],
    "fadeOut": {"at": {"shot": "cta", "offset": 3.5}, "dur": 1.5},
}

TAGS = "#Worldbuilding #FantasyWriting #CreatureDesign #WritingTips #WorldcraftShorts"
BODY = (
    "If your giant predator eats everything, why hasn't everything gone extinct?\n\n"
    "We ran it. The Grimmaw eats anything that moves. By year five the mossbacks are gone, and then the Grimmaw starves too. "
    "A monster that eats everything doesn't rule your world. It ends it.\n\n"
    "Real predators live inside limits: prey that breeds faster than it's eaten, one territory per predator, a big body that hunts rarely "
    "and sleeps a lot, and slow breeding. Then the twist: delete the monster, and the grazers strip the meadow bare and starve instead. "
    "The predator was holding the island together.\n\n"
    "Don't design a monster. Design its place in the world.\n\n"
    "Share this with someone designing fantasy monsters."
)
METADATA = {
    "youtube": {
        "title": "Don't Design a Monster. Design an Ecosystem. (Worldbuilding)",
        "titleAlternate": "Why your apex predator would starve",
        "description": BODY + "\n\nEpisode 26 of 50 in Worldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 6: Creatures and Species.\n\n" + TAGS,
        "pinnedComment": "Design check: which of the five does your monster break? Prey, range, energy, breeding, or its role? Name the creature and the rule.",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated creature sprite; the island and creatures are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "Your apex predator would starve 🦖 We ran it: it eats everything, then there's nothing left, then it's gone too. 5 rules for a believable monster, and #5 is the twist. " + TAGS,
        "pinnedComment": "Which rule does your monster break: prey, range, energy, breeding, or its role?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nEpisode 26 of 50. Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "What keeps the scariest creature in your world from eating everything? Prey, territory, energy, breeding, or something it's needed for?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": "Your monster would starve.\n\n" + BODY + "\n\nEpisode 26 of 50 · Worldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": "First 26 characters: 'Your monster would starve.'",
        "pinnedComment": "Save the five-rule checklist, then tell us: which rule is your monster missing?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep26] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots")
