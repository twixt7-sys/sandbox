"""Generate episodes/ep32/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep32/make_ep32.py
EP32 is Arc 7's second episode (History and Mythology): "Create an Ancient War That Still Matters". It closes EP31's
loop (two war standards rose over the two crowds before Maren's split statue: A WAR THAT NEVER ENDED) a thousand years
later: the truce line still runs down the statue's seam.

Its own device is THE STRATA: the war is a layer in the Isle's cut side, with every century since laid on top of it.
A war that only ended sinks under the centuries and fades (forgotten); a war that matters sends VEINS up through every
layer to the grass (a border, cursed ground, a stolen relic, a grudge), and at the twist the war's own colour floods up
through the centuries to the surface: it never ended. Camera language: THE CUTAWAY CRANE, the camera faces the Isle's
cut side on one azimuth and moves only up and down (the war below, today above), never orbiting until the lesson
(EP26 orbited, EP27 rode a dragon, EP28 sat at eye height, EP29 was a locked-off tripod, EP30 looked up, EP31 split the
frame). Motif colour: verdigris #46c2a0 (the war's bronze, turned green in the ground). Music band: `dirge` (a march
slowed to a dirge) and `earth` (war drums heard through the earth).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep32" / "timing.json"
SCOUT = os.environ.get("SCOUT")


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
    ("L1", "hook", "This war ended a thousand years ago. Why are people still dying?", 0.3, ["thousand", "dying?"]),
    ("L2", "hook", "Meet the Seam War. It ended in one truce.", 0.3, ["seam", "truce."]),
    ("L3", "setup", "The lazy version: the war ends, and everyone moves on.", 0.25, ["lazy", "moves"]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "Ten centuries pile on. The war sinks. Forgotten.", 0.35, ["sinks.", "forgotten."]),
    ("L6", "drop", "A war nobody feels is just a date.", 0.4, ["nobody", "date."]),
    ("L7", "rehook", "Real wars don't stay buried. Four climb out. The fifth is the twist.", 0.25, ["buried.", "twist."]),
    ("L8", "border", "One: a border. The truce line still splits the statue.", 0.2, ["border.", "splits"]),
    ("L9", "curse", "Two: cursed ground. Nobody has farmed the burned field since.", 0.2, ["cursed", "nobody"]),
    ("L10", "relic", "Three: a stolen relic. The court still keeps her torch.", 0.2, ["stolen", "torch."]),
    ("L11", "grudge", "Four: a grudge. Every child is taught who to hate.", 0.3, ["grudge.", "hate."]),
    ("L12", "run2", "Run it again. A thousand years. It's all still here.", 0.3, ["thousand", "here."]),
    ("L13", "twist", "Rule five? The claim. Nobody ever signed the peace.", 0.3, ["claim.", "peace."]),
    ("L14", "twist", "That truce was a pause. The war never ended.", 0.35, ["pause.", "never"]),
    ("L15", "role", "So hand one character the pen.", 0.3, ["one", "pen."]),
    ("L16", "lesson", "Fighting stops in a day. A war ends when its consequences do.", 0.35, ["day.", "consequences"]),
    ("L17", "cta", "What unresolved conflict would your ancestors leave behind?", 0.25, ["unresolved", "ancestors"]),
    ("L18", "next", "Part 32 of 50. Follow for part 33: a god built from fear.", 0.25, ["follow", "fear."]),
]
SHOTS = ["hook", "setup", "run1", "drop", "rehook", "border", "curse", "relic", "grudge", "run2", "twist", "role", "lesson", "cta", "next"]

# The block wipe into the end card: the world resets to frame 0 under it (the Isle today, a thousand years on).
WIPE = cue("L17", "What", -0.3)
RESET = cue("L3", "lazy", -0.15)          # the lazy version: the truce day, and everyone moves on
REWIND = cue("L6", "date.", 0.55)         # back to the truce day, the war still on the surface
RULES = cue("L8", "One:", -0.1)           # the rules: day
RUN2 = cue("L12", "Run", -0.05)
TWIST = cue("L13", "Rule", -0.1)          # back to today: the war layer deep under the centuries
FLOOD = cue("L14", "never", -0.05)        # the war's colour climbs through the centuries
ROLE = cue("L15", "So", -0.15)
HOOK_DRIFT = 0.5

# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle (it remembers): EP27's humans in the valley under the cliff, EP28's Fenn hall on the lake and
# the cairn, EP29's Undying Queen on her dais, EP30's worshipped Grimmaw (on the north-west meadow), EP31's Maren statue
# on the south-east meadow. EP32 is a thousand years after EP31's standards rose: the truce line runs north-south down
# the statue's seam (x = 18), the valley (gold) west of it and the court (rust) east of it. Every cutaway pose looks
# due north at the south-east cliff, where the line meets the edge, so the island's cut side fills the bottom of the
# frame and the older landmarks fall outside it (checked with pipeline/camprobe.ts).
CAIRN = (8.95, -5.38)
LAKE_HALL = (6.0, 4.6)
HUMAN_B = [("hall", (-3.6, -4.6)), ("house", (-1.8, -2.4)), ("house", (-4.8, -2.4)), ("house", (-1.0, -5.8)),
           ("house", (-5.6, -0.9)), ("house", (-3.4, -0.7)), ("house", (0.4, -4.2))]
HUMAN_TOWER = (-6.4, -5.6)
HUMAN_ROAD = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
DAIS = (9.4, -2.2)
QUEEN = (9.1, -2.2)
G_NOW = (8.5, -9.6)                      # the Grimmaw (EP30's worshipped beast), out of the cutaway frames
AZ = 0                                   # every cutaway camera looks due north at the cut
STATUE = (18.0, 1.5)
FACE = AZ - 90                           # as in EP31: the gilded half is screen-left (west, the valley's side)
LINE_A, LINE_B = (18.0, -7.0), (18.0, 8.3)   # the truce line, down the statue's seam to the cliff edge
SKIP = (0.46, 0.65)                      # no stones under the statue's plinth
FIELD = (20.9, -0.4, 3.4, 3.4)           # the court's field, burned in the war and never farmed again
RELIC = (20.3, 5.4)                      # her gilded torch, kept by the court on its side of the line
CROWD = [[15.4, 3.8], [21.2, 3.0]]       # the valley's people (left, wheat gold) and the court's (right, rust)
STD_L, STD_R = (15.0, 2.2), (21.0, 2.2)  # EP31's two war standards: still planted
PEN = (18.0, 5.6)                        # where one character steps onto the line (rule 5's job)
VERD = "#46c2a0"
GOLD = "#f4c46e"
RUST = "#d0603f"

# The strata (in world y). Today the war lies under ten centuries; on the truce day it is the topsoil.
SURF = 2.55                              # the grass lip at the south-east cliff (column top 3 - 0.45)
WAR_NOW = (-0.8, 0.0)
WAR_THEN = (1.75, SURF)
# the veins, on the south face of the cliff under each consequence (x0, x1, z0, z1)
V_GRUDGE = [15.2, 15.8, 12.2, 13.2]
V_BORDER = [17.7, 18.3, 8.2, 10.2]
V_RELIC = [19.25, 19.75, 7.2, 8.2]
V_CURSE = [21.2, 21.8, 6.2, 7.2]
RULER = (14.0, 14.1)                     # the depth ruler stands on the cut's left end


def shift(c, d):
    """The same cue, `d` seconds later."""
    return {**c, "offset": round(c.get("offset", 0.0) + d, 3)}


def jump(at, before, after):
    """A hard change of value on a cut: hold `before` until just before the cue, then step to `after`."""
    return [[shift(at, -0.02), before], [at, after, "step"]]


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


def tcue(c):
    """A cue's time in seconds from the measured timing (None before the first TTS run)."""
    if not TIMING.exists():
        return None
    tm = json.loads(TIMING.read_text())
    ln = next(l for l in tm["lines"] if l["id"] == c["line"])
    hits = [w for w in ln["words"] if w["text"].strip(".,?!:").lower() == c["word"].strip(".,?!:").lower()]
    return hits[c.get("nth", 1) - 1]["start"] + c.get("offset", 0.0)


