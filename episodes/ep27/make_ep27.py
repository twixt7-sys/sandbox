"""Generate episodes/ep27/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep27/make_ep27.py
Copied from make_ep26.py and adapted. The world timeline (camera, the dragon's flights, the village layer, the HUD
series) is written here in Python, so flight paths and counts can be computed instead of typed by hand.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep27" / "timing.json"


def cue(line, word=None, offset=0.0, nth=None):
    c = {"line": line}
    if word:
        c["word"] = word
    if nth:
        c["nth"] = nth
    if offset:
        c["offset"] = round(offset, 3)
    return c


# The block wipe into the end card. Everything that must jump back to frame 0's state (the camera's hook pose, the
# dragon on its perch, the Grimmaw looking up, the naive village, 60 sheep, 6 carts) jumps on this frame, under the blocks.
WIPE = cue("L17", "What", -0.3)


def loop_span():
    """Seconds from the wipe to the end of the episode, so the end camera's drift lands exactly on frame 0's pose.
    Needs public/ep27/timing.json: run tts.py first, then this script (build.sh does both, in that order, on a rerun)."""
    if not TIMING.exists():
        print("[make_ep27] no timing.json yet: using an estimate for the loop camera; rerun after tts.py")
        return 10.4
    tm = json.loads(TIMING.read_text())
    words = next(l for l in tm["lines"] if l["id"] == "L17")["words"]
    w = next(w for w in words if w["text"].strip(".,!?:;").lower() == "what")["start"] - 0.3
    return round(tm["duration"] - w, 3)


LINES = [
    ("L1", "hook", "If dragons existed, your world's architecture would look very different.", 0.32, ["dragons", "different."]),
    ("L2", "setup", "Let's test it. This village was built before the dragon came.", 0.25, ["village", "dragon"]),
    ("L3", "setup", "Press run.", 0.3, ["run."]),
    ("L4", "run1", "Week one: thatch burns. Week two: open pens, empty. Week three: no one travels.", 0.35, ["burns.", "empty."]),
    ("L5", "drop", "Nobody fought a war. The village just stopped working.", 0.45, ["war.", "stopped"]),
    ("L6", "rehook", "So rebuild it. Four changes are easy. The fifth is the twist.", 0.3, ["rebuild", "twist."]),
    ("L7", "roofs", "One: roofs. Slate and turf don't burn.", 0.2, ["slate", "burn."]),
    ("L8", "pens", "Two: pens. Flocks sleep in covered barns.", 0.2, ["covered"]),
    ("L9", "place", "Three: place. Move into the valley, out of sight.", 0.2, ["valley,", "sight."]),
    ("L10", "travel", "Four: travel. Trade moves at night, under the trees.", 0.3, ["night,", "trees."]),
    ("L11", "run2", "Run it again.", 0.25, ["again."]),
    ("L12", "run2", "Now the roofs hold, the flocks grow, and trade returns.", 0.32, ["hold,", "returns."]),
    ("L13", "twist", "Rule five? Someone has to watch the sky.", 0.3, ["watch"]),
    ("L14", "twist", "A tower rises, with a bell. Whoever rings it decides when everyone hides.", 0.35, ["bell.", "decides"]),
    ("L15", "role", "Rule five is power. The dragon changed who's in charge.", 0.32, ["power.", "charge."]),
    ("L16", "lesson", "Don't just add a dragon. Ask what ordinary people do differently.", 0.35, ["dragon.", "ordinary"]),
    ("L17", "cta", "What would your civilization invent to survive dragons? Comment below.", 0.25, ["invent", "comment"]),
    ("L18", "next", "Part 27 of 50. Follow for part 28: something on the Isle learns to build.", 0.25, ["follow", "build."]),
]

SHOTS = ["hook", "setup", "run1", "drop", "rehook", "roofs", "pens", "place", "travel", "run2", "twist", "role", "lesson", "cta", "next"]


# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle (world units; see src/s2/world/island.ts). EP27 adds the first village.
G1_HOME = (8.0, -1.0)          # the Grimmaw's meadow (EP26)
PERCH = (4.4, -1.8)            # where the dragon lands (frame 0 and the loop frame)
LAIR = (-2.5, -12.5)           # the dragon's rock shoulder under the peak
VILLAGE_A = (7.0, -9.0)        # the naive village: open meadow on the slope, the hall at its top
VALLEY_B = (-2.4, -3.6)        # the rebuilt village: the valley under the cliff, between the rock and the trees
TOWER = (-6.4, -5.6)           # the watchtower on the cliff above the valley
CAIRN = (11.8, -0.8)            # the EP28 tease: stones that stack themselves on the lake shore
# Buildings: (kind, site A, site B)
BUILDINGS = [
    ("hall", (3.6, -10.4), (-3.6, -4.6)),
    ("house", (6.2, -7.0), (-1.8, -2.4)),
    ("house", (8.7, -8.2), (-4.8, -2.4)),
    ("house", (5.6, -10.6), (-1.0, -5.8)),
    ("house", (9.2, -11.2), (-5.6, -0.9)),
    ("house", (3.9, -7.6), (-3.4, -0.7)),
    ("house", (7.6, -12.4), (0.4, -4.2)),
]
PEN_A, PEN_B = (11.2, -4.4), (2.2, -6.4)
HERD_A = [[11.2, -4.6], [9.6, -5.6]]
HERD_B = [[2.2, -6.4], [3.4, -7.8]]
ROAD_A = [[5.6, -9.0], [8.2, -12.2], [11.2, -14.6], [14.2, -16.2]]
ROAD_B = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
SHEEP = 60
CARTS = 6


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


def dk(at, x, z, y=None, state="fly", face=None, dur=0.0, ease=None):
    k = {"at": at, "x": round(x, 3), "z": round(z, 3), "state": state}
    if y is not None:
        k["y"] = round(y, 3)
    if face is not None:
        k["face"] = face
    if dur:
        k["dur"] = round(dur, 3)
    if ease:
        k["ease"] = ease
    return k


def orbit(line, word, off, dur, center, r, y, a0=0.0, laps=1.0, step=0.2, state="fly"):
    """Dense linear keys for a circling flight (the timeline interpolates between them)."""
    n = max(2, int(round(dur / step)))
    out = []
    for k in range(1, n + 1):
        u = k / n
        a = a0 + 2 * math.pi * laps * u
        out.append(dk(cue(line, word, off + u * dur), center[0] + r * math.cos(a), center[1] + r * math.sin(a), y + math.sin(u * math.pi * 2) * 0.8,
                      state=state, dur=dur / n, ease="linear"))
    return out


def orbit_start(center, r, a0):
    return (center[0] + r * math.cos(a0), center[1] + r * math.sin(a0))


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": off} if off else {})}

    # ---- the dragon
    PF = 20  # perched in profile to the hook camera (az 20), facing screen-right, towards the Grimmaw
    a1 = 2.4
    o1 = orbit_start(VILLAGE_A, 7.0, a1)
    a2 = 0.6
    o2 = orbit_start(VALLEY_B, 7.5, a2)
    dragon = [
        dk(shot("hook"), *PERCH, state="perch", face=PF),
        dk(cue("L1", "dragons", 0.05), *PERCH, state="roar", face=PF),
        dk(cue("L1", "your", 0.2), *PERCH, state="perch", face=PF),
        # "This village was built before the dragon came": it leaves (the village we meet is the one before it)
        dk(cue("L2", "Let's", -0.15), *PERCH, state="perch", face=PF),
        dk(cue("L2", "Let's", 0.45), PERCH[0] - 4.0, PERCH[1] - 8.0, 13.0, state="fly", dur=0.9),
        dk(cue("L2", "This", 0.1), -22.0, -30.0, 30.0, state="fly", dur=1.2),
        dk(cue("L2", "This", 0.15), -22.0, -30.0, 30.0, state="hidden"),
        # "Press run": it comes back out of the sky and circles the open village, low over the thatch
        dk(cue("L3", "run.", 0.0), -24.0, -22.0, 26.0, state="fly"),
        dk(cue("L3", "run.", 0.05), -24.0, -22.0, 26.0, state="fly"),
        dk(cue("L3", "run.", 1.25), o1[0], o1[1], 14.0, state="fly", dur=1.2),
    ]
    dragon += orbit("L3", "run.", 1.25, 5.6, VILLAGE_A, 7.0, 14.0, a0=a1, laps=1.35)
    # the drop: it leaves for its lair under the peak
    dragon += [
        dk(cue("L5", "Nobody", 0.0), *LAIR, y=18.0, state="glide", dur=1.4),
        dk(cue("L5", "war.", 0.0), *LAIR, state="perch", face=300, dur=0.7),
        # run two: it hunts over the new valley and finds nothing in the open
        dk(cue("L11", "Run", 0.15), *LAIR, state="perch", face=300),
        dk(cue("L11", "Run", 0.4), o2[0], o2[1], 15.0, state="fly", dur=1.0),
    ]
    dragon += orbit("L11", "Run", 1.4, 3.6, VALLEY_B, 7.5, 15.0, a0=a2, laps=0.9)
    # the twist: someone has to watch the sky; it passes over the valley while the bell rings, then goes home
    dragon += [
        dk(cue("L13", "Someone", 0.0), 9.0, 2.0, 17.0, state="glide", dur=1.0),
        dk(cue("L14", "bell.", -0.2), -14.0, -6.0, 13.0, state="fly", dur=2.3, ease="linear"),
        dk(cue("L14", "decides", 0.2), -10.0, -16.0, 15.0, state="fly", dur=1.4),
        dk(cue("L15", "Rule", 0.0), *LAIR, state="perch", face=300, dur=1.0),
        # back on its perch under the wipe, for the loop
        dk(WIPE, *PERCH, state="perch", face=PF),
    ]

    # ---- the Grimmaw: looks up at the dragon on frame 0 and on the loop frame (gaze), grazes its meadow in between
    g1 = [
        pk(shot("hook"), *G1_HOME, "gaze", face=200),
        pk(cue("L2", "Let's", 0.0), *G1_HOME, "idle", face=200),
        pk(WIPE, *G1_HOME, "gaze", face=200),
    ]

    # ---- HUD series and the village keys (the HUD reads the same keys the world draws)
    herd = [
        [shot("hook"), SHEEP],
        [cue("L4", "two:", 0.1), SHEEP],
        [cue("L4", "empty.", 0.2), 12, "linear"],
        [cue("L4", "travels.", 0.3), 9, "linear"],
        [cue("L5", "working.", 0.45), 9],
        [cue("L6", "So", 0.2), SHEEP, "out"],
        [cue("L12", "the", 0.0, nth=2), SHEEP],
        [cue("L12", "grow,", 0.4), 92, "out"],
        [WIPE, 92],
        [cue("L17", "What", -0.28), SHEEP, "step"],
    ]
    trade = [
        [shot("hook"), CARTS],
        [cue("L4", "three:", 0.0), CARTS],
        [cue("L4", "travels.", 0.35), 0, "linear"],
        [cue("L5", "working.", 0.45), 0],
        [cue("L6", "So", 0.2), CARTS, "out"],
        [cue("L12", "trade", 0.0), CARTS],
        [cue("L12", "returns.", 0.4), 9, "out"],
        # everyone hides when the bell rings, then trade comes back out
        [cue("L14", "hides.", -0.3), 9],
        [cue("L14", "hides.", 0.15), 0, "linear"],
        [cue("L15", "power.", 0.0), 0],
        [cue("L15", "charge.", 0.0), 9, "out"],
        [WIPE, 9],
        [cue("L17", "What", -0.28), CARTS, "step"],
    ]
    char = [
        [shot("hook"), 0],
        [cue("L4", "thatch", -0.1), 0],
        [cue("L4", "burns.", 0.5), 0.55, "linear"],
        [cue("L4", "travels.", 0.2), 1.0, "linear"],
        [cue("L5", "working.", 0.45), 1.0],
        [cue("L6", "So", 0.2), 0, "linear"],
    ]
    smoke = [[shot("hook"), 0], [cue("L4", "thatch", -0.1), 0], [cue("L4", "burns."), 1], [cue("L5", "working.", 0.4), 1], [cue("L6", "So", 0.1), 0, "linear"]]
    roof = [[shot("hook"), 0], [cue("L7", "Slate", -0.1), 0], [cue("L7", "burn.", 0.2), 1, "linear"], [WIPE, 1], [cue("L17", "What", -0.28), 0, "step"]]
    cover = [[shot("hook"), 0], [cue("L8", "covered", -0.3), 0], [cue("L8", "barns.", 0.3), 1, "linear"], [WIPE, 1], [cue("L17", "What", -0.28), 0, "step"]]
    place = [[shot("hook"), 0], [cue("L9", "Move", -0.1), 0], [cue("L9", "sight.", 0.5), 1, "linear"], [WIPE, 1], [cue("L17", "What", -0.28), 0, "step"]]
    route = [[shot("hook"), 0], [cue("L10", "Trade", -0.1), 0], [cue("L10", "night,", 0.1), 1, "linear"], [WIPE, 1], [cue("L17", "What", -0.28), 0, "step"]]
    lanterns = [[shot("hook"), 0], [cue("L10", "Trade", 0.0), 0], [cue("L10", "night,"), 1, "linear"], [cue("L11", "Run", -0.2), 1], [cue("L11", "Run", 0.2), 0, "linear"]]
    tower = [[shot("hook"), 0], [cue("L14", "tower", -0.05), 0], [cue("L14", "rises,", 0.35), 1, "out"], [WIPE, 1], [cue("L17", "What", -0.28), 0, "step"]]

    clock = [
        [shot("hook"), 0],
        [cue("L3", "run."), 0],
        [cue("L4", "one:", 0.2), 1, "linear"],
        [cue("L4", "two:", 0.2), 2, "linear"],
        [cue("L4", "three:", 0.2), 3, "linear"],
        [cue("L5", "working.", 0.4), 3],
        [cue("L6", "So", 0.2), 0, "linear"],
        [cue("L11", "Run", 0.1), 0],
        [cue("L12", "returns.", 0.6), 12, "linear"],
        [WIPE, 12],
        [cue("L17", "What", -0.28), 0, "step"],
    ]
    speed = [
        [shot("hook"), 1],
        [cue("L3", "run."), 1],
        [cue("L3", "run.", 0.35), 9],
        [cue("L4", "travels.", 0.3), 9],
        [cue("L5", "Nobody", 0.0), 1],
        [cue("L5", "working.", 0.4), 1],
        [cue("L5", "working.", 0.6), -10],
        [cue("L6", "So", 0.15), -10],
        [cue("L6", "So", 0.35), 1],
        [cue("L11", "Run", 0.1), 1],
        [cue("L11", "Run", 0.4), 9],
        [cue("L12", "returns.", 0.5), 9],
        [cue("L13", "Rule", 0.0), 1],
    ]
    rings = [
        # PLACE: the open site is seen from the sky (rust); the valley is out of sight (ember)
        {"x": VILLAGE_A[0], "z": VILLAGE_A[1], "r": 6.0, "on": cue("L9", "place."), "off": cue("L9", "Move", 0.3), "color": "#d0603f"},
        {"x": VALLEY_B[0], "z": VALLEY_B[1], "r": 5.5, "on": cue("L9", "valley,"), "off": cue("L10", "Four:", -0.15), "color": "#f4c46e"},
        # the twist: the tower's watch, the whole valley inside it
        {"x": TOWER[0], "z": TOWER[1], "r": 9.0, "on": cue("L14", "rises,", 0.1), "off": cue("L16", "Don't", -0.3), "color": "#f4c46e"},
    ]
    ripple = [shot("hook", 0.05), cue("L3", "run."), cue("L11", "Run"), cue("L15", "charge.")]
    dust = [{"at": cue("L1", "dragons", 0.05), "x": PERCH[0] + 0.6, "z": PERCH[1], "r": 3.4}]

    # The hook: a long lens across the Grimmaw's meadow to the dragon on its perch, the open village behind it.
    hook_pose = dict(az=20, el=8, dist=88, target=(6.4, 10.0, -1.4), fov=18)
    camera = [
        cam(shot("hook"), drift=1.0, **hook_pose),
        cam(cue("L1", "If", 0.0), hook_pose["az"] + 0.4, hook_pose["el"], 78, (6.4, 9.6, -1.4), fov=hook_pose["fov"], dur=3.8, drift=1.0),
        cam(cue("L2", "Let's", -0.2), 20, 24, 64, (6.2, 10.5, -8.6), fov=22, dur=1.6, drift=1.5),
        cam(cue("L3", "run.", 0.05), 22, 46, 192, (2.0, 10.5, -2.0), fov=26, dur=1.3, drift=2.0),
        cam(cue("L5", "Nobody", -0.25), 38, 24, 52, (6.6, 7.0, -8.8), fov=22, dur=1.3, drift=2.5),
        cam(cue("L5", "working.", 0.5), 20, 30, 96, (4.0, 9.0, -5.0), fov=24, dur=0.9, drift=2.0),
        cam(cue("L7", "One:", -0.2), 18, 22, 46, (6.6, 7.6, -9.0), fov=22, dur=1.1, drift=1.5),
        cam(cue("L8", "Two:", -0.2), 40, 26, 40, (11.0, 6.0, -5.4), fov=22, dur=1.1, drift=1.5),
        cam(cue("L9", "Three:", -0.15), 12, 62, 160, (2.4, 12.0, -5.0), fov=26, dur=1.1, drift=1.0),
        cam(cue("L10", "Four:", -0.15), 32, 44, 66, (-7.6, 10.0, 5.4), fov=24, dur=1.3, drift=2.0),
        cam(cue("L11", "Run", -0.05), 25, 44, 196, (0.0, 12.0, 0.0), fov=26, dur=1.0, drift=3.0),
        cam(cue("L13", "Rule", -0.1), 22, 20, 74, (-4.2, 12.0, -3.8), fov=24, dur=1.0, drift=1.5),
        cam(cue("L15", "Rule", -0.1), 28, 12, 50, (-6.2, 18.0, -5.2), fov=22, dur=1.2, drift=2.0),
        cam(cue("L16", "Don't", -0.25), 15, 30, 190, (2.0, 2.0, 0.0), fov=26, dur=1.6, drift=3.0),
        cam(WIPE, hook_pose["az"] - 1.0 * loop_span(), hook_pose["el"], hook_pose["dist"], hook_pose["target"], fov=hook_pose["fov"], cut=True, drift=1.0),
    ]
    light = [
        {"at": shot("hook"), "mood": "golden"},
        {"at": cue("L2", "Let's", -0.3), "mood": "day", "dur": 1.3},
        {"at": cue("L5", "Nobody", -0.2), "mood": "gloom", "dur": 1.2},
        {"at": cue("L5", "working.", 0.5), "mood": "day", "dur": 0.8},
        {"at": cue("L10", "Four:", -0.2), "mood": "night", "dur": 0.8},
        {"at": cue("L11", "Run", -0.2), "mood": "day", "dur": 0.6},
        {"at": cue("L16", "Don't", -0.3), "mood": "golden", "dur": 2.2},
    ]
    settlement = {
        "buildings": [{"kind": k, "a": list(a), "b": list(b), "face": 0} for k, a, b in BUILDINGS],
        "roof": roof, "char": char, "smoke": smoke,
        "pens": [{"a": list(PEN_A), "b": list(PEN_B), "r": 2.2}], "cover": cover,
        "place": place,
        "roads": {"a": ROAD_A, "b": ROAD_B}, "route": route,
        "tradeKey": "trade", "lanterns": lanterns,
        "tower": {"x": TOWER[0], "z": TOWER[1], "h": 6.0, "keys": tower, "rings": [cue("L14", "bell."), cue("L14", "rings")]},
    }
    # the EP28 tease: on frame 0 (and so on the loop frame) the cairn already stands by the lake; it's gone while the
    # village story runs, and its stones stack themselves again on "something on the Isle learns to build"
    cairn = [
        [shot("hook"), 3],
        [cue("L2", "Let's", -0.25), 3],
        [cue("L2", "Let's", -0.2), 0, "step"],
        [cue("L18", "something", 0.0), 0],
        [cue("L18", "Isle", 0.0), 1, "linear"],
        [cue("L18", "learns", 0.05), 2, "linear"],
        [cue("L18", "build.", 0.0), 3, "linear"],
    ]
    return {
        "clock": {"label": "WEEK", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": herd, "max": 100, "base": SHEEP, "centers": HERD_A, "centersB": HERD_B, "skin": "sheep"},
        "pred": [[shot("hook"), 1]],
        "predators": [{"id": "g1", "keys": g1}],
        "dragons": [{"id": "dragon", "scale": 1.35, "keys": dragon}],
        "series": {"trade": trade},
        "settlement": settlement,
        "props": [{"kind": "cairn", "x": CAIRN[0], "z": CAIRN[1], "stones": cairn}],
        "layers": {"rings": rings, "ripple": ripple, "dust": dust},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        # seamless loop: under the wipe, sim time jumps so it reaches 0 at the end (sheep and carts back where frame 0 has them)
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "ROOFS", "text": "slate and turf, not thatch", "at": cue("L7", "roofs.")},
    {"n": 2, "label": "PENS", "text": "flocks sleep under cover", "at": cue("L8", "pens.")},
    {"n": 3, "label": "PLACE", "text": "in a valley, out of sight", "at": cue("L9", "place.")},
    {"n": 4, "label": "TRAVEL", "text": "by night, under the trees", "at": cue("L10", "travel.")},
    {"n": 5, "label": "POWER", "text": "whoever rings the bell", "at": cue("L6", "easy."), "locked": True, "unlockAt": cue("L15", "power.")},
]
SPRITE = {"sprite": "ep27/dragon_sprite.png", "spriteW": 168, "spriteH": 116}
COUNTERS = [
    {"icon": "house", "label": "ROOFS", "key": "roofs", "color": "ember", "digits": 2},
    {"icon": "sheep", "label": "FLOCK", "key": "herd", "color": "prey", "digits": 3},
    {"icon": "cart", "label": "TRADE", "key": "trade", "color": "sky", "digits": 2},
]


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "IF DRAGONS", "color": "ember"}, {"text": "EXISTED"}]
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 100, "start": {"shot": "hook"}, "end": cue("L1", "your", -0.08), "preShow": True},
        {"type": "kinetic", "parts": [{"text": "YOUR WORLD", "at": cue("L1", "your")}, {"text": "WOULD LOOK", "at": cue("L1", "would")}, {"text": "DIFFERENT.", "at": cue("L1", "different."), "color": "rust"}],
         "y": 452, "size": 100, "start": cue("L1", "your", -0.02), "end": cue("L2", "Let's", -0.1)},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 27 · CREATURES", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
    ]
    G["setup"] += [
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "This", -0.1), "end": cue("L3", "Press", -0.1), "dietAt": cue("L2", "dragon"),
         "kicker": "FIELD CARD · NO. 002", "kind": "FLYING APEX", "name": "DRAGON", "dietLabel": "HUNTS", "diet": "anything in the open", **SPRITE},
        {"type": "simBar", "compact": True, "counters": COUNTERS, "start": cue("L3", "Press", -0.15), "end": cue("L16", "Don't", -0.3),
         "runAt": [cue("L3", "run."), cue("L11", "Run")]},
    ]
    G["run1"] += [
        {"type": "simGraph", "y": 456, "h": 214, "from": cue("L3", "run."), "to": cue("L4", "travels.", 0.4), "start": cue("L4", "Week", -0.15), "end": cue("L5", "Nobody", -0.1), "caption": "WEEKS 0–3",
         "series": [{"key": "roofs", "color": "#f4c46e", "max": 8, "label": "ROOFS"}, {"key": "herd", "color": "#9bd16a", "max": 66, "label": "FLOCK"}, {"key": "trade", "color": "#8fc8ff", "max": 7, "label": "TRADE"}]},
        {"type": "pin", "at": [ROAD_A[2][0], None, ROAD_A[2][1]], "kicker": "TRADE ROAD", "text": "EMPTY", "color": "rust", "lift": 90, "start": cue("L4", "travels.", 0.1), "end": cue("L5", "Nobody", -0.1)},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "COLLAPSED", "sub": "NO WAR · WEEK 3", "color": "rust", "y": 560, "size": 96, "start": cue("L5", "war."), "end": cue("L5", "The", -0.1)},
        {"type": "kinetic", "parts": [{"text": "IT JUST", "at": cue("L5", "just")}, {"text": "STOPPED.", "at": cue("L5", "stopped"), "color": "rust"}], "font": "pixel", "size": 100, "y": 1110,
         "start": cue("L5", "just", -0.02), "end": cue("L5", "working.", 0.5)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L5", "working.", 0.5), "end": cue("L6", "So", 0.3)},
        {"type": "blockWipe", "at": cue("L5", "working.", 0.48), "dur": 0.34},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L6", "Four", -0.1), "end": cue("L16", "Don't", -0.3),
         "kicker": "DESIGN CHECK", "title": "DRAGON-PROOF", "blinkAt": cue("L6", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L9", "place.", 0.3), 0], [cue("L9", "place.", 0.65), 1], [cue("L10", "Four:", -0.25), 1], [cue("L10", "Four:", 0.1), 0],
                      [cue("L11", "Run", -0.2), 0], [cue("L11", "Run", 0.15), 1], [cue("L15", "Rule", -0.3), 1], [cue("L15", "Rule", 0.05), 0]]},
    ]
    G["roofs"] += [
        {"type": "pin", "at": [BUILDINGS[1][1][0], None, BUILDINGS[1][1][1]], "kicker": "THATCH → SLATE", "text": "WON'T CATCH", "color": "ember", "lift": 110,
         "start": cue("L7", "Slate", 0.1), "end": cue("L8", "Two:", -0.1)},
    ]
    G["pens"] += [
        {"type": "pin", "at": [PEN_A[0], None, PEN_A[1] - 3.1], "kicker": "FLOCKS", "text": "UNDER COVER", "color": "prey", "lift": 120, "start": cue("L8", "covered", 0.1), "end": cue("L9", "Three:", -0.1)},
    ]
    G["place"] += [
        {"type": "pin", "at": [VILLAGE_A[0], None, VILLAGE_A[1]], "kicker": "OPEN MEADOW", "text": "SEEN FROM THE SKY", "color": "rust", "lift": 80, "size": 28,
         "start": cue("L9", "place.", 0.05), "end": cue("L9", "Move", 0.25)},
        {"type": "pin", "at": [VALLEY_B[0], None, VALLEY_B[1]], "kicker": "THE VALLEY", "text": "OUT OF SIGHT", "color": "ember", "lift": 80, "start": cue("L9", "sight.", 0.0), "end": cue("L10", "Four:", -0.15)},
    ]
    G["travel"] += [
        {"type": "pin", "at": [ROAD_B[2][0], None, ROAD_B[2][1]], "kicker": "NIGHT ROAD", "text": "UNDER THE TREES", "color": "sky", "lift": 110, "start": cue("L10", "night,", 0.1), "end": cue("L11", "Run", -0.1)},
    ]
    G["run2"] += [
        {"type": "simGraph", "y": 566, "h": 214, "from": cue("L11", "Run"), "to": cue("L12", "returns.", 0.5), "start": cue("L11", "Run", 0.1), "end": cue("L13", "Rule", -0.1), "caption": "WEEKS 0–12",
         "series": [{"key": "roofs", "color": "#f4c46e", "max": 8, "label": "ROOFS"}, {"key": "herd", "color": "#9bd16a", "max": 100, "label": "FLOCK"}, {"key": "trade", "color": "#8fc8ff", "max": 10, "label": "TRADE"}]},
        {"type": "pin", "dragon": "dragon", "kicker": "HUNTING", "text": "NOTHING IN THE OPEN", "color": "rust", "lift": 70, "size": 28, "start": cue("L12", "Now", 0.0), "end": cue("L12", "grow,", 0.2)},
        {"type": "stamp", "text": "THRIVING", "sub": "NO ROOF LOST", "color": "stable", "rotate": -4, "y": 900, "size": 92, "start": cue("L12", "grow,"), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}], "size": 150, "y": 640, "start": cue("L13", "Rule", -0.02), "end": cue("L13", "Someone", -0.08)},
        {"type": "pin", "at": [TOWER[0], 14.6, TOWER[1]], "kicker": "THE BELL-RINGER", "text": "DECIDES WHEN WE HIDE", "color": "ember", "lift": 90, "size": 30,
         "start": cue("L14", "Whoever", 0.0), "end": cue("L15", "Rule", -0.15)},
    ]
    G["role"] += [
        {"type": "pin", "at": [TOWER[0], 14.6, TOWER[1]], "kicker": "NEW POWER", "text": "THE TOWER", "color": "ember", "lift": 110, "start": cue("L15", "power.", 0.0), "end": cue("L16", "Don't", -0.3)},
        # a light mid-video follow nudge right after the payoff (~74% through), where the sting booted
        {"type": "followChip", "start": cue("L15", "power.", 0.4), "end": cue("L16", "Don't", -0.45), "text": "FOLLOW", "sub": "PART 27/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "Don't", -0.3), **({"unlockAt": cue("L16", "Don't", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "Don't", -0.3), "end": cue("L17", "What", -0.52), "kicker": "BEFORE YOU ADD A DRAGON", "title": "VILLAGE", **SPRITE,
         "subtitle": "Ask what ordinary people change.", "subtitleAt": cue("L16", "Ask")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 27 / 50",
         "title": "What Would Dragons Actually Change?", "cta": "COMMENT", "icon": "bubble", "with": "What would your civilization invent to survive dragons?"},
    ]
    # The ending formula: say the part number, ask for the follow with a reason (part 28), open the next loop.
    gone = cue("L18", "build.", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 27, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6,
         "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone,
         "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 28"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "28:", -0.1), "revealAt": cue("L18", "learns"), "end": gone,
         "kicker": "NEXT RUN · 28", "title": "BUILDERS", "sub": "SOMETHING LEARNS TO BUILD.", "sprite": "cairn", "spritePx": 7},
        # The loop: the hook's opening words fade back in as the ending clears, matching frame 0.
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 100, "start": cue("L18", "build.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("A monster changes a world through what ordinary people must do differently: what they roof with, where they keep "
          "their animals, where they build, how they travel, and who holds power once someone has to watch the sky.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Pay off EP26's open loop and stop the scroll: the dragon has landed on the Isle.",
             "The dragon perched on the Grimmaw's meadow in golden light, wings raised; the Grimmaw looks up at it; the open thatched village behind. It rears on 'dragons' (dust ring). WORLD ENGINE boots top-right.",
             "Long lens (fov 17 from dist 66, el 9, az 14), slow drift and push; the last 10 s return to this exact pose.", ("kinetic question", "dragon, Grimmaw, cairn", "the naive village, the peak"),
             "Golden hour (low sun from the east, long shadows).", "IF DRAGONS / EXISTED then YOUR WORLD / WOULD LOOK / DIFFERENT.",
             "Continuous camera into the setup.", "Hook: the series theme on celesta over strings; a hit on 'different'."),
    "setup": ("Meet the subject (the dragon) and the naive village it lands on, then press RUN.",
              "Field card intro (DRAGON sprite x3, FLYING APEX, HUNTS anything in the open) over the village: thatch roofs, open pens, the hall at the top of the slope, the trade road. The sim bar slides in with ROOFS / FLOCK / TRADE; RUN is pressed and the dragon takes off.",
              "Medium on the village (dist 62), then rise to the wide on 'run'.", ("field card, sim bar", "village, sheep, carts", "the peak"),
              "Day.", "Field card; RUN.", "Ripple + rise to the wide on 'run'.", "Pulse: pizzicato eighths, the theme's answer on celesta."),
    "run1": ("The naive village runs and fails, in numbers.",
             "The whole Isle; the dragon circles the open village; thatch roofs char one by one and smoke; FLOCK 60→9; carts leave the road; WEEK 0→3; ROOFS 07→00.",
             "Wide (dist 192, el 46).", ("sim bar + graph, pin", "dragon, smoking roofs, empty road", "island"), "Day.", "WEEK 01..03; graph WEEKS 0–3; TRADE ROAD: EMPTY.",
             "Push into the burnt village.", "Drive: 16th marimba, square-lead arps, pizzicato, bass, drums; a burn crackle bed."),
    "drop": ("The punchline of the failure: no battle, the way of life just stops working.",
             "Close on the burnt, empty village in gloom; the dragon glides home to its lair under the peak. COLLAPSED stamp; IT JUST STOPPED.",
             "Close (dist 52, az 38).", ("stamp, kinetic", "charred roofs, empty pens", "the peak"), "Gloom.", "COLLAPSED · NO WAR · WEEK 3; IT JUST STOPPED.",
             "Rewind + block wipe.", "Drop: near silence, a taiko boom on 'stopped'."),
    "rehook": ("Re-hook: rewind and open a loop (four easy changes, one locked twist).",
               "REWIND chip and scanlines; roofs un-char, sheep and carts return; the DRAGON-PROOF checklist with a blinking locked row 5.",
               "Medium (dist 96).", ("rewind, checklist", "the restored village", "island"), "Back to day.", "DESIGN CHECK 0/5, row 5 '??? the twist'.", "Cut on 'One'.",
               "Mystery: celesta arpeggios and harp; a riser into 'the twist'."),
    "roofs": ("Change 1: roofs that don't burn.", "Close on the houses; thatch roofs flip to slate and turf one by one; pin THATCH → SLATE / WON'T CATCH; row 1 ticks.",
              "Close (dist 46).", ("pin", "houses re-roofing", "meadow"), "Day.", "1 ROOFS · slate and turf, not thatch", "Pan to the pens.", "Build 1 (F major): marimba and strings."),
    "pens": ("Change 2: livestock under cover.", "Close on the open pen; a covered barn rises beside it; pin FLOCKS / UNDER COVER; row 2 ticks.",
             "Close (dist 40).", ("pin", "pen, barn, sheep", "village"), "Day.", "2 PENS · flocks sleep under cover", "Rise to top-down.", "Build 2: bass and pizzicato join."),
    "place": ("Change 3: settle out of the sky's sight lines.", "Near top-down; a rust ring marks the open site (SEEN FROM THE SKY); each building unbuilds and rises again in the valley under the cliff, the flock follows; an ember ring and OUT OF SIGHT.",
              "Near top-down (el 62, dist 160).", ("pins, folded card", "village moving", "island"), "Day.", "3 PLACE · in a valley, out of sight", "Down to the forest road.", "Build 3: light drums join."),
    "travel": ("Change 4: travel at night, under the trees.", "Night; the road moves into the forest; carts with lit lanterns roll under the canopy; pin NIGHT ROAD / UNDER THE TREES.",
               "Medium (dist 64).", ("pin", "carts with lanterns", "forest"), "Night.", "4 TRAVEL · by night, under the trees", "Rise to the wide on 'Run'.", "Build 4: the theme on glockenspiel."),
    "run2": ("The dragon-proof village runs: it holds.", "Wide Isle; the dragon circles the valley and finds nothing in the open; roofs stay 07, FLOCK 60→92, TRADE 6→9; THRIVING stamp.",
             "Wide (dist 196).", ("folded card, graph, pin, stamp", "dragon over the valley", "island"), "Day.", "WEEKS 0–12; HUNTING: NOTHING IN THE OPEN; THRIVING · NO ROOF LOST",
             "Down to the valley.", "Drive with the theme on flute and glockenspiel; a stab and cymbal on 'grow'."),
    "twist": ("The locked rule: someone has to watch the sky.", "RULE 5?, then a stone watchtower rises on the cliff with a bell; its watch ring covers the valley; the dragon passes, the bell swings, the carts vanish (everyone hides); pin THE BELL-RINGER / DECIDES WHEN WE HIDE.",
              "Medium on the valley (dist 74).", ("kinetic, pin", "tower, bell, dragon", "valley"), "Day.", "RULE 5?; THE BELL-RINGER · DECIDES WHEN WE HIDE",
              "Push to the bell.", "A held A7♭9 and a timpani roll, the tower bell on 'bell' and 'rings', a hard stop on 'hides'."),
    "role": ("Unlock rule 5: power.", "Row 5 unlocks (POWER · whoever rings the bell); close on the tower and bell; NEW POWER / THE TOWER; trade comes back; the island ripples on 'charge'.",
             "Close (dist 46).", ("unlocked card, pin, follow chip", "tower", "valley"), "Day.", "5/5", "Card goes full.", "Swell into a big D-major hit on 'charge'."),
    "lesson": ("The takeaway: the full design check, screenshot-able.", "The complete DRAGON-PROOF card (BEFORE YOU ADD A DRAGON, 5 rows ticked) with 'Ask what ordinary people change.' in serif italic.",
               "Wide orbit (dist 190).", ("full card", "the island at golden hour", "stars"), "Golden hour.", "Full card.", "Block wipe to the end card.",
               "Anthem: the theme in D major on flute, horns and glockenspiel; the World Engine chime as the card lands."),
    "cta": ("Comment CTA.", "End card: logo, PART 27 / 50, title, a speech-bubble COMMENT panel: What would your civilization invent to survive dragons?",
            "Cut (under the block wipe) to the hook pose.", ("end card", "the Isle", "void"), "Golden hour (the loop frame).", "End card.", "The card lifts on 'Part'.",
            "Outro: the theme's answer on celesta and music box."),
    "next": ("Say the part number, ask for the follow with a specific reason (part 28), and open the next loop: stones stack themselves on the lake shore.",
             "The end card lifts onto the hook frame; PART 27/50 season bar; FOLLOW FOR PART 28 pressed on 'Follow'; NEXT RUN 28 · BUILDERS decodes from a locked cairn; on the shore a cairn's three stones stack themselves; then the hook title returns for the loop.",
             "The hook pose (long lens), drifting onto frame 0.", ("progress bar, follow button, next-run card", "dragon, Grimmaw, the cairn", "the village at golden hour"),
             "Golden hour.", "PART 27/50 · FOLLOW FOR PART 28 · NEXT RUN: BUILDERS · SOMETHING LEARNS TO BUILD.", "Loop to frame 0.",
             "Tease: the theme's opening as a question over a held A, a horn call, the engine chime on 'Follow'; it resolves into frame 0's D minor on the loop."),
}


def build():
    ep = {
        "id": "ep27",
        "number": 27,
        "season": 2,
        "title": "What Would Dragons Actually Change?",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.07},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same curious lab host as EP26: brisk, warm, a little playful. The hook is a confident claim. The week count is quick and flat. "
                         "'Nobody fought a war' lands low; 'just stopped working' is a shrug. The four changes are crisp list beats. "
                         "'Someone has to watch the sky' is a quiet aha; 'Rule five is power' is sure. The comment ask is genuinely curious.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L5", "from": "just"}, {"line": "L13", "from": "Rule", "to": "five?"}],
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
    # The World Engine chime at its three fixed moments: frame 0 (and so every loop), the lesson card, the follow press.
    "hook": [hit("chime", {"shot": "hook"}, -11), hit("worldRipple", {"shot": "hook", "offset": 0.05}, -17),
             hit("roar", cue("L1", "dragons", 0.05), -12), hit("stompHit", cue("L1", "dragons", 0.1), -14)],
    "setup": [hit("dragonPass", cue("L2", "Let's", -0.1), -15), hit("cardSlide", cue("L2", "This", -0.1), -17), hit("check", cue("L2", "dragon"), -20),
              hit("runPress", cue("L3", "run."), -11), hit("worldRipple", cue("L3", "run."), -16), hit("dragonPass", cue("L3", "run.", 0.4), -12)],
    "run1": [bed("simTicks", cue("L3", "run.", 0.3), cue("L4", "travels.", 0.2), -21), bed("burn", cue("L4", "thatch", -0.1), cue("L4", "travels.", 0.4), -19),
             bed("losses", cue("L4", "two:", 0.1), cue("L4", "empty.", 0.2), -23)],
    "drop": [hit("dragonPass", cue("L5", "Nobody", -0.2), -17), hit("stamp", cue("L5", "war."), -10)],
    "rehook": [hit("rewind", cue("L5", "working.", 0.45), -11), hit("cardSlide", cue("L6", "Four", -0.1), -17)],
    "roofs": [hit("check", cue("L7", "roofs."), -13), hit("restore", cue("L7", "Slate"), -15), hit("stompHit", cue("L7", "burn.", 0.1), -20)],
    "pens": [hit("check", cue("L8", "pens."), -13), hit("restore", cue("L8", "covered", -0.2), -15), bed("stomp", cue("L8", "covered", -0.2), cue("L8", "barns.", 0.2), -22)],
    "place": [hit("check", cue("L9", "place."), -13), hit("ringOn", cue("L9", "place."), -16), hit("restore", cue("L9", "Move"), -14),
              hit("worldRipple", cue("L9", "valley,"), -17), hit("ringOn", cue("L9", "valley,"), -18)],
    "travel": [hit("check", cue("L10", "travel."), -13), hit("snowAir", cue("L10", "Four:", -0.2), -20), hit("restore", cue("L10", "Trade"), -17)],
    "run2": [hit("runPress", cue("L11", "Run"), -11), hit("worldRipple", cue("L11", "Run"), -16), hit("dragonPass", cue("L11", "Run", 0.3), -13),
             bed("simTicks", cue("L11", "Run", 0.3), cue("L12", "returns.", 0.5), -21), bed("births", cue("L12", "the", 0.0, nth=2), cue("L12", "grow,", 0.4), -22),
             hit("stamp", cue("L12", "grow,"), -13)],
    "twist": [hit("dragonPass", cue("L13", "Someone", -0.2), -13), hit("stompHit", cue("L14", "tower", 0.0), -15), hit("restore", cue("L14", "tower", 0.0), -15),
              hit("ringOn", cue("L14", "rises,", 0.1), -16), hit("towerBell", cue("L14", "bell."), -10), hit("towerBell", cue("L14", "rings"), -12),
              hit("dragonPass", cue("L14", "bell.", -0.3), -14)],
    "role": [hit("unlock", cue("L15", "power."), -10), hit("worldRipple", cue("L15", "charge."), -14)],
    "lesson": [hit("engineWind", cue("L16", "Don't", -0.8), -15), hit("chime", cue("L16", "Don't", -0.3), -10),
               hit("cardSlide", cue("L16", "Don't", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("cardSlide", cue("L17", "What", -0.1), -20)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11),
             hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "28:", -0.1), -18), hit("unlock", cue("L18", "learns"), -15),
             # the stones stack: three soft knocks
             hit("cubPop", cue("L18", "Isle", 0.0), -17), hit("cubPop", cue("L18", "learns", 0.05), -16), hit("stompHit", cue("L18", "build.", 0.0), -18),
             # the wind-up into the loop: its catch lands 40 ms before the end, and frame 0 answers with the chime
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score (pipeline/music_s2.py), EP26's plan re-cued: the series theme in D minor for the problem, D major for the payoff.
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 100,
    "sections": [
        msec({"shot": "hook"}, "hook", ["Dm", "Bb"], "D minor"),
        msec(cue("L2", "Let's", -0.1), "pulse", ["Dm", "Bb", "F", "C"], "D minor"),
        msec(cue("L3", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.8),
        msec(cue("L5", "Nobody", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L5", "The"), "void", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L5", "working.", 0.45), "mystery", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=2),
        msec(cue("L7", "One:", -0.1), "build", ["F", "C", "Dm", "Bb"], "F major", layer=1),
        msec(cue("L8", "Two:", -0.1), "build", ["F", "C", "Dm", "Bb"], "F major", layer=2),
        msec(cue("L9", "Three:", -0.1), "build", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L10", "Four:", -0.1), "build", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L11", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(cue("L14", "Whoever", -0.1), "mystery", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=2),
        msec(cue("L14", "hides.", 0.0), "rest", ["Dm"], "D minor"),
        msec(cue("L15", "Rule"), "swell", ["Bb", "F", "C", "A"], "D minor", beatsPerChord=2),
        msec(cue("L15", "charge.", 0.0), "anthem", ["D", "G", "Bm", "A"], "D major"),
        msec(cue("L17", "What", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "different."), "chord": "Dm"},
        {"kind": "boom", "at": cue("L5", "stopped"), "chord": "Dm"},
        {"kind": "riser", "at": cue("L6", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "grow,"), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "grow,")},
        {"kind": "hit", "at": cue("L15", "charge."), "chord": "D"},
        {"kind": "call", "at": cue("L18", "learns"), "chord": "A"},           # the next run
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"}, # into the loop point
    ],
    # the beat after "hides": everyone is hiding, the music too (the bell's tail owns it)
    "rests": [{"from": cue("L14", "hides.", 0.05), "to": cue("L15", "Rule", -0.02)}],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #Dragons #WritingTips #WorldcraftShorts"
BODY = (
    "If dragons existed, your world's architecture would look very different.\n\n"
    "We ran it. A village built before the dragon came: thatch roofs, open pens, a trade road across open meadow. "
    "Week one, the thatch burns. Week two, the pens are empty. Week three, no one travels. Nobody fought a war; the village just stopped working.\n\n"
    "So rebuild it: slate and turf roofs, flocks in covered barns, the village moved into a valley out of sight, and trade at night under the trees. "
    "Then the twist: someone has to watch the sky. A tower rises with a bell, and whoever rings it decides when everyone hides. "
    "The dragon changed who's in charge.\n\n"
    "Don't just add a dragon. Ask what ordinary people do differently.\n\n"
    "What would your civilization invent to survive dragons? Comment below.\n\n"
    "Part 27 of 50. Follow for part 28: something on the Isle learns to build."
)
METADATA = {
    "youtube": {
        "title": "What Would Dragons Actually Change? (Worldbuilding)",
        "titleAlternate": "Your village wouldn't survive a dragon",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 6: Creatures and Species.\n\n" + TAGS,
        "pinnedComment": "Comment check: what would YOUR civilization invent to survive dragons? Roofs, barns, tunnels, bells, something stranger? "
                         "(Part 28: something on the Isle learns to build.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated dragon sprite; the island, village and creatures are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "Dragons wouldn't need to fight you. Your village would just stop working 🐉 We ran it: thatch burns, pens empty, roads empty. 4 fixes, and #5 is the twist: whoever rings the bell holds the power. "
                   "What would your world invent? Part 27/50 · follow for part 28 🪨 " + TAGS,
        "pinnedComment": "What would your civilization invent to survive dragons?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "If dragons were real where you live, what would change first: roofs, farms, roads, or who's in charge?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": "Dragons change architecture.\n\n" + BODY + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": "First 28 characters: 'Dragons change architecture.'",
        "pinnedComment": "Save the dragon-proof checklist, then tell us: what would your civilization invent to survive dragons?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep27] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots")
