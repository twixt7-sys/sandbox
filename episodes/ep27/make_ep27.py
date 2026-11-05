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


# The block wipe into the end card. Everything that must jump back to frame 0's state (the dragon onto its hook orbit,
# the follow camera with it, the Grimmaw looking up, the naive village, 60 sheep, 6 carts) jumps on this frame, under the blocks.
WIPE = cue("L18", "What", -0.3)


def timing():
    return json.loads(TIMING.read_text()) if TIMING.exists() else None


def loop_span():
    """Seconds from the wipe to the end of the episode, so the dragon's closing orbit lands exactly on frame 0's spot
    (and the follow camera with it). Needs public/ep27/timing.json: run tts.py first, then this script."""
    tm = timing()
    if not tm:
        print("[make_ep27] no timing.json yet: using an estimate for the loop; rerun after tts.py")
        return 10.4
    words = next(l for l in tm["lines"] if l["id"] == "L18")["words"]
    w = next(w for w in words if w["text"].strip(".,!?:;").lower() == "what")["start"] - 0.3
    return round(tm["duration"] - w, 3)


LINES = [
    ("L1", "hook", "If dragons existed, your world's architecture would look very different.", 0.25, ["dragons", "different."]),
    ("L2", "hook", "Because this is what a dragon sees.", 0.3, ["sees."]),
    ("L3", "setup", "Every thatch roof, open pen and cart: a target.", 0.25, ["every", "target."]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "Week one: roofs burn. Week two: flocks gone. Week three: nobody travels.", 0.3, ["burn.", "gone."]),
    ("L6", "drop", "Nobody fought a war. They just lived in plain sight.", 0.4, ["war.", "plain"]),
    ("L7", "rehook", "So hide the village. Four changes are easy. The fifth is the twist.", 0.3, ["hide", "twist."]),
    ("L8", "roofs", "One: roofs. Slate and turf don't burn.", 0.2, ["slate", "burn."]),
    ("L9", "pens", "Two: pens. Flocks sleep in covered barns.", 0.2, ["covered"]),
    ("L10", "place", "Three: place. Build in the valley, under the cliff.", 0.2, ["valley,", "cliff."]),
    ("L11", "travel", "Four: travel. Move at night, under the trees.", 0.3, ["night,", "trees."]),
    ("L12", "run2", "Run it again.", 0.25, ["again."]),
    ("L13", "run2", "The dragon looks down, and finds nothing.", 0.35, ["nothing."]),
    ("L14", "twist", "Rule five? Look back.", 0.3, ["back."]),
    ("L15", "twist", "A watchtower sees the dragon first. One bell, and everyone hides.", 0.35, ["first.", "hides."]),
    ("L16", "role", "Whoever rings it runs the village. The dragon changed who's in charge.", 0.32, ["runs", "charge."]),
    ("L17", "lesson", "Don't just add a dragon. Ask what ordinary people do differently.", 0.35, ["dragon.", "ordinary"]),
    ("L18", "cta", "What would your civilization invent to survive dragons? Comment below.", 0.25, ["invent", "comment"]),
    ("L19", "next", "Part 27 of 50. Follow for part 28: something on the Isle learns to build.", 0.25, ["follow", "build."]),
]

SHOTS = ["hook", "setup", "run1", "drop", "rehook", "roofs", "pens", "place", "travel", "run2", "twist", "role", "lesson", "cta", "next"]


# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle (world units; see src/s2/world/island.ts). EP27 adds the first village.
G1_HOME = (8.0, -1.0)          # the Grimmaw's meadow (EP26)
LAIR = (-2.5, -12.5)           # the dragon's rock shoulder under the peak
VALLEY_B = (-2.4, -3.6)        # the hidden village: the valley under the cliff, between the rock and the trees
TOWER = (-6.4, -5.6)           # the watchtower on the cliff above the valley
FAR = (26.0, -22.0)            # where the dragon comes from in the twist (out past the north-east coast)
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
VILLAGE_A = (sum(a[0] for _, a, _ in BUILDINGS) / 7, sum(a[1] for _, a, _ in BUILDINGS) / 7)
PEN_A, PEN_B = (11.2, -4.4), (2.2, -6.4)
HERD_A = [[11.2, -4.6], [9.6, -5.6]]
HERD_B = [[2.2, -6.4], [3.4, -7.8]]
ROAD_A = [[5.6, -9.0], [8.2, -12.2], [11.2, -14.6], [14.2, -16.2]]
ROAD_B = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
SHEEP = 60
CARTS = 6

# The hook orbit: the dragon glides a wide circle over the open village (frame 0 and the loop frame ride on it).
O1 = dict(center=VILLAGE_A, r=11.0, y=15.0, w=0.3)
A0 = 1.3                       # its angle on frame 0 (radians, x = cx + r cos a, z = cz + r sin a): over the Grimmaw's meadow
# The over-the-shoulder follow camera (az from directly behind the dragon; the target is offset from the dragon).
FOLLOW = dict(az=-16, el=0, dist=0, target=(0.0, 0.0, 0.0), fov=38, follow={"dragon": "dragon", "look": [VILLAGE_A[0], 5.0, VILLAGE_A[1]], "back": 20.0, "up": 24.0})


def cam(at, az, el, dist, target, fov=24, dur=1.4, drift=0.0, cut=False, follow=None):
    c = {"at": at, "az": az, "el": el, "dist": dist, "target": list(target), "fov": fov, "dur": dur, "drift": drift}
    if cut:
        c["cut"] = True
    if follow:
        c["follow"] = follow
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


