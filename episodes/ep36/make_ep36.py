"""Generate episodes/ep36/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep36/make_ep36.py
EP36 opens Arc 8 (Conflict and Warfare): "Wars Need More Than Two Armies". It closes EP35's loop (on "two armies are
never enough" three small standards, red, blue and gold, were planted round the Builders' ruin for a breath, then
sank): frame 0 has them standing for good, three sides camped round the ruin, each wanting it for its own reason.

Its own device is THE WAR ROOM'S THREADS: every reason a side has for war is a coloured thread pinned from its camp to
what it wants, and the war starts where the threads meet, a knot on a tall war pin stuck in the ruin (flashpoint
lime). Under the world, the war room strip lists each side's reasons and its verdict (WORTH IT?). The lazy version is
two armies and one angry king: one thread (anger), and after ten years of shouting nobody marches. The rules pin one
thread each: something to gain (Red needs the ruin's harbour), fear (Blue can't let Red hold it), a claim (Gold's
prince says it's his by birth) and allies (Blue swore to stand with Gold, a thread braided blue and gold). The twist
is the miscalculation: nobody wants this war, every side is sure the others will blink, the threads pull taut and the
knot catches. No one fights on screen; the war never starts on camera.
Camera language: THE PULL-BACK. Every beat starts close on one thing and the camera backs away along its own line of
sight (the target fixed, the distance growing) to reveal what that thing is tied to: a camp, then its thread, then the
knot, then the other sides. It never pushes in; a closer view is always a cut (EP26 orbited, EP27 rode a dragon, EP28
sat at eye height, EP29 was a locked-off tripod, EP30 looked up, EP31 split the frame, EP32 craned, EP33 looked down
at a map table, EP34 dolly-zoomed, EP35 tracked sideways).
Motif colour: flashpoint lime #c8f04a (the knot, the war room's frame, flashpoints). Music band: `council` (the war room
at night: a ticking clock, taut threads plucked, the theme on a muted trumpet over harpsichord) and `muster` (the
armies gathering, one family per rule: field snare, tuba, timpani, the theme on a fife).
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep36" / "timing.json"
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
    ("L1", "hook", "Nobody sends a million soldiers to die for an angry king.", 0.3, ["million", "angry"]),
    ("L2", "hook", "Meet the Ruin War. It hasn't started yet.", 0.3, ["ruin", "yet."]),
    ("L3", "setup", "The lazy version: two armies, one angry king.", 0.25, ["lazy", "angry"]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "Ten years of shouting. Nobody marches.", 0.35, ["shouting.", "marches."]),
    ("L6", "drop", "One angry king is a tantrum, not a war.", 0.4, ["tantrum,", "war."]),
    ("L7", "rehook", "Real wars need reasons on every side. Four rules. The fifth is the twist.", 0.25, ["reasons.", "twist."]),
    ("L8", "gain", "One: something to gain. Red needs the ruin's harbour.", 0.25, ["gain.", "harbour."]),
    ("L9", "fear", "Two: fear. Blue can't let Red hold it.", 0.25, ["fear.", "hold"]),
    ("L10", "claim", "Three: a claim. Gold's prince says it's his by birth.", 0.25, ["claim.", "birth."]),
    ("L11", "allies", "Four: allies. Blue swore to stand with Gold.", 0.3, ["allies.", "swore"]),
    ("L12", "run2", "Run it again. Ten years. Three armies, one ruin.", 0.35, ["three", "ruin."]),
    ("L13", "twist", "Rule five? Nobody here wants this war.", 0.3, ["nobody", "wants"]),
    ("L14", "twist", "Each side is sure the others will blink. All three are wrong.", 0.4, ["blink.", "wrong."]),
    ("L15", "role", "So give every side a reason worth the cost.", 0.4, ["every", "cost."]),
    ("L16", "lesson", "Show what each side wants. Nobody thinks they're the villain.", 0.35, ["wants.", "villain."]),
    ("L17", "cta", "What would finally push your kingdom into war?", 0.25, ["push", "war?"]),
    ("L18", "next", "Part 36 of 50. Follow for part 37: big armies still lose.", 0.25, ["follow", "lose."]),
]
SHOTS = ["hook", "setup", "run1", "drop", "rehook", "gain", "fear", "claim", "allies", "run2", "twist", "role", "lesson", "cta", "next"]

# The block wipe into the end card: the world resets to frame 0 under it (the full web, every side camped).
WIPE = cue("L17", "What", -0.3)
RESET = cue("L3", "lazy", -0.15)          # the lazy version: two armies, one angry king (one thread)
REWIND = cue("L6", "war.", 0.6)           # three camps, no threads yet
RULES = cue("L8", "One:", -0.1)
RUN2 = cue("L12", "Run", -0.05)
TWIST = cue("L13", "Rule", -0.1)
SURE = cue("L14", "sure", -0.05)          # every thread pulls taut: each side is sure the others will blink
WRONG = cue("L14", "wrong.", -0.05)       # the knot catches
ROLE = cue("L15", "So", -0.15)
END = {"end": True}

# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle (it remembers): EP27's valley village and watchtower (west), the cairn (east of the lake),
# EP29's Queen on her dais, EP30's Grimmaw (north-east), EP31's split statue and EP32's boundary stones and relic
# (south-east), EP33's Lamplight faith (candles at the cairn, boats with lamps, the sheaves) and its crack of light,
# EP34's giant's bones and its pillars, and EP35's Builders' wall with its finds (the ruin everyone wants).
# EP34's painted sky is not over the Isle; EP28's Fenn hall stays out. The valley's crowd has gone to the camps.
CAIRN = (8.95, -5.38)
HUMAN_B = [("hall", (-3.6, -4.6)), ("house", (-1.8, -2.4)), ("house", (-4.8, -2.4)), ("house", (-1.0, -5.8)),
           ("house", (-5.6, -0.9)), ("house", (-3.4, -0.7)), ("house", (0.4, -4.2))]
HUMAN_TOWER = (-6.4, -5.6)
HUMAN_ROAD = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
DAIS = (9.4, -2.2)
QUEEN = (9.1, -2.2)
G_NOW = (13.0, -10.5)
STATUE = (18.0, 1.5)
LINE_A, LINE_B = (18.0, -7.0), (18.0, 8.3)
RELIC = (20.3, 5.4)
LAKE = (6.5, 4.5)
FIELD = (3.0, -11.0, 4.0, 3.4)
RIFT_A, RIFT_B = (-0.5, 10.6), (12.0, 8.8)
BONES = (6.5, 12.2)
BONES_FACE = 8.2
PILLARS = (12.8, 13.4)
WALL_A, WALL_B = (0.6, 14.6), (10.2, 14.6)
PROFILE = [3, 5, 6, 7, 6, 4, 6, 7, 5, 2, 4, 3]
FRESH = [6, 5]
TONIGHT = [7, 6]
COLX = lambda i: WALL_A[0] + (WALL_B[0] - WALL_A[0]) / len(PROFILE) * (i + 0.5)
GEAR = (1.5, 16.0)
KITCHEN = (3.9, 16.6)
WELLS = (6.5, 15.8)
HANDS = (COLX(10), WALL_A[1] + 0.47)

# EP36: three sides camped round the ruin, the knot on its war pin in the ruin's middle.
RED, BLUE, GOLD = "#c0573c", "#4f7fbf", "#d4b23f"
FLASH = "#c8f04a"
HUB = (5.4, 14.6)                   # the knot: the war pin stuck through the Builders' wall
KNOT_Y = 4.6                        # the knot's height above the ground
C_RED = (-1.2, 12.4)
C_BLUE = (12.2, 10.8)
C_GOLD = (4.8, 18.4)
TOWARD = lambda c, d: (c[0] + (HUB[0] - c[0]) * d / math.dist(c, HUB), c[1] + (HUB[1] - c[1]) * d / math.dist(c, HUB))
PIN = {k: TOWARD(c, 1.0) for k, c in (("r", C_RED), ("b", C_BLUE), ("g", C_GOLD))}   # where each side's threads start
STD = {k: TOWARD(c, -0.4) for k, c in (("r", C_RED), ("b", C_BLUE), ("g", C_GOLD))}  # each side's standard
THREAD_Y = 2.2
ARMY = [TOWARD(C_RED, 2.6), TOWARD(C_BLUE, 2.6), TOWARD(C_GOLD, 2.4)]               # the crowds, in front of the tents
TEASE = (9.4, 9.8)                # EP37's tease: one far bigger standard, north of the ruin (low left in the hook frame)


def shift(c, d):
    """The same cue, `d` seconds later."""
    return {**c, "offset": round(c.get("offset", 0.0) + d, 3)}


def jump(at, before, after):
    """A hard change of value on a cut: hold `before` until just before the cue, then step to `after`."""
    return [[shift(at, -0.02), before], [at, after, "step"]]


def cam(at, az, el, dist, target, fov=24, dur=1.4, drift=0.0, cut=False):
    c = {"at": at, "az": az, "el": el, "dist": round(dist, 3), "target": [round(v, 3) for v in target], "fov": fov, "dur": round(dur, 3), "drift": drift}
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
    if c.get("end"):
        return tm["duration"] + c.get("offset", 0.0)
    ln = next(l for l in tm["lines"] if l["id"] == c["line"])
    hits = [w for w in ln["words"] if w["text"].strip(".,?!:").lower() == c["word"].strip(".,?!:").lower()]
    return hits[c.get("nth", 1) - 1]["start"] + c.get("offset", 0.0)


def loop_span():
    """Seconds from the wipe to the end: the loop camera key pulls back this long and lands exactly on the hook pose."""
    if not TIMING.exists():
        return 6.0
    return tcue(END) - tcue(WIPE)


# ---- the pull-back. A pose is a target, an azimuth, an elevation and `h`, the frame's half-height at the target
# (dist = h / tan(fov / 2)). `back(p, k)` is the same line of sight with the camera k times as far away: every move
# in the episode is one of these (or a cut to a closer pose).
def dist_for(h, fov):
    return h / math.tan(math.radians(fov / 2))


def pose(target, az, el, h, fov=20):
    return dict(target=target, az=az, el=el, h=h, fov=fov)


def back(p, k):
    return dict(p, h=p["h"] * k)


def facing(frm, to):
    """The azimuth of a camera standing behind `frm`, looking toward `to` (so the thread runs away from the lens)."""
    return math.degrees(math.atan2(frm[0] - to[0], frm[1] - to[1]))


# Poses (planned with pipeline/camprobe.ts; BRIEF.md §6).
def along(c, f=0.3, y=6.0):
    """A point `f` of the way from side `c`'s pin to the knot (the rule poses' target)."""
    p = PIN[c]
    return (p[0] + (HUB[0] - p[0]) * f, y, p[1] + (HUB[1] - p[1]) * f)


HOOK_POSE = pose(*json.loads(os.environ["HOOK"])) if os.environ.get("HOOK") else pose((5.2, 7.2, 15.0), 170, 34, 9.5)
HOOK_BACK = 1.08                                   # the hook pulls back this much while the title holds
WIDE = pose((4.0, 2.0, 6.0), 170, 32, 31.0, 22)    # the whole Isle (dist 160)
RULE_BACK = 2.3                                    # every rule pulls back this far: from a pin to its knot
P_LAZY = pose((PIN["r"][0] + (PIN["b"][0] - PIN["r"][0]) * 0.3, 6.0, PIN["r"][1] + (PIN["b"][1] - PIN["r"][1]) * 0.3), facing(C_RED, C_BLUE) + 15, 30, 6.5)
P_RED = pose(along("r"), facing(C_RED, HUB) + 60, 34, 6.0)
P_BLUE = pose(along("b"), facing(C_BLUE, HUB) - 45, 34, 6.0)
P_GOLD = pose(along("g"), facing(C_GOLD, HUB) + 60, 34, 6.0)
P_ALLY = pose(((PIN["b"][0] + PIN["g"][0]) / 2, 6.0, (PIN["b"][1] + PIN["g"][1]) / 2), 350, 32, 6.0)
P_KNOT = pose((HUB[0], 4.0 + KNOT_Y - 0.6, HUB[1]), 170, 22, 5.0)


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    lin = lambda at, v: [at, v, "linear"]
    H = shot("hook")
    span = loop_span()

    # ---- the clock: YEAR of the standoff. Frame 0 is year 10 (after run 2); each run is ten years.
    R1A, R1B = cue("L4", "run.", 0.3), cue("L5", "marches.", 0.2)
    R2A, R2B = cue("L12", "Run", 0.25), cue("L12", "ruin.", 0.1)
    clock = [[H, 10], *jump(RESET, 10, 0), [R1A, 0], lin(R1B, 10), *jump(REWIND, 10, 0), [R2A, 0], lin(R2B, 10), [WIPE, 10]]
    speed = [[H, 1], [cue("L4", "run."), 1], [R1A, 5], [R1B, 5], [cue("L6", "One"), 1],
             [R2A, 1], [cue("L12", "Run", 0.5), 5], [R2B, 5], [cue("L13", "Rule"), 1]]

    # ---- rule cues: each thread is pinned on its spoken word
    T_RED = cue("L8", "harbour.", -0.2)
    T_BLUE = cue("L9", "Red", -0.1)
    T_GOLD = cue("L10", "prince", -0.1)
    T_ALLY = cue("L11", "swore", -0.1)
    T_ANGER = cue("L3", "angry", -0.1)
    QUIT = cue("L5", "Nobody", -0.1)        # run 1: the camps strike, the anger thread goes slack and reels back

    # ---- the HUD: armies in the field and the reasons pinned
    armies = [[H, 3], *jump(RESET, 3, 2), [QUIT, 2], lin(shift(QUIT, 0.5), 1), lin(shift(QUIT, 1.0), 0), *jump(REWIND, 0, 3), [WIPE, 3]]
    reasons = [[H, 4], *jump(RESET, 4, 0), *jump(T_ANGER, 0, 1), *jump(shift(QUIT, 0.8), 1, 0), [REWIND, 0],
               *jump(T_RED, 0, 1), *jump(T_BLUE, 1, 2), *jump(T_GOLD, 2, 3), *jump(T_ALLY, 3, 4), [WIPE, 4]]

    # ---- threads: frame 0 has the whole web; the lazy version has only anger; each rule draws one
    def drawn(at, dur=0.7):
        return [[H, 1], *jump(RESET, 1, 0), [at, 0], lin(shift(at, dur), 1), [WIPE, 1]]
    taut = [[H, 0], [SURE, 0], lin(shift(SURE, 0.9), 1), [ROLE, 1], lin(shift(ROLE, 0.8), 0), [WIPE, 0]]
    anger = [[H, 0], [T_ANGER, 0], lin(shift(T_ANGER, 0.7), 1), [QUIT, 1], lin(shift(QUIT, 0.9), 0), [WIPE, 0]]
    knot_rise = [[H, 1], *jump(RESET, 1, 0), [shift(T_RED, -0.3), 0], lin(shift(T_RED, 0.2), 1), [WIPE, 1]]
    flare = [[H, 0], [TWIST, 0], lin(shift(TWIST, 0.6), 0.25), [WRONG, 0.25], lin(shift(WRONG, 0.3), 1), [ROLE, 1], lin(shift(ROLE, 0.6), 0.0), [WIPE, 0]]
    # ---- camps and armies: the lazy version has Red and Blue only; in run 1 both strike camp and go home
    camp_rg = lambda first: [[H, 1], *jump(RESET, 1, 1), [shift(QUIT, first), 1], lin(shift(QUIT, first + 0.6), 0), *jump(REWIND, 0, 1), [WIPE, 1]]
    camp_gold = [[H, 1], *jump(RESET, 1, 0), *jump(REWIND, 0, 1), [WIPE, 1]]
    side_rb = lambda first: [[H, 1], [shift(QUIT, first), 1], lin(shift(QUIT, first + 0.8), 0), *jump(REWIND, 0, 1), [WIPE, 1]]
    side_gold = [[H, 1], *jump(RESET, 1, 0), *jump(REWIND, 0, 1), [WIPE, 1]]
    advance = [[H, 1], *jump(RESET, 1, 0), [cue("L12", "Three", -0.3), 0], lin(cue("L12", "ruin.", 0.2), 1), [WIPE, 1]]
    # EP37's tease: one standard many times bigger rises on "army" and sinks before the hook title returns
    tease = [[H, 0], [cue("L18", "armies", -0.15), 0], [cue("L18", "still", 0.0), 1, "out"], [cue("L18", "lose.", 0.4), 1], [cue("L18", "lose.", 0.85), 0]]

    rift = [[H, 1]]
    fears = [{"id": "rift", "x": RIFT_A[0], "z": RIFT_A[1], "r": 0.0, "kind": "rift", "to": list(RIFT_B), "dark": rift}]
    dust = [{"at": shift(T_RED, 0.1), "x": PIN["r"][0], "z": PIN["r"][1], "r": 0.9}, {"at": shift(T_BLUE, 0.1), "x": PIN["b"][0], "z": PIN["b"][1], "r": 0.9},
            {"at": shift(T_GOLD, 0.1), "x": PIN["g"][0], "z": PIN["g"][1], "r": 0.9}, {"at": shift(T_RED, 0.2), "x": HUB[0], "z": HUB[1] + 0.8, "r": 1.4}]
    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run")]
    rings = [{"x": HUB[0], "z": HUB[1], "r": 3.2, "on": WRONG, "off": ROLE, "color": FLASH}]
    bells = [cue("L18", "armies")]

    ruler = [pk(H, *QUEEN, "idle", face=0), pk(cue("L18", "armies"), *QUEEN, "alert", face=0), pk(cue("L18", "lose.", 0.6), *QUEEN, "idle", face=0)]
    g_now = [pk(H, *G_NOW, "idle", face=160)]

    # Camera language: the pull-back. Every key either cuts to a closer pose or backs away along its line of sight.
    def k(at, p, dur=1.2, cut=False):
        return cam(at, round(p["az"], 2), p["el"], dist_for(p["h"], p["fov"]), p["target"], fov=p["fov"], dur=dur, cut=cut)
    LESSON_AT = cue("L16", "Show", -0.25)
    camera = [
        k(H, HOOK_POSE),
        k(shot("hook", 0.02), back(HOOK_POSE, HOOK_BACK), dur=(tcue(cue("L2", "Meet")) or 4.0)),
        k(cue("L2", "Meet"), back(HOOK_POSE, HOOK_BACK * 1.12), dur=2.4),
        # the lazy version: close on Red's camp, pulling back to reveal Blue across the anger thread
        k(RESET, P_LAZY, cut=True),
        k(shift(RESET, 0.02), back(P_LAZY, 2.2), dur=3.0),
        # run 1: the whole Isle, backing away as the years pass
        k(cue("L4", "run.", 0.05), back(WIDE, 0.86), cut=True),
        k(cue("L4", "run.", 0.07), back(WIDE, 1.0), dur=3.4),
        k(cue("L6", "One", -0.2), back(WIDE, 1.06), dur=2.2),
        k(REWIND, back(WIDE, 0.84), cut=True),
        k(shift(REWIND, 0.02), back(WIDE, 0.96), dur=3.0),
        # the rules: close on each camp, pulling back along its thread to the knot
        k(RULES, P_RED, cut=True),
        k(shift(RULES, 0.02), back(P_RED, RULE_BACK), dur=2.8),
        k(cue("L9", "Two:", -0.1), P_BLUE, cut=True),
        k(cue("L9", "Two:", -0.08), back(P_BLUE, RULE_BACK), dur=2.4),
        k(cue("L10", "Three:", -0.1), P_GOLD, cut=True),
        k(cue("L10", "Three:", -0.08), back(P_GOLD, RULE_BACK), dur=2.8),
        k(cue("L11", "Four:", -0.1), P_ALLY, cut=True),
        k(cue("L11", "Four:", -0.08), back(P_ALLY, 2.2), dur=2.6),
        # run 2: the whole Isle, backing away as the armies march up and stand
        k(RUN2, back(WIDE, 0.84), cut=True),
        k(shift(RUN2, 0.02), back(WIDE, 1.0), dur=3.6),
        # the twist: close on the knot at dusk, backing away as the threads pull taut, then a long pull-back as it catches
        k(TWIST, P_KNOT, cut=True),
        k(shift(TWIST, 0.02), back(P_KNOT, 1.5), dur=2.4),
        k(SURE, back(P_KNOT, 1.9), dur=1.6),
        k(WRONG, back(P_KNOT, 3.0), dur=1.8),
        k(ROLE, back(HOOK_POSE, 0.9), cut=True),
        k(shift(ROLE, 0.02), back(HOOK_POSE, 1.1), dur=2.0),
        # the lesson: the whole Isle in golden light, one slow pull-back
        k(LESSON_AT, back(WIDE, 0.86), cut=True),
        k(shift(LESSON_AT, 0.02), back(WIDE, 1.0), dur=3.2),
        # the loop: cut under the wipe to a closer view, then pull back so it lands exactly on frame 0's pose
        k(WIPE, back(HOOK_POSE, 0.88), cut=True),
        k(shift(WIPE, 0.02), HOOK_POSE, dur=span - 0.02),
    ]
    if SCOUT:
        camera = [k(H, WIDE)]
    light = [
        {"at": H, "mood": "golden"},
        {"at": RESET, "mood": "day", "dur": 0.4},
        {"at": cue("L6", "One", -0.2), "mood": "gloom", "dur": 0.6},
        {"at": REWIND, "mood": "day", "dur": 0.3},
        {"at": TWIST, "mood": "dusk", "dur": 0.6},
        {"at": ROLE, "mood": "day", "dur": 0.5},
        {"at": cue("L16", "Show", -0.3), "mood": "golden", "dur": 1.4},
    ]
    human_valley = {
        "buildings": [{"kind": kk, "a": list(a), "face": 0} for kk, a in HUMAN_B],
        "roof": [[H, 1]], "pens": [{"a": [-6.4, -1.4], "r": 1.6}], "cover": [[H, 1]],
        "roads": {"b": HUMAN_ROAD}, "route": [[H, 1]], "tradeKey": "tradeH", "lanterns": [[H, 0]],
        "tower": {"x": HUMAN_TOWER[0], "z": HUMAN_TOWER[1], "h": 6.0, "keys": [[H, 1]], "rings": bells},
    }
    clear = [BONES, (BONES[0] - 4, BONES[1]), (BONES[0] + 4, BONES[1] - 0.5), CAIRN, (FIELD[0], FIELD[1]), PILLARS, HUB,
             GEAR, KITCHEN, WELLS, *[(COLX(i), WALL_A[1]) for i in range(len(PROFILE))],
             *[(c[0] + dx, c[1] + dz) for c in (C_RED, C_BLUE, C_GOLD) for dx in (-1.6, 0, 1.6) for dz in (-1.6, 0, 1.6)],
             *PIN.values(), *STD.values(), *ARMY, TEASE]
    lane = lambda a, b: [[a[0] + (b[0] - a[0]) * kk / 8, a[1] + (b[1] - a[1]) * kk / 8, 1.6] for kk in range(9)]
    thread_lanes = lane(PIN["r"], HUB) + lane(PIN["b"], HUB) + lane(PIN["g"], HUB) + lane(PIN["b"], PIN["g"]) + lane(PIN["r"], PIN["b"])
    rift_lane = [[RIFT_A[0] + (RIFT_B[0] - RIFT_A[0]) * kk / 8, RIFT_A[1] + (RIFT_B[1] - RIFT_A[1]) * kk / 8 + dz, 2.2] for kk in range(9) for dz in (0.0, 2.6)]
    hub_xz = list(HUB)

    def thread(frm, to, color, draw, color2=None, y1=KNOT_Y, sag=1.3):
        t = {"kind": "thread", "x": frm[0], "z": frm[1], "to": list(to), "y0": THREAD_Y, "y1": y1, "color": color, "draw": draw, "taut": taut, "sag": sag}
        if color2:
            t["color2"] = color2
        return t
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": [[H, 24]], "max": 30, "base": 24, "centers": [[-9.5, -1.0], [-8.4, 1.2]], "skin": "sheep"},
        "pred": [[H, 1]],
        "predators": [{"id": "g1", "scale": 1.3, "keys": g_now, "adorn": True}],
        "series": {"armies": armies, "reasons": reasons, "tradeH": [[H, 4]]},
        "settlement": human_valley,
        "people": {"count": [[H, 36], [WIPE, 36]], "centers": ARMY, "spread": 1.3, "life": 70, "tints": [RED, BLUE, GOLD],
                   "sideShow": [side_rb(0.0), side_rb(0.35), side_gold],
                   "advance": {"at": hub_xz, "f": 0.3, "keys": advance}, "watch": hub_xz, "watchOn": [[H, 1], *jump(RESET, 1, 0), [cue("L12", "Three", -0.3), 0], [cue("L12", "Three", -0.28), 1, "step"], [WIPE, 1]],
                   "ruler": {"keys": ruler, "dais": {"x": DAIS[0], "z": DAIS[1], "face": 0}}},
        "fields": {"plots": [{"x": FIELD[0], "z": FIELD[1], "w": FIELD[2], "d": FIELD[3]}], "ripe": [[H, 1]]},
        "props": [{"kind": "cairn", "x": CAIRN[0], "z": CAIRN[1], "stones": [[H, 3]]},
                  {"kind": "offerings", "x": CAIRN[0], "z": CAIRN[1], "r": 1.7, "lights": [[H, 1]]},
                  {"kind": "lanterns", "x": LAKE[0], "z": LAKE[1], "r": 3.8, "n": 9, "lights": [[H, 1]]},
                  {"kind": "sheaves", "x": FIELD[0], "z": FIELD[1], "r": 2.7, "n": 8, "sheaves": [[H, 8]]},
                  {"kind": "statue", "x": STATUE[0], "z": STATUE[1], "face": -90, "rise": [[H, 1]], "gild": [[H, 1]], "tar": [[H, 1]], "grow": [[H, 1.35]], "torch": [[H, 0]]},
                  {"kind": "border", "x": LINE_A[0], "z": LINE_A[1], "to": list(LINE_B), "skip": [0.46, 0.65], "rise": [[H, 1]]},
                  {"kind": "relic", "x": RELIC[0], "z": RELIC[1], "face": -90, "rise": [[H, 1]]},
                  {"kind": "bones", "x": BONES[0], "z": BONES[1], "face": BONES_FACE, "r": 1.7, "rise": [[H, 1]]},
                  {"kind": "ruin", "x": PILLARS[0], "z": PILLARS[1], "face": 20, "r": 2.2, "rise": [[H, 1]]},
                  {"kind": "wall", "x": WALL_A[0], "z": WALL_A[1], "to": list(WALL_B), "profile": PROFILE, "fresh": FRESH, "tonight": TONIGHT,
                   "log": [[H, 0]], "glow": [[H, 0]], "place": [[H, 1]]},
                  {"kind": "find", "find": "gear", "x": GEAR[0], "z": GEAR[1], "face": 0, "r": 2.2, "rise": [[H, 1]]},
                  {"kind": "find", "find": "kitchen", "x": KITCHEN[0], "z": KITCHEN[1], "face": 0, "r": 2.2, "rise": [[H, 1]]},
                  {"kind": "find", "find": "wells", "x": WELLS[0], "z": WELLS[1], "face": 0, "r": 2.2, "rise": [[H, 1]]},
                  {"kind": "find", "find": "hands", "x": HANDS[0], "z": HANDS[1], "face": 0, "r": 2.2, "y": 0.8, "rise": [[H, 1]]},
                  # the three camps and their standards (plain single colours, no device)
                  {"kind": "camp", "x": C_RED[0], "z": C_RED[1], "face": 0, "color": RED, "n": 3, "r": 2.2, "rise": camp_rg(0.0)},
                  {"kind": "camp", "x": C_BLUE[0], "z": C_BLUE[1], "face": 40, "color": BLUE, "n": 3, "r": 2.2, "rise": camp_rg(0.35)},
                  {"kind": "camp", "x": C_GOLD[0], "z": C_GOLD[1], "face": 200, "color": GOLD, "n": 3, "r": 2.2, "rise": camp_gold},
                  {"kind": "standard", "x": STD["r"][0], "z": STD["r"][1], "face": 90, "color": RED, "size": 0.62, "loop": True, "rise": camp_rg(0.0)},
                  {"kind": "standard", "x": STD["b"][0], "z": STD["b"][1], "face": 90, "color": BLUE, "size": 0.62, "loop": True, "rise": camp_rg(0.35)},
                  {"kind": "standard", "x": STD["g"][0], "z": STD["g"][1], "face": 90, "color": GOLD, "size": 0.62, "loop": True, "rise": camp_gold},
                  # the war room's threads, and the knot where they meet
                  {"kind": "knot", "x": HUB[0], "z": HUB[1], "y": KNOT_Y, "rise": knot_rise, "flare": flare},
                  thread(PIN["r"], HUB, RED, drawn(T_RED)),
                  thread(PIN["b"], HUB, BLUE, drawn(T_BLUE)),
                  thread(PIN["g"], HUB, GOLD, drawn(T_GOLD)),
                  thread(PIN["b"], PIN["g"], BLUE, drawn(T_ALLY, 0.9), color2=GOLD, y1=THREAD_Y, sag=1.6),
                  {"kind": "thread", "x": PIN["r"][0], "z": PIN["r"][1], "to": list(PIN["b"]), "y0": THREAD_Y, "y1": THREAD_Y, "color": RED, "draw": anger, "taut": [[H, 0]], "sag": 2.2},
                  # EP37's tease: an army ten times bigger, one standard over everything
                  {"kind": "standard", "x": TEASE[0], "z": TEASE[1], "face": -90, "color": "#8f98a6", "size": 1.25, "rise": tease}],
        "fears": fears,
        "clearTrees": [[d[0], d[1], 2.2] for d in clear] + rift_lane + thread_lanes,
        "layers": {"ripple": ripple, "rings": rings, "dust": dust},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "GAIN", "text": "a harbour to take", "at": cue("L8", "gain.")},
    {"n": 2, "label": "FEAR", "text": "can't let them win", "at": cue("L9", "fear.")},
    {"n": 3, "label": "A CLAIM", "text": "his by birth", "at": cue("L10", "claim.")},
    {"n": 4, "label": "ALLIES", "text": "a promise to keep", "at": cue("L11", "allies.")},
    {"n": 5, "label": "A GUESS", "text": "they'll back down", "at": cue("L7", "Four"), "locked": True, "unlockAt": cue("L15", "cost.", -0.1)},
]
SPRITE = {"sprite": "ep36/war_sprite.png", "spriteW": 64, "spriteH": 116}


def tag(text, head, at, end, pos, color, lift=90, dx=0, **kw):
    return {"kind": "ground", "text": text, "head": head, "at": at, "end": end, "pos": list(pos), "lift": lift, "dx": dx, "color": color, "headColor": color, **kw}


def side(name, color, rows, verdicts, show=None):
    s = {"name": name, "color": color, "rows": rows, "verdicts": verdicts}
    if show:
        s["show"] = show
    return s


def war_room():
    blink = lambda: {"icon": "spark", "text": "they'll blink", "at": cue("L14", "sure"), "end": ROLE, "strikeAt": cue("L14", "wrong."), "color": FLASH}
    q = {"at": RESET, "text": "WORTH IT?", "color": "rgba(239,230,210,0.55)"}
    no = {"at": cue("L5", "Nobody"), "text": "NOT WORTH IT", "color": "rust"}
    q2 = {"at": REWIND, "text": "WORTH IT?", "color": "rgba(239,230,210,0.55)"}
    wrong = {"at": cue("L14", "wrong."), "text": "GUESSED WRONG", "color": "rust"}
    back_ = lambda c: {"at": ROLE, "text": "WORTH IT", "color": c}
    sides = [
        side("RED", RED, [{"icon": "fume", "text": "the king is angry", "at": cue("L3", "angry"), "end": REWIND, "color": "parchment"},
                          {"icon": "anchor", "text": "a harbour to take", "at": cue("L8", "harbour.")}, blink()],
             [q, no, q2, {"at": cue("L8", "harbour."), "text": "WORTH IT", "color": RED}, wrong, back_(RED)]),
        side("BLUE", BLUE, [{"icon": "shield", "text": "can't let Red win", "at": cue("L9", "hold")},
                            {"icon": "clasp", "text": "sworn to Gold", "at": cue("L11", "swore")}, blink()],
             [q, no, q2, {"at": cue("L9", "hold"), "text": "WORTH IT", "color": BLUE}, wrong, back_(BLUE)]),
        side("GOLD", GOLD, [{"icon": "crown", "text": "his by birth", "at": cue("L10", "birth.")},
                            {"icon": "clasp", "text": "Blue has our back", "at": cue("L11", "Gold.")}, blink()],
             [q2, {"at": cue("L10", "birth."), "text": "WORTH IT", "color": GOLD}, wrong, back_(GOLD)],
             show=[[RESET, 0], [shift(REWIND, -0.02), 0], [REWIND, 1]]),
    ]
    status = [{"at": RESET, "text": "NO WAR", "color": "rgba(239,230,210,0.55)"}, {"at": cue("L5", "Nobody"), "text": "NOBODY CAME", "color": "rust"},
              {"at": REWIND, "text": "NO REASONS", "color": "rgba(239,230,210,0.55)"}, {"at": cue("L9", "hold"), "text": "1 FLASHPOINT", "color": FLASH},
              {"at": cue("L14", "wrong."), "text": "IT CATCHES", "color": FLASH}, {"at": ROLE, "text": "1 FLASHPOINT", "color": FLASH}]
    return {"type": "warRoom", "y": 1352, "sides": sides, "status": status, "start": shift(RESET, 0.3), "end": cue("L16", "Show", -0.3)}


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "A MILLION SOLDIERS", "color": "parchment", "size": 54, "pulseAt": cue("L1", "million")},
                 {"text": "FOR ONE ANGRY KING?", "color": FLASH, "size": 50, "pulseAt": cue("L1", "angry")}]
    knot_pos = (HUB[0], HUB[1], KNOT_Y + 0.4)
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 60, "start": {"shot": "hook"}, "end": cue("L2", "Meet", -0.1), "preShow": True},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 36 · THE WAR", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "skyTags", "start": cue("L1", "angry", 0.1), "end": RESET, "tags": [tag("3 SIDES · 4 REASONS", "NOT ONE KING", cue("L1", "angry", 0.1), cue("L2", "Meet", -0.1), knot_pos, FLASH, lift=-150, dx=200)]},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Meet", -0.05), "end": RESET, "dietAt": cue("L2", "yet."),
         "kicker": "FIELD CARD · NO. 011", "kind": "A WAR · NOT YET", "name": "THE RUIN WAR", "dietLabel": "SIDES", "diet": "three, all sure they're right", **SPRITE},
    ]
    G["setup"] += [
        {"type": "blockWipe", "at": RESET, "dur": 0.34, "color": "#2b2f1c"},
        {"type": "kinetic", "parts": [{"text": "TWO ARMIES", "at": cue("L3", "two"), "size": 64, "color": "parchment"},
                                      {"text": "ONE ANGRY KING", "at": cue("L3", "one"), "color": "rust", "size": 64}],
         "y": 600, "size": 64, "start": cue("L3", "two", -0.05), "end": cue("L4", "Press", -0.15)},
        {"type": "simBar", "counters": [{"icon": "standard", "label": "ARMIES", "key": "armies", "color": "parchment", "digits": 2},
                                        {"icon": "pin", "label": "REASONS", "key": "reasons", "color": FLASH, "digits": 2}],
         "compact": True, "start": cue("L4", "Press", -0.15), "end": cue("L16", "Show", -0.3), "runAt": [cue("L4", "run."), cue("L12", "Run")]},
        war_room(),
    ]
    G["run1"] += [
        {"type": "kinetic", "parts": [{"text": "10 YEARS", "at": cue("L5", "Ten"), "color": "parchment", "size": 56},
                                      {"text": "OF SHOUTING", "at": cue("L5", "shouting."), "color": "parchment", "size": 56},
                                      {"text": "NOBODY MARCHES", "at": cue("L5", "Nobody"), "color": "rust", "size": 56}],
         "y": 600, "size": 56, "start": cue("L5", "Ten", -0.05), "end": cue("L6", "One", -0.25)},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "JUST A TANTRUM", "sub": "1 REASON · 0 ARMIES · NO WAR", "color": "rust", "y": 640, "size": 80, "start": cue("L6", "tantrum,"), "end": cue("L6", "war.", 0.55)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "war.", 0.6), "end": cue("L7", "Real", 0.3)},
        {"type": "blockWipe", "at": cue("L6", "war.", 0.58), "dur": 0.34},
        {"type": "kinetic", "parts": [{"text": "REAL WARS", "at": cue("L7", "Real"), "size": 78, "color": "parchment"}, {"text": "NEED REASONS", "at": cue("L7", "reasons"), "color": FLASH, "size": 78}],
         "y": 600, "size": 78, "start": cue("L7", "Real", -0.05), "end": cue("L7", "Four", -0.15)},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L16", "Show", -0.3),
         "kicker": "THE RUIN WAR · WHY THEY MARCH", "title": "PULL THE THREADS", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L8", "One:", -0.3), 0], [cue("L8", "One:", 0.0), 1], [ROLE, 1], [shift(ROLE, 0.3), 0]]},
    ]
    up = lambda c: (c[0], c[1], THREAD_Y + 0.4)
    G["gain"] += [{"type": "skyTags", "start": cue("L8", "harbour."), "end": cue("L9", "Two:", -0.15), "tags": [
        tag("A HARBOUR TO TAKE", "RED · GAIN", cue("L8", "harbour."), cue("L9", "Two:", -0.15), up(PIN["r"]), RED, lift=170, dx=0, band=[600, 1080])]}]
    G["fear"] += [{"type": "skyTags", "start": cue("L9", "hold"), "end": cue("L10", "Three:", -0.15), "tags": [
        tag("CAN'T LET RED WIN", "BLUE · FEAR", cue("L9", "hold"), cue("L10", "Three:", -0.15), up(PIN["b"]), BLUE, lift=170, dx=0, band=[600, 1080])]}]
    G["claim"] += [{"type": "skyTags", "start": cue("L10", "birth."), "end": cue("L11", "Four:", -0.15), "tags": [
        tag("HIS BY BIRTH", "GOLD · A CLAIM", cue("L10", "birth."), cue("L11", "Four:", -0.15), up(PIN["g"]), GOLD, lift=170, dx=0, band=[600, 1080])]}]
    G["allies"] += [{"type": "skyTags", "start": cue("L11", "Gold."), "end": cue("L12", "Run", -0.15), "tags": [
        tag("A PROMISE TO KEEP", "BLUE + GOLD · ALLIES", cue("L11", "Gold."), cue("L12", "Run", -0.15), ((PIN["b"][0] + PIN["g"][0]) / 2, (PIN["b"][1] + PIN["g"][1]) / 2, 1.2), GOLD, lift=170, dx=0, band=[600, 1080])]}]
    G["run2"] += [
        {"type": "kinetic", "parts": [{"text": "10 YEARS", "at": cue("L12", "Ten"), "color": "parchment", "size": 56},
                                      {"text": "THREE ARMIES", "at": cue("L12", "Three"), "color": "parchment", "size": 56},
                                      {"text": "ONE RUIN", "at": cue("L12", "one"), "color": FLASH, "size": 56}],
         "y": 600, "size": 56, "start": cue("L12", "Ten", -0.05), "end": cue("L12", "ruin.", 0.1)},
        {"type": "stamp", "text": "EVERYONE'S RIGHT", "sub": "3 SIDES · 4 REASONS · 1 RUIN", "color": FLASH, "rotate": -4, "y": 880, "size": 76, "start": cue("L12", "ruin.", 0.15), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}, {"text": "NOBODY WANTS IT", "at": cue("L13", "Nobody"), "color": "parchment", "size": 60}],
         "size": 150, "y": 560, "start": cue("L13", "Rule", -0.02), "end": cue("L14", "Each", -0.1)},
        {"type": "kinetic", "parts": [{"text": "THEY'LL BLINK", "at": cue("L14", "blink."), "color": "parchment", "size": 72}, {"text": "ALL WRONG", "at": cue("L14", "wrong."), "color": FLASH, "size": 96}],
         "size": 80, "y": 600, "start": cue("L14", "sure", -0.05), "end": ROLE},
        {"type": "skyTags", "start": shift(WRONG, 0.3), "end": ROLE, "tags": [
            tag("ONE WRONG GUESS", "THE FLASHPOINT", shift(WRONG, 0.3), ROLE, (HUB[0], HUB[1], KNOT_Y + 0.5), FLASH, lift=-200, dx=0, band=[760, 1120])]},
    ]
    G["role"] += [
        {"type": "followChip", "start": cue("L15", "cost.", 0.2), "end": cue("L16", "villain.", 0.3), "text": "FOLLOW", "sub": "PART 36/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "Show", -0.3), **({"unlockAt": cue("L16", "Show", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "Show", -0.3), "end": WIPE, "kicker": "BEFORE YOU START A WAR", "title": "RUIN WAR", **SPRITE,
         "subtitle": "Nobody thinks they're the villain.", "subtitleAt": cue("L16", "wants.")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 36 / 50",
         "title": "Wars Need More Than Two Armies", "cta": "COMMENT", "icon": "bubble", "with": "One reason. Name it.", "withAt": cue("L17", "war?", -0.05), "choiceSize": 30,
         "choices": [{"text": "A STOLEN HEIR", "color": GOLD, "at": cue("L17", "push")}, {"text": "THE LAST WELL", "color": BLUE, "at": cue("L17", "kingdom")}]},
    ]
    gone = cue("L18", "lose.", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 36, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6, "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone, "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 37"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "37:", -0.1), "revealAt": cue("L18", "armies"), "end": gone,
         "kicker": "NEXT RUN · 37", "title": "BIG ARMY", "sub": "TEN TIMES BIGGER. LOSING.", "sprite": "host", "spritePx": 6},
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 60, "start": cue("L18", "lose.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("A war with one reason (an angry king) is a tantrum, not a war: nobody marches for it. Give every side its own "
          "reason worth the cost: something to gain, something to fear, a claim, a promise to an ally. Then let it start "
          "by mistake, because every side was sure the others would back down. Nobody thinks they're the villain.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Close EP35's loop (three standards were planted round the ruin on 'two armies are never enough') and stop the scroll.",
             "Golden hour over the Builders' ruin: three camps round it (red tents and standard west, blue north-east, gold south), their armies standing in front of the tents, and four coloured threads strung from the camps' pins to a knot on a tall war pin stuck in the ruin, glowing flashpoint lime, with one thread braided blue and gold between two camps. A MILLION SOLDIERS / FOR ONE ANGRY KING? from frame 0, each line pulsing on its word (NOT ONE KING · 3 SIDES · 4 REASONS at the knot). Then the field card: THE RUIN WAR · A WAR · NOT YET · SIDES: three, all sure they're right.",
             "From the south-south-west (az 340, el 27, fov 20), pulling slowly back.", ("kinetic, sting, tag, field card", "the knot, the threads, the camps", "the lake, the Queen's dais"),
             "Golden hour.", "A MILLION SOLDIERS / FOR ONE ANGRY KING? · FIELD CARD NO. 011 · THE RUIN WAR", "Olive block wipe into the lazy version.", "Council: a ticking clock, plucked fifths, the theme on a muted trumpet; a hit on 'angry'."),
    "setup": ("The lazy version: two armies, one angry king.",
              "A wipe to two camps only (Red and Blue), no knot, one red thread (anger) strung from Red's camp to Blue's. TWO ARMIES / ONE ANGRY KING. The war room strip slides in under the world (RED: the king is angry; BLUE: nothing; GOLD absent; NO WAR); the sim bar arrives (ARMIES 02, REASONS 01) and RUN is pressed.",
              "Cut close on Red's camp, pulling back along the anger thread to Blue's.", ("kinetic, sim bar, war room", "the two camps", "the Isle"), "Day.", "TWO ARMIES · ONE ANGRY KING · THE WAR ROOM", "A cut to the whole Isle on 'run'.", "Council, thin."),
    "run1": ("Run the lazy version: ten years of shouting and nobody marches.",
             "The whole Isle; YEAR 0→10; on 'Nobody' both camps strike their tents, the standards sink, the armies go home and the anger thread goes slack and reels back. 10 YEARS / OF SHOUTING / NOBODY MARCHES. ARMIES 2→0, REASONS 1→0; both verdicts read NOT WORTH IT.",
             "Wide (dist 160, fov 22), backing away.", ("sim bar, kinetic, war room", "the Isle", "the void"), "Day.", "10 YEARS / OF SHOUTING / NOBODY MARCHES", "Gloom.", "Drive."),
    "drop": ("The punchline: one angry king is a tantrum, not a war.", "Gloom: JUST A TANTRUM · 1 REASON · 0 ARMIES · NO WAR, over the empty camps.",
             "Wide, the pull-back easing to a stop.", ("stamp, war room", "the Isle", "the void"), "Gloom.", "JUST A TANTRUM · 1 REASON · 0 ARMIES · NO WAR", "Rewind + block wipe.", "Drop; a boom on 'war'."),
    "rehook": ("Re-hook: the thesis, four rules, one locked.",
               "REWIND to three camps with their armies and no threads (NO REASONS). REAL WARS / NEED REASONS; then the checklist PULL THE THREADS, row 5 locked (the twist).",
               "Wide, backing away.", ("rewind, kinetic, checklist, war room", "the Isle", "the void"), "Day.",
               "REAL WARS NEED REASONS · PULL THE THREADS 0/5", "Cut close on Red's camp.", "Muster, bare (a field snare); a riser into 'the twist'."),
    "gain": ("Rule 1: something to gain (interests and resources).", "Close on Red's camp; on 'harbour' a war pin is pushed into the ruin and Red's thread runs from its camp to the knot (RED · GAIN · A HARBOUR TO TAKE).",
             "Cut close behind Red's tents, pulling back along the thread to the knot.", ("tag, checklist (folded), war room", "Red's camp and its thread", "the ruin"), "Day.", "1 GAIN · a harbour to take", "Cut.", "Muster 1: a field snare."),
    "fear": ("Rule 2: fear (security).", "Close on Blue's camp; on 'Red' Blue's thread runs to the same knot: the first flashpoint (BLUE · FEAR · CAN'T LET RED WIN).",
             "Cut close behind Blue's tents, pulling back.", ("tag, checklist (folded), war room", "Blue's camp and its thread", "the knot"), "Day.", "2 FEAR · can't let them win", "Cut.", "Muster 2: a tuba."),
    "claim": ("Rule 3: a claim (succession).", "Close on Gold's camp; on 'prince' Gold's thread runs to the knot (GOLD · A CLAIM · HIS BY BIRTH).",
              "Cut close behind Gold's tents, pulling back.", ("tag, checklist (folded), war room", "Gold's camp and its thread", "the knot"), "Day.", "3 A CLAIM · his by birth", "Cut.", "Muster 3: timpani and cymbal."),
    "allies": ("Rule 4: allies.", "On 'swore' a thread braided blue and gold runs between Blue's camp and Gold's (BLUE + GOLD · ALLIES · A PROMISE TO KEEP): now any move pulls all three.",
               "Cut to the web from the south, pulling back.", ("tag, checklist (folded), war room", "the braided thread", "the camps"), "Day.", "4 ALLIES · a promise to keep", "Cut to the whole Isle.", "Muster 4: the theme on a fife, horns."),
    "run2": ("Run with every side's reasons: ten years, and three armies march up to one ruin.",
             "The whole Isle; YEAR 0→10; the three armies advance from their camps and stand facing the ruin; 10 YEARS / THREE ARMIES / ONE RUIN. EVERYONE'S RIGHT · 3 SIDES · 4 REASONS · 1 RUIN, stamped in lime.",
             "Wide, backing away.", ("sim bar, war room, stamp", "the armies standing", "the Isle"), "Day.", "EVERYONE'S RIGHT · 3 SIDES · 4 REASONS · 1 RUIN", "Cut to dusk.", "Drive with the theme; a stab and a cymbal on 'ruin'."),
    "twist": ("The locked rule: nobody wants it, and it starts by mistake.",
              "Dusk, close on the knot: RULE 5? NOBODY WANTS IT. On 'sure' every thread pulls taut and hums, and each side's column in the war room adds 'they'll blink' (THEY'LL BLINK); on 'wrong' the knot catches, blazing lime with a ring of light on the ground (ALL WRONG; THE FLASHPOINT · ONE WRONG GUESS), every 'they'll blink' is struck through and each verdict reads GUESSED WRONG. Nobody moves; nothing is shown fighting.",
              "Cut close on the knot, then pulling back further and further as it catches.", ("kinetic, tag, war room", "the knot, the taut threads", "the armies, the camps"), "Dusk.",
              "RULE 5? NOBODY WANTS IT · THEY'LL BLINK · ALL WRONG · THE FLASHPOINT", "Day on 'So'.", "Twist (a held A7♭9), then council with the clock louder."),
    "role": ("Unlock rule 5: a wrong guess.",
             "Day returns, the threads slacken and the knot settles; the checklist opens and row 5 unlocks on 'cost': A GUESS · they'll back down · 5/5. The follow chip (+ FOLLOW · PART 36/50) after 'cost'.",
             "The web from the south, pulling back.", ("open checklist, follow chip, war room", "the web", "the Isle"), "Day.", "5 A GUESS · they'll back down · 5/5", "The card goes full.", "Anthem from 'So'; a D-major hit on 'cost'."),
    "lesson": ("The takeaway.", "The full card (BEFORE YOU START A WAR · RUIN WAR, all five rows ticked) over the whole Isle in golden light, with 'Nobody thinks they're the villain.' in serif italic from the end of the first sentence.",
               "Wide: one slow pull-back.", ("full card, follow chip", "the Isle", "the void"), "Golden hour.", "BEFORE YOU START A WAR · RUIN WAR · Nobody thinks they're the villain.", "Block wipe to the end card.", "Anthem; the World Engine chime as the card lands."),
    "cta": ("Comment CTA: what would finally push your kingdom into war?", "End card: logo, PART 36 / 50, the title, and a COMMENT panel where A STOLEN HEIR and THE LAST WELL pop as starters, then 'One reason. Name it.'",
            "Cut (under the block wipe) close on the knot, pulling back onto the hook pose.", ("end card", "the web", "the Isle"),
            "Golden hour (the loop frame).", "COMMENT · A STOLEN HEIR / THE LAST WELL · One reason. Name it.", "The card lifts on 'Part'.", "Outro."),
    "next": ("Say the part number, ask for the follow with a reason (part 37), open the next loop.",
             "The hook frame; PART 36/50; FOLLOW FOR PART 37, pressed on 'Follow'; NEXT RUN · 37 decodes from a locked host of banners to THE BIG ARMY · TEN TIMES BIGGER. LOSING. In the world, on 'army', one grey standard far bigger than the three rises at the Isle's south-east tip and the horn calls; the Queen looks up; it sinks before the hook title returns.",
             "The hook frame.", ("progress bar, follow button, next-run card", "the web", "one giant standard rising"), "Golden hour.",
             "PART 36/50 · FOLLOW FOR PART 37 · NEXT RUN: THE BIG ARMY · TEN TIMES BIGGER. LOSING.", "Loop to frame 0.", "Tease over a held A; a horn call on 'army'; the engine chime on 'Follow'."),
}


def build():
    ep = {
        "id": "ep36", "number": 36, "season": 2,
        "title": "Wars Need More Than Two Armies",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 0.95},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same lab host, like someone walking a general through a war room at night. The hook is flat and certain. 'Two armies, one angry king' is the cliché; 'a tantrum, not a war' lands dry. "
                         "The rules are crisp, two beats each, each side's reason said as if it were obviously right. 'Nobody here wants this war' is quiet; 'All three are wrong' drops. The comment ask is playful.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L3", "from": "two"}, {"line": "L5", "from": "Ten"}, {"line": "L7", "from": "Real", "to": "Four"}, {"line": "L12", "from": "Ten"}, {"line": "L13", "from": "Rule"}, {"line": "L14", "from": "Each"}],
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
             hit("threadPull", cue("L1", "million", -0.3), -20), hit("spark", cue("L1", "angry", -0.1), -18),
             hit("cardSlide", cue("L2", "Meet", -0.05), -18), hit("check", cue("L2", "yet."), -20)],
    "setup": [hit("rewind", RESET, -15), hit("pinIn", cue("L3", "angry", -0.1), -16), hit("cardSlide", shift(RESET, 0.35), -22),
              hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "marches.", 0.2), -22), hit("stamp", cue("L5", "Nobody"), -21), hit("restore", cue("L5", "Nobody", -0.1), -21)],
    "drop": [hit("stamp", cue("L6", "tantrum,"), -10)],
    "rehook": [hit("rewind", cue("L6", "war.", 0.55), -11), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "gain": [hit("check", cue("L8", "gain."), -13), hit("pinIn", cue("L8", "harbour.", -0.5), -13), hit("threadPull", cue("L8", "harbour.", -0.25), -15)],
    "fear": [hit("check", cue("L9", "fear."), -13), hit("pinIn", cue("L9", "Red", -0.15), -14), hit("threadPull", cue("L9", "Red", -0.15), -15), hit("spark", cue("L9", "hold"), -19)],
    "claim": [hit("check", cue("L10", "claim."), -13), hit("pinIn", cue("L10", "prince", -0.15), -14), hit("threadPull", cue("L10", "prince", -0.15), -15)],
    "allies": [hit("check", cue("L11", "allies."), -13), hit("pinIn", cue("L11", "swore", -0.15), -14), hit("threadPull", cue("L11", "swore", -0.15), -15)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L12", "ruin."), -22),
             hit("frameDrum", cue("L12", "Three"), -18), hit("check", cue("L12", "one"), -19), hit("stamp", cue("L12", "ruin.", 0.15), -13)],
    "twist": [hit("unlock", cue("L13", "Rule"), -15), hit("threadPull", SURE, -11), hit("spark", WRONG, -9), hit("stamp", cue("L14", "wrong.", 0.1), -20)],
    "role": [hit("restore", ROLE, -17), hit("unlock", cue("L15", "cost.", -0.1), -10)],
    "lesson": [hit("engineWind", cue("L16", "Show", -0.8), -15), hit("chime", cue("L16", "Show", -0.3), -10), hit("cardSlide", cue("L16", "Show", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("check", cue("L17", "push"), -17), hit("check", cue("L17", "kingdom"), -17)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11), hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "37:", -0.1), -18), hit("unlock", cue("L18", "armies"), -15),
             hit("stoneRise", cue("L18", "armies", -0.1), -17),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score: the series theme stays (D minor for the problem, D major for the payoff). EP36's band is `council` (the
# war room at night: a clock ticking on the side-stick, taut threads plucked as pizzicato fifths, harpsichord chords,
# the theme on a muted trumpet) and `muster` (the armies gathering, one family per rule: a field snare in rudiments; a
# tuba marching; timpani and a soft cymbal; the theme on a fife with horns).
COUNCIL_P = {"lead": 59, "celesta": 6, "cello": 42}
MUSTER_P = {"lead": 72, "bass": 58, "celesta": 8}
BACK_P = {"lead": 73, "bass": 32, "celesta": 8, "cello": 42}
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 96,
    "sections": [
        msec({"shot": "hook"}, "council", ["Dm", "Bb", "Gm", "A"], "D minor", programs=COUNCIL_P),
        msec(RESET, "council", ["Dm", "C", "Bb", "A"], "D minor", thin=True),
        msec(cue("L4", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.85, programs=BACK_P),
        msec(cue("L6", "One", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "war.", 0.55), "muster", ["Dm", "C", "Bb", "A"], "D minor", layer=1, programs=MUSTER_P),
        msec(cue("L8", "One:", -0.1), "muster", ["Dm", "C", "Bb", "C"], "D minor", layer=1),
        msec(cue("L9", "Two:", -0.1), "muster", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "muster", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L11", "Four:", -0.1), "muster", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True, programs=BACK_P),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(SURE, "council", ["Dm", "Bb", "Gm", "A"], "D minor", programs=COUNCIL_P),
        msec(cue("L15", "So", -0.1), "anthem", ["D", "G", "Bm", "A"], "D major", programs=BACK_P),
        msec(cue("L17", "What", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "angry"), "chord": "Dm"},
        {"kind": "boom", "at": cue("L6", "war."), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "ruin."), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "ruin.")},
        {"kind": "boom", "at": WRONG, "chord": "Dm"},
        {"kind": "hit", "at": cue("L15", "cost."), "chord": "D"},
        {"kind": "call", "at": cue("L18", "armies"), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #WritingTips #Lore #WorldcraftShorts"
IG_HOOK = "Nobody sends a million soldiers to die for an angry king."
BODY = (
    "Nobody sends a million soldiers to die for an angry king.\n\n"
    "Meet the Ruin War: it hasn't started yet. The lazy version of a war is two armies and one angry king, and we "
    "ran it: ten years of shouting, and nobody marches. One angry king is a tantrum, not a war.\n\n"
    "Real wars need reasons. Something to gain: Red needs the ruin's harbour. Fear: Blue can't let Red hold it. A "
    "claim: Gold's prince says it's his by birth. Allies: Blue swore to stand with Gold. Run it again: ten years, three "
    "armies, one ruin.\n\n"
    "Then the twist: nobody here wants this war. Each side is sure the others will blink. All three are wrong. So give "
    "every side a reason worth the cost.\n\n"
    "Show what each side wants. Nobody thinks they're the villain.\n\n"
    "What would finally push your kingdom into war?\n\n"
    "Part 36 of 50. Follow for part 37: big armies still lose."
)
METADATA = {
    "youtube": {
        "title": "Wars Need More Than Two Armies (Worldbuilding)",
        "titleAlternate": "Nobody sends a million soldiers to die for an angry king.",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 8: Conflict and Warfare (the arc's first episode). The Ruin "
        "War, its three sides and their plain coloured standards are invented for this video; no real war, army, flag "
        "or nation is depicted, and nobody fights on screen.\n\n" + TAGS,
        "pinnedComment": "What would finally push your kingdom into war? One reason, then which side holds it. (Part 37: big armies still lose.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated field-card sprite; the island, the camps, the threads and the people are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "Nobody sends a million soldiers to die for an angry king. 🧵 Four reasons a war feels real, and rule #5 is the twist. "
                   "What would finally push your kingdom into war? Part 36/50 · follow for part 37 ⚔️ " + TAGS,
        "pinnedComment": "What would finally push your kingdom into war?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "Which side of your war thinks it's the hero? (All of them should.)",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": IG_HOOK + "\n\n" + BODY.split("\n\n", 1)[1] + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": f"First {len(IG_HOOK)} characters: '{IG_HOOK}'",
        "pinnedComment": "Save the PULL THE THREADS card, then tell us: what would finally push your kingdom into war?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep36] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots, loop span {loop_span():.2f} s")
