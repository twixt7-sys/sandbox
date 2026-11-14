"""Generate episodes/ep31/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep31/make_ep31.py
EP31 opens Arc 7 (History and Mythology) and is the season's REFERENCE EPISODE (see BRIEF.md: the benchmark scorecard).
Its own device is THE TWO CHRONICLES: two open pages under the world, one per teller, recording the same night. Each
fact is written, never written, or lost on each page, and the spine counts how many facts the two pages still agree on.
In the world, a WITNESS VEIL hatches out the half of the frame a witness never saw. Camera language: THE SPLIT FRAME,
everything staged frontally on one centre line, the valley's telling on the left and the court's on the right (EP26
orbited, EP27 rode a dragon, EP28 sat at eye height, EP29 was a locked-off tripod, EP30 looked up). Motif colour:
chronicle ink #7f95ff. Music band: `chronicle` (lute, tambourine, the theme on recorder) and `dispute` (the theme split
between a recorder and a bassoon that never quite agree).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep31" / "timing.json"
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
    ("L1", "hook", "What if history's greatest hero was also its worst monster?", 0.3, ["hero", "monster?"]),
    ("L2", "hook", "Meet Maren. Three hundred years ago, she did one thing.", 0.3, ["maren.", "one"]),
    ("L3", "setup", "The lazy version: one history, and everybody agrees.", 0.25, ["lazy", "agrees."]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "Three hundred years. One statue. One story. Zero questions.", 0.35, ["story.", "zero"]),
    ("L6", "drop", "Case closed. Nothing left to solve.", 0.4, ["closed.", "solve."]),
    ("L7", "rehook", "Real history has witnesses. Four rules crack it open. The fifth is the twist.", 0.25, ["witnesses.", "twist."]),
    ("L8", "witness", "One: witnesses. The valley saw her drive the monster off. The court saw their fields burn.", 0.2, ["valley", "court"]),
    ("L9", "motive", "Two: motive. Each side keeps the half that flatters it.", 0.2, ["motive.", "flatters"]),
    ("L10", "loss", "Three: loss. Pages burn. Witnesses die.", 0.2, ["burn.", "die."]),
    ("L11", "retell", "Four: retelling. Every generation makes her bigger.", 0.3, ["retelling.", "bigger."]),
    ("L12", "run2", "Run it again. One night. Two histories.", 0.3, ["one", "two"]),
    ("L13", "twist", "Rule five? The truth. She did both.", 0.3, ["truth.", "both."]),
    ("L14", "twist", "She burned the fields to drive it off. Now hide that from your world.", 0.3, ["burned", "hide"]),
    ("L15", "role", "Let your characters fight over the pieces.", 0.3, ["fight", "pieces."]),
    ("L16", "lesson", "History isn't what happened. It's who's telling it.", 0.35, ["happened.", "telling"]),
    ("L17", "cta", "Hero or monster? Give us your verdict.", 0.25, ["hero", "verdict."]),
    ("L18", "next", "Part 31 of 50. Follow for part 32: a war that never ended.", 0.25, ["follow", "never"]),
]
SHOTS = ["hook", "setup", "run1", "drop", "rehook", "witness", "motive", "loss", "retell", "run2", "twist", "role", "lesson", "cta", "next"]

# The block wipe into the end card: the world resets to frame 0 under it (the statue as it stands today).
WIPE = cue("L17", "Hero", -0.3)
AFTER = cue("L17", "Hero", -0.28)
RESET = cue("L3", "lazy", -0.15)          # the lazy version: one plain statue, one story
REWIND = cue("L6", "solve.", 0.55)        # back to the night itself
NIGHT2 = cue("L13", "She", -0.1)          # the twist: the night again, unveiled
TODAY = cue("L15", "Let", -0.15)
HOOK_DRIFT = 0.6

# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle (it remembers): EP27's humans in the valley under the cliff, EP28's Fenn in their hall on the
# lake, the cairn, EP29's Undying Queen on her dais, EP30's worshipped Grimmaw (today on the north-west meadow). EP31
# stands Maren's statue on the south-east meadow, on the spot where she stood that night. Every frontal pose looks due
# north along the statue's centre line, so the valley's side (west) is always the left of the frame and the court's
# (east) the right; the dais, the cairn and the Fenn's hall all fall outside those frames (checked by projection).
CAIRN = (8.95, -5.38)
LAKE_HALL = (6.0, 4.6)
HUMAN_B = [("hall", (-3.6, -4.6)), ("house", (-1.8, -2.4)), ("house", (-4.8, -2.4)), ("house", (-1.0, -5.8)),
           ("house", (-5.6, -0.9)), ("house", (-3.4, -0.7)), ("house", (0.4, -4.2))]
HUMAN_TOWER = (-6.4, -5.6)
HUMAN_ROAD = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
DAIS = (9.4, -2.2)
QUEEN = (9.1, -2.2)
AZ = 0                                   # the centre line: every frontal camera looks due north
STATUE = (18.0, 1.5)
FACE = AZ - 90                           # the statue faces the camera: its gilded half is screen-left
G_NOW = (8.5, -9.6)                      # the Grimmaw today (EP30's worshipped beast), out of the frontal frames
G_THEN = (14.2, 0.2)                     # that night: on the meadow, screen-left of Maren, facing her
G_FLED = (7.0, 0.3)                      # where she drove it: west along the shore, out of the left of the frame
FIELD = (20.9, -0.4, 3.4, 3.4)           # the court's field, screen-right of her
ARCH_L, ARCH_R = (14.6, -4.2), (20.4, -4.4)      # the two archives behind the statue (rule 3)
CROWD = [[15.2, 3.6], [20.8, 3.6]]       # the valley's people (left, in wheat gold) and the court's (right, in rust)
STD_L, STD_R = (15.0, 2.2), (21.0, 2.2)  # the EP32 tease: two war standards, one raised by each side
INK = "#7f95ff"
GOLD = "#f4c46e"
RUST = "#d0603f"


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


def loop_span():
    """Seconds from the wipe to the end: the loop camera key drifts this long and lands exactly on the hook pose."""
    if not TIMING.exists():
        return 6.0
    tm = json.loads(TIMING.read_text())
    ln = next(l for l in tm["lines"] if l["id"] == WIPE["line"])
    w = next(w for w in ln["words"] if w["text"].strip(".,?!:").lower() == WIPE["word"].lower())
    return tm["duration"] - (w["start"] + WIPE.get("offset", 0.0))


# The frontal poses (az 0). px/unit and the statue's place in the frame were computed for each (BRIEF.md §6).
HOOK_POSE = dict(el=9, dist=76, target=(18.0, 8.6, 1.5), fov=15)        # the split statue under the title
MEDIUM = dict(el=12, dist=60, target=(18.0, 7.6, 1.5), fov=20)          # the plain statue and both crowds
DROP_POSE = dict(el=20, dist=53, target=(18.0, 7.6, 1.5), fov=20)
NIGHT_POSE = dict(el=22, dist=60, target=(18.25, 5.8, 1.5), fov=22)      # the whole night in one frame, held
MOTIVE_POSE = dict(el=9, dist=56, target=(18.0, 6.8, 1.5), fov=16)
LOSS_POSE = dict(el=16, dist=64, target=(18.0, 7.2, 0.5), fov=20)
RETELL_POSE = dict(el=9, dist=68, target=(18.0, 7.5, 1.5), fov=16)
TWIST_POSE = dict(el=6, dist=60, target=(18.0, 10.1, 1.5), fov=12)             # close on the split face and the two torches
ROLE_POSE = dict(el=9, dist=76, target=(18.0, 9.95, 1.5), fov=15)             # the hook framing, lowered to sit under the open card
WIDE = dict(el=48, dist=196, target=(4.0, 10.5, 0.0), fov=26)


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    lin = lambda at, v: [at, v, "linear"]
    H = shot("hook")
    T2 = cue("L9", "Two:", -0.1)          # the cut from that night back to the statue

    # ---- the clock (YEARS since that night). Today is year 300.
    clock = [[H, 300], *jump(RESET, 300, 0), [cue("L4", "run."), 0], lin(cue("L5", "hundred"), 100), lin(cue("L5", "statue."), 200), lin(cue("L5", "Zero"), 300), *jump(REWIND, 300, 0),
             [cue("L10", "Witnesses", -0.1), 0], lin(cue("L10", "die.", 0.3), 70), [cue("L11", "Every", -0.1), 70], lin(cue("L11", "bigger.", 0.3), 300),
             *jump(cue("L12", "Run", -0.05), 300, 0), [cue("L12", "Run", 0.1), 0], lin(cue("L12", "histories.", 0.2), 300),
             *jump(NIGHT2, 300, 0), *jump(TODAY, 0, 300), [WIPE, 300]]
    speed = [[H, 1], [cue("L4", "run."), 1], [cue("L4", "run.", 0.35), 6], [cue("L5", "Zero", 0.0), 6], [cue("L6", "Case"), 1],
             [cue("L12", "Run", 0.1), 1], [cue("L12", "Run", 0.4), 6], [cue("L12", "histories.", 0.2), 6], [cue("L13", "Rule"), 1]]
    # HUD: how many tellings exist, and how many questions are still open (a closed case has none)
    tellings = [[H, 2], *jump(RESET, 2, 1), *jump(REWIND, 1, 0), *jump(cue("L8", "off.", -0.1), 0, 1), *jump(cue("L8", "fields", 0.0), 1, 2), [WIPE, 2]]
    questions = [[H, 40], *jump(RESET, 40, 0), [cue("L8", "fields", 0.0), 0], [cue("L8", "burn.", 0.2), 4], [cue("L9", "flatters", 0.0), 4], [cue("L9", "it.", 0.1), 8],
                 [cue("L10", "burn.", 0.0), 8], [cue("L10", "die.", 0.2), 14], [cue("L11", "Every", 0.0), 14], [cue("L11", "bigger.", 0.2), 20],
                 [cue("L12", "Run", 0.1), 20], lin(cue("L12", "histories.", 0.2), 40), [WIPE, 40]]

    # ---- the statue: today it is gilded on the valley's side, tarred on the court's, and a third taller
    rise = [[H, 1], *jump(REWIND, 1, 0), [T2, 0], [cue("L9", "Two:", 0.4), 1, "out"], *jump(NIGHT2, 1, 0), *jump(TODAY, 0, 1), [WIPE, 1]]
    gild = [[H, 1], *jump(RESET, 1, 0), [cue("L9", "keeps", -0.1), 0], [cue("L9", "half", 0.0), 1], [WIPE, 1]]
    tar = [[H, 1], *jump(RESET, 1, 0), [cue("L9", "flatters", -0.2), 0], [cue("L9", "it.", 0.0), 1], [WIPE, 1]]
    grow = [[H, 1.35], *jump(RESET, 1.35, 1.0), [cue("L11", "Every", 0.0), 1.0], lin(cue("L11", "bigger.", 0.3), 1.35), [WIPE, 1.35]]

    # ---- that night: Maren with her torch on the centre line, the Grimmaw to her left, the court's field to her right
    g_then = [pk(H, *G_THEN, "hidden"), pk(REWIND, *G_THEN, "idle", face=0),
              pk(cue("L8", "valley", -0.1), *G_THEN, "roar", face=0), pk(cue("L8", "monster", -0.1), *G_FLED, "idle", dur=0.9), pk(cue("L8", "court", -0.25), *G_FLED, "hidden"),
              pk(NIGHT2, *G_THEN, "idle", face=0), pk(cue("L13", "did", 0.0), *G_THEN, "roar", face=0),
              pk(cue("L14", "drive", -0.1), *G_FLED, "idle", dur=1.0), pk(cue("L14", "Now", 0.1), *G_FLED, "hidden")]
    g_now = [pk(H, *G_NOW, "idle", face=160), pk(REWIND, *G_NOW, "hidden"), pk(T2, *G_NOW, "idle", face=160),
             pk(NIGHT2, *G_NOW, "hidden"), pk(TODAY, *G_NOW, "idle", face=160),
             pk(cue("L18", "war", 0.0), *G_NOW, "alert", face=160), pk(cue("L18", "ended.", 1.0), *G_NOW, "idle", face=160)]
    maren = [pk(H, *STATUE, "hidden"), pk(REWIND, *STATUE, "idle", face=FACE), pk(T2, *STATUE, "hidden"),
             pk(NIGHT2, *STATUE, "idle", face=FACE), pk(TODAY, *STATUE, "hidden")]
    # the field: green today, harvest-gold that night; it burns from the moment the valley looks away
    ripe = [[H, 0.5], *jump(REWIND, 0.5, 1.0), *jump(T2, 1.0, 0.5), *jump(NIGHT2, 0.5, 1.0), *jump(TODAY, 1.0, 0.5), [WIPE, 0.5]]
    burn = [[H, 0], [cue("L8", "valley", -0.2), 0], lin(cue("L8", "burn.", 0.3), 0.55), *jump(T2, 0.55, 0),
            *jump(NIGHT2, 0, 0.15), lin(cue("L14", "Now", 0.2), 0.6), *jump(TODAY, 0.6, 0)]

    # ---- the people: two crowds on the clock; three witnesses a side that night; almost nobody after "witnesses die"
    count = [[H, 22], *jump(REWIND, 22, 6), *jump(T2, 6, 22), [cue("L10", "Witnesses", -0.1), 22], [cue("L10", "die.", 0.2), 2],
             [cue("L11", "Every", 0.0), 2], lin(cue("L11", "bigger.", 0.2), 22), *jump(NIGHT2, 22, 6), *jump(TODAY, 6, 22), [WIPE, 22]]
    ruler = [pk(H, *QUEEN, "idle", face=0), pk(cue("L18", "war", 0.1), *QUEEN, "alert", face=0), pk(cue("L18", "ended.", 1.0), *QUEEN, "idle", face=0)]

    # ---- the two archives (rule 3): they stand behind the statue until their pages burn; today nothing is left of them
    arch_show = [[H, 0], *jump(T2, 0, 1), *jump(cue("L11", "Four:", -0.15), 1, 0)]
    archives = {"buildings": [{"kind": "hall", "a": list(a), "face": 0, "w": 3.0, "d": 2.2, "h": 1.7, "show": arch_show} for a in (ARCH_L, ARCH_R)],
                "roof": [[H, 0]], "pens": [],
                "char": [[H, 0], [cue("L10", "Pages", -0.1), 0], lin(cue("L10", "Witnesses", 0.2), 1.0)],
                "smoke": [[H, 0], [cue("L10", "Pages", 0.0), 0], [cue("L10", "burn.", 0.0), 1], [cue("L11", "Four:", -0.2), 1]]}
    standard = [[H, 0], [cue("L18", "war", -0.1), 0], [cue("L18", "war", 0.5), 1, "out"], [cue("L18", "ended.", 0.9), 1], [cue("L18", "ended.", 1.3), 0]]

    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run")]

    # Camera language: the split frame. Every pose but the two wides and the lesson is frontal on the centre line.
    span = loop_span()
    front = lambda at, pose, **kw: cam(at, AZ, dur=0.01, cut=True, **pose, **kw)
    camera = [
        cam(H, AZ, drift=HOOK_DRIFT, **HOOK_POSE),
        front(RESET, MEDIUM),
        cam(cue("L4", "run.", 0.05), 18, dur=1.2, **WIDE),
        front(cue("L6", "Case", -0.2), DROP_POSE),
        front(REWIND, NIGHT_POSE),
        front(T2, MOTIVE_POSE),
        front(cue("L10", "Three:", -0.15), LOSS_POSE),
        front(cue("L11", "Four:", -0.15), RETELL_POSE),
        cam(cue("L12", "Run", -0.05), 20, dur=0.01, cut=True, **WIDE),
        front(cue("L13", "Rule", -0.1), TWIST_POSE),
        front(NIGHT2, NIGHT_POSE),
        front(TODAY, ROLE_POSE, drift=0.5),
        cam(cue("L16", "History", -0.25), 15, 34, 190, (2.0, 3.0, 0.0), fov=26, dur=1.6, drift=2.0),
        cam(WIPE, AZ - HOOK_DRIFT * span, HOOK_POSE["el"], HOOK_POSE["dist"], HOOK_POSE["target"], fov=HOOK_POSE["fov"], cut=True, drift=HOOK_DRIFT),
    ]
    if SCOUT:
        camera = [cam(H, 0, 89, 120, (10.0, 0.0, 0.0), fov=30)]
    light = [
        {"at": H, "mood": "golden"},
        {"at": RESET, "mood": "day", "dur": 0.4},
        {"at": cue("L6", "Case", -0.2), "mood": "gloom", "dur": 0.6},
        {"at": REWIND, "mood": "dusk", "dur": 0.3},
        {"at": T2, "mood": "day", "dur": 0.3},
        {"at": cue("L10", "Three:", -0.15), "mood": "dusk", "dur": 0.4},
        {"at": cue("L11", "Four:", -0.15), "mood": "day", "dur": 0.4},
        {"at": NIGHT2, "mood": "dusk", "dur": 0.2},
        {"at": TODAY, "mood": "day", "dur": 0.3},
        {"at": cue("L16", "History", -0.3), "mood": "golden", "dur": 2.0},
    ]
    human_valley = {
        "buildings": [{"kind": k, "a": list(a), "face": 0} for k, a in HUMAN_B],
        "roof": [[H, 1]], "pens": [{"a": [-6.4, -1.4], "r": 1.6}], "cover": [[H, 1]],
        "roads": {"b": HUMAN_ROAD}, "route": [[H, 1]], "tradeKey": "tradeH", "lanterns": [[H, 0]],
        "tower": {"x": HUMAN_TOWER[0], "z": HUMAN_TOWER[1], "h": 6.0, "keys": [[H, 1]], "rings": [cue("L18", "war", 0.1)]},
    }
    fenn_hall = {"buildings": [{"kind": "greathall", "a": list(LAKE_HALL), "b": list(LAKE_HALL), "stiltsB": 1.6, "face": 0}],
                 "place": [[H, 1]], "open": [[H, 1]], "glow": [[H, 1]], "roof": [[H, 1]], "pens": []}
    clear = [STATUE, G_THEN, ARCH_L, ARCH_R, (FIELD[0], FIELD[1]), *[tuple(c) for c in CROWD]]
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": [[H, 30]], "max": 40, "base": 30, "centers": [[-7.2, -1.4], [-6.0, 0.4]], "skin": "sheep"},
        "pred": [[H, 1]],
        "predators": [{"id": "g1", "scale": 1.3, "keys": g_now, "adorn": True}, {"id": "g0", "scale": 1.3, "keys": g_then}],
        "series": {"tellings": tellings, "questions": questions, "tradeH": [[H, 4]]},
        "settlement": human_valley,
        "settlements": [fenn_hall, archives],
        "folk": {"count": [[H, 9]], "centers": [list(LAKE_HALL)], "spread": 2.0, "site": [[H, 0]],
                 "eyes": [[H, 1]], "wet": [[H, 1]], "glow": [[H, 1]], "hero": []},
        "people": {"count": count, "centers": CROWD, "spread": 1.5, "life": 70, "royal": [[H, 0]],
                   "tints": ["#f0c04a", "#b0452f"], "watch": list(STATUE),
                   "figures": [{"keys": maren, "tunic": "#e9e2cf", "torch": True, "scale": 2.0}],
                   "ruler": {"keys": ruler, "dais": {"x": DAIS[0], "z": DAIS[1], "face": 0}}},
        "fields": {"plots": [{"x": FIELD[0], "z": FIELD[1], "w": FIELD[2], "d": FIELD[3]}], "ripe": ripe, "burn": burn},
        "props": [{"kind": "cairn", "x": CAIRN[0], "z": CAIRN[1], "stones": [[H, 3]]},
                  {"kind": "statue", "x": STATUE[0], "z": STATUE[1], "face": FACE, "rise": rise, "gild": gild, "tar": tar, "grow": grow},
                  {"kind": "standard", "x": STD_L[0], "z": STD_L[1], "face": -90, "rise": standard, "color": "#f0c04a"},
                  {"kind": "standard", "x": STD_R[0], "z": STD_R[1], "face": 90, "rise": standard, "color": "#b0452f"}],
        "clearTrees": [[d[0], d[1], 3.0] for d in clear] + [[18.0, 6.5, 3.5], [10.5, 0.3, 2.0]],
        "layers": {"ripple": ripple},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "WITNESSES", "text": "each saw half", "at": cue("L8", "witnesses.")},
    {"n": 2, "label": "MOTIVE", "text": "each keeps its half", "at": cue("L9", "motive.")},
    {"n": 3, "label": "LOSS", "text": "pages burn", "at": cue("L10", "loss.")},
    {"n": 4, "label": "RETELLING", "text": "she grows", "at": cue("L11", "retelling.")},
    {"n": 5, "label": "THE TRUTH", "text": "know it. hide it.", "at": cue("L7", "crack"), "locked": True, "unlockAt": cue("L15", "fight", -0.1)},
]
SPRITE = {"sprite": "ep31/statue_sprite.png", "spriteW": 62, "spriteH": 127}

# The two chronicles. State per page: 0 never written, 1 written, 2 lost, 3 the truth.
# After the rewind both pages are blank (nothing is written at year 0); each is written as its witness is named.
T8V, T8V2 = cue("L8", "off.", -0.1), cue("L8", "off.", 0.2)      # the valley writes: she drove the monster off
T8C = cue("L8", "fields", 0.0)                                   # the court writes: their fields burned
T10, T13, T14 = cue("L10", "burn.", 0.0), cue("L13", "both.", 0.0), cue("L14", "hide", 0.0)
L0 = cue("L3", "lazy")
CHRON_ROWS = [
    {"icon": "grimmaw", "label": "MONSTER GONE", "left": [[L0, 1], [REWIND, 0], [T8V, 1], [T13, 3], [T14, 1]], "right": [[L0, 1], [REWIND, 0], [T13, 3], [T14, 0]]},
    {"icon": "sheep", "label": "FLOCK SAVED", "left": [[L0, 1], [REWIND, 0], [T8V2, 1], [T10, 2], [T13, 3], [T14, 2]], "right": [[L0, 1], [REWIND, 0], [T13, 3], [T14, 0]]},
    {"icon": "flame", "label": "FIELDS BURNED", "left": [[L0, 0], [T13, 3], [T14, 0]], "right": [[L0, 0], [T8C, 1], [T13, 3], [T14, 1]]},
    {"icon": "sheaf", "label": "HARVEST LOST", "left": [[L0, 0], [T13, 3], [T14, 0]], "right": [[L0, 0], [cue("L8", "burn.", 0.0), 1], [T10, 2], [T13, 3], [T14, 2]]},
]


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "HERO", "color": GOLD, "size": 128, "pulseAt": cue("L1", "hero")}, {"text": "OR MONSTER?", "color": RUST, "size": 84, "pulseAt": cue("L1", "monster?")}]
    G["hook"] += [
        {"type": "splitTone", "start": {"shot": "hook"}, "end": cue("L2", "Meet", -0.15), "fadeOut": 0.3, "pulses": [[cue("L1", "hero"), "left"], [cue("L1", "monster?"), "right"]]},
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 96, "start": {"shot": "hook"}, "end": cue("L2", "Meet", -0.1), "preShow": True},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 31 · HISTORY", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Meet", -0.05), "end": RESET, "dietAt": cue("L2", "she"),
         "kicker": "FIELD CARD · NO. 006", "kind": "DISPUTED FIGURE", "name": "MAREN", "dietLabel": "DID", "diet": "one thing, 300 years ago", **SPRITE},
    ]
    chron = {"type": "chronicles", "y": 1352, "start": cue("L3", "lazy", 0.1), "end": shift(TODAY, -0.1), "rows": CHRON_ROWS,
             "left": {"title": "THE VALLEY SAYS", "color": GOLD}, "right": {"title": "THE COURT SAYS", "color": RUST},
             "verdicts": [[L0, "HERO", "HERO"], [REWIND, "· · ·", "· · ·"], [T8V, "HERO", "· · ·"], [T8C, "HERO", "MONSTER"], [cue("L11", "bigger.", 0.0), "SAINT", "DEMON"]],
             "motiveAt": cue("L9", "motive.", 0.0), "hideAt": T14}
    G["setup"] += [
        # rule 2's split grade (each side keeps its half): listed here, before the HUD, so it is drawn under it
        {"type": "splitTone", "start": cue("L9", "keeps", -0.1), "fadeIn": 0.5, "end": cue("L10", "Three:", -0.15), "fadeOut": 0.01},
        {"type": "blockWipe", "at": RESET, "dur": 0.34, "color": "#1b2350"},
        {"type": "kinetic", "parts": [{"text": "ONE HISTORY", "at": cue("L3", "one"), "size": 84}, {"text": "EVERYBODY AGREES", "at": cue("L3", "everybody"), "color": "rust", "size": 60}],
         "y": 470, "size": 84, "start": cue("L3", "one", -0.05), "end": cue("L4", "Press", -0.15)},
        chron,
        {"type": "simBar", "counters": [{"icon": "book", "label": "TELLINGS", "key": "tellings", "color": INK, "digits": 2},
                                        {"icon": "eye", "label": "QUESTIONS", "key": "questions", "color": "ember", "digits": 2}],
         "compact": True, "start": cue("L4", "Press", -0.15), "end": cue("L16", "History", -0.3), "runAt": [cue("L4", "run."), cue("L12", "Run")]},
    ]
    G["run1"] += [
        {"type": "kinetic", "parts": [{"text": "YEAR 100 · HERO", "at": cue("L5", "hundred"), "color": GOLD, "size": 58},
                                      {"text": "YEAR 200 · HERO", "at": cue("L5", "statue."), "color": GOLD, "size": 58},
                                      {"text": "YEAR 300 · HERO", "at": cue("L5", "Zero"), "color": GOLD, "size": 58}],
         "y": 468, "size": 58, "start": cue("L5", "hundred", -0.05), "end": cue("L6", "Case", -0.25)},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "CASE CLOSED", "sub": "0 QUESTIONS · NOTHING TO SOLVE", "color": "rust", "y": 560, "size": 76, "start": cue("L6", "closed."), "end": cue("L6", "solve.", 0.5)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "solve.", 0.55), "end": cue("L7", "Real", 0.3)},
        {"type": "pin", "at": [STATUE[0], 7.0, STATUE[1]], "kicker": "THAT NIGHT", "text": "MAREN", "color": "ember", "lift": 60, "size": 30,
         "start": cue("L7", "Real", 0.35), "end": cue("L7", "Four", -0.25)},
        {"type": "blockWipe", "at": cue("L6", "solve.", 0.53), "dur": 0.34},
        {"type": "kinetic", "parts": [{"text": "REAL HISTORY", "at": cue("L7", "Real"), "size": 78}, {"text": "HAS WITNESSES", "at": cue("L7", "has"), "color": INK, "size": 72}],
         "y": 470, "size": 84, "start": cue("L7", "Real", -0.05), "end": cue("L7", "Four", -0.15)},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L16", "History", -0.3),
         "kicker": "MAREN · THE RECORD", "title": "CRACK IT OPEN", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L8", "The", -0.3), 0], [cue("L8", "The", 0.0), 1], [cue("L15", "Let", -0.15), 1], [cue("L15", "Let", 0.15), 0]]},
    ]
    G["witness"] += [
        {"type": "veil", "side": "right", "w": 460, "label": "THE VALLEY SAW", "color": GOLD, "start": cue("L8", "valley", -0.25), "end": cue("L8", "court", -0.25)},
        {"type": "veil", "side": "left", "w": 460, "label": "THE COURT SAW", "color": RUST, "start": cue("L8", "court", -0.2), "end": cue("L9", "Two:", -0.2)},
    ]
    G["loss"] += [
        {"type": "pin", "at": [STATUE[0], 8.6, ARCH_L[1]], "kicker": "BOTH ARCHIVES", "text": "PAGES BURN", "color": "rust", "lift": 30, "size": 30,
         "start": cue("L10", "Pages", 0.0), "end": cue("L11", "Four:", -0.25)},
    ]
    G["run2"] += [
        {"type": "stamp", "text": "DISPUTED", "sub": "1 NIGHT · 2 HISTORIES", "color": INK, "rotate": -4, "y": 880, "size": 96, "start": cue("L12", "histories."), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}, {"text": "THE TRUTH", "at": cue("L13", "truth."), "color": INK, "size": 96}],
         "size": 150, "y": 570, "start": cue("L13", "Rule", -0.02), "end": cue("L13", "She", -0.12)},
        {"type": "kinetic", "parts": [{"text": "SHE DID", "at": cue("L13", "She"), "size": 84}, {"text": "BOTH", "at": cue("L13", "both."), "color": "ember", "size": 150}],
         "size": 84, "y": 560, "start": cue("L13", "She", -0.02), "end": cue("L14", "fields", -0.05)},
        {"type": "pin", "at": [STATUE[0], 7.4, STATUE[1]], "kicker": "ONE TORCH", "text": "BOTH STORIES", "color": "ember", "lift": 70, "size": 30,
         "start": cue("L14", "fields", 0.05), "end": cue("L14", "Now", -0.1)},
        {"type": "veil", "side": "middle", "w": 220, "textSize": 30, "hiddenText": "HIDDEN", "label": "ONLY YOU KNOW", "color": "ember", "start": cue("L14", "hide", -0.05), "end": cue("L15", "Let", -0.2)},
    ]
    G["role"] += [
        {"type": "followChip", "start": cue("L15", "pieces.", 0.2), "end": cue("L16", "telling", 0.3), "text": "FOLLOW", "sub": "PART 31/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "History", -0.3), **({"unlockAt": cue("L16", "History", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "History", -0.3), "end": WIPE, "kicker": "BEFORE YOU WRITE HISTORY", "title": "MAREN", **SPRITE,
         # the line to keep: on screen from the end of the first sentence until the wipe covers the card (1.7 s to read it)
         "subtitle": "History is who's telling it.", "subtitleAt": cue("L16", "happened.")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 31 / 50",
         "title": "Your World Needs a History Nobody Agrees On", "cta": "COMMENT", "icon": "bubble", "with": "Give us your verdict.", "withAt": cue("L17", "Give", -0.05),
         "choices": [{"text": "HERO", "color": GOLD, "at": cue("L17", "Hero")}, {"text": "MONSTER", "color": RUST, "at": cue("L17", "monster?")}]},
    ]
    gone = cue("L18", "ended.", 0.6)
    G["next"] += [
        # the hook's split grade again, so the last frame matches frame 0
        {"type": "splitTone", "start": cue("L18", "Part", -0.12), "fadeIn": 0.3},
        {"type": "seasonBar", "y": 350, "part": 31, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6, "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone, "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 32"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "32:", -0.1), "revealAt": cue("L18", "war"), "end": gone,
         "kicker": "NEXT RUN · 32", "title": "UNFINISHED", "titleSize": 66, "sub": "A WAR THAT NEVER ENDED.", "sprite": "standard", "spritePx": 9},
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 96, "start": cue("L18", "ended.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("Don't write one true history for your world. Write the event, then write who saw which half of it, what each "
          "side gains from its telling, what was lost, and how retelling changed it. You know the truth; your characters "
          "only have the pieces, and the gap between the accounts is the plot.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Close EP30's loop (hero, or monster?) and stop the scroll on the question.",
             "Golden hour, frontal: a hooded stone woman raising two torches on a stepped plinth, split down the middle. The valley's half is gilded, its torch lit, flowers and candles at its foot; the court's half is tarred, its torch dead, scratched in rust. The frame is split the same way: warm on the left, drained and rust on the right. The valley's people (wheat gold) stand left, the court's (rust) right. HERO / OR MONSTER? is on screen from frame 0; the gold half flares on 'hero', the rust half on 'monster?'. Then the field card: MAREN · DISPUTED FIGURE · DID: one thing, 300 years ago.",
             "Frontal long lens on the centre line (az 0, el 9, dist 76, fov 15), a slow 0.6°/s drift; the loop lands on the same frame.", ("kinetic, sting, split tone, field card", "the split statue", "two crowds, the meadow"),
             "Golden hour.", "HERO / OR MONSTER? · FIELD CARD NO. 006 · MAREN", "Ink-blue block wipe into the lazy version.", "Dispute: the theme split between recorder and bassoon; a hit on 'monster?'."),
    "setup": ("The lazy version: one history, and everybody agrees.",
              "An ink wipe to day and year 0: the same statue in plain stone, both crowds before it. ONE HISTORY / EVERYBODY AGREES. The two chronicles slide in under the world, both pages saying HERO with MONSTER GONE and FLOCK SAVED: AGREE 100%. The sim bar arrives (TELLINGS 01, QUESTIONS 00) and RUN is pressed.",
              "Frontal medium (az 0, el 12, dist 60, fov 20).", ("kinetic, chronicles, sim bar", "the plain statue, both crowds", "the meadow"), "Day.", "ONE HISTORY · EVERYBODY AGREES · AGREE 100%", "A pull-out to the wide on 'run'.", "Chronicle, thin (lute alone)."),
    "run1": ("Run the lazy version: three hundred years of one story.",
             "Whole Isle; YEAR 0→300; the crowds turn over, generation after generation, and nothing else changes: TELLINGS 01, QUESTIONS 00. The same verdict is stamped under the clock each century: YEAR 100 · HERO, YEAR 200 · HERO, YEAR 300 · HERO.",
             "Wide (az 18, el 48, dist 196).", ("sim bar, kinetic, chronicles", "the statue, the crowds ageing", "island"), "Day.", "YEAR 100 · HERO / YEAR 200 · HERO / YEAR 300 · HERO", "Cut to the statue.", "Drive."),
    "drop": ("The punchline: a closed case is no story.", "The plain statue from above, in gloom: CASE CLOSED · 0 QUESTIONS · NOTHING TO SOLVE. The chronicles still agree, 100%.",
             "Frontal, higher (az 0, el 20, dist 53, fov 20).", ("stamp, chronicles", "the statue", "void"), "Gloom.", "CASE CLOSED · 0 QUESTIONS · NOTHING TO SOLVE", "Rewind + block wipe.", "Drop; a boom on 'closed'."),
    "rehook": ("Re-hook: the thesis, then four easy rules and one locked.",
               "REWIND to the night itself, year 0, dusk: no statue yet, and both chronicle pages go blank. Maren stands on the spot with her torch (THAT NIGHT · MAREN), the Grimmaw to her left, the court's ripe field to her right, three witnesses from each side in the foreground. REAL HISTORY / HAS WITNESSES; then the checklist CRACK IT OPEN, row 5 locked (the twist).",
               "Frontal, higher (az 0, el 22, dist 60, fov 22): the whole night in one frame.", ("rewind, kinetic, pin, checklist, chronicles", "Maren, the Grimmaw, the field, six witnesses", "the meadow at dusk"), "Dusk.",
               "REAL HISTORY · HAS WITNESSES · CRACK IT OPEN 0/5", "Hold: the same frame runs through rule 1.", "Mystery; a riser into 'the twist'."),
    "witness": ("Rule 1: two witnesses, each saw half.",
                "The same frame, held. THE VALLEY SAW: the right of the frame is hatched out UNSEEN while the Grimmaw roars and is driven off to the left, and the valley's page is written: HERO, MONSTER GONE, FLOCK SAVED. THE COURT SAW: the veil swaps sides, on the right the field burns, and the court's page is written: MONSTER, FIELDS BURNED, HARVEST LOST. The spine, blank until both pages exist, pops to AGREE 0%. TELLINGS 00, 01, 02.",
                "The night frame, locked.", ("veil, chronicles, checklist (folded)", "the Grimmaw fleeing, the field burning", "dusk"), "Dusk.", "THE VALLEY SAW · THE COURT SAW · UNSEEN · AGREE 0%", "Cut to day.", "Chronicle 1: lute alone."),
    "motive": ("Rule 2: each side keeps the half that flatters it.",
               "Day: the statue rises on the spot in plain stone, between the two sides' archives. A coin stamps onto each page on 'motive'. On 'keeps' the valley's half is gilded, its torch lit, flowers and candles at its foot; on 'flatters' the court's half is tarred and scratched. The frame itself splits: warm on the left, drained and rust on the right.",
               "Frontal long lens (az 0, el 9, dist 56, fov 16).", ("split tone, chronicles, checklist (folded)", "the statue gilding and tarring", "two archives, two crowds"), "Day.", "2 MOTIVE · each keeps its half", "Cut.", "Chronicle 2: tambourine joins."),
    "loss": ("Rule 3: the record itself is lost.",
             "Dusk: both archives behind the statue char and smoke (BOTH ARCHIVES · PAGES BURN), and a row is struck out of each chronicle: PAGE LOST. On 'witnesses die' seventy years pass and the crowds thin to two.",
             "Frontal, pulled back and higher (az 0, el 16, dist 64, fov 20), the archives behind the statue.", ("pin, chronicles", "the burning archives", "the statue, dusk"), "Dusk.", "BOTH ARCHIVES · PAGES BURN · PAGE LOST", "Cut.", "Chronicle 3: bass joins (F major)."),
    "retell": ("Rule 4: retelling inflates.",
               "Day: the archives are gone. The years race from 70 to 300, the crowds grow back, and the statue grows a third taller on its plinth; on 'bigger' the verdicts become SAINT and DEMON.",
               "Frontal long lens (az 0, el 9, dist 68, fov 16).", ("chronicles, checklist (folded)", "the statue growing", "the crowds turning over"), "Day.", "4 RETELLING · she grows · SAINT / DEMON", "Cut to the wide.", "Chronicle 4: the theme on recorder, harp and glockenspiel."),
    "run2": ("Run with the rules: one night, two histories.",
             "Whole Isle; YEAR 0→300; TELLINGS 02; QUESTIONS climbs from 20 to 40: DISPUTED · 1 NIGHT · 2 HISTORIES, stamped in chronicle ink.",
             "Wide (az 20, el 48, dist 196).", ("sim bar, stamp, chronicles", "the split statue, the crowds", "island"), "Day.", "DISPUTED · 1 NIGHT · 2 HISTORIES", "Cut to the statue's face.", "Drive with the theme; a stab and a cymbal on 'histories'."),
    "twist": ("The locked rule: the truth, and what to do with it.",
              "RULE 5? THE TRUTH over a close-up of the split statue and its two torches. Then the night again, unveiled: Maren's torch lights the field and the Grimmaw flees from the fire, both halves in one frame. SHE DID / BOTH; every row on both pages turns ember: BOTH TRUE. ONE TORCH · BOTH STORIES. On 'hide' a HIDDEN band hatches out the centre of the frame (ONLY YOU KNOW), the pages fall back to their halves and the spine locks: THE TRUTH · HIDDEN.",
              "Frontal close on a very long lens (az 0, el 6, dist 60, fov 12), then the night frame, locked.", ("kinetic, veil, pin, chronicles", "Maren, the fire, the fleeing Grimmaw", "dusk"), "Day for the question, dusk for the night.",
              "RULE 5? THE TRUTH · SHE DID BOTH · ONLY YOU KNOW · HIDDEN", "Cut to today.", "Twist (a held A7♭9), a boom on 'both', then dispute."),
    "role": ("Unlock rule 5: give the pieces to the characters.",
             "Today: the split statue and both crowds under the open checklist. On 'fight' row 5 unlocks: THE TRUTH · know it. hide it. 5/5. The follow chip (+ FOLLOW · PART 31/50) appears after 'pieces'.",
             "The hook framing, lowered to sit under the open card (az 0, el 9, dist 76, fov 15), a slow 0.5°/s drift.", ("open checklist, follow chip", "the split statue, two crowds", "the meadow"), "Day.", "5 THE TRUTH · know it. hide it. · 5/5", "The card goes full.", "Anthem from 'Let'; a big D-major hit on 'fight'."),
    "lesson": ("The takeaway.", "The full card (BEFORE YOU WRITE HISTORY · MAREN, all five rows ticked) over the whole Isle, with 'History is who's telling it.' in serif italic on 'telling'.",
               "Wide (az 15, el 34, dist 190), a slow 2°/s orbit.", ("full card, follow chip", "the island at golden hour", "stars"), "Golden hour.", "BEFORE YOU WRITE HISTORY · MAREN · History is who's telling it.", "Block wipe to the end card.", "Anthem; the World Engine chime as the card lands."),
    "cta": ("Comment CTA: a one-word verdict.", "End card: logo, PART 31 / 50, the title, and a COMMENT panel where two vote chips pop on their words: HERO (gold), then MONSTER (rust). Then 'Give us your verdict.'",
            "Cut (under the block wipe) back to the hook pose, drifting into it.", ("end card", "the Isle", "void"),
            "Golden hour (the loop frame).", "COMMENT · HERO / MONSTER · Give us your verdict.", "The card lifts on 'Part'.", "Outro."),
    "next": ("Say the part number, ask for the follow with a reason (part 32), open the next loop.",
             "The hook frame, split-toned again; PART 31/50; FOLLOW FOR PART 32, pressed on 'Follow'; NEXT RUN · 32 decodes from a locked battle standard to UNFINISHED · A WAR THAT NEVER ENDED. In the world, on 'war', each crowd raises a war standard in its own colour (wheat gold on the left, rust on the right), the valley's bell tolls, and the Queen and the Grimmaw look up; the standards sink and the hook title returns.",
             "The hook frame.", ("split tone, progress bar, follow button, next-run card", "the statue, two standards", "the meadow"), "Golden hour.",
             "PART 31/50 · FOLLOW FOR PART 32 · NEXT RUN: UNFINISHED · A WAR THAT NEVER ENDED.", "Loop to frame 0.", "Tease over a held A, a horn call on 'war', the engine chime on 'Follow'."),
}


def build():
    ep = {
        "id": "ep31", "number": 31, "season": 2,
        "title": "Your World Needs a History Nobody Agrees On",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.05},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same lab host, a storyteller this time. The hook is a dare. 'One history, and everybody agrees' is the knowing setup; 'Case closed' lands dry. "
                         "The rules are crisp, two beats each. 'She did both' is the reveal, said plainly; 'Now hide that from your world' is the instruction, almost a whisper. The verdict ask is a genuine question.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L3", "from": "one"}, {"line": "L6", "from": "Case"}, {"line": "L7", "from": "Real", "to": "Four"}, {"line": "L13", "from": "Rule"}],
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
             hit("crownPass", cue("L1", "hero"), -19), hit("stompHit", cue("L1", "monster?"), -20),
             hit("cardSlide", cue("L2", "Meet", -0.05), -18), hit("check", cue("L2", "she"), -20)],
    "setup": [hit("rewind", RESET, -15), hit("cardSlide", cue("L3", "lazy", 0.1), -18), hit("quill", cue("L3", "one", 0.0), -15), hit("stamp", cue("L3", "everybody"), -19),
              hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "Zero", 0.0), -22), bed("clockTicks", cue("L4", "run.", 0.3), cue("L5", "Zero", 0.0), -23),
             hit("quill", cue("L5", "hundred"), -15), hit("quill", cue("L5", "statue."), -15), hit("quill", cue("L5", "Zero"), -15)],
    "drop": [hit("stamp", cue("L6", "closed."), -10)],
    "rehook": [hit("rewind", cue("L6", "solve.", 0.5), -11), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "witness": [hit("check", cue("L8", "witnesses."), -13), hit("eyeOn", cue("L8", "valley", -0.25), -17), hit("roar", cue("L8", "valley", -0.1), -19),
                hit("quill", cue("L8", "off.", -0.1), -15), hit("eyeOn", cue("L8", "court", -0.2), -17), bed("burn", cue("L8", "court", -0.2), cue("L9", "Two:", -0.2), -20),
                hit("quill", cue("L8", "fields", 0.0), -15)],
    "motive": [hit("check", cue("L9", "motive."), -13), hit("restore", cue("L9", "Two:", 0.0), -16), hit("unlock", cue("L9", "keeps", 0.0), -17), hit("stamp", cue("L9", "flatters", 0.0), -18)],
    "loss": [hit("check", cue("L10", "loss."), -13), bed("burn", cue("L10", "Pages", 0.0), cue("L10", "die.", 0.1), -21), hit("pageTear", cue("L10", "burn.", 0.0), -12),
             hit("crownPass", cue("L10", "die.", 0.0), -18)],
    "retell": [hit("check", cue("L11", "retelling."), -13), bed("clockTicks", cue("L11", "Every", 0.0), cue("L11", "bigger.", 0.3), -23), hit("morph", cue("L11", "makes", 0.0), -15),
               hit("quill", cue("L11", "bigger.", 0.0), -14)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L12", "histories.", 0.2), -22),
             hit("stamp", cue("L12", "histories."), -13)],
    "twist": [hit("eyeOn", NIGHT2, -16), bed("burn", cue("L13", "She", 0.0), cue("L14", "Now", 0.1), -21), hit("roar", cue("L13", "did", 0.0), -20),
              hit("unlock", cue("L13", "both.", 0.0), -12), hit("cardSlide", cue("L14", "fields", 0.05), -20), hit("stamp", cue("L14", "hide", -0.05), -14)],
    "role": [hit("restore", TODAY, -17), hit("unlock", cue("L15", "fight", -0.1), -10)],
    "lesson": [hit("engineWind", cue("L16", "History", -0.8), -15), hit("chime", cue("L16", "History", -0.3), -10), hit("cardSlide", cue("L16", "History", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("check", cue("L17", "Hero"), -17), hit("check", cue("L17", "monster?"), -17)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11), hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "32:", -0.1), -18), hit("unlock", cue("L18", "war"), -15), hit("restore", cue("L18", "war", 0.0), -19),
             hit("towerBell", cue("L18", "war", 0.15), -20), hit("frameDrum", cue("L18", "never", 0.0), -17),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score: the series theme stays (D minor for the problem, D major for the payoff). EP31's band is `chronicle` (a
# lute, on the marimba channel as a nylon guitar; a tambourine; the theme on recorder) for the record being written,
# one family per rule, and `dispute` (the theme's bars split between the recorder and a bassoon on the horns channel)
# wherever two tellings share the frame: the hook and the truth.
CHRON_P = {"marimba": 24, "lead": 74, "horns": 70}
BACK_P = {"marimba": 12, "lead": 73, "horns": 60}
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 96,
    "sections": [
        msec({"shot": "hook"}, "dispute", ["Dm", "Bb", "Gm", "A"], "D minor", programs=CHRON_P),
        msec(RESET, "chronicle", ["Dm", "Bb", "F", "C"], "D minor", layer=1),
        msec(cue("L4", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.85, programs=BACK_P),
        msec(cue("L6", "Case", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "solve.", 0.5), "mystery", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=2),
        msec(cue("L8", "One:", -0.1), "chronicle", ["Dm", "C", "Bb", "C"], "D minor", layer=1, programs=CHRON_P),
        msec(cue("L9", "Two:", -0.1), "chronicle", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "chronicle", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L11", "Four:", -0.1), "chronicle", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True, programs=BACK_P),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(NIGHT2, "dispute", ["Dm", "Bb", "Gm", "A"], "D minor", beatsPerChord=2, programs=CHRON_P),
        msec(cue("L15", "Let", -0.1), "anthem", ["D", "G", "Bm", "A"], "D major", programs=BACK_P),
        msec(cue("L17", "Hero", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "monster?"), "chord": "Dm"},
        {"kind": "boom", "at": cue("L6", "closed."), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "histories."), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "histories.")},
        {"kind": "boom", "at": cue("L13", "both."), "chord": "Dm"},
        {"kind": "hit", "at": cue("L15", "fight"), "chord": "D"},
        {"kind": "call", "at": cue("L18", "war"), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #WritingTips #Lore #WorldcraftShorts"
IG_HOOK = "Hero to one village. Monster to the next."
BODY = (
    "What if history's greatest hero was also its worst monster?\n\n"
    "Meet Maren. Three hundred years ago, she did one thing. The lazy version gives your world one history that "
    "everybody agrees on, and we ran it: three hundred years, one statue, one story, zero questions. Case closed. "
    "Nothing left to solve.\n\n"
    "Real history has witnesses. The valley saw her drive the monster off; the court saw their fields burn. Each side "
    "keeps the half that flatters it. Pages burn, witnesses die, and every generation makes her bigger. Run it again: "
    "one night, two histories.\n\n"
    "Then the twist: the truth. She did both: she burned the fields to drive it off. Now hide that from your world, "
    "and let your characters fight over the pieces.\n\n"
    "History isn't what happened. It's who's telling it.\n\n"
    "Hero or monster? Give us your verdict.\n\n"
    "Part 31 of 50. Follow for part 32: a war that never ended."
)
METADATA = {
    "youtube": {
        "title": "Your World Needs a History Nobody Agrees On (Worldbuilding)",
        "titleAlternate": "Their greatest hero. Their worst monster. Same person.",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 7: History and Mythology.\n\n" + TAGS,
        "pinnedComment": "Hero or monster? One word, then your reason. (Part 32: a war that never ended.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated field-card sprite; the island, statue, people and fire are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "Same night. Two histories. One calls her a hero, one calls her a monster, and both are true 🔥 Four rules that crack your world's history open, and rule #5 is the one writers skip. "
                   "Hero or monster? Part 31/50 · follow for part 32 ⚔️ " + TAGS,
        "pinnedComment": "Hero or monster? Give us your verdict.",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "Which figure in your world would two villages remember in opposite ways?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": IG_HOOK + "\n\n" + BODY + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": f"First {len(IG_HOOK)} characters: '{IG_HOOK}'",
        "pinnedComment": "Save the CRACK IT OPEN card, then give us your verdict: hero or monster?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep31] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots, loop span {loop_span():.2f} s")