def circle(center, r, a):
    return (center[0] + r * math.cos(a), center[1] + r * math.sin(a))


def orbit(base, t0, dur, center, r, y, a0, w, step=0.2, state="fly"):
    """Dense linear keys for a circling flight from angle a0 at angular speed w (rad/s). `base(off)` makes the cue."""
    n = max(2, int(round(dur / step)))
    out = []
    for k in range(1, n + 1):
        tt = t0 + dur * k / n
        x, z = circle(center, r, a0 + w * (tt - t0))
        # a key moves from the previous key's spot over its `dur`, starting at its own time: so each key starts one
        # step early and arrives exactly on the circle at tt
        out.append(dk(base(tt - dur / n), x, z, y, state=state, dur=dur / n, ease="linear"))
    return out


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    tm = timing()
    word_t = lambda line, word: next(w["start"] for l in tm["lines"] if l["id"] == line for w in l["words"] if w["text"].strip(".,!?:;").lower() == word.lower())
    run_t = word_t("L4", "run")
    end = tm["duration"]
    span = loop_span()

    # ---- the dragon
    # the orbit starts 0.6 s before frame 0 and the closing one runs 0.6 s past the end, so heading and bank are sampled
    # the same way on both sides of the loop point
    pre = 0.6
    a_pre = A0 - O1["w"] * pre
    dragon = [dk(shot("hook", -pre), *circle(O1["center"], O1["r"], a_pre), O1["y"], state="glide")]
    dragon += orbit(lambda tt: shot("hook", tt), -pre, run_t + 0.05 + pre, O1["center"], O1["r"], O1["y"], a_pre, O1["w"], state="glide")
    a_run = A0 + O1["w"] * (run_t + 0.05)
    # "Press run": it drops into a tight, fast circle over the thatch
    a2 = a_run + 0.6
    dragon.append(dk(cue("L4", "run.", 1.0), *circle(VILLAGE_A, 7.0, a2), 12.0, state="fly", dur=0.95))
    dragon += orbit(lambda tt: cue("L4", "run.", tt), 1.0, 5.2, VILLAGE_A, 7.0, 12.0, a2, 1.25)
    # the drop: it glides home to its lair under the peak
    dragon += [
        dk(cue("L6", "Nobody", 0.0), *LAIR, y=18.0, state="glide", dur=1.4),
        dk(cue("L6", "war.", 0.1), *LAIR, state="perch", face=300, dur=0.7),
        # run two: it hunts over the hidden valley and finds nothing
        dk(cue("L12", "Run", 0.15), *LAIR, state="perch", face=300),
        dk(cue("L12", "Run", 0.4), *circle(VALLEY_B, 9.0, 0.4), 16.0, state="fly", dur=1.0),
    ]
    dragon += orbit(lambda tt: cue("L12", "Run", tt), 1.4, 3.2, VALLEY_B, 9.0, 16.0, 0.4, 0.9, state="glide")
    # the twist: it leaves, then comes back over the cliff, and this time the village sees it first
    dragon += [
        dk(cue("L14", "Rule", 0.4), FAR[0], FAR[1], 20.0, state="fly", dur=1.6),
        dk(cue("L15", "sees", -0.6), FAR[0], FAR[1], 20.0, state="glide"),
        dk(cue("L15", "bell,", 0.0), 6.0, -14.0, 17.0, state="glide", dur=2.6, ease="linear"),
        dk(cue("L16", "Whoever", 0.2), -18.0, 6.0, 22.0, state="fly", dur=2.2),
        dk(cue("L16", "charge.", 0.0), *LAIR, state="perch", face=300, dur=1.6),
    ]
    # the loop: under the wipe it jumps onto the hook orbit, timed to arrive at frame 0's spot at the end
    a_w = A0 - O1["w"] * span
    dragon.append(dk(WIPE, *circle(O1["center"], O1["r"], a_w), O1["y"], state="glide"))
    dragon += orbit(lambda tt: {"end": True, "offset": round(-span + tt, 3)}, 0.0, span + pre, O1["center"], O1["r"], O1["y"], a_w, O1["w"], state="glide")

    # ---- the Grimmaw: looks up at the dragon on frame 0 and on the loop frame (gaze), grazes its meadow in between
    g1 = [
        pk(shot("hook"), *G1_HOME, "gaze", face=110),
        pk(cue("L3", "Every", 0.0), *G1_HOME, "idle", face=110),
        pk(WIPE, *G1_HOME, "gaze", face=110),
    ]

    # ---- HUD series and the village keys (the HUD and the dragon's-eye targets read the same keys the world draws)
    herd = [
        [shot("hook"), SHEEP],
        [cue("L5", "two:", 0.1), SHEEP],
        [cue("L5", "gone.", 0.3), 12, "linear"],
        [cue("L5", "travels.", 0.3), 9, "linear"],
        [cue("L6", "sight.", 0.45), 9],
        [cue("L7", "So", 0.2), SHEEP, "out"],
        [cue("L12", "Run", 0.3), SHEEP],
        [cue("L13", "nothing.", 0.4), 92, "out"],
        [WIPE, 92],
        [cue("L18", "What", -0.28), SHEEP, "step"],
    ]
    trade = [
        [shot("hook"), CARTS],
        [cue("L5", "three:", 0.0), CARTS],
        [cue("L5", "travels.", 0.35), 0, "linear"],
        [cue("L6", "sight.", 0.45), 0],
        [cue("L7", "So", 0.2), CARTS, "out"],
        [cue("L12", "Run", 0.3), CARTS],
        [cue("L13", "nothing.", 0.4), 9, "out"],
        # one bell, and everyone hides; then trade comes back out
        [cue("L15", "hides.", -0.35), 9],
        [cue("L15", "hides.", 0.1), 0, "linear"],
        [cue("L16", "runs", 0.0), 0],
        [cue("L16", "charge.", 0.0), 9, "out"],
        [WIPE, 9],
        [cue("L18", "What", -0.28), CARTS, "step"],
    ]
    char = [[shot("hook"), 0], [cue("L5", "roofs", -0.1), 0], [cue("L5", "burn.", 0.5), 0.55, "linear"], [cue("L5", "travels.", 0.2), 1.0, "linear"],
            [cue("L6", "sight.", 0.45), 1.0], [cue("L7", "So", 0.2), 0, "linear"]]
    smoke = [[shot("hook"), 0], [cue("L5", "roofs", -0.1), 0], [cue("L5", "burn."), 1], [cue("L6", "sight.", 0.4), 1], [cue("L7", "So", 0.1), 0, "linear"]]
    reset = lambda v: [[WIPE, v], [cue("L18", "What", -0.28), 0, "step"]]
    roof = [[shot("hook"), 0], [cue("L8", "Slate", -0.1), 0], [cue("L8", "burn.", 0.2), 1, "linear"]] + reset(1)
    cover = [[shot("hook"), 0], [cue("L9", "covered", -0.3), 0], [cue("L9", "barns.", 0.3), 1, "linear"]] + reset(1)
    place = [[shot("hook"), 0], [cue("L10", "Build", -0.1), 0], [cue("L10", "cliff.", 0.3), 1, "linear"]] + reset(1)
    route = [[shot("hook"), 0], [cue("L11", "Move", -0.1), 0], [cue("L11", "night,", 0.1), 1, "linear"]] + reset(1)
    lanterns = [[shot("hook"), 0], [cue("L11", "Move", 0.0), 0], [cue("L11", "night,"), 1, "linear"], [cue("L12", "Run", -0.2), 1], [cue("L12", "Run", 0.2), 0, "linear"]]
    tower = [[shot("hook"), 0], [cue("L14", "Look", -0.05), 0], [cue("L14", "back.", 0.4), 1, "out"]] + reset(1)

    clock = [
        [shot("hook"), 0], [cue("L4", "run."), 0],
        [cue("L5", "one:", 0.2), 1, "linear"], [cue("L5", "two:", 0.2), 2, "linear"], [cue("L5", "three:", 0.2), 3, "linear"],
        [cue("L6", "sight.", 0.4), 3], [cue("L7", "So", 0.2), 0, "linear"],
        [cue("L12", "Run", 0.1), 0], [cue("L13", "nothing.", 0.5), 12, "linear"],
        [WIPE, 12], [cue("L18", "What", -0.28), 0, "step"],
    ]
    speed = [
        [shot("hook"), 1], [cue("L4", "run."), 1], [cue("L4", "run.", 0.35), 9], [cue("L5", "travels.", 0.3), 9],
        [cue("L6", "Nobody", 0.0), 1], [cue("L6", "sight.", 0.4), 1], [cue("L6", "sight.", 0.6), -10],
        [cue("L7", "So", 0.15), -10], [cue("L7", "So", 0.35), 1],
        [cue("L12", "Run", 0.1), 1], [cue("L12", "Run", 0.4), 9], [cue("L13", "nothing.", 0.5), 9], [cue("L14", "Rule", 0.0), 1],
    ]
    rings = [
        {"x": VILLAGE_A[0], "z": VILLAGE_A[1], "r": 6.0, "on": cue("L10", "place."), "off": cue("L10", "Build", 0.3), "color": "#ff5a4e"},
        {"x": VALLEY_B[0], "z": VALLEY_B[1], "r": 5.5, "on": cue("L10", "valley,"), "off": cue("L11", "Four:", -0.15), "color": "#f4c46e"},
        # the twist: the tower's watch covers the whole valley
        {"x": TOWER[0], "z": TOWER[1], "r": 9.0, "on": cue("L15", "sees", 0.0), "off": cue("L17", "Don't", -0.3), "color": "#8fc8ff"},
    ]
    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run"), cue("L16", "charge.")]

    camera = [
        cam(shot("hook"), **FOLLOW),
        cam(cue("L4", "run.", 0.05), 22, 46, 192, (2.0, 10.5, -2.0), fov=26, dur=1.3, drift=2.0),
        cam(cue("L6", "Nobody", -0.25), 38, 24, 52, (6.6, 7.0, -8.8), fov=22, dur=1.3, drift=2.5),
        cam(cue("L6", "sight.", 0.5), 20, 30, 96, (4.0, 9.0, -5.0), fov=24, dur=0.9, drift=2.0),
        cam(cue("L8", "One:", -0.2), 18, 24, 50, (6.6, 7.6, -9.0), fov=22, dur=1.1, drift=1.5),
        cam(cue("L9", "Two:", -0.2), 40, 26, 40, (11.0, 6.0, -5.4), fov=22, dur=1.1, drift=1.5),
        cam(cue("L10", "Three:", -0.15), 12, 62, 160, (2.4, 12.0, -5.0), fov=26, dur=1.1, drift=1.0),
        cam(cue("L11", "Four:", -0.15), 32, 44, 66, (-7.6, 10.0, 5.4), fov=24, dur=1.3, drift=2.0),
        cam(cue("L12", "Run", -0.05), 25, 44, 196, (0.0, 12.0, 0.0), fov=26, dur=1.0, drift=3.0),
        cam(cue("L13", "The", -0.15), dur=0.8, **{**FOLLOW, "follow": {"dragon": "dragon", "look": [VALLEY_B[0], 6.0, VALLEY_B[1]], "back": 20.0, "up": 24.0}}),
        cam(cue("L14", "Rule", -0.1), 22, 20, 74, (-4.2, 12.0, -3.8), fov=24, dur=1.0, drift=1.5),
        # the watchtower's view: from behind the tower top, out over the cliff to the north-east sky the dragon comes from
        cam(cue("L15", "A", -0.1), -62, 6, 40, (4.0, 19.0, -11.0), fov=32, dur=1.0, drift=0.5),
        cam(cue("L16", "Whoever", -0.1), 28, 12, 50, (-6.2, 18.0, -5.2), fov=22, dur=1.2, drift=2.0),
        cam(cue("L17", "Don't", -0.25), 15, 30, 190, (2.0, 2.0, 0.0), fov=26, dur=1.6, drift=3.0),
        cam(WIPE, cut=True, **FOLLOW),
    ]
    light = [
        {"at": shot("hook"), "mood": "golden"},
        {"at": cue("L3", "Every", -0.3), "mood": "day", "dur": 1.3},
        {"at": cue("L6", "Nobody", -0.2), "mood": "gloom", "dur": 1.2},
        {"at": cue("L6", "sight.", 0.5), "mood": "day", "dur": 0.8},
        {"at": cue("L11", "Four:", -0.2), "mood": "night", "dur": 0.8},
        {"at": cue("L12", "Run", -0.2), "mood": "day", "dur": 0.6},
        {"at": cue("L17", "Don't", -0.3), "mood": "golden", "dur": 2.2},
        {"at": WIPE, "mood": "golden", "dur": 0.01},
    ]
    settlement = {
        "buildings": [{"kind": k, "a": list(a), "b": list(b), "face": 0} for k, a, b in BUILDINGS],
        "roof": roof, "char": char, "smoke": smoke,
        "pens": [{"a": list(PEN_A), "b": list(PEN_B), "r": 2.2}], "cover": cover,
        "place": place,
        "roads": {"a": ROAD_A, "b": ROAD_B}, "route": route,
        "tradeKey": "trade", "lanterns": lanterns,
        "tower": {"x": TOWER[0], "z": TOWER[1], "h": 6.0, "keys": tower, "rings": [cue("L15", "bell,"), cue("L16", "rings")]},
    }
    # The EP28 tease: a cairn that stacks itself. It stands where the follow camera looks in the loop's last second, so
    # it is in frame 0 too (already built: "it was there all along"), gone while the village story runs, and its stones
    # stack again on "something on the Isle learns to build".
    a_c = A0 - O1["w"] * 0.9
    dx, dz = circle(O1["center"], O1["r"], a_c)
    cx_, cz_ = VILLAGE_A[0] + (dx - VILLAGE_A[0]) * 0.45, VILLAGE_A[1] + (dz - VILLAGE_A[1]) * 0.45
    cairn = [
        [shot("hook"), 3], [cue("L3", "Every", -0.35), 3], [cue("L3", "Every", -0.3), 0, "step"],
        [cue("L19", "something", 0.0), 0], [cue("L19", "Isle", 0.0), 1, "linear"], [cue("L19", "learns", 0.05), 2, "linear"], [cue("L19", "build.", 0.0), 3, "linear"],
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
        "props": [{"kind": "cairn", "x": round(cx_, 2), "z": round(cz_, 2), "stones": cairn}],
        "layers": {"rings": rings, "ripple": ripple},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "ROOFS", "text": "slate and turf, not thatch", "at": cue("L8", "roofs.")},
    {"n": 2, "label": "PENS", "text": "flocks sleep under cover", "at": cue("L9", "pens.")},
    {"n": 3, "label": "PLACE", "text": "the valley, under the cliff", "at": cue("L10", "place.")},
    {"n": 4, "label": "TRAVEL", "text": "by night, under the trees", "at": cue("L11", "travel.")},
    {"n": 5, "label": "WATCH", "text": "the bell-ringer runs it", "at": cue("L7", "easy."), "locked": True, "unlockAt": cue("L16", "runs")},
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
         "y": 452, "size": 100, "start": cue("L1", "your", -0.02), "end": cue("L2", "Because", -0.1)},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 27 · CREATURES", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Because", -0.05), "end": cue("L3", "Every", -0.2), "dietAt": cue("L2", "sees."),
         "kicker": "FIELD CARD · NO. 002", "kind": "FLYING APEX", "name": "DRAGON", "dietLabel": "HUNTS", "diet": "anything it can see", **SPRITE},
        # the signature of this episode: the world through the dragon's eye, every target locked and counted
        {"type": "dragonEye", "mode": "dragon", "start": cue("L2", "sees.", -0.1), "end": cue("L4", "run.", 0.1), "lockAt": cue("L3", "Every", -0.1), "stagger": 0.12},
    ]
    G["setup"] += [
        {"type": "simBar", "compact": True, "counters": COUNTERS, "start": cue("L4", "Press", -0.15), "end": cue("L17", "Don't", -0.3),
         "runAt": [cue("L4", "run."), cue("L12", "Run")]},
    ]
    G["run1"] += [
        {"type": "simGraph", "y": 456, "h": 214, "from": cue("L4", "run."), "to": cue("L5", "travels.", 0.4), "start": cue("L5", "Week", -0.15), "end": cue("L6", "Nobody", -0.1), "caption": "WEEKS 0–3",
         "series": [{"key": "roofs", "color": "#f4c46e", "max": 8, "label": "ROOFS"}, {"key": "herd", "color": "#9bd16a", "max": 66, "label": "FLOCK"}, {"key": "trade", "color": "#8fc8ff", "max": 7, "label": "TRADE"}]},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "COLLAPSED", "sub": "NO WAR · WEEK 3", "color": "rust", "y": 560, "size": 96, "start": cue("L6", "war."), "end": cue("L6", "They", -0.1)},
        {"type": "kinetic", "parts": [{"text": "IN PLAIN", "at": cue("L6", "plain")}, {"text": "SIGHT.", "at": cue("L6", "sight."), "color": "rust"}], "font": "pixel", "size": 110, "y": 1080,
         "start": cue("L6", "plain", -0.02), "end": cue("L6", "sight.", 0.5)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "sight.", 0.5), "end": cue("L7", "So", 0.3)},
        {"type": "blockWipe", "at": cue("L6", "sight.", 0.48), "dur": 0.34},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L17", "Don't", -0.3),
         "kicker": "HIDE FROM THE SKY", "title": "SKY-PROOF", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L10", "place.", 0.3), 0], [cue("L10", "place.", 0.65), 1], [cue("L11", "Four:", -0.25), 1], [cue("L11", "Four:", 0.1), 0],
                      [cue("L12", "Run", -0.2), 0], [cue("L12", "Run", 0.15), 1], [cue("L16", "Whoever", -0.3), 1], [cue("L16", "Whoever", 0.05), 0]]},
    ]
    # Through the four changes, the dragon's sight stays on (brackets only): each change visibly takes targets away,
    # and the TARGETS count falls 16 → 9 → 7 → 6 → 0.
    G["roofs"] += [
        {"type": "dragonEye", "mode": "light", "minY": 1040, "start": cue("L8", "One:", -0.3), "end": cue("L11", "trees.", 0.7), "zeroText": "HIDDEN FROM THE SKY"},
    ]
    G["place"] += [
        {"type": "pin", "at": [VALLEY_B[0], None, VALLEY_B[1]], "kicker": "THE VALLEY", "text": "UNDER THE CLIFF", "color": "ember", "lift": 80, "start": cue("L10", "cliff.", 0.0), "end": cue("L11", "Four:", -0.15)},
    ]
    G["run2"] += [
        {"type": "dragonEye", "mode": "dragon", "start": cue("L13", "The", -0.1), "end": cue("L14", "Rule", -0.1), "lockAt": cue("L13", "The"), "zeroText": "NOTHING TO HUNT"},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L14", "Rule"), "color": "ember"}, {"text": "LOOK BACK.", "at": cue("L14", "Look"), "size": 110}],
         "size": 150, "y": 600, "start": cue("L14", "Rule", -0.02), "end": cue("L15", "A", -0.15)},
        {"type": "dragonEye", "mode": "tower", "start": cue("L15", "sees", -0.25), "end": cue("L15", "hides.", 0.4), "lockAt": cue("L15", "sees")},
    ]
    G["role"] += [
        {"type": "pin", "at": [TOWER[0], 16.2, TOWER[1]], "kicker": "NEW POWER", "text": "THE BELL-RINGER", "color": "ember", "lift": 110, "start": cue("L16", "runs", 0.0), "end": cue("L17", "Don't", -0.3)},
        # a light mid-video follow nudge right after the payoff, where the sting booted
        {"type": "followChip", "start": cue("L16", "runs", 0.5), "end": cue("L17", "Don't", -0.45), "text": "FOLLOW", "sub": "PART 27/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L17", "Don't", -0.3), **({"unlockAt": cue("L17", "Don't", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L17", "Don't", -0.3), "end": cue("L18", "What", -0.52), "kicker": "BEFORE YOU ADD A DRAGON", "title": "SKY-PROOF", **SPRITE,
         "subtitle": "Ask what ordinary people change.", "subtitleAt": cue("L17", "Ask")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L19", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 27 / 50",
         "title": "What Would Dragons Actually Change?", "cta": "COMMENT", "icon": "bubble", "with": "What would your civilization invent to survive dragons?"},
    ]
    gone = cue("L19", "build.", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 27, "of": 50, "start": cue("L19", "Part", -0.1), "fillAt": cue("L19", "Part", -0.05), "fillDur": 0.6,
         "ofAt": cue("L19", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L19", "Follow", -0.6), "pressAt": cue("L19", "Follow"), "end": gone,
         "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 28"},
        {"type": "nextRun", "y": 772, "start": cue("L19", "28:", -0.1), "revealAt": cue("L19", "learns"), "end": gone,
         "kicker": "NEXT RUN · 28", "title": "BUILDERS", "sub": "SOMETHING LEARNS TO BUILD.", "sprite": "cairn", "spritePx": 7},
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 100, "start": cue("L19", "build.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("A monster changes a world through what ordinary people must do differently. A dragon hunts what it can see, so "
          "people hide from the sky (roofs that don't burn, covered barns, villages in valleys, travel by night), and once someone "
          "has to watch the sky, whoever watches holds power.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Pay off EP26's loop and stop the scroll: the dragon is here, and we ride on its back. Then switch to its eye.",
             "Over the dragon's shoulder as it glides a wide circle over the open village in golden light; the Grimmaw looks up from its meadow; a cairn stands below. On 'sees' the frame turns to the DRAGON'S-EYE VIEW (red vignette, scanlines). The field card names it: DRAGON · HUNTS anything it can see.",
             "Follow camera: over its shoulder (az −28 from behind, el 20, dist 17, fov 34); the last 10 s ride the same orbit back to this exact frame.",
             ("kinetic question, field card", "the dragon's back and wings", "the village, the meadow, the Isle"),
             "Golden hour.", "IF DRAGONS / EXISTED → YOUR WORLD / WOULD LOOK / DIFFERENT. → DRAGON'S-EYE VIEW",
             "Continuous ride into the lock-on.", "Soar: horns in open fifths, a taiko wingbeat, the theme low on horns; a hit on 'different', a stab on 'sees'."),
    "setup": ("Show the stakes in the dragon's own terms: everything in the open is a target.",
              "Still riding: red brackets lock onto every thatch roof, both flocks in their open pens, the village itself and each cart on the road; TARGETS counts up to 16. The sim bar slides in and RUN is pressed.",
              "Follow camera, then rise to the wide on 'run'.", ("lock-on brackets, TARGETS, sim bar", "the village", "the Isle"),
              "Day.", "TARGETS 16; RUN.", "Ripple + rise to the wide.", "Mystery: celesta arpeggios over a held pad, lock-on beeps."),
    "run1": ("The naive village runs and fails, in numbers.", "The whole Isle; the dragon circles low and fast; roofs char one by one and smoke; FLOCK 60→9; carts leave the road; WEEK 0→3.",
             "Wide (dist 192, el 46).", ("sim bar + graph", "dragon, smoking roofs", "island"), "Day.", "WEEK 01..03; graph WEEKS 0–3.",
             "Push into the burnt village.", "Raid: taiko eighths, low horn stabs, driving bass; a burn crackle bed."),
    "drop": ("The punchline: no battle; they lived in plain sight.", "Close on the burnt, empty village in gloom; the dragon glides home to its lair. COLLAPSED · NO WAR; IN PLAIN SIGHT.",
             "Close (dist 52, az 38).", ("stamp, kinetic", "charred roofs, empty pens", "the peak"), "Gloom.", "COLLAPSED · NO WAR · WEEK 3; IN PLAIN SIGHT.",
             "Rewind + block wipe.", "Drop to near silence; a taiko boom on 'sight'."),
    "rehook": ("Re-hook: rewind, then the job is to hide. Four easy changes and one locked twist.", "REWIND; the village restored; the SKY-PROOF checklist (HIDE FROM THE SKY) with a blinking locked row 5.",
               "Medium (dist 96).", ("rewind, checklist", "the restored village", "island"), "Day.", "0/5, row 5 '??? the twist'.", "Cut on 'One'.", "Mystery; a riser into 'the twist'."),
    "roofs": ("Change 1: roofs that don't burn.", "Close on the houses; thatch flips to slate and turf one by one; each roof's red bracket flashes green and drops away; TARGETS 16→9.",
              "Close (dist 50).", ("brackets, TARGETS", "houses re-roofing", "meadow"), "Day.", "1 ROOFS · slate and turf, not thatch", "Pan to the pens.", "Stealth 1: tiptoe pizzicato, harp, celesta."),
    "pens": ("Change 2: livestock under cover.", "A covered barn rises over the open pen; both FLOCK brackets go green, HIDDEN; TARGETS 9→7.",
             "Close (dist 40).", ("brackets", "pen, barn, sheep", "village"), "Day.", "2 PENS · flocks sleep under cover", "Rise to top-down.", "Stealth 2: bass joins."),
    "place": ("Change 3: get out of the sky's sight lines.", "Near top-down; a red ring marks the open site; every building unbuilds and rises in the valley under the cliff, the flock follows; the VILLAGE bracket goes green; TARGETS 7→6.",
              "Near top-down (el 62, dist 160).", ("pin, folded card", "village moving", "island"), "Day.", "3 PLACE · the valley, under the cliff", "Down to the forest road.", "Stealth 3: brushes join."),
    "travel": ("Change 4: travel at night, under the trees.", "Night; the road moves into the forest; lanterns on; the last cart brackets go green; TARGETS 00 · HIDDEN FROM THE SKY.",
               "Medium (dist 66).", ("TARGETS 00", "carts with lanterns", "forest"), "Night.", "4 TRAVEL · by night, under the trees", "Rise to the wide on 'Run'.", "Stealth 4: the theme on glockenspiel."),
    "run2": ("The hidden village runs, and the dragon's own eye proves it.", "Wide, then over the dragon's shoulder above the valley in DRAGON'S-EYE VIEW: no brackets, TARGETS 00, NOTHING TO HUNT; the flock grows to 92, trade to 9.",
             "Wide (dist 196), then the follow camera.", ("dragon's-eye view, TARGETS 00", "the valley below", "island"), "Day.", "TARGETS 00 · NOTHING TO HUNT",
             "Cut to the cliff.", "Drive with the theme on flute and glockenspiel; a stab and cymbal on 'nothing'."),
    "twist": ("The locked rule: look back. The village watches the sky.", "RULE 5? / LOOK BACK.; a stone watchtower rises on the cliff; WATCHTOWER VIEW (blue): from behind its bell, a blue bracket locks on the dragon far out over the coast, DRAGON · SPOTTED; the bell swings and the carts vanish (everyone hides).",
              "Medium on the cliff (dist 74), then the tower's view (az −62, el 6, fov 32).", ("kinetic, watchtower view", "tower, bell, dragon", "the north-east sky"), "Day.",
              "RULE 5? LOOK BACK.; WATCHTOWER VIEW; DRAGON · SPOTTED", "Close on the bell.", "Twist (held A7♭9, timpani), then soar as the dragon comes in; the tower bell; a hard stop on 'hides'."),
    "role": ("Unlock rule 5: watching is power.", "Row 5 unlocks (WATCH · the bell-ringer runs it); close on the tower and bell; NEW POWER / THE BELL-RINGER; trade comes back; ripple on 'charge'.",
             "Close (dist 50).", ("unlocked card, pin, follow chip", "tower", "valley"), "Day.", "5/5", "Card goes full.", "Swell into a big D-major hit on 'charge'."),
    "lesson": ("The takeaway: the full checklist, screenshot-able.", "The complete SKY-PROOF card (BEFORE YOU ADD A DRAGON) with 'Ask what ordinary people change.' in serif italic.",
               "Wide orbit (dist 190).", ("full card", "the island at golden hour", "stars"), "Golden hour.", "Full card.", "Block wipe to the end card.",
               "Anthem: the theme in D major; the World Engine chime as the card lands."),
    "cta": ("Comment CTA.", "End card: logo, PART 27 / 50, title, a speech-bubble COMMENT panel.",
            "Cut (under the block wipe) back onto the dragon's shoulder, on its hook orbit.", ("end card", "the Isle", "void"), "Golden hour (the loop frame).", "End card.", "The card lifts on 'Part'.",
            "Outro: the theme's answer on celesta and music box."),
    "next": ("Say the part number, ask for the follow with a reason (part 28), open the next loop.",
             "Riding the dragon's circle again; PART 27/50; FOLLOW FOR PART 28 pressed on 'Follow'; NEXT RUN 28 · BUILDERS from a locked cairn; below, a cairn's three stones stack themselves; the orbit lands on frame 0 and the hook title returns.",
             "The follow camera on the hook orbit, landing on frame 0.", ("progress bar, follow button, next-run card", "the dragon's back", "the village, the cairn"),
             "Golden hour.", "PART 27/50 · FOLLOW FOR PART 28 · NEXT RUN: BUILDERS · SOMETHING LEARNS TO BUILD.", "Loop to frame 0.",
             "Tease over a held A, a horn call, the engine chime on 'Follow'; it resolves into frame 0's D minor."),
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
            "direction": "The same lab host, a shade darker for a predator episode. 'Because this is what a dragon sees' drops low and close. "
                         "The target list is a calm, cold inventory. 'They just lived in plain sight' is the sting. The four changes are crisp. "
                         "'Look back' is the turn; 'Whoever rings it runs the village' is a quiet reveal. The comment ask is genuinely curious.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L6", "from": "plain"}, {"line": "L14", "from": "Rule", "to": "back."}],
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
            shot["hideLogoBugUntil"] = cue("L19", "Part", 0.0)
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
             hit("roar", cue("L1", "dragons", 0.05), -13), hit("dragonPass", cue("L1", "existed,", 0.0), -17),
             hit("cardSlide", cue("L2", "Because", -0.05), -18), hit("eyeOn", cue("L2", "sees.", -0.15), -11)],
    "setup": [bed("lockOn", cue("L3", "Every", -0.1), cue("L3", "target.", 0.2), -21),
              hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16), hit("dragonPass", cue("L4", "run.", 0.4), -12)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "travels.", 0.2), -21), bed("burn", cue("L5", "roofs", -0.1), cue("L5", "travels.", 0.4), -19),
             bed("losses", cue("L5", "two:", 0.1), cue("L5", "gone.", 0.3), -23)],
    "drop": [hit("dragonPass", cue("L6", "Nobody", -0.2), -17), hit("stamp", cue("L6", "war."), -10)],
    "rehook": [hit("rewind", cue("L6", "sight.", 0.45), -11), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "roofs": [hit("check", cue("L8", "roofs."), -13), hit("restore", cue("L8", "Slate"), -15), hit("unlock", cue("L8", "burn.", 0.25), -20)],
    "pens": [hit("check", cue("L9", "pens."), -13), hit("restore", cue("L9", "covered", -0.2), -15), bed("stomp", cue("L9", "covered", -0.2), cue("L9", "barns.", 0.2), -22),
             hit("unlock", cue("L9", "barns.", 0.3), -20)],
    "place": [hit("check", cue("L10", "place."), -13), hit("ringOn", cue("L10", "place."), -16), hit("restore", cue("L10", "Build"), -14),
              hit("worldRipple", cue("L10", "valley,"), -17), hit("ringOn", cue("L10", "valley,"), -18)],
    "travel": [hit("check", cue("L11", "travel."), -13), hit("snowAir", cue("L11", "Four:", -0.2), -20), hit("restore", cue("L11", "Move"), -17), hit("unlock", cue("L11", "night,", 0.2), -16)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), hit("dragonPass", cue("L12", "Run", 0.3), -13),
             bed("simTicks", cue("L12", "Run", 0.3), cue("L13", "nothing.", 0.5), -21), hit("eyeOn", cue("L13", "The", -0.15), -13),
             bed("births", cue("L13", "looks", 0.0), cue("L13", "nothing.", 0.4), -23)],
    "twist": [hit("stompHit", cue("L14", "Look", 0.0), -15), hit("restore", cue("L14", "Look", 0.0), -15),
              hit("ringOn", cue("L15", "sees", 0.0), -16), hit("eyeOn", cue("L15", "sees", -0.25), -15), hit("dragonPass", cue("L15", "dragon", 0.0), -13),
              hit("towerBell", cue("L15", "bell,"), -10)],
    "role": [hit("towerBell", cue("L16", "rings"), -14), hit("unlock", cue("L16", "runs"), -10), hit("worldRipple", cue("L16", "charge."), -14)],
    "lesson": [hit("engineWind", cue("L17", "Don't", -0.8), -15), hit("chime", cue("L17", "Don't", -0.3), -10),
               hit("cardSlide", cue("L17", "Don't", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("cardSlide", cue("L18", "What", -0.1), -20)],
    "next": [bed("simTicks", cue("L19", "Part", -0.05), cue("L19", "Part", 0.55), -22),
             hit("engineWind", cue("L19", "Follow", -0.5), -15), hit("followPress", cue("L19", "Follow"), -11),
             hit("chime", cue("L19", "Follow", 0.02), -11),
             hit("cardSlide", cue("L19", "28:", -0.1), -18), hit("unlock", cue("L19", "learns"), -15),
             hit("cubPop", cue("L19", "Isle", 0.0), -17), hit("cubPop", cue("L19", "learns", 0.05), -16), hit("stompHit", cue("L19", "build.", 0.0), -18),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score (pipeline/music_s2.py). The series theme stays (D minor for the problem, D major for the payoff), but EP27
# has its own band around it: `soar` (horns in open fifths, a taiko wingbeat) whenever the dragon is in the air,
# `raid` war drums for run 1, and `stealth` (tiptoe pizzicato) layering up as the village hides.
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 96,
    "sections": [
        msec({"shot": "hook"}, "soar", ["Dm", "Bb"], "D minor"),
        msec(cue("L3", "Every", -0.15), "mystery", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=2),
        msec(cue("L4", "run."), "raid", ["Dm", "Bb", "Gm", "A"], "D minor"),
        msec(cue("L6", "Nobody", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "They"), "void", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "sight.", 0.45), "mystery", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=2),
        msec(cue("L8", "One:", -0.1), "stealth", ["Dm", "C", "Bb", "C"], "D minor", layer=1),
        msec(cue("L9", "Two:", -0.1), "stealth", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "stealth", ["Dm", "C", "Bb", "C"], "D minor", layer=3),
        msec(cue("L11", "Four:", -0.1), "stealth", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True),
        msec(cue("L14", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(cue("L15", "A", -0.1), "soar", ["Dm", "Bb", "Gm", "A"], "D minor", beatsPerChord=2),
        msec(cue("L15", "hides.", 0.0), "rest", ["Dm"], "D minor"),
        msec(cue("L16", "Whoever"), "swell", ["Bb", "F", "C", "A"], "D minor", beatsPerChord=2),
        msec(cue("L16", "charge.", 0.0), "anthem", ["D", "G", "Bm", "A"], "D major"),
        msec(cue("L18", "What", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L19", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "different."), "chord": "Dm"},
        {"kind": "stab", "at": cue("L2", "sees."), "chord": "Bb"},
        {"kind": "boom", "at": cue("L6", "sight."), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L13", "nothing."), "chord": "F"},
        {"kind": "cymbal", "at": cue("L13", "nothing.")},
        {"kind": "hit", "at": cue("L16", "charge."), "chord": "D"},
        {"kind": "call", "at": cue("L19", "learns"), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    # one bell, and everyone hides: the music too (the bell's tail owns it)
    "rests": [{"from": cue("L15", "hides.", 0.05), "to": cue("L16", "Whoever", -0.02)}],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #Dragons #WritingTips #WorldcraftShorts"
BODY = (
    "If dragons existed, your world's architecture would look very different. Because this is what a dragon sees: "
    "every thatch roof, every open pen, every cart on the road is a target.\n\n"
    "We ran it. Week one, the roofs burn. Week two, the flocks are gone. Week three, nobody travels. Nobody fought a war; "
    "they just lived in plain sight.\n\n"
    "So hide the village: slate and turf roofs, flocks in covered barns, the village moved into the valley under the cliff, "
    "and travel at night under the trees. Run it again, and the dragon looks down and finds nothing.\n\n"
    "Then the twist: look back. A watchtower sees the dragon first; one bell, and everyone hides. Whoever rings it runs the "
    "village. The dragon changed who's in charge.\n\n"
    "Don't just add a dragon. Ask what ordinary people do differently.\n\n"
    "What would your civilization invent to survive dragons? Comment below.\n\n"
    "Part 27 of 50. Follow for part 28: something on the Isle learns to build."
)
METADATA = {
    "youtube": {
        "title": "What Would Dragons Actually Change? (Worldbuilding)",
        "titleAlternate": "This is what a dragon sees",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 6: Creatures and Species.\n\n" + TAGS,
        "pinnedComment": "Comment check: what would YOUR civilization invent to survive dragons? Roofs, barns, tunnels, bells, something stranger? "
                         "(Part 28: something on the Isle learns to build.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated dragon sprite; the island, village and creatures are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "This is what a dragon sees 🐉 Every thatch roof, open pen and cart: a target. We hid the village in 4 moves, and #5 is the twist: whoever watches the sky runs the village. "
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
        "caption": "This is what a dragon sees.\n\n" + BODY + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": "First 27 characters: 'This is what a dragon sees.'",
        "pinnedComment": "Save the sky-proof checklist, then tell us: what would your civilization invent to survive dragons?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep27] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots")