def loop_span():
    """Seconds from the wipe to the end: the loop camera key drifts this long and lands exactly on the hook pose."""
    if not TIMING.exists():
        return 6.0
    tm = json.loads(TIMING.read_text())
    ln = next(l for l in tm["lines"] if l["id"] == WIPE["line"])
    w = next(w for w in ln["words"] if w["text"].strip(".,?!:").lower() == WIPE["word"].lower())
    return tm["duration"] - (w["start"] + WIPE.get("offset", 0.0))


# The cutaway poses (az 0, looking north at the south-east cliff). Planned with pipeline/camprobe.ts (BRIEF.md §6).
HOOK_POSE = dict(el=12, dist=130, target=(18.0, 6.5, 6.0), fov=15)         # today: the statue on the line, the war below
LAZY_POSE = dict(el=7, dist=70, target=(18.0, 4.2, 6.0), fov=15)
DROP_POSE = dict(el=8, dist=95, target=(18.0, 2.6, 8.5), fov=15)         # craned down onto the forgotten layer
TRUCE_POSE = dict(el=12, dist=115, target=(18.0, 6.0, 6.0), fov=15)      # the truce day, the war under the grass
DEEP = dict(el=6, dist=80, target=(18.0, 2.6, 8.5), fov=15)              # down at the war layer (each rule starts here)
UP = dict(el=16, dist=105, target=(18.0, 6.0, 4.0), fov=15)              # up at the surface (the consequence)
TWIST_DEEP = dict(el=6, dist=82, target=(18.0, 1.4, 8.5), fov=15)        # today, down at the buried war
TWIST_UP = dict(el=12, dist=130, target=(18.0, 6.5, 6.0), fov=15)          # the flood reaches the grass
WIDE = dict(el=12, dist=196, target=(3.0, 1.0, 0.0), fov=26)             # the whole Isle in profile, its cut side showing


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    lin = lambda at, v: [at, v, "linear"]
    H = shot("hook")

    # ---- the clock (YEARS since the truce). Today is year 1000.
    R1A, R1B = cue("L4", "run.", 0.3), cue("L5", "Forgotten.", 0.2)        # run 1: the centuries pile on
    R2A, R2B = cue("L12", "Run", 0.25), cue("L12", "here.", 0.0)           # run 2
    clock = [[H, 1000], *jump(RESET, 1000, 0), [R1A, 0], lin(R1B, 1000), *jump(REWIND, 1000, 0),
             [R2A, 0], lin(R2B, 1000), *jump(TWIST, 1000, 1000), [WIPE, 1000]]
    speed = [[H, 1], [cue("L4", "run."), 1], [R1A, 6], [cue("L5", "Forgotten."), 6], [cue("L6", "A"), 1],
             [R2A, 1], [cue("L12", "Run", 0.5), 6], [R2B, 6], [cue("L13", "Rule"), 1]]
    # HUD: how many of the war's legacies reach today, and how many people have inherited it
    legacies = [[H, 4], *jump(RESET, 4, 0), *jump(REWIND, 0, 0),
                *jump(cue("L8", "border."), 0, 1), *jump(cue("L9", "cursed"), 1, 2), *jump(cue("L10", "stolen"), 2, 3), *jump(cue("L11", "grudge."), 3, 4),
                *jump(cue("L13", "claim."), 4, 5), *jump(WIPE, 5, 4)]
    heirs = [[H, 314], *jump(RESET, 314, 0), *jump(cue("L11", "taught"), 0, 22), [R2A, 22], lin(R2B, 314), [WIPE, 314]]

    # ---- the strata: today the war lies 1000 years down with four veins to the grass; the lazy war sinks and fades
    y0 = [[H, WAR_NOW[0]], *jump(RESET, WAR_NOW[0], WAR_THEN[0]), [R1A, WAR_THEN[0]], lin(R1B, WAR_NOW[0]), *jump(REWIND, WAR_NOW[0], WAR_THEN[0]),
          [R2A, WAR_THEN[0]], lin(R2B, WAR_NOW[0]), [WIPE, WAR_NOW[0]]]
    y1 = [[H, WAR_NOW[1]], *jump(RESET, WAR_NOW[1], WAR_THEN[1]), [R1A, WAR_THEN[1]], lin(R1B, WAR_NOW[1]), *jump(REWIND, WAR_NOW[1], WAR_THEN[1]),
          [R2A, WAR_THEN[1]], lin(R2B, WAR_NOW[1]), [WIPE, WAR_NOW[1]]]
    cent = [[H, 10], *jump(RESET, 10, 0), [R1A, 0], lin(R1B, 10), *jump(REWIND, 10, 0), [R2A, 0], lin(R2B, 10), [WIPE, 10]]
    fade = [[H, 0], [cue("L5", "sinks.", -0.1), 0], lin(cue("L5", "Forgotten.", 0.4), 0.9), *jump(REWIND, 0.9, 0)]
    flood = [[H, 0], [FLOOD, 0], lin(cue("L14", "ended.", 0.35), 1), *jump(WIPE, 1, 0)]
    vein = lambda on: [[H, 1], *jump(RESET, 1, 0), [on, 0], [shift(on, 0.35), 1], *jump(WIPE, 1, 1)]
    veins = [
        {"box": V_BORDER, "color": VERD, "on": vein(cue("L8", "border.")), "label": "BORDER"},
        {"box": V_CURSE, "color": VERD, "on": vein(cue("L9", "cursed")), "label": "CURSED"},
        {"box": V_RELIC, "color": VERD, "on": vein(cue("L10", "stolen")), "label": "RELIC"},
        {"box": V_GRUDGE, "color": VERD, "on": vein(cue("L11", "grudge.")), "label": "GRUDGE"},
    ]

    # ---- the surface. The lazy version has no line, no standards, a plain whole statue and a farmed field.
    line_rise = [[H, 1], *jump(RESET, 1, 0), [cue("L8", "truce"), 0], lin(cue("L8", "statue.", 0.1), 1), [WIPE, 1]]
    std = [[H, 1], *jump(RESET, 1, 0), *jump(REWIND, 0, 1), [WIPE, 1]]
    gild = [[H, 1], *jump(RESET, 1, 0), *jump(REWIND, 0, 1), [WIPE, 1]]
    tar = [[H, 1], *jump(RESET, 1, 0), *jump(REWIND, 0, 1), [WIPE, 1]]
    grow = [[H, 1.35], [WIPE, 1.35]]
    torch = [[H, 0], *jump(RESET, 0, 1), *jump(cue("L10", "court"), 1, 0), [WIPE, 0]]
    relic = [[H, 1], *jump(RESET, 1, 0), [cue("L10", "court", -0.05), 0], [cue("L10", "keeps", 0.15), 1, "out"], [WIPE, 1]]
    ripe = [[H, 0.5], *jump(RESET, 0.5, 1.0), *jump(REWIND, 1.0, 0.5), [WIPE, 0.5]]
    burn = [[H, 1], *jump(RESET, 1, 0), *jump(REWIND, 0, 0.35), [cue("L9", "cursed", -0.1), 0.35], lin(cue("L9", "burned", 0.1), 1), [WIPE, 1]]
    # the crowds face across the line once the grudge is taught (and today)
    watch_on = [[H, 1], *jump(RESET, 1, 0), [cue("L11", "taught", -0.05), 0], [cue("L11", "taught"), 1, "step"], [WIPE, 1]]
    count = [[H, 22], [WIPE, 22]]
    ruler = [pk(H, *QUEEN, "idle", face=0), pk(cue("L18", "fear.", -0.1), *QUEEN, "alert", face=0), pk(cue("L18", "fear.", 1.0), *QUEEN, "idle", face=0)]
    g_now = [pk(H, *G_NOW, "idle", face=160), pk(cue("L18", "fear.", -0.1), *G_NOW, "alert", face=160), pk(cue("L18", "fear.", 1.0), *G_NOW, "idle", face=160)]
    # one character steps onto the line (rule 5's job): hidden until "hand one character"
    pen = [pk(H, *PEN, "hidden"), pk(cue("L15", "one", -0.1), PEN[0] + 1.8, PEN[1] + 0.4, "idle", face=180), pk(cue("L15", "character"), *PEN, "idle", face=90, dur=0.8),
           pk(cue("L16", "Fighting", -0.3), *PEN, "hidden")]

    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run")]

    # Camera language: the cutaway crane. One azimuth, vertical moves between the war (below) and today (above).
    span = loop_span()
    LESSON_AT, PUSH_AT = cue("L16", "Fighting", -0.25), cue("L16", "ends", -0.1)
    push_gap = (tcue(PUSH_AT) - tcue(LESSON_AT)) if TIMING.exists() else 2.0
    front = lambda at, pose, **kw: cam(at, AZ, dur=0.01, cut=True, **pose, **kw)
    crane = lambda at, pose, dur=0.9, **kw: cam(at, AZ, dur=dur, **pose, **kw)
    camera = [
        cam(H, AZ, drift=HOOK_DRIFT, **HOOK_POSE),
        front(RESET, LAZY_POSE),
        cam(cue("L4", "run.", 0.05), 0, dur=1.0, **WIDE),
        crane(cue("L5", "sinks.", -0.1), dict(WIDE, target=(3.0, -2.5, 0.0)), dur=1.6),
        front(cue("L6", "A", -0.2), DROP_POSE),
        front(REWIND, TRUCE_POSE),
        # each rule: down at the war layer as it is named, then craned up to what it left on the surface
        front(RULES, DEEP), crane(cue("L8", "truce", -0.15), UP),
        front(cue("L9", "Two:", -0.1), DEEP), crane(cue("L9", "Nobody", -0.15), dict(UP, el=20, target=(19.0, 5.6, 2.5))),
        front(cue("L10", "Three:", -0.1), DEEP), crane(cue("L10", "court", -0.15), dict(UP, el=13, target=(18.8, 6.3, 4.0))),
        front(cue("L11", "Four:", -0.1), DEEP), crane(cue("L11", "Every", -0.15), dict(UP, el=14, dist=112, target=(18.0, 6.0, 4.0))),
        cam(RUN2, 0, dur=0.01, cut=True, **WIDE),
        crane(cue("L12", "thousand", -0.1), dict(WIDE, target=(3.0, -2.5, 0.0)), dur=1.6),
        front(TWIST, TWIST_DEEP),
        crane(FLOOD, TWIST_UP, dur=1.3),
        front(ROLE, dict(TRUCE_POSE, el=12, dist=108, target=(18.0, 6.2, 5.5)), drift=0.4),
        cam(LESSON_AT, 15, 34, 190, (2.0, 3.0, 0.0), fov=26, dur=1.6, drift=2.0),
        # a slow push down onto the Isle while the line is read (the orbit carries on through it)
        cam(PUSH_AT, 15 + 2.0 * push_gap, 28, 184, (2.0, 2.0, 0.0), fov=26, dur=1.8, drift=2.0),
        cam(WIPE, AZ - HOOK_DRIFT * span, HOOK_POSE["el"], HOOK_POSE["dist"], HOOK_POSE["target"], fov=HOOK_POSE["fov"], cut=True, drift=HOOK_DRIFT),
    ]
    if SCOUT:
        camera = [cam(H, 0, 89, 120, (10.0, 0.0, 0.0), fov=30)]
    light = [
        {"at": H, "mood": "golden"},
        {"at": RESET, "mood": "day", "dur": 0.4},
        {"at": cue("L6", "A", -0.2), "mood": "gloom", "dur": 0.6},
        {"at": REWIND, "mood": "dusk", "dur": 0.3},
        {"at": RULES, "mood": "day", "dur": 0.4},
        {"at": TWIST, "mood": "dusk", "dur": 0.3},
        {"at": ROLE, "mood": "day", "dur": 0.3},
        {"at": cue("L16", "Fighting", -0.3), "mood": "golden", "dur": 2.0},
        # EP33's tease: the sun goes dark over the Isle for a breath (what people fear), then the golden hour returns
        {"at": cue("L18", "fear.", -0.15), "mood": "night", "dur": 0.35},
        {"at": cue("L18", "fear.", 0.75), "mood": "golden", "dur": 0.6},
    ]
    human_valley = {
        "buildings": [{"kind": k, "a": list(a), "face": 0} for k, a in HUMAN_B],
        "roof": [[H, 1]], "pens": [{"a": [-6.4, -1.4], "r": 1.6}], "cover": [[H, 1]],
        "roads": {"b": HUMAN_ROAD}, "route": [[H, 1]], "tradeKey": "tradeH", "lanterns": [[H, 0]],
        "tower": {"x": HUMAN_TOWER[0], "z": HUMAN_TOWER[1], "h": 6.0, "keys": [[H, 1]], "rings": []},
    }
    fenn_hall = {"buildings": [{"kind": "greathall", "a": list(LAKE_HALL), "b": list(LAKE_HALL), "stiltsB": 1.6, "face": 0}],
                 "place": [[H, 1]], "open": [[H, 1]], "glow": [[H, 1]], "roof": [[H, 1]], "pens": []}
    clear = [STATUE, RELIC, PEN, (FIELD[0], FIELD[1]), *[tuple(c) for c in CROWD]]
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": [[H, 30]], "max": 40, "base": 30, "centers": [[-7.2, -1.4], [-6.0, 0.4]], "skin": "sheep"},
        "pred": [[H, 1]],
        "predators": [{"id": "g1", "scale": 1.3, "keys": g_now, "adorn": True}],
        "series": {"legacies": legacies, "heirs": heirs, "tradeH": [[H, 4]]},
        "settlement": human_valley,
        "settlements": [fenn_hall],
        "folk": {"count": [[H, 9]], "centers": [list(LAKE_HALL)], "spread": 2.0, "site": [[H, 0]],
                 "eyes": [[H, 1]], "wet": [[H, 1]], "glow": [[H, 1]], "hero": []},
        "people": {"count": count, "centers": CROWD, "spread": 1.5, "life": 70, "royal": [[H, 0]],
                   "tints": ["#f0c04a", "#b0452f"], "watch": list(STATUE), "watchOn": watch_on,
                   "figures": [{"keys": pen, "tunic": "#e9e2cf", "torch": False, "scale": 1.7}],
                   "ruler": {"keys": ruler, "dais": {"x": DAIS[0], "z": DAIS[1], "face": 0}}},
        "fields": {"plots": [{"x": FIELD[0], "z": FIELD[1], "w": FIELD[2], "d": FIELD[3]}], "ripe": ripe, "burn": burn},
        "props": [{"kind": "cairn", "x": CAIRN[0], "z": CAIRN[1], "stones": [[H, 3]]},
                  {"kind": "statue", "x": STATUE[0], "z": STATUE[1], "face": FACE, "rise": [[H, 1]], "gild": gild, "tar": tar, "grow": grow, "torch": torch},
                  {"kind": "border", "x": LINE_A[0], "z": LINE_A[1], "to": list(LINE_B), "skip": list(SKIP), "rise": line_rise},
                  {"kind": "relic", "x": RELIC[0], "z": RELIC[1], "face": -90, "rise": relic},
                  {"kind": "standard", "x": STD_L[0], "z": STD_L[1], "face": -90, "rise": std, "color": "#f0c04a"},
                  {"kind": "standard", "x": STD_R[0], "z": STD_R[1], "face": 90, "rise": std, "color": "#b0452f"}],
        "strata": {"war": {"y0": y0, "y1": y1}, "surface": SURF, "max": 10, "centuries": cent, "fade": fade, "flood": flood, "veins": veins},
        "clearTrees": [[d[0], d[1], 3.0] for d in clear] + [[18.0, 6.5, 3.5], [18.0, -3.0, 4.0], [16.0, 9.0, 3.0]],
        "layers": {"ripple": ripple},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "A BORDER", "text": "the line holds", "at": cue("L8", "border.")},
    {"n": 2, "label": "A CURSE", "text": "never farmed", "at": cue("L9", "cursed")},
    {"n": 3, "label": "A RELIC", "text": "stolen, kept", "at": cue("L10", "stolen")},
    {"n": 4, "label": "A GRUDGE", "text": "taught, not lived", "at": cue("L11", "grudge.")},
    {"n": 5, "label": "THE CLAIM", "text": "nobody signed", "at": cue("L7", "Four"), "locked": True, "unlockAt": cue("L15", "pen.", -0.1)},
]
SPRITE = {"sprite": "ep32/war_sprite.png", "spriteW": 84, "spriteH": 126}

