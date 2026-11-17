"""Generate episodes/ep35/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep35/make_ep35.py
EP35 is Arc 7's last episode (History and Mythology): "Give Your World a Lost Civilization". It closes EP34's loop
(on "the ruins are older than us" broken pillars rose beside the giant's bones for a breath, then sank): frame 0 has
them standing for good at the east end of a long broken wall, and one stone high in that wall is newer than the rest,
glowing faintly. Someone has been repairing it.

Its own device is THE FINDS TRAY: a specimen tray under the world with one compartment per find, and each find is a
fragment of the lost civilization (the Builders): their tools (a gear nobody here can make), their values (the biggest
room was a kitchen with one long table), their failure (every well is full of sand) and their days (a child's
handprints in the mortar). The lazy version is ancient, mysterious and gone: the tray stays EMPTY and the ruin is just
rocks. The twist is the tray's locked fifth compartment, read off the wall itself through THE REPAIR LOG (every stone
shows its age by colour: half the wall is newer than us, and one more stone is set every night). The writer's job is to
leave that question open: never say who.
Camera language: THE TRACKING SHOT. Every pose looks north at the wall from one fixed azimuth (az 0, so screen-x is
world-x) and the camera only slides sideways along it, like a walk down a dig trench: station to station for the rules,
across the whole Isle for the runs, never turning (EP26 orbited, EP27 rode a dragon, EP28 sat at eye height, EP29 was a
locked-off tripod, EP30 looked up, EP31 split the frame, EP32 craned up and down the cut, EP33 looked down at a map
table, EP34 dolly-zoomed).
Motif colour: quartz cyan #4fd6ff (freshly set stone). Music band: `hollow` (wind through an empty ruin: blown bottle,
vibraphone echoes, a contrabass drone) and `survey` (the walk along the wall, one family per rule).
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep35" / "timing.json"
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
    ("L1", "hook", "These ruins are older than humans. Someone keeps repairing them.", 0.3, ["older", "repairing"]),
    ("L2", "hook", "Meet the Builders. Their wall still stands.", 0.3, ["builders.", "stands."]),
    ("L3", "setup", "The lazy version: ancient, mysterious, gone.", 0.25, ["lazy", "gone."]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "A thousand years of digging. Nothing but stones.", 0.35, ["digging.", "stones."]),
    ("L6", "drop", "A ruin that says nothing is just rocks.", 0.4, ["nothing", "rocks."]),
    ("L7", "rehook", "Good ruins talk. Four rules. The fifth is the twist.", 0.25, ["talk.", "twist."]),
    ("L8", "tools", "One: their tools. A gear that nobody here can make.", 0.25, ["tools.", "gear"]),
    ("L9", "values", "Two: what they valued. Their biggest room was a kitchen.", 0.25, ["valued.", "kitchen."]),
    ("L10", "failure", "Three: how they failed. Every well is full of sand.", 0.25, ["failed.", "sand."]),
    ("L11", "days", "Four: their days. A child's handprints, pressed into the mortar.", 0.3, ["days.", "handprints,"]),
    ("L12", "run2", "Run it again. A thousand years. Every find opens two questions.", 0.35, ["thousand", "questions."]),
    ("L13", "twist", "Rule five? Look closer. Half this wall is newer than us.", 0.35, ["closer.", "newer"]),
    ("L14", "twist", "Someone replaces one stone every night. Nobody has seen them.", 0.4, ["night.", "seen"]),
    ("L15", "role", "So never tell us who.", 0.4, ["never", "who."]),
    ("L16", "lesson", "Show how they lived and fell. Every ruin keeps one secret.", 0.35, ["lived", "secret."]),
    ("L17", "cta", "What should archaeologists never find in your world?", 0.25, ["never", "world?"]),
    ("L18", "next", "Part 35 of 50. Follow for part 36: two armies are never enough.", 0.25, ["follow", "enough."]),
]
SHOTS = ["hook", "setup", "run1", "drop", "rehook", "tools", "values", "failure", "days", "run2", "twist", "role", "lesson", "cta", "next"]

# The block wipe into the end card: the world resets to frame 0 under it (today: every find dug, last night's stone lit).
WIPE = cue("L17", "What", -0.3)
RESET = cue("L3", "lazy", -0.15)          # the lazy version: ancient, mysterious, gone (nothing dug, nothing repaired)
REWIND = cue("L6", "rocks.", 0.6)         # back to the bare ruin, before anything is found
RULES = cue("L8", "One:", -0.1)
RUN2 = cue("L12", "Run", -0.05)
TWIST = cue("L13", "Rule", -0.1)
LOG = cue("L13", "Half", -0.05)           # the repair log: every stone shows its age
NIGHT = cue("L14", "night.", -0.1)        # tonight's stone is set
ROLE = cue("L15", "So", -0.15)
END = {"end": True}

# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle (it remembers): EP27's valley village and watchtower (west), the cairn (east of the lake),
# EP29's Queen on her dais, EP30's Grimmaw (north-east), EP31's split statue and EP32's boundary stones and relic
# (south-east), EP33's Lamplight faith (candles at the cairn, boats with lamps, the sheaves, the crowd's lamps), EP33's
# crack of light and EP34's giant's bones in the meadow south of the lake, and EP34's ruined pillars (its tease).
# EP34's painted sky is not over the Isle in EP35 (its device stays its own); EP28's Fenn hall stays out.
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
CROWD = [[-2.4, -3.2], [-0.4, -1.6], [-4.2, -1.8]]
RIFT_A, RIFT_B = (-0.5, 10.6), (12.0, 8.8)         # EP33's crack of light
BONES = (6.5, 12.2)                                 # EP34's giant's bones in their trench
BONES_FACE = 8.2
RUIN = (12.8, 13.4)                                 # EP34's tease: the broken pillars, standing for good

# The Builders' wall: twelve columns of squared blocks along z 14.6 between the bones and the south shore, broken
# at the top and breached in the middle. Last night's stone glows at the top of column 6; tonight's gap is the top of
# column 7. The finds lie in front of it, west to east: the gear, the kitchen, the wells, and the handprints on the
# wall's own face (column 10).
WALL_A, WALL_B = (0.6, 14.6), (10.2, 14.6)
PROFILE = [3, 5, 6, 7, 6, 4, 6, 7, 5, 2, 4, 3]
FRESH = [6, 5]
TONIGHT = [7, 6]
COLX = lambda i: WALL_A[0] + (WALL_B[0] - WALL_A[0]) / len(PROFILE) * (i + 0.5)
GEAR = (1.5, 16.0)
KITCHEN = (3.9, 16.6)
WELLS = (6.5, 15.8)
HANDS = (COLX(10), WALL_A[1] + 0.47)
GROUND = {GEAR: 5, KITCHEN: 4, WELLS: 4, HANDS: 4}   # the terrace heights (island.heightAt), for camera targets
PITS = [(0.2, 17.2), (5.9, 17.6), (8.6, 16.4), (2.2, 13.4), (11.2, 15.1), (-0.6, 15.4), (4.7, 13.6), (9.6, 13.4),
        (7.6, 17.0), (12.0, 13.9), (1.0, 18.2), (3.2, 18.6)]   # run 2: the dig spreads round the site

# EP36's tease (on "armies"): three small standards in three colours are planted round the ruin (three sides
# claiming it), low in the hook frame so the ending's cards don't cover them
STANDARDS = [((3.8, 18.2), "#c0573c"), ((6.4, 17.6), "#4f7fbf"), ((9.0, 16.4), "#d4b23f")]

QUARTZ = "#4fd6ff"
STONE_C = "#c9c4b4"


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
    """Seconds from the wipe to the end: the loop camera key slides this long and lands exactly on the hook pose."""
    if not TIMING.exists():
        return 6.0
    return tcue(END) - tcue(WIPE)


# ---- the tracking shot. Every pose has the same azimuth (AZ 0: the camera is south of its target, looking north),
# so screen-x is world-x and a move is the target sliding along x. A pose is a target, an elevation and `h`, the
# frame's half-height at the target (dist = h / tan(fov / 2)).
AZ = 0


def dist_for(h, fov):
    return h / math.tan(math.radians(fov / 2))


def pose(target, el, h, fov):
    return dict(target=target, el=el, dist=dist_for(h, fov), fov=fov)


def slide(p, dx, dz=0.0):
    """The same pose, slid sideways along the wall."""
    t = p["target"]
    return dict(p, target=(t[0] + dx, t[1], t[2] + dz))


# Poses (planned with pipeline/camprobe.ts; BRIEF.md §6).
HOOK_POSE = pose((6.4, 6.2, 15.0), 13, 5.6, 20)          # the wall's middle, last night's stone near the top
HOOK_SLIDE = 0.9                                          # the hook slides this far west while the title holds
WIDE = pose((0.0, 2.0, 0.0), 26, 31.0, 22)               # the whole Isle (dist 160)
STATION = dict(el=22, h=3.4, fov=20)                     # the rules: one height and lens, sliding station to station
P_GEAR = pose((GEAR[0] + 0.3, 5.8, GEAR[1]), STATION["el"], STATION["h"], STATION["fov"])
P_KITCHEN = pose((KITCHEN[0], 4.8, KITCHEN[1]), STATION["el"], STATION["h"], STATION["fov"])
P_WELLS = pose((WELLS[0] + 0.7, 4.8, WELLS[1]), STATION["el"], STATION["h"], STATION["fov"])
P_HANDS = pose((HANDS[0], 4.9, HANDS[1]), 6, 1.3, 20)
P_WALL = pose((5.4, 5.6, 14.6), 12, 7.0, 20)             # the whole wall for the repair log
P_NIGHT = pose((COLX(TONIGHT[0]), 6.9, 14.6), 10, 2.4, 20)


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    lin = lambda at, v: [at, v, "linear"]
    H = shot("hook")
    span = loop_span()

    # ---- the clock (YEAR since the Lamplight's First Lamp). Today is year 500; each run digs for a thousand years.
    R1A, R1B = cue("L4", "run.", 0.3), cue("L5", "stones.", 0.3)
    R2A, R2B = cue("L12", "Run", 0.25), cue("L12", "questions.", 0.1)
    clock = [[H, 500], [R1A, 500], lin(R1B, 1500), *jump(REWIND, 1500, 500), [R2A, 500], lin(R2B, 1500), *jump(TWIST, 1500, 500), [WIPE, 500]]
    speed = [[H, 1], [cue("L4", "run."), 1], [R1A, 6], [R1B, 6], [cue("L6", "A"), 1],
             [R2A, 1], [cue("L12", "Run", 0.5), 6], [R2B, 6], [cue("L13", "Rule"), 1]]

    # ---- rule cues
    G_UP = cue("L8", "gear")
    K_UP = cue("L9", "biggest")
    W_UP = cue("L10", "well")
    H_UP = cue("L11", "child's")

    # ---- the HUD: finds and the questions they open (run 2: every find opens two)
    finds = [[H, 4], *jump(RESET, 4, 0), *jump(G_UP, 0, 1), *jump(K_UP, 1, 2), *jump(W_UP, 2, 3), *jump(H_UP, 3, 4),
             [cue("L12", "A", 0.0), 4], lin(cue("L12", "questions.", 0.1), 16), [WIPE, 16], [shift(WIPE, 0.02), 4, "step"]]
    questions = [[H, 4], *jump(RESET, 4, 0), *jump(G_UP, 0, 1), *jump(K_UP, 1, 2), *jump(W_UP, 2, 3), *jump(H_UP, 3, 4),
                 [cue("L12", "A", 0.0), 4], lin(cue("L12", "questions.", 0.1), 32), [WIPE, 32], [shift(WIPE, 0.02), 4, "step"]]

    # ---- the ground: today every find is dug (frame 0); the lazy version has nothing; each rule unearths one
    def unearth(at, dur=0.9):
        return [[H, 1], *jump(RESET, 1, 0), [at, 0], lin(shift(at, dur), 1), [WIPE, 1]]
    # the repair log, last night's stone, tonight's stone
    log = [[H, 0], [LOG, 0], lin(shift(LOG, 0.8), 1), [ROLE, 1], lin(shift(ROLE, 0.7), 0), [WIPE, 0]]
    glow = [[H, 1], [cue("L1", "repairing", -0.05), 1], [cue("L1", "repairing", 0.25), 1.8], [cue("L1", "them.", 0.3), 1], *jump(RESET, 1, 0),
            [TWIST, 0], [LOG, 0], lin(shift(LOG, 0.8), 1), [WIPE, 1]]
    place = [[H, 0], [NIGHT, 0], [shift(NIGHT, 0.55), 1, "out"], [WIPE, 1], [shift(WIPE, 0.02), 0, "step"]]
    # run 2: the dig spreads round the site, one pit at a time, and is filled back in under the wipe
    r2a = tcue(cue("L12", "A")) or 34.0
    r2b = tcue(cue("L12", "questions.", -0.2)) or 37.0
    pits = []
    for k, (px, pz) in enumerate(PITS):
        on = shift(cue("L12", "A"), (r2b - r2a) * k / (len(PITS) - 1))
        pits.append({"kind": "find", "find": "pit", "x": px, "z": pz, "r": 1.4, "rise": [[H, 0], [on, 0], lin(shift(on, 0.5), 1), [WIPE, 1], [shift(WIPE, 0.02), 0, "step"]]})
    # EP36's tease: three standards rise on "armies" and sink back before the hook title returns
    std = [[H, 0], [cue("L18", "armies", -0.1), 0], [cue("L18", "never", 0.1), 1, "out"], [cue("L18", "enough.", 0.5), 1], [cue("L18", "enough.", 0.95), 0]]

    rift = [[H, 1]]
    fears = [{"id": "rift", "x": RIFT_A[0], "z": RIFT_A[1], "r": 0.0, "kind": "rift", "to": list(RIFT_B), "dark": rift}]
    dust = [{"at": shift(G_UP, 0.1), "x": GEAR[0], "z": GEAR[1], "r": 1.6}, {"at": shift(K_UP, 0.1), "x": KITCHEN[0], "z": KITCHEN[1], "r": 2.4},
            {"at": shift(W_UP, 0.1), "x": WELLS[0] + 0.6, "z": WELLS[1], "r": 1.8}, {"at": shift(NIGHT, 0.5), "x": COLX(TONIGHT[0]), "z": WALL_A[1] + 0.6, "r": 1.0}]
    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run")]
    bells = [cue("L18", "armies")]

    # ---- people: the crowd keeps the Lamplight's lamps; the Queen looks across at the standards on "armies"
    ruler = [pk(H, *QUEEN, "idle", face=0), pk(cue("L18", "armies"), *QUEEN, "alert", face=0), pk(cue("L18", "enough.", 0.7), *QUEEN, "idle", face=0)]
    g_now = [pk(H, *G_NOW, "idle", face=160)]

    # Camera language: the tracking shot. One azimuth; every move slides sideways along the wall.
    def k(at, p, dur=1.2, cut=False):
        return cam(at, AZ, p["el"], p["dist"], p["target"], fov=p["fov"], dur=dur, cut=cut)
    LESSON_AT = cue("L16", "Show", -0.25)
    hook_end = slide(HOOK_POSE, -HOOK_SLIDE)
    camera = [
        k(H, HOOK_POSE),
        # the hook: a slow slide west along the wall's top while the title holds, then on along it under the field card
        k(shot("hook", 0.02), hook_end, dur=(tcue(cue("L2", "Meet")) or 4.2)),
        k(cue("L2", "Meet"), slide(hook_end, -1.2), dur=2.4),
        # the lazy version: the bare wall (no finds, no repairs), sliding east
        k(RESET, slide(HOOK_POSE, -2.6), cut=True),
        k(shift(RESET, 0.02), slide(HOOK_POSE, 0.6), dur=3.2),
        # run 1: the whole Isle, sliding east as the centuries pass; the drop slows to a stop
        k(cue("L4", "run.", 0.05), slide(WIDE, -7.0), cut=True),
        k(cue("L4", "run.", 0.07), slide(WIDE, 2.0), dur=3.6),
        k(cue("L6", "A", -0.2), slide(WIDE, 4.0), dur=2.2),
        k(REWIND, slide(WIDE, 6.0), cut=True),
        k(shift(REWIND, 0.02), slide(WIDE, -3.0), dur=3.2),
        # the rules: one slide down the wall, station to station (west to east)
        k(RULES, slide(P_GEAR, -1.6), cut=True),
        k(shift(RULES, 0.02), P_GEAR, dur=1.4),
        k(cue("L9", "Two:", -0.1), P_KITCHEN, dur=1.1),
        k(cue("L10", "Three:", -0.1), P_WELLS, dur=1.1),
        k(cue("L11", "Four:", -0.1), slide(P_WELLS, 1.2), dur=0.9),
        k(cue("L11", "child's", -0.25), P_HANDS, dur=1.0),
        # run 2: the whole Isle again, sliding west as the dig spreads
        k(RUN2, slide(WIDE, 6.0), cut=True),
        k(shift(RUN2, 0.02), slide(WIDE, -4.0), dur=4.2),
        # the twist: the whole wall, sliding east; the repair log lights; then on to tonight's gap
        k(TWIST, slide(P_WALL, -1.6), cut=True),
        k(shift(TWIST, 0.02), P_WALL, dur=2.4),
        k(cue("L14", "Someone", -0.1), slide(P_NIGHT, -0.8), dur=1.0),
        k(cue("L14", "stone", -0.1), P_NIGHT, dur=1.4),
        k(cue("L14", "Nobody", -0.1), slide(P_NIGHT, 0.7), dur=1.6),
        k(ROLE, slide(P_WALL, 1.4), dur=1.6),
        # the lesson: the whole Isle in golden light, one slow slide
        k(LESSON_AT, slide(WIDE, -3.0), cut=True),
        k(shift(LESSON_AT, 0.02), slide(WIDE, 3.0), dur=4.0),
        # the loop: cut under the wipe, then slide so it lands exactly on frame 0's pose at the end
        k(WIPE, slide(HOOK_POSE, 1.4), cut=True),
        k(shift(WIPE, 0.02), HOOK_POSE, dur=span - 0.02),
    ]
    if SCOUT:
        camera = [k(H, WIDE)]
    light = [
        {"at": H, "mood": "golden"},
        {"at": RESET, "mood": "day", "dur": 0.4},
        {"at": cue("L6", "A", -0.2), "mood": "gloom", "dur": 0.6},
        {"at": REWIND, "mood": "day", "dur": 0.3},
        {"at": TWIST, "mood": "dusk", "dur": 0.6},
        {"at": cue("L14", "Someone", -0.1), "mood": "night", "dur": 0.8},
        {"at": ROLE, "mood": "day", "dur": 0.5},
        {"at": cue("L16", "Show", -0.3), "mood": "golden", "dur": 1.4},
    ]
    human_valley = {
        "buildings": [{"kind": kk, "a": list(a), "face": 0} for kk, a in HUMAN_B],
        "roof": [[H, 1]], "pens": [{"a": [-6.4, -1.4], "r": 1.6}], "cover": [[H, 1]],
        "roads": {"b": HUMAN_ROAD}, "route": [[H, 1]], "tradeKey": "tradeH", "lanterns": [[H, 0]],
        "tower": {"x": HUMAN_TOWER[0], "z": HUMAN_TOWER[1], "h": 6.0, "keys": [[H, 1]], "rings": bells},
    }
    clear = [BONES, (BONES[0] - 4, BONES[1]), (BONES[0] + 4, BONES[1] - 0.5), CAIRN, (FIELD[0], FIELD[1]), *[tuple(c) for c in CROWD], RUIN,
             GEAR, (GEAR[0] - 1.2, GEAR[1]), KITCHEN, (KITCHEN[0] - 1.6, KITCHEN[1]), (KITCHEN[0] + 1.6, KITCHEN[1]), (KITCHEN[0], KITCHEN[1] + 1.6), WELLS, (WELLS[0] + 1.4, WELLS[1]),
             *[(COLX(i), WALL_A[1]) for i in range(len(PROFILE))], *[(COLX(i), WALL_A[1] + 1.8) for i in range(0, len(PROFILE), 2)], *[(COLX(i), WALL_A[1] - 1.4) for i in range(0, len(PROFILE), 2)],
             *PITS, *[s[0] for s in STANDARDS], (2.5, 19.6), (4.0, 19.0), (0.5, 19.0)]
    rift_lane = [[RIFT_A[0] + (RIFT_B[0] - RIFT_A[0]) * kk / 8, RIFT_A[1] + (RIFT_B[1] - RIFT_A[1]) * kk / 8 + dz, 2.2] for kk in range(9) for dz in (0.0, 2.6)]
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": [[H, 24]], "max": 30, "base": 24, "centers": [[-9.5, -1.0], [-8.4, 1.2]], "skin": "sheep"},
        "pred": [[H, 1]],
        "predators": [{"id": "g1", "scale": 1.3, "keys": g_now, "adorn": True}],
        "series": {"finds": finds, "questions": questions, "tradeH": [[H, 4]]},
        "settlement": human_valley,
        "people": {"count": [[H, 30], [WIPE, 30]], "centers": CROWD, "spread": 1.6, "life": 70, "lamps": [[H, 1]],
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
                  {"kind": "ruin", "x": RUIN[0], "z": RUIN[1], "face": 20, "r": 2.2, "rise": [[H, 1]]},
                  {"kind": "wall", "x": WALL_A[0], "z": WALL_A[1], "to": list(WALL_B), "profile": PROFILE, "fresh": FRESH, "tonight": TONIGHT,
                   "log": log, "glow": glow, "place": place},
                  {"kind": "find", "find": "gear", "x": GEAR[0], "z": GEAR[1], "face": 0, "r": 2.2, "rise": unearth(G_UP)},
                  {"kind": "find", "find": "kitchen", "x": KITCHEN[0], "z": KITCHEN[1], "face": 0, "r": 2.2, "rise": unearth(K_UP, 1.0)},
                  {"kind": "find", "find": "wells", "x": WELLS[0], "z": WELLS[1], "face": 0, "r": 2.2, "rise": unearth(W_UP)},
                  {"kind": "find", "find": "hands", "x": HANDS[0], "z": HANDS[1], "face": 0, "r": 2.2, "y": 0.8, "rise": unearth(H_UP, 0.5)},
                  *pits,
                  *[{"kind": "standard", "x": p[0], "z": p[1], "face": 90, "color": c, "size": 0.42, "rise": std} for p, c in STANDARDS]],
        "fears": fears,
        "clearTrees": [[d[0], d[1], 2.2] for d in clear] + rift_lane,
        "layers": {"ripple": ripple, "rings": [], "dust": dust},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "TOOLS", "text": "a gear we can't make", "at": cue("L8", "tools.")},
    {"n": 2, "label": "VALUES", "text": "one table for all", "at": cue("L9", "valued.")},
    {"n": 3, "label": "A FAILURE", "text": "wells full of sand", "at": cue("L10", "failed.")},
    {"n": 4, "label": "DAILY LIFE", "text": "a child's hands", "at": cue("L11", "days.")},
    {"n": 5, "label": "A SECRET", "text": "never say who", "at": cue("L7", "Four"), "locked": True, "unlockAt": cue("L15", "who.", -0.1)},
]
SLOTS = [
    {"icon": "gear", "kind": "TOOLS", "text": "a gear we can't make", "at": shift(cue("L8", "gear"), 0.5)},
    {"icon": "pot", "kind": "VALUES", "text": "one table for all", "at": shift(cue("L9", "kitchen."), 0.1)},
    {"icon": "well", "kind": "FAILURE", "text": "wells full of sand", "at": shift(cue("L10", "sand."), 0.0)},
    {"icon": "handprint", "kind": "DAILY LIFE", "text": "a child's hands", "at": shift(cue("L11", "handprints,"), 0.2)},
    {"icon": "stone", "kind": "WHO?", "text": "no answer", "locked": True, "unlockAt": shift(NIGHT, 0.5)},
]
SPRITE = {"sprite": "ep35/builders_sprite.png", "spriteW": 120, "spriteH": 96}


def tag(text, head, at, end, pos, lift=90, dx=0, **kw):
    return {"kind": "ground", "text": text, "head": head, "at": at, "end": end, "pos": list(pos), "lift": lift, "dx": dx, "color": QUARTZ, "headColor": QUARTZ, **kw}


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "OLDER THAN US", "color": STONE_C, "size": 64, "pulseAt": cue("L1", "older")},
                 {"text": "WHO REPAIRS IT?", "color": QUARTZ, "size": 60, "pulseAt": cue("L1", "repairing")}]
    fresh_pos = (COLX(FRESH[0]), WALL_A[1] + 0.2, 0.22 + 0.5 * FRESH[1] + 0.35)
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 60, "start": {"shot": "hook"}, "end": cue("L2", "Meet", -0.1), "preShow": True},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 35 · RUINS", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "skyTags", "start": cue("L1", "repairing", 0.1), "end": RESET, "tags": [tag("LAST NIGHT", "NEW STONE", cue("L1", "repairing", 0.1), cue("L2", "Meet", -0.1), fresh_pos, lift=-150, dx=230)]},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Meet", -0.05), "end": RESET, "dietAt": cue("L2", "stands."),
         "kicker": "FIELD CARD · NO. 010", "kind": "LOST CIVILIZATION", "name": "THE BUILDERS", "dietLabel": "LEFT", "diet": "one wall, still standing", **SPRITE},
    ]
    G["setup"] += [
        {"type": "blockWipe", "at": RESET, "dur": 0.34, "color": "#3a3326"},
        {"type": "kinetic", "parts": [{"text": "ANCIENT", "at": cue("L3", "ancient,"), "size": 64, "color": STONE_C}, {"text": "MYSTERIOUS", "at": cue("L3", "mysterious,"), "color": "parchment", "size": 64},
                                      {"text": "GONE", "at": cue("L3", "gone."), "color": "rust", "size": 80}],
         "y": 460, "size": 64, "start": cue("L3", "ancient,", -0.05), "end": cue("L4", "Press", -0.15)},
        {"type": "simBar", "counters": [{"icon": "gear", "label": "FINDS", "key": "finds", "color": QUARTZ, "digits": 2},
                                        {"icon": "query", "label": "QUESTIONS", "key": "questions", "color": "ember", "digits": 2}],
         "compact": True, "start": cue("L4", "Press", -0.15), "end": cue("L16", "Show", -0.3), "runAt": [cue("L4", "run."), cue("L12", "Run")]},
        {"type": "findsTray", "y": 1352, "slots": SLOTS, "start": shift(RESET, 0.3), "end": cue("L16", "Show", -0.3), "askAt": cue("L12", "Every"), "lockedText": "THE TWIST"},
    ]
    G["run1"] += [
        {"type": "kinetic", "parts": [{"text": "1,000 YEARS", "at": cue("L5", "thousand"), "color": "parchment", "size": 56},
                                      {"text": "OF DIGGING", "at": cue("L5", "digging."), "color": "parchment", "size": 56},
                                      {"text": "JUST STONES", "at": cue("L5", "Nothing"), "color": "rust", "size": 56}],
         "y": 468, "size": 56, "start": cue("L5", "A", -0.05), "end": cue("L6", "A", -0.25)},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "JUST ROCKS", "sub": "0 FINDS · 0 QUESTIONS · 0 PEOPLE", "color": "rust", "y": 560, "size": 84, "start": cue("L6", "nothing"), "end": cue("L6", "rocks.", 0.55)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "rocks.", 0.6), "end": cue("L7", "Good", 0.3)},
        {"type": "blockWipe", "at": cue("L6", "rocks.", 0.58), "dur": 0.34},
        {"type": "kinetic", "parts": [{"text": "GOOD RUINS", "at": cue("L7", "Good"), "size": 78, "color": STONE_C}, {"text": "TALK", "at": cue("L7", "talk."), "color": QUARTZ, "size": 96}],
         "y": 470, "size": 84, "start": cue("L7", "Good", -0.05), "end": cue("L7", "Four", -0.15)},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L16", "Show", -0.3),
         "kicker": "THE BUILDERS · WHAT THEY LEFT", "title": "READ THE RUINS", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L8", "One:", -0.3), 0], [cue("L8", "One:", 0.0), 1], [ROLE, 1], [shift(ROLE, 0.3), 0]]},
    ]
    G["tools"] += [{"type": "skyTags", "start": shift(cue("L8", "gear"), 0.4), "end": cue("L9", "Two:", -0.15), "tags": [
        tag("NO FORGE HERE", "FIND 01 · TOOLS", shift(cue("L8", "gear"), 0.4), cue("L9", "Two:", -0.15), (GEAR[0], GEAR[1], 1.9), lift=-170, dx=200)]}]
    G["values"] += [{"type": "skyTags", "start": cue("L9", "kitchen."), "end": cue("L10", "Three:", -0.15), "tags": [
        tag("ONE TABLE FOR ALL", "FIND 02 · VALUES", cue("L9", "kitchen."), cue("L10", "Three:", -0.15), (KITCHEN[0], KITCHEN[1], 0.7), lift=-260, dx=60)]}]
    G["failure"] += [{"type": "skyTags", "start": cue("L10", "full"), "end": cue("L11", "Four:", -0.15), "tags": [
        tag("THE WATER RAN OUT", "FIND 03 · FAILURE", cue("L10", "full"), cue("L11", "Four:", -0.15), (WELLS[0], WELLS[1], 0.6), lift=-260, dx=80)]}]
    G["days"] += [{"type": "skyTags", "start": cue("L11", "handprints,", 0.2), "end": cue("L12", "Run", -0.15), "tags": [
        tag("A CHILD WAS HERE", "FIND 04 · DAILY LIFE", cue("L11", "handprints,", 0.2), cue("L12", "Run", -0.15), (HANDS[0] - 0.1, HANDS[1], 1.05), lift=-330, dx=-60)]}]
    G["run2"] += [
        {"type": "stamp", "text": "MORE QUESTIONS", "sub": "1,000 YEARS · 16 FINDS · 32 QUESTIONS", "color": QUARTZ, "rotate": -4, "y": 880, "size": 84, "start": cue("L12", "questions."), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}, {"text": "LOOK CLOSER", "at": cue("L13", "Look"), "color": "parchment", "size": 64}],
         "size": 150, "y": 500, "start": cue("L13", "Rule", -0.02), "end": cue("L13", "Half", -0.1)},
        {"type": "kinetic", "parts": [{"text": "NEWER", "at": cue("L13", "newer"), "color": QUARTZ, "size": 96}, {"text": "THAN US", "at": cue("L13", "us."), "color": "parchment", "size": 64}],
         "size": 96, "y": 540, "start": cue("L13", "newer", -0.05), "end": cue("L14", "Someone", -0.1)},
        {"type": "skyTags", "start": shift(LOG, 0.3), "end": ROLE, "tags": [
            tag("HALF OF IT IS NEW", "THE REPAIR LOG", shift(LOG, 0.3), cue("L14", "Someone", -0.1), (COLX(3), WALL_A[1] + 0.2, 3.6), lift=-120, dx=120),
            tag("ONE MORE STONE", "LAST NIGHT", shift(NIGHT, 0.4), cue("L14", "Nobody", -0.05), (COLX(TONIGHT[0]), WALL_A[1] + 0.2, 0.22 + 0.5 * TONIGHT[1] + 0.3), lift=-200, dx=-120),
            tag("NOBODY SEEN", "WHO?", cue("L14", "Nobody"), ROLE, (COLX(TONIGHT[0]), WALL_A[1] + 0.2, 0.22 + 0.5 * TONIGHT[1] + 0.3), lift=-200, dx=-120)]},
    ]
    G["role"] += [
        {"type": "followChip", "start": cue("L15", "who.", 0.2), "end": cue("L16", "Every", 0.3), "text": "FOLLOW", "sub": "PART 35/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "Show", -0.3), **({"unlockAt": cue("L16", "Show", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "Show", -0.3), "end": WIPE, "kicker": "BEFORE YOU BURY A CIVILIZATION", "title": "THE BUILDERS", **SPRITE,
         "subtitle": "Every ruin keeps one secret.", "subtitleAt": cue("L16", "fell.")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 35 / 50",
         "title": "Give Your World a Lost Civilization", "cta": "COMMENT", "icon": "bubble", "with": "One find. Name it.", "withAt": cue("L17", "world?", -0.05), "choiceSize": 30,
         "choices": [{"text": "OUR OWN NAMES", "color": QUARTZ, "at": cue("L17", "never")}, {"text": "A WARM HEARTH", "color": STONE_C, "at": cue("L17", "find")}]},
    ]
    gone = cue("L18", "enough.", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 35, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6, "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone, "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 36"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "36:", -0.1), "revealAt": cue("L18", "armies"), "end": gone,
         "kicker": "NEXT RUN · 36", "title": "THE WAR", "sub": "MORE THAN TWO SIDES.", "sprite": "banners", "spritePx": 7},
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 60, "start": cue("L18", "enough.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("A lost civilization that is only ancient and mysterious is just rocks. Let its remains say who they were: a "
          "tool nobody can make now (technology), the room they built biggest (values), how it ended (failure) and one "
          "small trace of an ordinary day. Then leave one question open and never answer it. Every ruin keeps one secret.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Close EP34's loop (broken pillars rose on 'the ruins are older than us') and stop the scroll on the mystery.",
             "Golden hour, looking north at a long broken wall of squared stone south of the lake: EP34's pillars stand for good at its east end, the gear's pit, the kitchen and the sand-filled wells lie dug in front of it, and one stone high in the wall is newer than the rest and glows faintly quartz cyan. OLDER THAN US / WHO REPAIRS IT? from frame 0, each line pulsing on its word; the new stone flares on 'repairing' (NEW STONE · LAST NIGHT). Then the field card: THE BUILDERS · LOST CIVILIZATION · LEFT: one wall, still standing.",
             "Frontal (az 0, el 13, fov 20), sliding slowly west along the wall's top.", ("kinetic, sting, tag, field card", "the wall and its finds", "the lake, the valley, the peak"),
             "Golden hour.", "OLDER THAN US / WHO REPAIRS IT? · FIELD CARD NO. 010 · THE BUILDERS", "Umber block wipe into the lazy version.", "Hollow: a blown bottle and vibraphone echoes over a contrabass drone; a hit on 'repairing'."),
    "setup": ("The lazy version: ancient, mysterious, gone.",
              "A wipe to the bare wall: nothing dug in front of it, no new stone, nothing to read. ANCIENT / MYSTERIOUS / GONE pop on their words. The finds tray slides in under the world, EMPTY; the sim bar arrives (FINDS 00, QUESTIONS 00) and RUN is pressed.",
              "The same frontal pose, sliding east along the bare wall.", ("kinetic, sim bar, finds tray", "the bare wall", "the Isle"), "Day.", "ANCIENT · MYSTERIOUS · GONE · THE FINDS TRAY: EMPTY", "A cut to the whole Isle on 'run'.", "Hollow, thinner."),
    "run1": ("Run the lazy version: a thousand years of digging and nothing to find.",
             "The whole Isle; YEAR 500→1500; the tray stays EMPTY. 1,000 YEARS / OF DIGGING / JUST STONES.",
             "Wide (dist 160, fov 22), sliding east across the Isle.", ("sim bar, kinetic, tray", "the Isle", "the void"), "Day.", "1,000 YEARS / OF DIGGING / JUST STONES", "Gloom.", "Drive."),
    "drop": ("The punchline: a ruin that says nothing is just rocks.", "Gloom: JUST ROCKS · 0 FINDS · 0 QUESTIONS · 0 PEOPLE, over the empty tray.",
             "Wide, the slide easing to a stop.", ("stamp, tray", "the Isle", "the void"), "Gloom.", "JUST ROCKS · 0 FINDS · 0 QUESTIONS · 0 PEOPLE", "Rewind + block wipe.", "Drop; a boom on 'rocks'."),
    "rehook": ("Re-hook: the thesis, four rules, one locked.",
               "REWIND. GOOD RUINS / TALK; then the checklist READ THE RUINS, row 5 locked (the twist); the tray's fifth compartment is locked too.",
               "Wide, sliding back west.", ("rewind, kinetic, checklist, tray", "the Isle", "the void"), "Day.",
               "GOOD RUINS TALK · READ THE RUINS 0/5", "Cut to the wall's west end.", "Survey, bare (a nylon guitar walking in eighths); a riser into 'the twist'."),
    "tools": ("Rule 1: their tools (technology).", "The wall's west end: on 'gear' a toothed bronze wheel rises half out of a dug pit (FIND 01 · TOOLS · NO FORGE HERE) and drops into the tray's first compartment.",
              "Cut, then the slide begins: the camera trucks east to the gear.", ("tag, checklist (folded), tray", "the gear in its pit", "the wall"), "Day.", "1 TOOLS · a gear we can't make", "Slide east.", "Survey 1: a nylon guitar."),
    "values": ("Rule 2: what they valued.", "Sliding east: on 'biggest' a great room's foundations rise in front of the wall, one long table for everyone, benches, bowls and a hearth with a great pot (FIND 02 · VALUES · ONE TABLE FOR ALL).",
               "A slide east along the wall (no cut).", ("tag, checklist (folded), tray", "the kitchen", "the wall"), "Day.", "2 VALUES · one table for all", "Slide east.", "Survey 2: a walking acoustic bass."),
    "failure": ("Rule 3: how they failed.", "Sliding east: on 'well' two stone wells rise, each filled to the brim with sand, sand drifting against the wall (FIND 03 · FAILURE · THE WATER RAN OUT).",
                "A slide east (no cut).", ("tag, checklist (folded), tray", "the wells", "the wall"), "Day.", "3 A FAILURE · wells full of sand", "Slide east, then in.", "Survey 3: brushes and a ride."),
    "days": ("Rule 4: their days.", "Sliding east and in to the wall's face: on 'child's' a mortar patch with two small handprints shows on a low block (FIND 04 · DAILY LIFE · A CHILD WAS HERE).",
             "A slide east that eases in to the wall's face (el 8).", ("tag, checklist (folded), tray", "the handprints", "the wall"), "Day.", "4 DAILY LIFE · a child's hands", "Cut to the whole Isle.", "Survey 4: the theme on vibraphone."),
    "run2": ("Run with the remains talking: a thousand years of digging, and every find opens two questions.",
             "The whole Isle; YEAR 500→1500; pits open round the site one after another; FINDS 4→16 and QUESTIONS 4→32; in the tray every find sprouts two question marks. MORE QUESTIONS · 1,000 YEARS · 16 FINDS · 32 QUESTIONS, stamped in quartz.",
             "Wide, sliding west.", ("sim bar, tray, stamp", "the dig spreading", "the Isle"), "Day.", "MORE QUESTIONS · 1,000 YEARS · 16 FINDS · 32 QUESTIONS", "Cut to dusk.", "Drive with the theme; a stab and a cymbal on 'questions'."),
    "twist": ("The locked rule: half this wall is newer than us.",
              "Dusk, the whole wall: RULE 5? LOOK CLOSER; on 'Half' the repair log lights: every original stone sinks to umber and every repair glows quartz cyan by how recent it is, half the wall (THE REPAIR LOG · HALF OF IT IS NEW; NEWER THAN US). Night falls; the camera slides to the gap at the top of the wall, and on 'night' one more stone settles into it, bright (LAST NIGHT · ONE MORE STONE); nobody is there (WHO? · NOBODY SEEN). The tray's fifth compartment opens: WHO? · no answer.",
              "Cut, then slides east along the wall to the gap.", ("kinetic, tags, tray", "the glowing repairs, the new stone", "the dark Isle"), "Dusk, then night.",
              "RULE 5? LOOK CLOSER · NEWER THAN US · THE REPAIR LOG · LAST NIGHT · WHO?", "Day on 'So'.", "Twist (a held A7♭9), then hollow at night with the theme on the blown bottle."),
    "role": ("Unlock rule 5: never say who.",
             "Day returns and the log fades; the checklist opens and row 5 unlocks on 'who': A SECRET · never say who · 5/5. The follow chip (+ FOLLOW · PART 35/50) after 'who'.",
             "A slide east along the wall.", ("open checklist, follow chip, tray", "the wall", "the Isle"), "Day.", "5 A SECRET · never say who · 5/5", "The card goes full.", "Anthem from 'So'; a D-major hit on 'who'."),
    "lesson": ("The takeaway.", "The full card (BEFORE YOU BURY A CIVILIZATION · THE BUILDERS, all five rows ticked) over the whole Isle in golden light, with 'Every ruin keeps one secret.' in serif italic from the end of the first sentence.",
               "Wide: one slow slide east.", ("full card, follow chip", "the Isle", "the void"), "Golden hour.", "BEFORE YOU BURY A CIVILIZATION · THE BUILDERS · Every ruin keeps one secret.", "Block wipe to the end card.", "Anthem; the World Engine chime as the card lands."),
    "cta": ("Comment CTA: what should archaeologists never find in your world?", "End card: logo, PART 35 / 50, the title, and a COMMENT panel where OUR OWN NAMES and A WARM HEARTH pop as starters, then 'One find. Name it.'",
            "Cut (under the block wipe) to the hook pose, sliding back onto it.", ("end card", "the wall", "the Isle"),
            "Golden hour (the loop frame).", "COMMENT · OUR OWN NAMES / A WARM HEARTH · One find. Name it.", "The card lifts on 'Part'.", "Outro."),
    "next": ("Say the part number, ask for the follow with a reason (part 36), open the next loop.",
             "The hook frame; PART 35/50; FOLLOW FOR PART 36, pressed on 'Follow'; NEXT RUN · 36 decodes from three locked banners to THE WAR · MORE THAN TWO SIDES. In the world, on 'armies', three standards in three colours rise on three meadows behind the wall and the war horn calls; the Queen looks up; they sink back before the hook title returns.",
             "The hook frame.", ("progress bar, follow button, next-run card", "the wall", "three standards rising"), "Golden hour.",
             "PART 35/50 · FOLLOW FOR PART 36 · NEXT RUN: THE WAR · MORE THAN TWO SIDES.", "Loop to frame 0.", "Tease over a held A; a horn call on 'armies'; the engine chime on 'Follow'."),
}


def build():
    ep = {
        "id": "ep35", "number": 35, "season": 2,
        "title": "Give Your World a Lost Civilization",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.0},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same lab host, quieter this time, like someone walking a dig at dusk. The hook is a mystery stated, not asked. 'Ancient, mysterious, gone' is a dry list of clichés; 'just rocks' lands flat. "
                         "The rules are crisp, two beats each, with a little wonder on the kitchen and the handprints. 'Half this wall is newer than us' is the chill; 'Nobody has seen them' is almost a whisper. The comment ask is playful.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L3", "from": "ancient,"}, {"line": "L5", "from": "A"}, {"line": "L7", "from": "Good", "to": "Four"}, {"line": "L13", "from": "Rule"}],
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
             hit("stoneSet", cue("L1", "older", -0.1), -19), hit("logOn", cue("L1", "repairing", -0.05), -15),
             hit("cardSlide", cue("L2", "Meet", -0.05), -18), hit("check", cue("L2", "stands."), -20)],
    "setup": [hit("rewind", RESET, -15), hit("trayDrop", shift(RESET, 0.35), -22),
              hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "stones.", 0.3), -22), bed("rumble", cue("L5", "A"), cue("L5", "digging.", 0.3), -24), hit("stamp", cue("L5", "Nothing"), -21)],
    "drop": [hit("stamp", cue("L6", "nothing"), -10)],
    "rehook": [hit("rewind", cue("L6", "rocks.", 0.55), -11), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "tools": [hit("check", cue("L8", "tools."), -13), hit("dig", cue("L8", "gear"), -14), hit("trayDrop", shift(cue("L8", "gear"), 0.5), -14)],
    "values": [hit("check", cue("L9", "valued."), -13), hit("stoneRise", cue("L9", "biggest", -0.1), -15), hit("trayDrop", shift(cue("L9", "kitchen."), 0.1), -14)],
    "failure": [hit("check", cue("L10", "failed."), -13), hit("dig", cue("L10", "well"), -15), bed("sandPour", cue("L10", "full"), cue("L10", "sand.", 0.4), -20), hit("trayDrop", cue("L10", "sand."), -14)],
    "days": [hit("check", cue("L11", "days."), -13), hit("restore", cue("L11", "child's"), -18), hit("trayDrop", shift(cue("L11", "handprints,"), 0.2), -14)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L12", "questions."), -22),
             hit("dig", cue("L12", "A", 0.1), -20), hit("dig", cue("L12", "years.", -0.1), -20), hit("dig", cue("L12", "find"), -20),
             hit("check", cue("L12", "Every", 0.1), -19), hit("check", cue("L12", "opens"), -19), hit("stamp", cue("L12", "questions."), -13)],
    "twist": [hit("unlock", cue("L13", "Rule"), -15), hit("logOn", LOG, -10), hit("stoneSet", NIGHT, -11), hit("unlock", shift(NIGHT, 0.5), -17)],
    "role": [hit("restore", ROLE, -17), hit("unlock", cue("L15", "who.", -0.1), -10)],
    "lesson": [hit("engineWind", cue("L16", "Show", -0.8), -15), hit("chime", cue("L16", "Show", -0.3), -10), hit("cardSlide", cue("L16", "Show", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("check", cue("L17", "never"), -17), hit("check", cue("L17", "find"), -17)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11), hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "36:", -0.1), -18), hit("unlock", cue("L18", "armies"), -15),
             hit("stoneRise", cue("L18", "armies", -0.1), -17),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score: the series theme stays (D minor for the problem, D major for the payoff). EP35's band is `hollow` (wind
# through an empty ruin: a blown bottle carrying the theme, vibraphone notes echoing off stone, a warm pad and a
# contrabass drone) and `survey` (the walk along the wall, one family per rule: a nylon guitar walking in eighths, a
# walking acoustic bass, brushes and a ride, the theme on vibraphone). At the twist, hollow returns at night.
HOLLOW_P = {"lead": 76, "strings": 89, "cello": 43, "celesta": 11}
SURVEY_P = {"marimba": 24, "lead": 11, "celesta": 11}
BACK_P = {"strings": 48, "marimba": 12, "lead": 73, "cello": 42, "celesta": 8}
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 92,
    "sections": [
        msec({"shot": "hook"}, "hollow", ["Dm", "Bb", "Gm", "A"], "D minor", programs=HOLLOW_P),
        msec(RESET, "hollow", ["Dm", "C", "Bb", "A"], "D minor", bars=(2, 4), thin=True),
        msec(cue("L4", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.85, programs=BACK_P),
        msec(cue("L6", "A", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "rocks.", 0.55), "survey", ["Dm", "C", "Bb", "A"], "D minor", layer=1, programs=SURVEY_P),
        msec(cue("L8", "One:", -0.1), "survey", ["Dm", "C", "Bb", "C"], "D minor", layer=1),
        msec(cue("L9", "Two:", -0.1), "survey", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "survey", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L11", "Four:", -0.1), "survey", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True, programs=BACK_P),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(cue("L14", "Someone", -0.1), "hollow", ["Dm", "Bb", "Gm", "A"], "D minor", programs=HOLLOW_P),
        msec(cue("L15", "So", -0.1), "anthem", ["D", "G", "Bm", "A"], "D major", programs=BACK_P),
        msec(cue("L17", "What", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "repairing"), "chord": "Dm"},
        {"kind": "boom", "at": cue("L6", "rocks."), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "questions."), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "questions.")},
        {"kind": "boom", "at": LOG, "chord": "Dm"},
        {"kind": "hit", "at": cue("L15", "who."), "chord": "D"},
        {"kind": "call", "at": cue("L18", "armies"), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #WritingTips #Lore #WorldcraftShorts"
IG_HOOK = "These ruins are older than humans. Someone keeps repairing them."
BODY = (
    "These ruins are older than humans. Someone keeps repairing them.\n\n"
    "Meet the Builders: their wall still stands. The lazy version of a lost civilization is ancient, mysterious and "
    "gone, and we ran it: a thousand years of digging, nothing but stones. A ruin that says nothing is just rocks.\n\n"
    "Good ruins talk. Their tools: a gear that nobody here can make. What they valued: their biggest room was a "
    "kitchen. How they failed: every well is full of sand. Their days: a child's handprints, pressed into the mortar. "
    "Run it again: a thousand years, and every find opens two questions.\n\n"
    "Then the twist: look closer. Half this wall is newer than us. Someone replaces one stone every night, and nobody "
    "has seen them. So never tell us who.\n\n"
    "Show how they lived and fell. Every ruin keeps one secret.\n\n"
    "What is the one thing archaeologists should never find in your world?\n\n"
    "Part 35 of 50. Follow for part 36: two armies are never enough."
)
METADATA = {
    "youtube": {
        "title": "Give Your World a Lost Civilization (Worldbuilding)",
        "titleAlternate": "These ruins are older than humans. Someone keeps repairing them.",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 7: History and Mythology (the arc's last episode). The "
        "Builders, their wall and everything found in it are invented for this video; no real civilization, ruin or "
        "script is depicted.\n\n" + TAGS,
        "pinnedComment": "What is the one thing archaeologists should never find in your world? One find, then why. (Part 36: two armies are never enough.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated field-card sprite; the island, the ruins, the finds and the people are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "These ruins are older than humans. Someone keeps repairing them. 🧱 Four rules for a lost civilization that talks, and rule #5 is the twist. "
                   "What should archaeologists never find in your world? Part 35/50 · follow for part 36 ⚔️ " + TAGS,
        "pinnedComment": "What is the one thing archaeologists should never find in your world?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "Which question would you never answer about your lost civilization?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": IG_HOOK + "\n\n" + BODY.split("\n\n", 1)[1] + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": f"First {len(IG_HOOK)} characters: '{IG_HOOK}'",
        "pinnedComment": "Save the READ THE RUINS card, then tell us: what is the one thing archaeologists should never find in your world?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep35] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots, loop span {loop_span():.2f} s")
