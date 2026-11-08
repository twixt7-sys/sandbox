"""Generate episodes/ep28/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep28/make_ep28.py
EP28's own device is the SPECIES EDITOR: a character-creator panel whose trait sliders run from HUMAN to the Fenn's own
biology. The lazy version moves one slider (EARS) and nothing in the world changes; every real trait visibly rebuilds
the village and the Fenn's bodies, and a HUMAN-LIKE meter falls from 96 % to 0 %. Camera language: at the Fenn's eye
height (low, long lenses), where EP27 rode on a dragon and EP26 stood back. Motif colour: bioluminescent teal #5fe0c0.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep28" / "timing.json"


def cue(line, word=None, offset=0.0, nth=None):
    c = {"line": line}
    if word:
        c["word"] = word
    if nth:
        c["nth"] = nth
    if offset:
        c["offset"] = round(offset, 3)
    return c


# The block wipe into the end card: the camera cuts back onto frame 0's pose under it (everything else in the world
# is already in its frame-0 state by then: the Fenn as they really are, the hall on the lake).
WIPE = cue("L17", "Invent", -0.3)


def loop_span():
    if not TIMING.exists():
        print("[make_ep28] no timing.json yet: using an estimate for the loop camera; rerun after tts.py")
        return 11.4
    tm = json.loads(TIMING.read_text())
    words = next(l for l in tm["lines"] if l["id"] == "L17")["words"]
    w = next(w for w in words if w["text"].strip(".,!?:;").lower() == "invent")["start"] - 0.3
    return round(tm["duration"] - w, 3)


LINES = [
    ("L1", "hook", "Giving elves pointy ears doesn't make them a distinct civilization.", 0.3, ["ears", "civilization."]),
    ("L2", "hook", "Meet the Fenn. They stacked these stones.", 0.3, ["fenn.", "stones."]),
    ("L3", "setup", "Now the lazy version: humans, with different ears.", 0.25, ["lazy", "ears."]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "A hundred years later: same houses, same barns, same bell tower.", 0.35, ["same", "tower."]),
    ("L6", "drop", "Spot the difference. There isn't one.", 0.45, ["difference.", "isn't"]),
    ("L7", "rehook", "Biology should change the build. Four traits are easy. The fifth is the twist.", 0.3, ["biology", "twist."]),
    ("L8", "senses", "One: senses. They see in the dark, so they live underground.", 0.2, ["dark,", "underground."]),
    ("L9", "lifespan", "Two: lifespan. Four hundred years, so they build in stone.", 0.2, ["hundred", "stone."]),
    ("L10", "family", "Three: family. One clan, one great hall.", 0.2, ["clan,", "hall."]),
    ("L11", "needs", "Four: needs. Their skin must stay wet, so they build on the lake.", 0.3, ["wet,", "lake."]),
    ("L12", "run2", "Run it again. Nothing here looks human now.", 0.35, ["nothing", "human"]),
    ("L13", "twist", "Rule five? How they talk. The Fenn speak in light.", 0.3, ["talk.", "light."]),
    ("L14", "twist", "So their hall has no walls, only windows.", 0.3, ["walls,", "windows."]),
    ("L15", "role", "And from the human valley? Ghost lights on the lake.", 0.35, ["ghost", "lake."]),
    ("L16", "lesson", "Pointy ears are a costume. Biology is a blueprint.", 0.35, ["costume.", "blueprint."]),
    ("L17", "cta", "Invent one biological trait that would completely change a species' society. Comment it.", 0.25, ["invent", "comment"]),
    ("L18", "next", "Part 28 of 50. Follow for part 29: someone on the Isle never dies.", 0.25, ["follow", "dies."]),
]

SHOTS = ["hook", "setup", "run1", "drop", "rehook", "senses", "lifespan", "family", "needs", "run2", "twist", "role", "lesson", "cta", "next"]


# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle. EP27's humans live in the valley under the cliff (their sky-proof village, unchanged); the
# dragon is away hunting this episode; the Grimmaw grazes; EP27's cairn stands where the Fenn stacked it.
G1_HOME = (15.5, 9.5)           # the Grimmaw grazes the south-east meadow this time (out of the village shots)
LAIR = (-2.5, -12.5)
CAIRN = (8.95, -5.38)
HERO = (8.9, -6.6)                       # the Fenn who stacked the cairn (frame 0 and the loop frame)
FENN_A = (13.6, -5.8)                    # the lazy version: a copy of a human village on the east meadow
LAKE_HALL = (6.0, 4.6)                   # the Fenn's own home: one great hall on stilts on the lake
HUMAN_B = [("hall", (-3.6, -4.6)), ("house", (-1.8, -2.4)), ("house", (-4.8, -2.4)), ("house", (-1.0, -5.8)),
           ("house", (-5.6, -0.9)), ("house", (-3.4, -0.7)), ("house", (0.4, -4.2))]
HUMAN_TOWER = (-6.4, -5.6)
HUMAN_ROAD = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
# the Fenn's copy, house for house (the first five stand at the reset, the last two are built during run 1)
FENN_HOUSES = [("hall", (16.4, -8.4)), ("house", (12.2, -3.8)), ("house", (14.6, -3.4)), ("house", (11.6, -7.0)),
               ("house", (14.2, -7.8)), ("house", (16.6, -5.4)), ("house", (12.8, -10.0))]
FENN_ROAD = [[11.6, -5.2], [14.0, -12.0], [15.6, -15.6]]
FENN_TOWER = (15.2, -11.2)


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


# The lazy version replaces the real Fenn here (under the editor's RESET wipe), and the episode rebuilds them trait by trait.
RESET = cue("L3", "lazy", -0.15)


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    step = lambda at, v: [at, v, "step"]

    # ---- the Fenn: body (editor sliders) and crowd
    eyes = [[shot("hook"), 1], step(RESET, 0), [cue("L8", "dark,", -0.2), 0], [cue("L8", "dark,", 0.4), 1, "linear"]]
    wet = [[shot("hook"), 1], step(RESET, 0), [cue("L11", "wet,", -0.2), 0], [cue("L11", "wet,", 0.4), 1, "linear"]]
    glow = [[shot("hook"), 1], step(RESET, 0), [cue("L13", "light.", -0.1), 0], [cue("L13", "light.", 0.4), 1, "linear"]]
    pop = [[shot("hook"), 40], step(RESET, 24), [cue("L4", "run."), 24], [cue("L5", "tower.", 0.3), 40, "linear"],
           [cue("L7", "Biology", -0.2), 40], [cue("L7", "Biology", 0.3), 24, "linear"], [cue("L12", "Run", 0.2), 24], [cue("L12", "now.", 0.3), 40, "linear"]]
    human = [[shot("hook"), 0], step(RESET, 96), [cue("L8", "dark,"), 96], [cue("L8", "underground.", 0.4), 78, "linear"],
             [cue("L9", "stone."), 78], [cue("L9", "stone.", 0.4), 60, "linear"], [cue("L10", "great"), 60], [cue("L10", "hall.", 0.4), 42, "linear"],
             [cue("L11", "lake."), 42], [cue("L11", "lake.", 0.4), 22, "linear"], [cue("L15", "Ghost"), 22], [cue("L15", "lake.", 0.2), 0, "linear"]]
    site = [[shot("hook"), 1], step(RESET, 0), [cue("L11", "build", 0.0), 0], [cue("L11", "lake.", 0.5), 1, "linear"]]
    hero = [
        pk(shot("hook"), *HERO, "stack", face=-90),
        pk(cue("L2", "stones.", 0.3), *HERO, "idle", face=-90),
        pk(RESET, *HERO, "hidden"),
        pk(WIPE, *HERO, "stack", face=-90),
    ]

    # ---- the Fenn's village (the second settlement): the copy, then trait by trait its own
    houses = []
    for i, (kind, a) in enumerate(FENN_HOUSES):
        late = i >= 5   # built during run 1
        k0 = cue("L10", "one", 0.1 + i * 0.08, nth=2)
        show = [[shot("hook"), 0], step(RESET, 0 if late else 1)]
        if late:
            show += [[cue("L5", "same", 0.0, nth=2), 0], [cue("L5", "same", 0.5 + (i - 5) * 0.4, nth=2), 1, "linear"]]
        show += [[cue("L7", "Biology", -0.2), 1]]
        if late:
            # rewound with the years at the re-hook, and never rebuilt (the real Fenn don't build houses)
            show += [[cue("L7", "Biology", 0.3), 0, "linear"]]
        else:
            show += [[k0, 1], [cue("L10", "hall.", 0.0 + i * 0.05), 0, "linear"]]
        houses.append({"kind": kind, "a": list(a), "face": 0, "show": show})
    great = {"kind": "greathall", "a": [FENN_A[0] - 0.4, FENN_A[1] + 0.2], "b": list(LAKE_HALL), "stiltsB": 1.6, "face": 0,
             "show": [[shot("hook"), 1], step(RESET, 0), [cue("L10", "great", -0.1), 0], [cue("L10", "hall.", 0.3), 1, "out"]]}
    fenn_village = {
        "buildings": houses + [great],
        "roof": [[shot("hook"), 1]],
        "sink": [[shot("hook"), 1], step(RESET, 0), [cue("L8", "underground.", -0.1), 0], [cue("L8", "underground.", 0.6), 1, "linear"]],
        "stone": [[shot("hook"), 1], step(RESET, 0), [cue("L9", "stone.", -0.15), 0], [cue("L9", "stone.", 0.5), 1, "linear"]],
        "place": [[shot("hook"), 1], step(RESET, 0), [cue("L11", "build"), 0], [cue("L11", "lake.", 0.5), 1, "linear"]],
        "open": [[shot("hook"), 1], step(RESET, 0), [cue("L14", "walls,", -0.2), 0], [cue("L14", "walls,", 0.5), 1, "linear"]],
        "glow": [[shot("hook"), 1], step(RESET, 0), [cue("L14", "windows.", -0.2), 0], [cue("L14", "windows.", 0.4), 1, "linear"]],
        "pens": [],
        "roads": {"a": FENN_ROAD}, "route": [[shot("hook"), 0]],
        "tradeKey": "tradeF", "lanterns": [[shot("hook"), 0]],
        "tower": {"x": FENN_TOWER[0], "z": FENN_TOWER[1], "h": 4.5, "keys": [[shot("hook"), 0], step(RESET, 1), [cue("L10", "one", 0.1, nth=2), 1], [cue("L10", "hall.", 0.2), 0, "linear"]], "rings": [cue("L5", "bell")]},
    }
    tradeF = [[shot("hook"), 0], step(RESET, 4), [cue("L10", "one", 0.0, nth=2), 4], [cue("L10", "hall.", 0.0), 0, "linear"]]

    # ---- the human valley (EP27's sky-proof village, unchanged: slate and turf, barns, the watchtower, the forest road)
    human_valley = {
        "buildings": [{"kind": k, "a": list(a), "face": 0} for k, a in HUMAN_B],
        "roof": [[shot("hook"), 1]],
        "pens": [{"a": [2.2, -6.4], "r": 2.2}], "cover": [[shot("hook"), 1]],
        "roads": {"b": HUMAN_ROAD}, "route": [[shot("hook"), 1]],
        "tradeKey": "tradeH", "lanterns": [[shot("hook"), 0], [cue("L13", "Rule", -0.3), 0], [cue("L13", "Rule", 0.3), 1], [cue("L16", "Pointy", -0.3), 1], [cue("L16", "Pointy", 0.3), 0]],
        "tower": {"x": HUMAN_TOWER[0], "z": HUMAN_TOWER[1], "h": 6.0, "keys": [[shot("hook"), 1]]},
    }

    clock = [[shot("hook"), 0], [cue("L4", "run."), 0], [cue("L5", "tower.", 0.4), 100, "linear"], [cue("L6", "one.", 0.4), 100],
             [cue("L7", "Biology", 0.3), 0, "linear"], [cue("L12", "Run", 0.1), 0], [cue("L12", "now.", 0.5), 100, "linear"],
             [WIPE, 100], [cue("L17", "Invent", -0.28), 0, "step"]]
    speed = [[shot("hook"), 1], [cue("L4", "run."), 1], [cue("L4", "run.", 0.35), 9], [cue("L5", "tower.", 0.3), 9], [cue("L6", "Spot"), 1],
             [cue("L6", "one.", 0.3), 1], [cue("L6", "one.", 0.5), -10], [cue("L7", "Biology", 0.2), -10], [cue("L7", "Biology", 0.4), 1],
             [cue("L12", "Run", 0.1), 1], [cue("L12", "Run", 0.4), 9], [cue("L12", "now.", 0.5), 9], [cue("L13", "Rule"), 1]]
    # the EP29 tease: years race by (winters flicker, the forest thins and grows back) while the frame holds
    snow = [[shot("hook"), 0], [cue("L18", "never", -0.1), 0]]
    for k in range(3):
        b0 = 0.0 + k * 0.42
        snow += [[cue("L18", "never", b0), 0], [cue("L18", "never", b0 + 0.14), 0.7, "linear"], [cue("L18", "never", b0 + 0.36), 0, "linear"]]
    forest = [[shot("hook"), 1], [cue("L18", "never", 0.0), 1], [cue("L18", "never", 0.6), 0.55, "linear"], [cue("L18", "dies.", 0.5), 1, "linear"]]
    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run"), cue("L15", "Ghost")]
    rings = [{"x": LAKE_HALL[0], "z": LAKE_HALL[1], "r": 5.0, "on": cue("L15", "Ghost"), "off": cue("L16", "Pointy", -0.3), "color": "#5fe0c0"}]

    # Camera language: at the Fenn's eye height, long lenses. The hook is low and close on the one who stacked the cairn.
    hook_pose = dict(az=90, el=8, dist=16, target=(8.9, 6.2, -6.0), fov=28)
    camera = [
        cam(shot("hook"), drift=0.8, **hook_pose),
        cam(cue("L1", "Giving", 0.0), hook_pose["az"] + 0.3, hook_pose["el"], 14.0, (8.9, 6.1, -6.0), fov=hook_pose["fov"], dur=3.8, drift=0.8),
        cam(RESET, -10, 9, 38, (13.4, 9.0, -6.0), fov=24, dur=0.01, cut=True, drift=1.5),
        cam(cue("L4", "run.", 0.05), 18, 44, 192, (3.0, 10.5, -2.0), fov=26, dur=1.3, drift=2.0),
        # spot the difference: both villages side by side from the south
        cam(cue("L6", "Spot", -0.25), 2, 26, 110, (5.6, 9.0, -4.6), fov=26, dur=1.2, drift=0.8),
        cam(cue("L6", "one.", 0.5), 20, 30, 96, (8.0, 9.0, -4.0), fov=24, dur=0.9, drift=1.5),
        cam(cue("L8", "One:", -0.2), 20, 10, 44, (13.6, 8.6, -6.0), fov=24, dur=1.1, drift=1.5),
        cam(cue("L9", "Two:", -0.2), 32, 9, 40, (13.6, 8.0, -6.0), fov=24, dur=1.1, drift=1.5),
        cam(cue("L10", "Three:", -0.2), 30, 14, 52, (13.4, 9.0, -5.8), fov=24, dur=1.1, drift=1.0),
        cam(cue("L11", "Four:", -0.15), 8, 22, 70, (9.0, 8.0, 0.0), fov=24, dur=1.3, drift=1.5),
        cam(cue("L12", "Run", -0.05), 25, 44, 196, (2.0, 12.0, 0.0), fov=26, dur=1.0, drift=3.0),
        # the twist at the hall on the lake, at night, at a Fenn's eye height on the deck
        cam(cue("L13", "Rule", -0.1), 25, 7, 34, (LAKE_HALL[0], 7.0, LAKE_HALL[1] - 0.4), fov=30, dur=1.0, drift=1.5),
        # ghost lights: from the human valley, across the island to the lake
        cam(cue("L15", "And", -0.15), -105, 14, 26.0, (LAKE_HALL[0], 5.0, LAKE_HALL[1]), fov=34, dur=1.0, drift=0.6),
        cam(cue("L16", "Pointy", -0.25), 15, 30, 190, (2.0, 2.0, 0.0), fov=26, dur=1.6, drift=3.0),
        cam(WIPE, hook_pose["az"] - 0.8 * loop_span(), hook_pose["el"], hook_pose["dist"], hook_pose["target"], fov=hook_pose["fov"], cut=True, drift=0.8),
    ]
    light = [
        {"at": shot("hook"), "mood": "golden"},
        {"at": RESET, "mood": "day", "dur": 0.4},
        {"at": cue("L6", "Spot", -0.2), "mood": "gloom", "dur": 1.0},
        {"at": cue("L6", "one.", 0.5), "mood": "day", "dur": 0.8},
        {"at": cue("L8", "dark,", -0.4), "mood": "night", "dur": 0.8},
        {"at": cue("L9", "Two:", -0.2), "mood": "dusk", "dur": 0.8},
        {"at": cue("L10", "Three:", -0.2), "mood": "day", "dur": 0.8},
        {"at": cue("L13", "Rule", -0.2), "mood": "night", "dur": 0.8},
        {"at": cue("L16", "Pointy", -0.3), "mood": "golden", "dur": 2.2},
    ]
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": [[shot("hook"), 40]], "max": 60, "base": 40, "centers": [[2.2, -6.4], [3.4, -7.8]], "skin": "sheep"},
        "pred": [[shot("hook"), 1]],
        "predators": [{"id": "g1", "keys": [pk(shot("hook"), *G1_HOME, "idle", face=200)]}],
        "series": {"pop": pop, "human": human, "tradeF": tradeF, "tradeH": [[shot("hook"), 4]]},
        "settlement": human_valley,
        "settlements": [fenn_village],
        "folk": {"count": pop, "centers": [[13.4, -5.6], [12.4, -4.2], [14.6, -7.0]], "centersB": [[5.4, 4.0], [6.6, 5.0], [5.6, 5.2]],
                 "site": site, "eyes": eyes, "wet": wet, "glow": glow, "hero": hero, "spread": 2.4},
        "props": [{"kind": "cairn", "x": CAIRN[0], "z": CAIRN[1], "stones": [[shot("hook"), 3]]}],
        # the hook's line of sight (the camera stands south of the cairn): no meadow trees in front of the Fenn
        "clearTrees": [[11.5, -6.0, 2.2], [14.5, -6.0, 2.2], [17.5, -6.0, 2.2], [20.0, -6.0, 2.0]],
        "layers": {"snow": snow, "forest": forest, "ripple": ripple, "rings": rings},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "SENSES", "text": "see in the dark", "at": cue("L8", "senses.")},
    {"n": 2, "label": "LIFESPAN", "text": "400 years: stone", "at": cue("L9", "lifespan.")},
    {"n": 3, "label": "FAMILY", "text": "one clan, one hall", "at": cue("L10", "family.")},
    {"n": 4, "label": "NEEDS", "text": "wet skin: the lake", "at": cue("L11", "needs.")},
    {"n": 5, "label": "VOICE", "text": "they speak in light", "at": cue("L7", "easy."), "locked": True, "unlockAt": cue("L15", "Ghost")},
]
SPRITE = {"sprite": "ep28/fenn_sprite.png", "spriteW": 52, "spriteH": 127}
CARD_SPRITE = {"sprite": "ep28/fenn_sprite.png", "spriteW": 52, "spriteH": 127}


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "POINTY EARS", "color": "ember", "size": 84}, {"text": "AREN'T A", "size": 84}]
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 96, "start": {"shot": "hook"}, "end": cue("L1", "doesn't", -0.06), "preShow": True},
        {"type": "kinetic", "parts": [*hook_text, {"text": "CIVILIZATION.", "at": cue("L1", "civilization."), "color": "rust", "size": 78}],
         "y": 452, "size": 96, "start": cue("L1", "doesn't", -0.04), "end": cue("L2", "Meet", -0.1), "preShow": True},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 28 · CREATURES", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Meet", -0.05), "end": RESET, "dietAt": cue("L2", "stacked"),
         "kicker": "FIELD CARD · NO. 003", "kind": "INTELLIGENT SPECIES", "name": "FENN", "dietLabel": "BUILT", "diet": "these stones", **CARD_SPRITE},
    ]
    lazy_rows = [
        {"label": "EARS", "left": "ROUND", "right": "POINTY", "at": cue("L3", "ears.", -0.1)},
        {"label": "EYES", "left": "HUMAN", "right": "?"},
        {"label": "LIFESPAN", "left": "HUMAN", "right": "?"},
        {"label": "FAMILY", "left": "HUMAN", "right": "?"},
        {"label": "SKIN", "left": "HUMAN", "right": "?"},
        {"label": "VOICE", "left": "HUMAN", "right": "?"},
    ]
    G["setup"] += [
        {"type": "blockWipe", "at": RESET, "dur": 0.34, "color": "#06302a"},
        {"type": "editor", "y": 448, "kicker": "SPECIES EDITOR · THE LAZY VERSION", "title": "FENN = HUMAN + EARS", "rows": lazy_rows,
         "start": cue("L3", "lazy", 0.05), "end": cue("L4", "Press", -0.1)},
        {"type": "readout", "key": "human", "label": "HUMAN-LIKE", "start": cue("L3", "humans,", -0.1), "end": cue("L17", "Invent", -0.52), "sub": "ITS OWN PEOPLE"},
        {"type": "simBar", "counters": [{"icon": "fenn", "label": "FENN", "key": "pop", "color": "#5fe0c0"}], "start": cue("L4", "Press", -0.15), "end": cue("L16", "Pointy", -0.3),
         "runAt": [cue("L4", "run."), cue("L12", "Run")]},
    ]
    G["run1"] += [
        {"type": "simGraph", "y": 456, "h": 214, "from": cue("L4", "run."), "to": cue("L5", "tower.", 0.4), "start": cue("L5", "A", -0.15), "end": cue("L6", "Spot", -0.1), "caption": "YEARS 0–100",
         "series": [{"key": "pop", "color": "#5fe0c0", "max": 44, "label": "FENN"}, {"key": "human", "color": "#d0603f", "max": 100, "label": "HUMAN-LIKE"}]},
    ]
    G["drop"] += [
        {"type": "pin", "at": [-2.4, None, -3.0], "kicker": "THE VALLEY", "text": "HUMANS", "color": "parchment", "lift": 70, "size": 28, "start": cue("L6", "Spot", -0.05), "end": cue("L6", "one.", 0.45)},
        {"type": "pin", "at": [FENN_A[0], None, FENN_A[1]], "kicker": "THE MEADOW", "text": "FENN", "color": "#5fe0c0", "lift": 70, "size": 28, "start": cue("L6", "the", 0.0), "end": cue("L6", "one.", 0.45)},
        {"type": "stamp", "text": "0 DIFFERENCES", "sub": "HUMANS + EARS", "color": "rust", "y": 560, "size": 80, "start": cue("L6", "isn't"), "end": cue("L6", "one.", 0.45)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "one.", 0.5), "end": cue("L7", "Biology", 0.3)},
        {"type": "blockWipe", "at": cue("L6", "one.", 0.48), "dur": 0.34},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L16", "Pointy", -0.3), "sliders": True,
         "kicker": "SPECIES EDITOR · HUMAN → FENN", "title": "FENN", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L11", "Four:", -0.25), 0], [cue("L11", "Four:", 0.1), 1], [cue("L12", "Run", 0.4), 1], [cue("L12", "Run", 0.7), 1],
                      [cue("L15", "lake.", -0.1), 1], [cue("L15", "lake.", 0.25), 0]]},
    ]
    G["run2"] += [
        {"type": "stamp", "text": "ORIGINAL", "sub": "NOTHING COPIED", "color": "#5fe0c0", "rotate": -4, "y": 860, "size": 92, "start": cue("L12", "Nothing"), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}, {"text": "HOW THEY TALK", "at": cue("L13", "How"), "size": 76}],
         "size": 150, "y": 600, "start": cue("L13", "Rule", -0.02), "end": cue("L13", "The", -0.1)},
    ]
    G["role"] += [
        {"type": "pin", "at": [LAKE_HALL[0], 7.0, LAKE_HALL[1]], "kicker": "HUMAN LEGEND", "text": "GHOST LIGHTS", "color": "#5fe0c0", "lift": 120, "start": cue("L15", "Ghost"), "end": cue("L15", "lake.", -0.1)},
        {"type": "followChip", "start": cue("L15", "Ghost", 0.5), "end": cue("L16", "costume.", 0.1), "text": "FOLLOW", "sub": "PART 28/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "Pointy", -0.3), **({"unlockAt": cue("L16", "Pointy", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "Pointy", -0.3), "end": cue("L17", "Invent", -0.52), "kicker": "BEFORE YOU INVENT A SPECIES", "title": "FENN", "sliders": True, **SPRITE,
         "subtitle": "Biology is a blueprint.", "subtitleAt": cue("L16", "Biology")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 28 / 50",
         "title": "Intelligent Species Need More Than Different Ears", "cta": "COMMENT", "icon": "bubble", "with": "Invent one biological trait that would change a whole society."},
    ]
    gone = cue("L18", "dies.", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 28, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6, "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone, "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 29"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "29:", -0.1), "revealAt": cue("L18", "never"), "end": gone,
         "kicker": "NEXT RUN · 29", "title": "UNDYING", "sub": "SOMEONE NEVER DIES.", "sprite": "hourglass", "spritePx": 11},
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 96, "start": cue("L18", "dies.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("A different species isn't a human in a costume. Its biology (what it senses, how long it lives, how its families "
          "work, what its body needs, how it talks) decides what it builds and how it understands the world.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Close EP27's loop (who stacked the stones?) and stop the scroll on the claim.",
             "At a Fenn's eye height in golden light: the small teal Fenn who stacked EP27's cairn, lifting a stone over its head; big night eyes, fin frills, glowing spots. POINTY EARS / AREN'T A / CIVILIZATION. Then the field card: FENN · INTELLIGENT SPECIES · BUILT: these stones.",
             "Low and close (el 5, dist 17, fov 24), a slow push; the last 11 s return to this pose.", ("kinetic, field card", "the Fenn and the cairn", "the meadow, the peak"),
             "Golden hour.", "POINTY EARS / AREN'T A / CIVILIZATION.", "Reset wipe into the lazy version.", "Folk: kalimba, ocarina theme, hand drums; a hit on 'civilization'."),
    "setup": ("The lazy version, shown as a character editor: one slider moved, everything else left human.",
              "A teal block wipe (RESET): the Fenn become humans with pointy ears in a copy of a human village on the east meadow. The SPECIES EDITOR: EARS slides ROUND → POINTY; EYES, LIFESPAN, FAMILY, SKIN, VOICE stay on HUMAN. HUMAN-LIKE 96 %. RUN.",
              "Low at the copied village (el 6, dist 30), then the wide on 'run'.", ("editor, meter, sim bar", "elf-Fenn, copied houses", "meadow"),
              "Day.", "SPECIES EDITOR · FENN = HUMAN + EARS; HUMAN-LIKE 96%", "Rise to the wide.", "Pulse; a slider tick on 'ears'."),
    "run1": ("Run the lazy version: it grows exactly like a human village.", "Whole Isle; YEAR 0→100; the Fenn copy grows (two more houses, the bell tower rings); FENN 24→40; the graph's HUMAN-LIKE line stays flat at 96.",
             "Wide (dist 192).", ("sim bar + graph", "two look-alike villages", "island"), "Day.", "YEARS 0–100", "Down to both villages.", "Drive."),
    "drop": ("The punchline: spot the difference, there isn't one.", "Both villages side by side from the south, pinned HUMANS and FENN: slate roofs, barns, bell towers, the same. 0 DIFFERENCES · HUMANS + EARS.",
             "Medium (dist 110) on both villages.", ("pins, stamp", "the valley and the meadow", "the peak"), "Gloom.", "0 DIFFERENCES · HUMANS + EARS", "Rewind + block wipe.", "Drop; a boom on 'isn't'."),
    "rehook": ("Re-hook: the editor again, now with five real traits, four easy and one locked.", "REWIND to year 0; the SPECIES EDITOR · HUMAN → FENN checklist, each row a slider still on HUMAN, row 5 locked and blinking.",
               "Medium.", ("rewind, editor checklist", "the copy village", "island"), "Day.", "0/5", "Cut on 'One'.", "Mystery; a riser into 'the twist'."),
    "senses": ("Trait 1: night senses.", "Night. The SENSES slider slides; the Fenn's eyes grow huge and dark; the houses sink into the earth as turf mounds with glowing doors. HUMAN-LIKE 96→78.",
               "At eye height (el 4, dist 26).", ("slider, meter", "Fenn with night eyes, turf mounds", "night meadow"), "Night.", "1 SENSES · see in the dark", "Next trait.", "Folk 1: kalimba alone."),
    "lifespan": ("Trait 2: a 400-year life.", "Dusk. LIFESPAN slides; the mounds' walls turn to dressed stone and stand taller. 78→60.",
                 "Eye height (el 6, dist 30).", ("slider, meter", "stone mounds", "meadow"), "Dusk.", "2 LIFESPAN · 400 years: stone", "Next trait.", "Folk 2: hand drums join."),
    "family": ("Trait 3: one clan.", "Day. FAMILY slides; the houses, tower and road give way, and one great round hall rises in their place. 60→42.",
               "Eye height, a little higher (el 10, dist 40).", ("slider, meter", "the great hall rising", "meadow"), "Day.", "3 FAMILY · one clan, one hall", "Rise.", "Folk 3: bass joins."),
    "needs": ("Trait 4: wet skin.", "NEEDS slides; the Fenn's skin turns glossy teal and their ears become fins; the great hall unbuilds and rises again on stilts on the lake, and they follow. 42→22.",
              "Medium over the lake (el 22, dist 70).", ("slider, meter", "the hall on stilts", "lake"), "Day.", "4 NEEDS · wet skin: the lake", "Rise to the wide.", "Folk 4: the theme on ocarina."),
    "run2": ("Run the real Fenn: nothing is copied any more.", "Whole Isle; YEAR 0→100; the hall on the lake; FENN 24→40; ORIGINAL · NOTHING COPIED.",
             "Wide (dist 196).", ("stamp", "island", "void"), "Day.", "ORIGINAL · NOTHING COPIED", "Down to the lake at night.", "Folk at full, a stab and cymbal on 'nothing'."),
    "twist": ("The locked rule: how they talk.", "Night, on the hall's deck at a Fenn's eye height: RULE 5? HOW THEY TALK; the Fenn's spots light up; the hall's walls open into pillars and its windows flicker in travelling waves of light.",
              "Eye height on the deck (el 5, dist 22).", ("kinetic", "glowing Fenn, the open hall", "the night lake"), "Night.", "RULE 5? HOW THEY TALK", "Cross to the valley.", "Twist, then glow: choir, vibraphone ripples, celesta theme."),
    "role": ("Unlock rule 5, and the payoff: how another species understands them.", "From the human valley at night, across the island: lights flicker on the lake. HUMAN LEGEND · GHOST LIGHTS. Row 5 unlocks (VOICE · they speak in light); HUMAN-LIKE 00 %, ITS OWN PEOPLE.",
             "Long lens from the valley (el 7, dist 34, fov 22).", ("pin, unlocked card, meter, follow chip", "the ghost lights", "the night lake"), "Night.", "GHOST LIGHTS; 5/5; 00%", "Card goes full.", "Glow; a big D-major hit on 'lake'."),
    "lesson": ("The takeaway: the full editor card.", "The complete FENN card (BEFORE YOU INVENT A SPECIES, all five sliders on FENN) with 'Biology is a blueprint.' in serif italic.",
               "Wide orbit (dist 190).", ("full card", "the island at golden hour", "stars"), "Golden hour.", "Full card.", "Block wipe to the end card.", "Anthem; the World Engine chime as the card lands."),
    "cta": ("Comment CTA.", "End card: logo, PART 28 / 50, title, a speech-bubble COMMENT panel.", "Cut (under the block wipe) back to the hook pose.", ("end card", "the Isle", "void"),
            "Golden hour (the loop frame).", "End card.", "The card lifts on 'Part'.", "Outro."),
    "next": ("Say the part number, ask for the follow with a reason (part 29), open the next loop.",
             "The hook frame; PART 28/50; FOLLOW FOR PART 29; NEXT RUN 29 · UNDYING from a locked hourglass; behind, years race (winters flicker, the forest thins and grows back) while the Fenn stacks its stone; the hook title returns.",
             "The hook pose.", ("progress bar, follow button, next-run card", "the Fenn at the cairn", "the meadow in time-lapse"), "Golden hour.",
             "PART 28/50 · FOLLOW FOR PART 29 · NEXT RUN: UNDYING · SOMEONE NEVER DIES.", "Loop to frame 0.", "Tease over a held A, a horn call, the engine chime on 'Follow'."),
}


def build():
    ep = {
        "id": "ep28",
        "number": 28,
        "season": 2,
        "title": "Intelligent Species Need More Than Different Ears",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.07},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same lab host, warmer and more wondering for a people rather than a monster. The hook is a friendly challenge. "
                         "'Now the lazy version' is a knowing grin. 'Spot the difference. There isn't one.' lands dry. The traits are crisp. "
                         "'The Fenn speak in light' is a quiet wonder; 'Ghost lights on the lake' is the reveal. The comment ask is curious.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L13", "from": "Rule", "to": "talk."}],
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
        if s in ("hook", "lesson", "cta", "next"):
            shot["captions"] = False
        if s == "cta":
            shot["hideLogoBug"] = True
            shot["hideLogoBugUntil"] = cue("L18", "Part", 0.0)
        ep["shots"].append(shot)
    ep["music"] = MUSIC
    ep["mix"] = {"musicLufs": -25.0, "duckDb": -8.0, "sfxLufs": -29.0, "voiceFx": True}
    ep["metadata"] = METADATA
    return ep


# ---------------------------------------------------------------- sound (pipeline/score_s2.py palette)

def hit(sound, at, gain):
    return {"sound": sound, "at": at, "gain": gain}


def bed(sound, a, b, gain):
    return {"sound": sound, "from": a, "to": b, "gain": gain}


SFX = {
    "hook": [hit("chime", {"shot": "hook"}, -11), hit("worldRipple", {"shot": "hook", "offset": 0.05}, -17),
             hit("stompHit", cue("L1", "ears", 0.0), -19), hit("cardSlide", cue("L2", "Meet", -0.05), -18), hit("check", cue("L2", "stacked"), -20)],
    "setup": [hit("rewind", RESET, -15), hit("morph", RESET, -13), hit("cardSlide", cue("L3", "lazy", 0.05), -18),
              hit("slide", cue("L3", "ears.", -0.1), -12), hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "tower.", 0.2), -21), bed("births", cue("L5", "A"), cue("L5", "tower.", 0.2), -24),
             hit("towerBell", cue("L5", "bell"), -16), hit("restore", cue("L5", "same", 0.2, nth=2), -20)],
    "drop": [hit("stamp", cue("L6", "isn't"), -10)],
    "rehook": [hit("rewind", cue("L6", "one.", 0.45), -11), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "senses": [hit("check", cue("L8", "senses."), -13), hit("slide", cue("L8", "dark,", -0.2), -13), hit("morph", cue("L8", "dark,", -0.1), -13),
               hit("snowAir", cue("L8", "dark,", -0.4), -21), hit("stompHit", cue("L8", "underground.", 0.0), -16)],
    "lifespan": [hit("check", cue("L9", "lifespan."), -13), hit("slide", cue("L9", "hundred", 0.0), -13), hit("restore", cue("L9", "stone.", -0.1), -14),
                 bed("stomp", cue("L9", "stone.", -0.1), cue("L9", "stone.", 0.5), -22)],
    "family": [hit("check", cue("L10", "family."), -13), hit("slide", cue("L10", "clan,", 0.0), -13), hit("delete", cue("L10", "one", 0.1, nth=2), -18),
               hit("restore", cue("L10", "great", -0.1), -13), hit("stompHit", cue("L10", "hall.", 0.25), -15)],
    "needs": [hit("check", cue("L11", "needs."), -13), hit("slide", cue("L11", "wet,", -0.2), -13), hit("morph", cue("L11", "wet,", -0.1), -13),
              hit("restore", cue("L11", "build"), -14), hit("worldRipple", cue("L11", "lake."), -17)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L12", "now.", 0.5), -21),
             hit("stamp", cue("L12", "Nothing"), -13)],
    "twist": [hit("morph", cue("L13", "light.", -0.1), -12), hit("ringOn", cue("L14", "walls,", -0.1), -17), hit("eyeOn", cue("L14", "windows.", -0.2), -18)],
    "role": [hit("unlock", cue("L15", "Ghost"), -10), hit("ringOn", cue("L15", "Ghost"), -18), hit("worldRipple", cue("L15", "lake."), -15)],
    "lesson": [hit("engineWind", cue("L16", "Pointy", -0.8), -15), hit("chime", cue("L16", "Pointy", -0.3), -10), hit("cardSlide", cue("L16", "Pointy", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("cardSlide", cue("L17", "Invent", -0.1), -20)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11), hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "29:", -0.1), -18), hit("unlock", cue("L18", "never"), -15),
             bed("simTicks", cue("L18", "never", -0.05), cue("L18", "dies.", 0.4), -20), hit("snowAir", cue("L18", "never", 0.0), -19),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score: the series theme stays (D minor for the problem, D major for the payoff); EP28's band is folk (kalimba,
# ocarina, hand drums) for the Fenn at home, layering up as their traits return, and glow (choir, vibraphone) for the
# light-speech twist. Programs are set where the colour starts and set back where it ends.
FOLK_P = {"marimba": 108, "lead": 79}
GLOW_P = {"strings": 52, "glock": 11}
BACK_P = {"marimba": 12, "lead": 73, "strings": 48, "glock": 9}
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 98,
    "sections": [
        msec({"shot": "hook"}, "folk", ["Dm", "Bb"], "D minor", layer=4, programs=FOLK_P),
        msec(RESET, "pulse", ["Dm", "Bb", "F", "C"], "D minor", programs=BACK_P),
        msec(cue("L4", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.8),
        msec(cue("L6", "Spot", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "one.", 0.45), "mystery", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=2),
        msec(cue("L8", "One:", -0.1), "folk", ["Dm", "C", "Bb", "C"], "D minor", layer=1, programs=FOLK_P),
        msec(cue("L9", "Two:", -0.1), "folk", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "folk", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L11", "Four:", -0.1), "folk", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True, programs=BACK_P),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(cue("L13", "The", -0.1), "glow", ["Dm", "Bb", "Gm", "A"], "D minor", beatsPerChord=2, programs=GLOW_P),
        msec(cue("L15", "Ghost", -0.05), "anthem", ["D", "G", "Bm", "A"], "D major", programs=BACK_P),
        msec(cue("L17", "Invent", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "civilization."), "chord": "Dm"},
        {"kind": "boom", "at": cue("L6", "isn't"), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "Nothing"), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "Nothing")},
        {"kind": "hit", "at": cue("L15", "Ghost"), "chord": "D"},
        {"kind": "call", "at": cue("L18", "never"), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #Elves #WritingTips #WorldcraftShorts"
BODY = (
    "Giving elves pointy ears doesn't make them a distinct civilization.\n\n"
    "Meet the Fenn: they stacked the stones on the Isle. The lazy version is humans with different ears, and we ran it: "
    "a hundred years later, same houses, same barns, same bell tower. Spot the difference. There isn't one.\n\n"
    "So change their biology instead. They see in the dark, so they live underground. They live four hundred years, so "
    "they build in stone. One clan shares one great hall. Their skin must stay wet, so they build on the lake. "
    "Then the twist: they speak in light, so their hall has no walls, only windows. And to the humans in the valley? "
    "Ghost lights on the lake.\n\n"
    "Pointy ears are a costume. Biology is a blueprint.\n\n"
    "Invent one biological trait that would completely change a species' society. Comment it.\n\n"
    "Part 28 of 50. Follow for part 29: someone on the Isle never dies."
)
METADATA = {
    "youtube": {
        "title": "Intelligent Species Need More Than Different Ears (Worldbuilding)",
        "titleAlternate": "Your elves are just humans with ears",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 6: Creatures and Species.\n\n" + TAGS,
        "pinnedComment": "Comment one biological trait that would completely change a species' society. The weirder the better. (Part 29: someone on the Isle never dies.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated Fenn sprite; the island, villages and creatures are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "Your elves are just humans with ears 👂 We ran it: same houses, same barns, same bell tower. Then we changed their biology, and their whole village rebuilt itself. Trait #5 makes ghost stories. "
                   "What trait would you invent? Part 28/50 · follow for part 29 ⏳ " + TAGS,
        "pinnedComment": "Invent one biological trait that would completely change a species' society.",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "What's the most alien trait you've given a species, and what did it change about how they live?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": "Your elves are just humans.\n\n" + BODY + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": "First 27 characters: 'Your elves are just humans.'",
        "pinnedComment": "Save the species editor, then tell us: which biological trait would change a society the most?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep28] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots")