TAGS_V = [
    {"vein": 0, "text": "BORDER", "at": cue("L8", "splits"), "lift": 60},
    {"vein": 1, "text": "CURSED", "at": cue("L9", "farmed"), "lift": 90},
    {"vein": 2, "text": "RELIC", "at": cue("L10", "keeps"), "lift": 60},
    {"vein": 3, "text": "GRUDGE", "at": cue("L11", "hate."), "lift": 90},
]


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "1000 YEARS AGO", "color": VERD, "size": 60, "pulseAt": cue("L1", "thousand")},
                 {"text": "STILL DYING?", "color": RUST, "size": 80, "pulseAt": cue("L1", "dying?")}]
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 430, "size": 84, "start": {"shot": "hook"}, "end": cue("L2", "Meet", -0.1), "preShow": True},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 32 · HISTORY", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "strata", "ruler": list(RULER), "start": cue("L1", "Why", -0.05), "end": RESET, "topText": "TODAY"},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Meet", -0.05), "end": RESET, "dietAt": cue("L2", "truce."),
         "kicker": "FIELD CARD · NO. 007", "kind": "ANCIENT WAR", "name": "THE SEAM WAR", "dietLabel": "ENDED", "diet": "one truce, 1000 years ago", **SPRITE},
    ]
    G["setup"] += [
        {"type": "blockWipe", "at": RESET, "dur": 0.34, "color": "#173a33"},
        {"type": "kinetic", "parts": [{"text": "THE WAR ENDS", "at": cue("L3", "war"), "size": 80}, {"text": "EVERYONE MOVES ON", "at": cue("L3", "everyone"), "color": "rust", "size": 58}],
         "y": 470, "size": 80, "start": cue("L3", "war", -0.05), "end": cue("L4", "Press", -0.15)},
        {"type": "strata", "ruler": list(RULER), "start": cue("L3", "lazy", 0.1), "end": cue("L6", "A", -0.2), "warText": "THE WAR", "topText": "TODAY", "zeroText": "YEAR 0"},
        {"type": "simBar", "counters": [{"icon": "strata", "label": "LEGACIES", "key": "legacies", "color": VERD, "digits": 2},
                                        {"icon": "mortal", "label": "HEIRS", "key": "heirs", "color": "ember", "digits": 3}],
         "compact": True, "start": cue("L4", "Press", -0.15), "end": cue("L16", "Fighting", -0.3), "runAt": [cue("L4", "run."), cue("L12", "Run")]},
    ]
    G["run1"] += [
        {"type": "kinetic", "parts": [{"text": "YEAR 300 · BURIED", "at": cue("L5", "centuries"), "color": "parchment", "size": 56},
                                      {"text": "YEAR 600 · FADED", "at": cue("L5", "sinks."), "color": "parchment", "size": 56},
                                      {"text": "YEAR 1000 · FORGOTTEN", "at": cue("L5", "Forgotten."), "color": "rust", "size": 56}],
         "y": 468, "size": 56, "start": cue("L5", "centuries", -0.05), "end": cue("L6", "A", -0.25)},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "JUST A DATE", "sub": "0 LEGACIES · NOBODY CARES", "color": "rust", "y": 560, "size": 80, "start": cue("L6", "just"), "end": cue("L6", "date.", 0.5)},
        {"type": "strata", "ruler": list(RULER), "start": cue("L6", "A", -0.2), "end": REWIND, "warText": "FORGOTTEN", "topText": "TODAY"},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "date.", 0.55), "end": cue("L7", "Real", 0.3)},
        {"type": "blockWipe", "at": cue("L6", "date.", 0.53), "dur": 0.34},
        {"type": "kinetic", "parts": [{"text": "REAL WARS", "at": cue("L7", "Real"), "size": 78}, {"text": "DON'T STAY BURIED", "at": cue("L7", "stay"), "color": VERD, "size": 60}],
         "y": 470, "size": 84, "start": cue("L7", "Real", -0.05), "end": cue("L7", "Four", -0.15)},
        {"type": "strata", "ruler": list(RULER), "start": cue("L7", "Real"), "end": TWIST, "warText": "THE WAR", "topText": "TODAY", "zeroText": "YEAR 0", "tags": TAGS_V},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L16", "Fighting", -0.3),
         "kicker": "THE SEAM WAR · WHAT SURVIVES", "title": "DIG IT UP", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L8", "The", -0.3), 0], [cue("L8", "The", 0.0), 1], [ROLE, 1], [shift(ROLE, 0.3), 0]]},
    ]
    G["border"] += [
        {"type": "pin", "at": [18.0, 6.2, 0.0], "kicker": "THE TRUCE LINE", "text": "DOWN HER SEAM", "color": VERD, "lift": 30, "size": 28,
         "start": cue("L8", "splits", 0.0), "end": cue("L9", "Two:", -0.15)},
    ]
    G["curse"] += [
        {"type": "pin", "at": [FIELD[0], 3.6, FIELD[1]], "kicker": "THE BURNED FIELD", "text": "NEVER FARMED", "color": VERD, "lift": 40, "size": 28,
         "start": cue("L9", "farmed", 0.0), "end": cue("L10", "Three:", -0.15)},
    ]
    G["relic"] += [
        {"type": "pin", "at": [RELIC[0], 7.4, RELIC[1]], "kicker": "HER TORCH", "text": "ON THEIR SIDE", "color": VERD, "lift": 30, "size": 28,
         "start": cue("L10", "torch.", 0.0), "end": cue("L11", "Four:", -0.15)},
    ]
    G["grudge"] += [
        {"type": "pin", "at": [STATUE[0], 9.4, 3.4], "kicker": "EVERY CHILD", "text": "FACES THE LINE", "color": VERD, "lift": 30, "size": 28,
         "start": cue("L11", "taught", 0.0), "end": cue("L12", "Run", -0.15)},
    ]
    G["run2"] += [
        {"type": "stamp", "text": "STILL HERE", "sub": "1000 YEARS · 4 LEGACIES · 314 HEIRS", "color": VERD, "rotate": -4, "y": 880, "size": 96, "start": cue("L12", "here."), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}, {"text": "THE CLAIM", "at": cue("L13", "claim."), "color": VERD, "size": 96}],
         "size": 150, "y": 560, "start": cue("L13", "Rule", -0.02), "end": cue("L13", "Nobody", -0.12)},
        {"type": "pin", "at": [18.0, -0.4, 9.2], "kicker": "THE PEACE", "text": "NEVER SIGNED", "color": "ember", "lift": 90, "size": 30,
         "start": cue("L13", "Nobody", 0.0), "end": cue("L14", "pause.", 0.2)},
        {"type": "strata", "ruler": list(RULER), "start": TWIST, "end": ROLE, "warText": "THE WAR", "topText": "TODAY"},
        {"type": "kinetic", "parts": [{"text": "A PAUSE", "at": cue("L14", "pause."), "color": "parchment", "size": 84}, {"text": "IT NEVER ENDED", "at": cue("L14", "never"), "color": "ember", "size": 84}],
         "size": 84, "y": 560, "start": cue("L14", "pause.", -0.05), "end": shift(ROLE, -0.05)},
    ]
    G["role"] += [
        {"type": "followChip", "start": cue("L15", "pen.", 0.2), "end": cue("L16", "consequences", 0.3), "text": "FOLLOW", "sub": "PART 32/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "Fighting", -0.3), **({"unlockAt": cue("L16", "Fighting", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "Fighting", -0.3), "end": WIPE, "kicker": "BEFORE YOU END A WAR", "title": "THE SEAM WAR", **SPRITE,
         # the line to keep: on screen from the end of the first sentence until the wipe covers the card
         "subtitle": "A war ends when its consequences do.", "subtitleAt": cue("L16", "day.")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 32 / 50",
         "title": "Create an Ancient War That Still Matters", "cta": "COMMENT", "icon": "bubble", "with": "What did they leave you?", "withAt": cue("L17", "ancestors", -0.05), "choiceSize": 34,
         "choices": [{"text": "BORDER", "color": VERD, "at": cue("L17", "unresolved")}, {"text": "RELIC", "color": VERD, "at": cue("L17", "conflict")},
                     {"text": "GRUDGE", "color": VERD, "at": cue("L17", "your")}]},
    ]
    gone = cue("L18", "fear.", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 32, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6, "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone, "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 33"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "33:", -0.1), "revealAt": cue("L18", "god"), "end": gone,
         "kicker": "NEXT RUN · 33", "title": "BELIEF", "sub": "A GOD BUILT FROM FEAR.", "sprite": "sun", "spritePx": 9},
        {"type": "kinetic", "parts": hook_text, "y": 430, "size": 84, "start": cue("L18", "fear.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("A war that only ended is a date in your backstory. Write what it left behind instead: a border still drawn, "
          "ground nobody will farm, a relic one side still keeps, a grudge each generation is taught. Then decide what "
          "was never settled. A war ends when its consequences do, and one character can be the one to end it.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Close EP31's loop (two standards rose: a war that never ended) and stop the scroll on the question.",
             "Golden hour, a thousand years on: frontal on the Isle's south-east cliff. Above, Maren's split statue (gilded left, tarred right, the gilded hand empty) with a line of boundary stones running down its seam to the cliff edge, the valley's people in gold on the left and the court's in rust on the right, each facing the line, EP31's two war standards still planted, the court's field black and unfarmed, her torch on a plinth on the court's side. Below, the cut side of the island: the war is a dark layer flecked with bronze-green, ten century bands are laid on top of it, and four verdigris veins run up through them to the grass. 1000 YEARS AGO / STILL DYING? is on screen from frame 0, each line pulsing on its spoken word. A depth ruler pins TODAY at the grass and THE WAR · 1000 YRS DOWN on the layer. Then the field card: THE SEAM WAR · ANCIENT WAR · ENDED: one truce, 1000 years ago.",
             "Cutaway, frontal long lens (az 0, el 12, dist 130, fov 15), a slow 0.5°/s drift; the loop lands on the same frame.", ("kinetic, sting, strata labels, field card", "the statue on the line, the two crowds", "the cut side: the war layer, ten centuries, four veins"),
             "Golden hour.", "1000 YEARS AGO / STILL DYING? · FIELD CARD NO. 007 · THE SEAM WAR", "Verdigris block wipe into the lazy version.", "Dirge: the theme at half speed on low horns over a muffled drum; a hit on 'dying?'."),
    "setup": ("The lazy version: the war ends, and everyone moves on.",
              "A wipe to the truce day, year 0, in daylight: no line, no standards, the statue whole and plain, the field gold and farmed. The war is a dark band directly under the grass (THE WAR · YEAR 0). THE WAR ENDS / EVERYONE MOVES ON. The sim bar arrives (LEGACIES 00, HEIRS 000) and RUN is pressed.",
              "Cutaway (az 0, el 7, dist 70, fov 15), closer than the hook.", ("kinetic, strata labels, sim bar", "the whole statue, both crowds mixing", "the cut side, the war just under the grass"), "Day.", "THE WAR ENDS · EVERYONE MOVES ON", "A pull-out to the whole Isle on 'run'.", "Earth, thin (the heartbeat alone)."),
    "run1": ("Run the lazy version: a thousand years bury it.",
             "The whole Isle in profile, its cut side showing all round; YEAR 0→1000; century bands pile onto the war layer, which sinks down the cliff and greys into the clay as the camera cranes down after it. YEAR 300 · BURIED, YEAR 600 · FADED, YEAR 1000 · FORGOTTEN.",
             "Wide profile (az 0, el 12, dist 196), craning down 3.5 units after the sinking layer.", ("sim bar, kinetic", "the island's cut side, the war layer sinking", "void"), "Day.", "YEAR 300 · BURIED / YEAR 600 · FADED / YEAR 1000 · FORGOTTEN", "Cut down onto the layer.", "Drive."),
    "drop": ("The punchline: a war nobody feels is just a date.", "Craned down onto the cliff in gloom: the war layer deep and grey under ten centuries, nothing reaching the grass: JUST A DATE · 0 LEGACIES · NOBODY CARES. The ruler reads FORGOTTEN · 1000 YRS DOWN.",
             "Cutaway, craned down onto the layer (az 0, el 8, dist 95, fov 15).", ("stamp, strata labels", "the forgotten layer", "void"), "Gloom.", "JUST A DATE · 0 LEGACIES · NOBODY CARES", "Rewind + block wipe.", "Drop; a boom on 'date'."),
    "rehook": ("Re-hook: the thesis, then four easy rules and one locked.",
               "REWIND to the truce day, year 0, dusk: the centuries peel off and the war is the topsoil again, vivid. The two standards stand planted, the statue split (gilded and tarred), the field black; the ruler reads THE WAR · YEAR 0. REAL WARS / DON'T STAY BURIED; then the checklist DIG IT UP, row 5 locked (the twist).",
               "Cutaway (az 0, el 12, dist 115, fov 15).", ("rewind, kinetic, checklist, strata labels", "the statue, the standards, the black field", "the war under the grass"), "Dusk.",
               "THE WAR · YEAR 0 · REAL WARS · DON'T STAY BURIED · DIG IT UP 0/5", "Cut down to the war layer.", "Earth, the heartbeat; a riser into 'the twist'."),
    "border": ("Rule 1: a border.", "Down at the war layer in daylight, a verdigris seed lights in it under the seam; craning up, a line of boundary stones rises down the statue's seam to the cliff edge (THE TRUCE LINE · DOWN HER SEAM). Tag: BORDER.",
               "Crane: down at the layer (el 6, dist 80, fov 15), then up to the surface (el 16, dist 105, fov 15).", ("strata labels, checklist (folded), pin", "the stones rising", "the cut side"), "Day.", "1 A BORDER · the line holds", "Cut down.", "Earth 1: the heartbeat alone."),
    "curse": ("Rule 2: cursed ground.", "Down at the layer a second seed lights under the court's field; craning up, the field burns black and stays black (THE BURNED FIELD · NEVER FARMED). Tag: CURSED.",
              "Crane: down, then up and over the field.", ("strata labels, checklist (folded), pin", "the black field", "the court's crowd"), "Day.", "2 CURSED GROUND · never farmed", "Cut down.", "Earth 2: a side-stick march joins."),
    "relic": ("Rule 3: a stolen relic.", "A third seed; craning up, the torch leaves the statue's gilded hand and rises on a plinth on the court's side of the line (HER TORCH · ON THEIR SIDE). Tag: RELIC.",
              "Crane: down, then up to the statue and the plinth.", ("strata labels, checklist (folded), pin", "the empty hand, the torch on its plinth", "the line"), "Day.", "3 A STOLEN RELIC · kept, not returned", "Cut down.", "Earth 3: a tuba on the roots."),
    "grudge": ("Rule 4: a grudge, taught.", "A fourth seed under the valley's crowd; craning up, on 'taught' both crowds stop and turn to face the line (EVERY CHILD · FACES THE LINE); HEIRS 022. Tag: GRUDGE.",
               "Crane: down, then up and back to both crowds.", ("strata labels, checklist (folded), pin", "the crowds facing off", "the line"), "Day.", "4 A GRUDGE · taught, not lived · HEIRS 022", "Cut to the whole Isle.", "Earth 4: the theme on muted trumpet, far away."),
    "run2": ("Run with the rules: a thousand years, still here.",
             "The whole Isle in profile; YEAR 0→1000; the war layer sinks under the centuries as in run 1, but the four veins stretch with it and keep it tied to the grass; HEIRS climbs to 314: STILL HERE · 1000 YEARS · 4 LEGACIES · 314 HEIRS, stamped in verdigris.",
             "Wide profile (az 0, el 12, dist 196), craning down after the layer.", ("sim bar, stamp", "the cut side: the layer and four veins", "void"), "Day.", "STILL HERE · 1000 YEARS · 4 LEGACIES · 314 HEIRS", "Cut down to the layer.", "Drive with the theme; a stab and a cymbal on 'here'."),
    "twist": ("The locked rule: the claim. The war never ended.",
              "Today, down at the war layer in dusk: RULE 5? THE CLAIM; a pin on the layer, THE PEACE · NEVER SIGNED; LEGACIES 05. On 'never' the war's own colour floods up through all ten centuries to the grass while the camera cranes up with it to the hook frame: A PAUSE / IT NEVER ENDED, and the ruler's THE WAR turns ember.",
              "Cutaway: down at the buried layer (el 6, dist 82, fov 15), craning up 1.3 s to the hook framing.", ("kinetic, pin, strata labels", "the war flooding up through the centuries", "dusk"), "Dusk.",
              "RULE 5? THE CLAIM · THE PEACE · NEVER SIGNED · A PAUSE · IT NEVER ENDED", "Cut to the surface.", "Twist (a held A7♭9), a boom on 'peace', then the dirge."),
    "role": ("Unlock rule 5: give the ending to a character.",
             "Today, in daylight: one figure in pale cloth walks onto the line in front of the statue. The checklist opens and row 5 unlocks on 'pen': THE CLAIM · nobody signed · 5/5. The follow chip (+ FOLLOW · PART 32/50) appears after 'pen'.",
             "Cutaway (az 0, el 12, dist 108, fov 15), a slow 0.4°/s drift.", ("open checklist, follow chip", "one figure on the line", "the statue, two crowds"), "Day.", "5 THE CLAIM · nobody signed · 5/5", "The card goes full.", "Anthem from 'So'; a big D-major hit on 'pen'."),
    "lesson": ("The takeaway.", "The full card (BEFORE YOU END A WAR · THE SEAM WAR, all five rows ticked) over the whole Isle, with 'A war ends when its consequences do.' in serif italic from the end of the first sentence.",
               "Wide (az 15, el 34, dist 190), a slow 2°/s orbit: the only orbit in the episode.", ("full card, follow chip", "the island at golden hour", "stars"), "Golden hour.", "BEFORE YOU END A WAR · THE SEAM WAR · A war ends when its consequences do.", "Block wipe to the end card.", "Anthem; the World Engine chime as the card lands."),
    "cta": ("Comment CTA: invent the unfinished war.", "End card: logo, PART 32 / 50, the title, and a COMMENT panel where three idea chips pop (BORDER, RELIC, GRUDGE), then 'What did they leave you?'",
            "Cut (under the block wipe) back to the hook pose, drifting into it.", ("end card", "the Isle", "void"),
            "Golden hour (the loop frame).", "COMMENT · BORDER / RELIC / GRUDGE · What did they leave you?", "The card lifts on 'Part'.", "Outro."),
    "next": ("Say the part number, ask for the follow with a reason (part 33), open the next loop.",
             "The hook frame; PART 32/50; FOLLOW FOR PART 33, pressed on 'Follow'; NEXT RUN · 33 decodes from a locked, eclipsed sun to BELIEF · A GOD BUILT FROM FEAR. In the world, on 'fear', the sun goes dark over the Isle for a breath (an eclipse), the Queen and the Grimmaw look up, and the golden hour comes back; the hook title returns.",
             "The hook frame.", ("progress bar, follow button, next-run card", "the Isle under an eclipse", "the cut side"), "Golden hour, an eclipse on 'fear'.",
             "PART 32/50 · FOLLOW FOR PART 33 · NEXT RUN: BELIEF · A GOD BUILT FROM FEAR.", "Loop to frame 0.", "Tease over a held A, a low eclipse swell on 'fear', the engine chime on 'Follow'."),
}


def build():
    ep = {
        "id": "ep32", "number": 32, "season": 2,
        "title": "Create an Ancient War That Still Matters",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.04},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same lab host, an archaeologist this time. The hook is a puzzle, not a threat. 'Everyone moves on' is the knowing setup; 'just a date' lands dry. "
                         "The rules are crisp, two beats each. 'Nobody ever signed the peace' is the reveal, said plainly; 'So hand one character the pen' is the instruction. The comment ask is a genuine invitation.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L3", "from": "war"}, {"line": "L6", "from": "just"}, {"line": "L7", "from": "Real", "to": "Four"}, {"line": "L13", "from": "Rule", "to": "Nobody"},
                        {"line": "L14", "from": "pause."}],
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
             hit("dig", cue("L1", "thousand"), -18), hit("stompHit", cue("L1", "dying?"), -20),
             hit("cardSlide", cue("L2", "Meet", -0.05), -18), hit("check", cue("L2", "truce."), -20)],
    "setup": [hit("rewind", RESET, -15), hit("stamp", cue("L3", "everyone"), -19),
              hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "Forgotten.", 0.2), -22), bed("rumble", cue("L4", "run.", 0.3), cue("L5", "Forgotten.", 0.3), -19),
             hit("dig", cue("L5", "centuries"), -17), hit("dig", cue("L5", "sinks."), -17), hit("crownPass", cue("L5", "Forgotten."), -18)],
    "drop": [hit("stamp", cue("L6", "just"), -10)],
    "rehook": [hit("rewind", cue("L6", "date.", 0.5), -11), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "border": [hit("check", cue("L8", "border."), -13), hit("dig", cue("L8", "border."), -15), bed("stomp", cue("L8", "truce"), cue("L8", "statue.", 0.1), -26), hit("stones", cue("L8", "line"), -13)],
    "curse": [hit("check", cue("L9", "cursed"), -13), hit("dig", cue("L9", "cursed"), -15), bed("burn", cue("L9", "cursed", -0.1), cue("L9", "field.", 0.3), -20)],
    "relic": [hit("check", cue("L10", "stolen"), -13), hit("dig", cue("L10", "stolen"), -15), hit("delete", cue("L10", "court"), -19), hit("restore", cue("L10", "keeps"), -16)],
    "grudge": [hit("check", cue("L11", "grudge."), -13), hit("dig", cue("L11", "grudge."), -15), hit("stompHit", cue("L11", "taught"), -18), hit("frameDrum", cue("L11", "hate."), -18)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L12", "here."), -22),
             bed("rumble", cue("L12", "Run", 0.3), cue("L12", "here.", 0.1), -20), hit("stamp", cue("L12", "here."), -13)],
    "twist": [hit("dig", TWIST, -16), hit("unlock", cue("L13", "claim."), -14), hit("stamp", cue("L13", "Nobody", 0.0), -15),
              bed("rumble", FLOOD, cue("L14", "ended.", 0.4), -17), hit("eyeOn", cue("L14", "never"), -15)],
    "role": [hit("restore", ROLE, -17), hit("cardSlide", cue("L15", "character", 0.1), -19), hit("unlock", cue("L15", "pen.", -0.1), -10)],
    "lesson": [hit("engineWind", cue("L16", "Fighting", -0.8), -15), hit("chime", cue("L16", "Fighting", -0.3), -10), hit("cardSlide", cue("L16", "Fighting", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("check", cue("L17", "unresolved"), -17), hit("check", cue("L17", "conflict"), -17), hit("check", cue("L17", "your"), -17)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11), hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "33:", -0.1), -18), hit("unlock", cue("L18", "god"), -15),
             hit("eclipse", cue("L18", "fear.", -0.25), -14),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score: the series theme stays (D minor for the problem, D major for the payoff). EP32's band is `dirge` (the theme
# at half speed on low horns over a muffled march drum and a snare roll: a march slowed to a dirge) wherever the war is
# felt today, and `earth` (a taiko heartbeat, a distant side-stick march, a tuba, the theme on muted trumpet: war drums
# heard through the ground), one family per rule.
EARTH_P = {"horns": 58, "lead": 59}
DIRGE_P = {"horns": 60}
BACK_P = {"lead": 73, "horns": 60}
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 92,
    "sections": [
        msec({"shot": "hook"}, "dirge", ["Dm", "Bb", "Gm", "A"], "D minor", programs=DIRGE_P),
        msec(RESET, "earth", ["Dm", "Bb", "F", "C"], "D minor", layer=1, programs=EARTH_P),
        msec(cue("L4", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.85, programs=BACK_P),
        msec(cue("L6", "A", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "date.", 0.5), "mystery", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=2),
        msec(cue("L8", "One:", -0.1), "earth", ["Dm", "C", "Bb", "C"], "D minor", layer=1, programs=EARTH_P),
        msec(cue("L9", "Two:", -0.1), "earth", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "earth", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L11", "Four:", -0.1), "earth", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True, programs=BACK_P),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(cue("L14", "That", -0.1), "dirge", ["Dm", "Bb", "Gm", "A"], "D minor", beatsPerChord=2, programs=DIRGE_P),
        msec(cue("L15", "So", -0.1), "anthem", ["D", "G", "Bm", "A"], "D major", programs=BACK_P),
        msec(cue("L17", "What", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "dying?"), "chord": "Dm"},
        {"kind": "boom", "at": cue("L6", "date."), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "here."), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "here.")},
        {"kind": "boom", "at": cue("L13", "peace."), "chord": "Dm"},
        {"kind": "hit", "at": cue("L15", "pen."), "chord": "D"},
        {"kind": "boom", "at": cue("L18", "fear."), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #WritingTips #Lore #WorldcraftShorts"
IG_HOOK = "The war ended 1000 years ago. Nobody signed the peace."
BODY = (
    "This war ended a thousand years ago. Why are people still dying?\n\n"
    "Meet the Seam War. It ended in one truce. The lazy version lets the war end and everyone move on, and we ran it: "
    "ten centuries pile on, the war sinks, forgotten. A war nobody feels is just a date.\n\n"
    "Real wars don't stay buried. A border: the truce line still splits the statue. Cursed ground: nobody farms the "
    "burned field. A stolen relic: the court kept her torch. A grudge: children are taught who to hate. Run it again: "
    "a thousand years, still here.\n\n"
    "Then the twist: the claim. Nobody ever signed the peace. That truce was a pause, and the war never ended. So hand "
    "one character the pen.\n\n"
    "Fighting stops in a day. A war ends when its consequences do.\n\n"
    "What unresolved conflict would your ancestors leave behind?\n\n"
    "Part 32 of 50. Follow for part 33: a god built from fear."
)
METADATA = {
    "youtube": {
        "title": "Create an Ancient War That Still Matters (Worldbuilding)",
        "titleAlternate": "The war ended 1000 years ago. Nobody signed the peace.",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 7: History and Mythology.\n\n" + TAGS,
        "pinnedComment": "What unresolved conflict would your ancestors leave behind? A border, a relic, a grudge, or something worse? (Part 33: a god built from fear.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated field-card sprite; the island, statue, people, stones and strata are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "The war ended 1000 years ago. So why is it still here? ⚔️ Four things an old war leaves behind, and rule #5 is the one writers skip. "
                   "What would your ancestors leave you? Part 32/50 · follow for part 33 🌑 " + TAGS,
        "pinnedComment": "What unresolved conflict would your ancestors leave behind?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "Which old war in your world is still being fought by people who never saw it?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": IG_HOOK + "\n\n" + BODY + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": f"First {len(IG_HOOK)} characters: '{IG_HOOK}'",
        "pinnedComment": "Save the DIG IT UP card, then tell us: what unresolved conflict would your ancestors leave behind?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep32] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots, loop span {loop_span():.2f} s")
