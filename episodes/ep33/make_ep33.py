"""Generate episodes/ep33/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep33/make_ep33.py
EP33 is Arc 7's third episode (History and Mythology): "How Do You Invent a Believable Religion?". It closes EP32's
loop (on "a god built from fear" the sun went dark over the Isle for a breath): frame 0 is that eclipse, its shadow
crossing the valley while the crowd looks up with lamps in their hands.

Its own device is THE FEAR MAP: what the people fear is drawn on the Isle as shadows (death at the cairn, the lake,
hunger over the field, the eclipse over the valley), and each belief is a light that answers one shadow, with its rite
growing inside the light (candles for the dead, a lamp in every boat, the first sheaves shared, keepers who read the
sky). Gods invented first answer nothing: their lamps stand in the sun and go out. The twist is the deepest fear,
that nobody is listening: the whole map goes dark, and the god is the last light, the one that answers it.
Camera language: THE MAP TABLE, every pose looks almost straight down at the Isle with north up and only slides and
zooms across it like a hand over a map; the only turn is the lesson, when the map rotates (EP26 orbited, EP27 rode a
dragon, EP28 sat at eye height, EP29 was a locked-off tripod, EP30 looked up, EP31 split the frame, EP32 craned up and
down the cut). Motif colour: lamplight #ffe45c. Music band: `vigil` (a bell tolling over bowed glass) and `lantern`
(a procession of lamps, one family per belief).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep33" / "timing.json"
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
    ("L1", "hook", "Inventing a religion? Don't start with gods. What do people fear?", 0.3, ["religion?", "fear?"]),
    ("L2", "hook", "Meet the Lamplight faith. They pray to an empty sky.", 0.3, ["lamplight", "empty"]),
    ("L3", "setup", "The lazy version: twelve gods first, one job each.", 0.25, ["lazy", "twelve"]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "Shrines rise. Nobody comes. The lamps go out.", 0.35, ["nobody", "out."]),
    ("L6", "drop", "Nobody prays to a god they don't need.", 0.4, ["prays", "need."]),
    ("L7", "rehook", "Real faith starts in the dark. Four fears come first. The fifth is the twist.", 0.25, ["dark.", "twist."]),
    ("L8", "death", "One: death. Candles keep the dead company at the cairn.", 0.2, ["death.", "candles"]),
    ("L9", "lake", "Two: the lake. No boat leaves without a lamp.", 0.2, ["lake.", "lamp."]),
    ("L10", "hunger", "Three: hunger. Hoarding grain becomes a sin.", 0.2, ["hunger.", "sin."]),
    ("L11", "eclipse", "Four: the eclipse. Keepers rise to read the sky.", 0.3, ["eclipse.", "keepers"]),
    ("L12", "run2", "Run it again. Five hundred years. Every lamp still burns.", 0.3, ["hundred", "burns."]),
    ("L13", "twist", "Rule five? The deepest fear. That nobody is listening.", 0.3, ["deepest", "listening."]),
    ("L14", "twist", "So they made someone who listens. A god.", 0.4, ["listens.", "god."]),
    ("L15", "role", "Write it last, and it feels real.", 0.4, ["last,", "real."]),
    ("L16", "lesson", "Gods don't come first. Every god answers a fear.", 0.35, ["first.", "answers"]),
    ("L17", "cta", "What question would your people ask their gods?", 0.25, ["question", "gods?"]),
    ("L18", "next", "Part 33 of 50. Follow for part 34: the gods are lying.", 0.25, ["follow", "lying."]),
]
SHOTS = ["hook", "setup", "run1", "drop", "rehook", "death", "lake", "hunger", "eclipse", "run2", "twist", "role", "lesson", "cta", "next"]

# The block wipe into the end card: the world resets to frame 0 under it (the faith today, under the eclipse).
WIPE = cue("L17", "What", -0.3)
RESET = cue("L3", "lazy", -0.15)          # the lazy version: gods first, no fears asked
REWIND = cue("L6", "need.", 0.55)         # back to before any faith: the fears in the dark
RULES = cue("L8", "One:", -0.1)
RUN2 = cue("L12", "Run", -0.05)
TWIST = cue("L13", "Rule", -0.1)
DEEP = cue("L13", "deepest", -0.05)       # the whole map goes dark
GOD = cue("L14", "listens.", -0.05)       # the last light: the one that answers it
ROLE = cue("L15", "Write", -0.15)
HOOK_DRIFT = 0.4
END = {"end": True}

# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle (it remembers): EP27's valley village and watchtower (west), the cairn (east of the lake),
# EP28's Fenn hall on the lake, EP29's Queen on her dais, EP30's Grimmaw (north-east), EP31's split statue and EP32's
# boundary stones down its seam (south-east). EP28's Fenn hall is left out: from overhead it
# covers the whole lake. EP33 lays the fear map over the rest.
CAIRN = (8.95, -5.38)
HUMAN_B = [("hall", (-3.6, -4.6)), ("house", (-1.8, -2.4)), ("house", (-4.8, -2.4)), ("house", (-1.0, -5.8)),
           ("house", (-5.6, -0.9)), ("house", (-3.4, -0.7)), ("house", (0.4, -4.2))]
HUMAN_TOWER = (-6.4, -5.6)
HUMAN_ROAD = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
DAIS = (9.4, -2.2)
QUEEN = (9.1, -2.2)
G_NOW = (8.5, -9.6)
STATUE = (18.0, 1.5)
LINE_A, LINE_B = (18.0, -7.0), (18.0, 8.3)
RELIC = (20.3, 5.4)

# The fear map
LAKE = (6.5, 4.5)
FIELD = (3.0, -11.0, 4.0, 3.4)           # the valley's grain field on the north meadow
VALLEY = (-2.2, -3.4)                    # the crowd's homes: the eclipse's shadow falls here
CROWD = [[-2.4, -3.2], [-0.4, -1.6], [-4.2, -1.8]]
UMBRA_X0, UMBRA_Z = -2.2, -3.2           # the eclipse's shadow on frame 0
UMBRA_V = 0.45                           # it drifts east this many units a second
# the lazy pantheon: twelve gods' lamps on sunny ground, each answering nothing
GODS = [(14, -11), (17, -5), (19, 1), (16, 7), (10, 11), (3, 13), (1, -17), (6, -15), (-18, -4), (-16, -12), (13, -1), (12, -14)]
SHRINES = [(15.5, -5.0), (6.0, -16.4), (3.0, 14.4)]
LAMP = "#ffe45c"
DREAD = "#b9b4d8"
ROBE = "#efe2b0"


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
    if c.get("end"):
        return tm["duration"] + c.get("offset", 0.0)
    ln = next(l for l in tm["lines"] if l["id"] == c["line"])
    hits = [w for w in ln["words"] if w["text"].strip(".,?!:").lower() == c["word"].strip(".,?!:").lower()]
    return hits[c.get("nth", 1) - 1]["start"] + c.get("offset", 0.0)


def loop_span():
    """Seconds from the wipe to the end: the loop camera key drifts this long and lands exactly on the hook pose."""
    if not TIMING.exists():
        return 6.0
    return tcue(END) - tcue(WIPE)


# The map-table poses (az 0: north up, looking almost straight down). Planned with pipeline/camprobe.ts (BRIEF.md §6).
EL = 80
HOOK_POSE = dict(el=EL, dist=130, target=(-1.4, 4.0, -5.4), fov=24)        # the eclipse's shadow over the valley
MAP = dict(el=EL, dist=178, target=(1.0, 2.0, 0.4), fov=26)              # the whole Isle as a map
LAZY_POSE = dict(el=EL, dist=150, target=(4.0, 2.0, -1.0), fov=26)
DARK_POSE = dict(el=EL, dist=122, target=(2.4, 3.0, -13.0), fov=26)       # the four shadows in one frame
P_DEATH = dict(el=EL, dist=100, target=(8.4, 4.0, -4.6), fov=24)
P_LAKE = dict(el=EL, dist=110, target=(6.2, 2.0, 4.2), fov=24)
P_HUNGER = dict(el=EL, dist=100, target=(3.0, 4.0, -10.4), fov=24)
P_ECLIPSE = dict(el=EL, dist=106, target=(-2.0, 4.0, -3.2), fov=24)
P_ROLE = dict(el=EL, dist=116, target=(0.4, 4.0, -2.2), fov=24)


def fear(fid, x, z, r, dark, lit, label, answer, light=None, lamp=False, **kw):
    f = {"id": fid, "x": x, "z": z, "r": r, "dark": dark, "lit": lit, "label": label, "answer": answer, "lamp": lamp, **kw}
    if light:
        f["light"] = light
    return f


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    lin = lambda at, v: [at, v, "linear"]
    H = shot("hook")
    span = loop_span()

    # ---- the clock (YEARS since the first lamp). Today is year 500.
    R1A, R1B = cue("L4", "run.", 0.3), cue("L5", "out.", 0.3)             # run 1: the pantheon's 300 years
    R2A, R2B = cue("L12", "Run", 0.25), cue("L12", "burns.", 0.1)          # run 2: 500 years of the faith
    clock = [[H, 500], *jump(RESET, 500, 0), [R1A, 0], lin(R1B, 300), *jump(REWIND, 300, 0),
             [R2A, 0], lin(R2B, 500), [WIPE, 500]]
    speed = [[H, 1], [cue("L4", "run."), 1], [R1A, 6], [R1B, 6], [cue("L6", "Nobody"), 1],
             [R2A, 1], [cue("L12", "Run", 0.5), 6], [R2B, 6], [cue("L13", "Rule"), 1]]

    # ---- the fear map. Rule cues: each fear is named, then its light is lit as its answer is spoken.
    D_NAME, D_LIT = cue("L8", "death."), cue("L8", "Candles")
    L_NAME, L_LIT = cue("L9", "lake."), cue("L9", "boat")
    H_NAME, H_LIT = cue("L10", "hunger."), cue("L10", "Hoarding")
    E_NAME, E_LIT = cue("L11", "eclipse."), cue("L11", "Keepers")
    BLOOM = cue("L7", "dark.", -0.1)                                        # the shadows bloom over the map
    # today (frame 0): every fear answered; the lazy version: no fears drawn at all; the dark: all four, unanswered
    stag = lambda k: shift(BLOOM, 0.12 * k)
    darkF = lambda k: [[H, 1], *jump(RESET, 1, 0), *jump(REWIND, 0, 0), [stag(k), 0], [shift(stag(k), 0.7), 1], [WIPE, 1]]
    litF = lambda on: [[H, 1], *jump(RESET, 1, 0), [on, 0], [shift(on, 0.7), 1, "out"], [WIPE, 1]]
    fears = [
        fear("death", *CAIRN, 5.2, darkF(0), litF(D_LIT), "DEATH", "CANDLES AT THE CAIRN", light=2.6, lamp=True),
        fear("lake", *LAKE, 6.4, darkF(1), litF(L_LIT), "THE LAKE", "A LAMP IN EVERY BOAT", light=4.2),
        fear("hunger", FIELD[0], FIELD[1], 5.2, darkF(2), litF(H_LIT), "HUNGER", "HOARDING IS A SIN", light=3.2),
        fear("eclipse", *VALLEY, 5.8, darkF(3), litF(E_LIT), "THE ECLIPSE", "KEEPERS READ THE SKY", light=3.4, lamp=True),
    ]
    # the eclipse itself: its shadow drifts across the valley at the hook, again in run 2, and back onto frame 0's
    # spot by the loop point
    hook_end = tcue(RESET) or 7.0
    ux = [[H, UMBRA_X0], lin(RESET, UMBRA_X0 + UMBRA_V * hook_end), *jump(RUN2, UMBRA_X0 + UMBRA_V * hook_end, -14.0),
          lin(cue("L12", "burns.", 0.4), 16.0), *jump(WIPE, 16.0, UMBRA_X0 - UMBRA_V * span), lin(END, UMBRA_X0)]
    udark = [[H, 1], *jump(RESET, 1, 0), *jump(RUN2, 0, 0), [cue("L12", "Run", 0.3), 0], [cue("L12", "again.", 0.2), 1],
             [cue("L12", "burns."), 1], [cue("L12", "burns.", 0.4), 0], *jump(WIPE, 0, 1)]
    fears.append({"id": "umbra", "x": UMBRA_X0, "z": UMBRA_Z, "r": 7.4, "kind": "umbra", "xk": ux, "dark": udark, "label": "THE ECLIPSE", "answer": "KEEPERS READ THE SKY"})
    # the deepest fear: the whole map goes dark; the god is the last light, the one that answers it
    void_dark = [[H, 0], [DEEP, 0], [shift(DEEP, 0.9), 1], [GOD, 1], [shift(GOD, 1.2), 0], *jump(WIPE, 0, 0)]
    void_lit = [[H, 0], [GOD, 0], lin(shift(GOD, 1.3), 1), *jump(WIPE, 1, 0)]
    fears.append({"id": "void", "x": 2.0, "z": -1.0, "r": 30.0, "light": 31.0, "glow": 0.2, "dark": void_dark, "lit": void_lit,
                  "label": "NOBODY LISTENING?", "answer": "SOMEONE LISTENS"})
    # the lazy pantheon: twelve lamps on sunny ground, lit one by one on "twelve", out one by one through run 1
    T_ON, T_OUT0 = cue("L3", "twelve", -0.05), cue("L5", "lamps", -0.1)
    out_dur = (tcue(cue("L5", "out.", 0.3)) - tcue(T_OUT0)) if TIMING.exists() else 1.0
    for k, (gx, gz) in enumerate(GODS):
        on = shift(T_ON, 0.07 * k)
        off = shift(T_OUT0, out_dur * k / len(GODS))
        fears.append({"id": f"god{k}", "x": gx, "z": gz, "r": 1.0, "light": 1.7, "lamp": True,
                      "lit": [[H, 0], [on, 0], [shift(on, 0.35), 1], [off, 1], [shift(off, 0.25), 0], [WIPE, 0]]})

    # ---- the HUD: lamps lit on the map (the world's own lights), and the faithful
    lamps = [[H, 4], *jump(RESET, 4, 0), [T_ON, 0], lin(shift(T_ON, 0.07 * 11 + 0.35), 12), [T_OUT0, 12], lin(cue("L5", "out.", 0.3), 0),
             *jump(D_LIT, 0, 1), *jump(L_LIT, 1, 2), *jump(H_LIT, 2, 3), *jump(E_LIT, 3, 4), *jump(GOD, 4, 5), *jump(WIPE, 5, 4)]
    faithful = [[H, 480], *jump(RESET, 480, 0), *jump(D_LIT, 0, 40), *jump(L_LIT, 40, 90), *jump(H_LIT, 90, 150), *jump(E_LIT, 150, 220),
                [R2A, 220], lin(R2B, 480), [WIPE, 480]]

    # ---- the rites that grow inside each light
    candles = [[H, 1], *jump(RESET, 1, 0), [D_LIT, 0], lin(cue("L8", "cairn.", 0.1), 1), [WIPE, 1]]
    boats = [[H, 1], *jump(RESET, 1, 0), [L_LIT, 0], lin(cue("L9", "lamp.", 0.1), 1), [WIPE, 1]]
    sheaves = [[H, 8], *jump(RESET, 8, 0), [H_LIT, 0], lin(cue("L10", "sin.", 0.1), 8), [WIPE, 8]]
    ripe = [[H, 1], *jump(RESET, 1, 1), *jump(REWIND, 1, 0.5), [H_NAME, 0.5], lin(H_LIT, 1), [WIPE, 1]]
    keepers = [[H, 0.22], *jump(RESET, 0.22, 0), [E_LIT, 0], lin(cue("L11", "read", 0.1), 0.22), [WIPE, 0.22]]
    shrine = lambda k: [[H, 0], [shift(cue("L5", "Shrines"), 0.15 * k), 0], [shift(cue("L5", "rise."), 0.15 * k), 1, "out"], *jump(REWIND, 1, 0), [WIPE, 0]]
    # the crowd: today they look up at the eclipse with lamps in their hands; at the twist they look up at the god
    look = [[H, 1], *jump(RESET, 1, 0), [cue("L14", "made", -0.1), 0], [cue("L14", "listens."), 1], [cue("L15", "real.", 0.3), 1],
            [cue("L16", "Gods", -0.3), 0], *jump(WIPE, 0, 1)]
    plamps = [[H, 1], *jump(RESET, 1, 0), [E_LIT, 0], lin(cue("L11", "sky.", 0.2), 0.6), [WIPE, 1]]
    ruler = [pk(H, *QUEEN, "alert", face=0), pk(shift(RESET, 0.0), *QUEEN, "idle", face=0), pk(cue("L18", "lying.", -0.1), *QUEEN, "alert", face=0)]
    g_now = [pk(H, *G_NOW, "idle", face=160)]
    rift = [[H, 0], [cue("L18", "lying.", -0.15), 0], [cue("L18", "lying.", 0.35), 1], [cue("L18", "lying.", 0.85), 1], [cue("L18", "lying.", 1.05), 0]]
    fears.append({"id": "rift", "x": -0.5, "z": 10.6, "r": 0.0, "kind": "rift", "to": [12.0, 8.8], "dark": rift})
    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run")]
    bells = [cue("L11", "sky."), cue("L12", "again.")]

    # Camera language: the map table. Almost straight down, north up; poses only slide and zoom across the map.
    slide = lambda at, pose, dur=0.9, **kw: cam(at, 0, dur=dur, **pose, **kw)
    jumpto = lambda at, pose, **kw: cam(at, 0, dur=0.01, cut=True, **pose, **kw)
    LESSON_AT = cue("L16", "Gods", -0.25)
    camera = [
        cam(H, 0, drift=HOOK_DRIFT, **HOOK_POSE),
        jumpto(RESET, LAZY_POSE),
        slide(cue("L4", "run.", 0.05), MAP, dur=1.0),
        slide(cue("L5", "lamps", -0.2), dict(MAP, dist=168, target=(4.0, 2.0, -1.0)), dur=1.4),
        slide(cue("L6", "Nobody", -0.2), dict(MAP, dist=128, target=(8.0, 2.0, -3.0)), dur=1.6),
        jumpto(REWIND, MAP),
        slide(cue("L7", "Four", -0.1), DARK_POSE, dur=1.2),
        # each rule: slide to the fear as it is named, push in as its light is lit
        slide(RULES, dict(P_DEATH, dist=124)), slide(D_LIT, P_DEATH, dur=1.4),
        slide(cue("L9", "Two:", -0.1), dict(P_LAKE, dist=134)), slide(L_LIT, P_LAKE, dur=1.4),
        slide(cue("L10", "Three:", -0.1), dict(P_HUNGER, dist=124)), slide(H_LIT, P_HUNGER, dur=1.2),
        slide(cue("L11", "Four:", -0.1), dict(P_ECLIPSE, dist=130)), slide(E_LIT, P_ECLIPSE, dur=1.4),
        slide(RUN2, MAP, dur=0.8),
        slide(cue("L12", "hundred", -0.1), dict(MAP, dist=168, target=(0.0, 2.0, -2.0)), dur=1.6),
        slide(TWIST, dict(MAP, dist=150), dur=0.8),
        slide(DEEP, dict(MAP, dist=184), dur=1.2),
        slide(GOD, dict(MAP, dist=160), dur=1.6),
        slide(ROLE, P_ROLE, dur=0.9, drift=0.3),
        # the lesson: the only turn in the episode, the map rotating slowly on the table
        cam(LESSON_AT, 8, EL, 176, (1.0, 2.0, 0.4), fov=26, dur=1.4, drift=3.0),
        cam(WIPE, -HOOK_DRIFT * span, HOOK_POSE["el"], HOOK_POSE["dist"], HOOK_POSE["target"], fov=HOOK_POSE["fov"], cut=True, drift=HOOK_DRIFT),
    ]
    if SCOUT:
        camera = [cam(H, 0, **MAP)]
    light = [
        {"at": H, "mood": "golden"},
        {"at": RESET, "mood": "day", "dur": 0.4},
        {"at": cue("L6", "Nobody", -0.2), "mood": "gloom", "dur": 0.6},
        {"at": REWIND, "mood": "day", "dur": 0.3},
        {"at": RULES, "mood": "day", "dur": 0.6},
        {"at": TWIST, "mood": "dusk", "dur": 0.5},
        {"at": GOD, "mood": "golden", "dur": 1.2},
        {"at": ROLE, "mood": "day", "dur": 0.4},
        {"at": cue("L16", "Gods", -0.3), "mood": "golden", "dur": 1.6},
    ]
    human_valley = {
        "buildings": [{"kind": k, "a": list(a), "face": 0} for k, a in HUMAN_B],
        "roof": [[H, 1]], "pens": [{"a": [-6.4, -1.4], "r": 1.6}], "cover": [[H, 1]],
        "roads": {"b": HUMAN_ROAD}, "route": [[H, 1]], "tradeKey": "tradeH", "lanterns": [[H, 0]],
        "tower": {"x": HUMAN_TOWER[0], "z": HUMAN_TOWER[1], "h": 6.0, "keys": [[H, 1]], "rings": bells},
    }
    clear = [*GODS, *SHRINES, VALLEY, CAIRN, (FIELD[0], FIELD[1]), *[tuple(c) for c in CROWD]]
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": [[H, 24]], "max": 30, "base": 24, "centers": [[-9.5, -1.0], [-8.4, 1.2]], "skin": "sheep"},
        "pred": [[H, 1]],
        "predators": [{"id": "g1", "scale": 1.3, "keys": g_now, "adorn": True}],
        "series": {"lamps": lamps, "faithful": faithful, "tradeH": [[H, 4]]},
        "settlement": human_valley,
                "people": {"count": [[H, 30], [WIPE, 30]], "centers": CROWD, "spread": 1.6, "life": 70, "royal": keepers, "robe": ROBE,
                   "look": look, "lamps": plamps,
                   "ruler": {"keys": ruler, "dais": {"x": DAIS[0], "z": DAIS[1], "face": 0}}},
        "fields": {"plots": [{"x": FIELD[0], "z": FIELD[1], "w": FIELD[2], "d": FIELD[3]}], "ripe": ripe},
        "props": [{"kind": "cairn", "x": CAIRN[0], "z": CAIRN[1], "stones": [[H, 3]]},
                  {"kind": "offerings", "x": CAIRN[0], "z": CAIRN[1], "r": 1.7, "lights": candles},
                  {"kind": "lanterns", "x": LAKE[0], "z": LAKE[1], "r": 3.8, "n": 9, "lights": boats},
                  {"kind": "sheaves", "x": FIELD[0], "z": FIELD[1], "r": 2.7, "n": 8, "sheaves": sheaves},
                  *[{"kind": "shrine", "x": x, "z": z, "face": 0, "r": 1.6, "rise": shrine(k), "lights": [[H, 0]]} for k, (x, z) in enumerate(SHRINES)],
                  {"kind": "statue", "x": STATUE[0], "z": STATUE[1], "face": -90, "rise": [[H, 1]], "gild": [[H, 1]], "tar": [[H, 1]], "grow": [[H, 1.35]], "torch": [[H, 0]]},
                  {"kind": "border", "x": LINE_A[0], "z": LINE_A[1], "to": list(LINE_B), "skip": [0.46, 0.65], "rise": [[H, 1]]},
                  {"kind": "relic", "x": RELIC[0], "z": RELIC[1], "face": -90, "rise": [[H, 1]]}],
        "fears": fears,
        "clearTrees": [[d[0], d[1], 2.2] for d in clear] + [[VALLEY[0], VALLEY[1], 4.0]],
        "layers": {"ripple": ripple},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "DEATH", "text": "candles at the cairn", "at": cue("L8", "death.")},
    {"n": 2, "label": "THE LAKE", "text": "a lamp in every boat", "at": cue("L9", "lake.")},
    {"n": 3, "label": "HUNGER", "text": "hoarding is a sin", "at": cue("L10", "hunger.")},
    {"n": 4, "label": "ECLIPSE", "text": "keepers read the sky", "at": cue("L11", "eclipse.")},
    {"n": 5, "label": "THE GOD", "text": "written last", "at": cue("L7", "Four"), "locked": True, "unlockAt": cue("L15", "last,", -0.1)},
]
SPRITE = {"sprite": "ep33/lamp_sprite.png", "spriteW": 60, "spriteH": 130}


def tag(fid, at, end, lift=60, dx=0, **kw):
    return {"fear": fid, "at": at, "end": end, "lift": lift, "dx": dx, **kw}


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "NOT GODS FIRST", "color": LAMP, "size": 60, "pulseAt": cue("L1", "gods.")},
                 {"text": "WHAT DO THEY FEAR?", "color": DREAD, "size": 58, "pulseAt": cue("L1", "fear?")}]
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 60, "start": {"shot": "hook"}, "end": cue("L2", "Meet", -0.1), "preShow": True},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 33 · BELIEF", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "fearTags", "start": cue("L1", "What", -0.05), "end": RESET, "tags": [tag("umbra", cue("L1", "What", -0.05), cue("L2", "Meet", -0.1), lift=150, text="THE LAMPS STAY LIT")]},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Meet", -0.05), "end": RESET, "dietAt": cue("L2", "empty"),
         "kicker": "FIELD CARD · NO. 008", "kind": "RELIGION", "name": "THE LAMPLIGHT", "dietLabel": "PRAYS TO", "diet": "an empty sky", **SPRITE},
    ]
    G["setup"] += [
        {"type": "blockWipe", "at": RESET, "dur": 0.34, "color": "#3a3410"},
        {"type": "kinetic", "parts": [{"text": "12 GODS FIRST", "at": cue("L3", "twelve"), "size": 80}, {"text": "ONE JOB EACH", "at": cue("L3", "one"), "color": "rust", "size": 58}],
         "y": 470, "size": 80, "start": cue("L3", "twelve", -0.05), "end": cue("L4", "Press", -0.15)},
        {"type": "simBar", "counters": [{"icon": "lantern", "label": "LAMPS", "key": "lamps", "color": LAMP, "digits": 2},
                                        {"icon": "mortal", "label": "FAITHFUL", "key": "faithful", "color": "ember", "digits": 3}],
         "compact": True, "start": cue("L4", "Press", -0.15), "end": cue("L16", "Gods", -0.3), "runAt": [cue("L4", "run."), cue("L12", "Run")]},
    ]
    G["run1"] += [
        {"type": "kinetic", "parts": [{"text": "SHRINES RISE", "at": cue("L5", "Shrines"), "color": "parchment", "size": 56},
                                      {"text": "NOBODY COMES", "at": cue("L5", "Nobody"), "color": "parchment", "size": 56},
                                      {"text": "THE LAMPS GO OUT", "at": cue("L5", "lamps"), "color": "rust", "size": 56}],
         "y": 468, "size": 56, "start": cue("L5", "Shrines", -0.05), "end": cue("L6", "Nobody", -0.25)},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "UNNEEDED", "sub": "12 GODS · 0 FEARS ANSWERED", "color": "rust", "y": 560, "size": 84, "start": cue("L6", "god"), "end": cue("L6", "need.", 0.5)},
    ]
    dark_tags = [tag("death", cue("L7", "dark.", 0.3), RULES, lift=50), tag("lake", cue("L7", "dark.", 0.42), RULES, lift=50),
                 tag("hunger", cue("L7", "dark.", 0.54), RULES, lift=50), tag("eclipse", cue("L7", "dark.", 0.66), RULES, lift=50)]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "need.", 0.55), "end": cue("L7", "Real", 0.3)},
        {"type": "blockWipe", "at": cue("L6", "need.", 0.53), "dur": 0.34},
        {"type": "kinetic", "parts": [{"text": "REAL FAITH", "at": cue("L7", "Real"), "size": 78}, {"text": "STARTS IN THE DARK", "at": cue("L7", "starts"), "color": DREAD, "size": 58}],
         "y": 470, "size": 84, "start": cue("L7", "Real", -0.05), "end": cue("L7", "Four", -0.15)},
        {"type": "fearTags", "start": cue("L7", "dark.", 0.3), "end": RULES, "tags": dark_tags},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L16", "Gods", -0.3),
         "kicker": "THE LAMPLIGHT · WHAT THEY FEAR", "title": "LIGHT THE DARK", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L8", "Candles", -0.3), 0], [cue("L8", "Candles", 0.0), 1], [ROLE, 1], [shift(ROLE, 0.3), 0]]},
    ]
    rule = lambda fid, name, lit, end: {"type": "fearTags", "start": name, "end": end, "tags": [tag(fid, name, end, lift=70)]}
    G["death"] += [rule("death", cue("L8", "death."), cue("L8", "death."), cue("L9", "Two:", -0.15))]
    G["lake"] += [rule("lake", cue("L9", "lake."), cue("L9", "boat"), cue("L10", "Three:", -0.15))]
    G["hunger"] += [rule("hunger", cue("L10", "hunger."), cue("L10", "Hoarding"), cue("L11", "Four:", -0.15))]
    G["eclipse"] += [rule("eclipse", cue("L11", "eclipse."), cue("L11", "Keepers"), cue("L12", "Run", -0.15))]
    G["run2"] += [
        {"type": "stamp", "text": "STILL BURNING", "sub": "500 YEARS · 4 LAMPS · 480 FAITHFUL", "color": LAMP, "rotate": -4, "y": 880, "size": 90, "start": cue("L12", "burns."), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}, {"text": "THE DEEPEST FEAR", "at": cue("L13", "deepest"), "color": DREAD, "size": 72}],
         "size": 150, "y": 540, "start": cue("L13", "Rule", -0.02), "end": cue("L13", "That", -0.12)},
        {"type": "kinetic", "parts": [{"text": "NOBODY", "at": cue("L13", "nobody"), "color": DREAD, "size": 84}, {"text": "LISTENING?", "at": cue("L13", "listening."), "color": DREAD, "size": 84}],
         "size": 84, "y": 560, "start": cue("L13", "nobody", -0.05), "end": shift(GOD, -0.1)},
        {"type": "kinetic", "parts": [{"text": "SO THEY MADE", "at": GOD, "color": "parchment", "size": 60}, {"text": "A GOD", "at": cue("L14", "god."), "color": LAMP, "size": 120}],
         "size": 84, "y": 540, "start": shift(GOD, -0.02), "end": shift(ROLE, -0.05)},
    ]
    G["role"] += [
        {"type": "followChip", "start": cue("L15", "real.", 0.2), "end": cue("L16", "answers", 0.3), "text": "FOLLOW", "sub": "PART 33/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "Gods", -0.3), **({"unlockAt": cue("L16", "Gods", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "Gods", -0.3), "end": WIPE, "kicker": "BEFORE YOU WRITE A GOD", "title": "THE LAMPLIGHT", **SPRITE,
         # the line to keep: on screen from the end of the first sentence until the wipe covers the card
         "subtitle": "Every god answers a fear.", "subtitleAt": cue("L16", "first.")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 33 / 50",
         "title": "How Do You Invent a Believable Religion?", "cta": "COMMENT", "icon": "bubble", "with": "Ask it in their words.", "withAt": cue("L17", "gods?", -0.05), "choiceSize": 30,
         "choices": [{"text": "WHY DO WE DIE?", "color": LAMP, "at": cue("L17", "question")}, {"text": "ARE YOU THERE?", "color": LAMP, "at": cue("L17", "people")}]},
    ]
    gone = cue("L18", "lying.", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 33, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6, "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone, "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 34"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "34:", -0.1), "revealAt": cue("L18", "gods", nth=1), "end": gone,
         "kicker": "NEXT RUN · 34", "title": "THE LIE", "sub": "THE GODS ARE LYING.", "sprite": "rift", "spritePx": 12},
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 60, "start": cue("L18", "lying.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("Gods invented first answer nothing, so nobody needs them. Start with what your people fear: death, the lake "
          "that drowns their fishers, a hungry winter, a sky that goes dark. Give each fear an answer and let a rite "
          "grow around it: candles, lamps, a shared harvest, keepers. Then write the god last, as the answer to the "
          "deepest fear of all: that nobody is listening. Every god answers a fear.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Close EP32's loop (the sun went dark on 'a god built from fear') and stop the scroll on the question.",
             "Golden hour, from almost straight above: the eclipse's round shadow lies over the valley village, drifting east. Inside it the crowd stands with lamps held up, faces turned to the sky (to the camera), and the keepers' lamp post burns at the centre in its pool of light; round the map the other answered fears glow (candles at the cairn, boats with lamps on the lake). NOT GODS FIRST / WHAT DO THEY FEAR? from frame 0, each line pulsing on its word. A map tag on the shadow: THE ECLIPSE · THE LAMPS STAY LIT. Then the field card: THE LAMPLIGHT · RELIGION · PRAYS TO: an empty sky.",
             "The map table: overhead (az 0, el 80, dist 84, fov 24), north up, a slow 0.4°/s turn; the loop lands on the same frame.", ("kinetic, sting, map tag, field card", "the crowd with lamps, the eclipse's shadow", "the valley, the tower"),
             "Golden hour, under an eclipse.", "NOT GODS FIRST / WHAT DO THEY FEAR? · FIELD CARD NO. 008 · THE LAMPLIGHT", "Lamplight block wipe into the lazy version.", "Vigil: a bell tolls the theme over bowed glass; a hit on 'fear?'."),
    "setup": ("The lazy version: twelve gods first.",
              "A wipe to an unbelieving Isle in daylight: no shadows, no lamps, no rites; the crowd wanders. On 'twelve' twelve gods' lamps pop up one by one on sunny ground all over the map, each in a small pool of light that answers nothing. 12 GODS FIRST / A NAME · A JOB. The sim bar arrives (LAMPS 12, FAITHFUL 000) and RUN is pressed.",
              "Map table (dist 150).", ("kinetic, sim bar", "twelve lamps on bright ground", "the Isle"), "Day.", "12 GODS FIRST · ONE JOB EACH", "A pull-out to the whole map on 'run'.", "Lantern, thin (the celesta alone)."),
    "run1": ("Run the lazy version: 300 years of gods nobody needs.",
             "The whole map; YEAR 0→300; three shrines rise beside the lamps, nobody walks to them, and the twelve lamps go out one by one (LAMPS 12→0, FAITHFUL 000). SHRINES RISE, NOBODY COMES, THE LAMPS GO OUT.",
             "Map table, the whole Isle (dist 178).", ("sim bar, kinetic", "the lamps going out, the empty shrines", "void"), "Day.", "SHRINES RISE / NOBODY COMES / THE LAMPS GO OUT", "Slide down onto the empty shrines.", "Drive."),
    "drop": ("The punchline: nobody prays to a god they don't need.", "Gloom over the map: the dark lamps and empty shrines: UNNEEDED · 12 GODS · 0 FEARS ANSWERED.",
             "Map table, pushed in (dist 128).", ("stamp", "the empty shrines", "void"), "Gloom.", "UNNEEDED · 12 GODS · 0 FEARS ANSWERED", "Rewind + block wipe.", "Drop; a boom on 'need'."),
    "rehook": ("Re-hook: the thesis, then four fears and one locked.",
               "REWIND to the Isle before any faith, at dusk: the shrines and lamps are gone. On 'dark' four shadows bloom over the map one after another and are labelled in dread grey: DEATH (the cairn), THE LAKE, HUNGER (the field), THE ECLIPSE (the valley). REAL FAITH / STARTS IN THE DARK; then the checklist LIGHT THE DARK, row 5 locked (the twist).",
               "Map table (dist 178 → 132).", ("rewind, kinetic, map tags, checklist", "four shadows", "the Isle at dusk"), "Dusk.",
               "REAL FAITH · STARTS IN THE DARK · DEATH · THE LAKE · HUNGER · THE ECLIPSE · LIGHT THE DARK 0/5", "Slide to the cairn.", "Vigil; a riser into 'the twist'."),
    "death": ("Rule 1: death.", "The map slides to the cairn in its shadow (DEATH); on 'Candles' a light opens from the cairn and pushes the shadow back, a lamp post rises and a ring of candles lights round the cairn: DEATH · CANDLES AT THE CAIRN.",
              "Map table: slide (dist 92), then push in (70) as the light opens.", ("map tag, checklist (folded)", "the candle ring", "the shadow"), "Day.", "1 DEATH · candles at the cairn", "Slide to the lake.", "Lantern 1: celesta."),
    "lake": ("Rule 2: the lake.", "The lake in its shadow (THE LAKE); on 'boat' the light spreads over the water and nine boats come out, each with a lamp: THE LAKE · A LAMP IN EVERY BOAT.",
             "Map table: slide, then push in.", ("map tag, checklist (folded)", "the boats with lamps", "the lake"), "Day.", "2 THE LAKE · a lamp in every boat", "Slide north to the field.", "Lantern 2: a dulcimer joins."),
    "hunger": ("Rule 3: hunger, and a rule: hoarding is a sin.", "The bare field in its shadow (HUNGER); the crop ripens as the light opens and eight sheaves are stood round it, shared: HUNGER · HOARDING IS A SIN.",
               "Map table: slide, then push in.", ("map tag, checklist (folded)", "the ripe field, the sheaves", "the north meadow"), "Day.", "3 HUNGER · hoarding is a sin", "Slide to the valley.", "Lantern 3: a hand drum and pizzicato bass."),
    "eclipse": ("Rule 4: the eclipse, and an institution: keepers.", "The valley in its shadow (THE ECLIPSE); on 'Keepers' the light opens round the village, a lamp post rises, robed keepers appear among the crowd, lamps come out in people's hands and the tower bell rings on 'sky': THE ECLIPSE · KEEPERS READ THE SKY.",
                "Map table: slide, then push in.", ("map tag, checklist (folded)", "the keepers, the lamps", "the valley"), "Day.", "4 ECLIPSE · keepers read the sky", "Slide out to the whole map.", "Lantern 4: the theme on ocarina, bells on the roots."),
    "run2": ("Run with the fears answered: 500 years, still burning.",
             "The whole map; YEAR 0→500; an eclipse's shadow sweeps across the Isle from west to east and every lamp holds inside it; FAITHFUL climbs to 480: STILL BURNING · 500 YEARS · 4 LAMPS · 480 FAITHFUL, stamped in lamplight.",
             "Map table, the whole Isle (dist 178 → 168).", ("sim bar, stamp", "the eclipse crossing, four lamps", "void"), "Day.", "STILL BURNING · 500 YEARS · 4 LAMPS · 480 FAITHFUL", "Pull out.", "Drive with the theme; a stab and a cymbal on 'burns'."),
    "twist": ("The locked rule: the deepest fear. The god comes last.",
              "Dusk: RULE 5? THE DEEPEST FEAR; on 'deepest' one shadow spreads over the whole map until only the four lamps burn: NOBODY / LISTENING?. On 'listens' every face on the Isle turns up to the camera, and a light opens from the middle of the map and sweeps out past the coast: SO THEY MADE / A GOD.",
              "Map table, pulled out to the whole Isle (dist 184 → 160).", ("kinetic", "the whole Isle dark, then lit", "dusk to golden"), "Dusk → golden.",
              "RULE 5? THE DEEPEST FEAR · NOBODY LISTENING? · SO THEY MADE A GOD", "Slide to the valley.", "Twist (a held A7♭9), a boom on 'listening', then the vigil."),
    "role": ("Unlock rule 5: the god is written last.",
             "Daylight over the valley: the crowd still looking up; the checklist opens and row 5 unlocks on 'last': THE GOD · written last · 5/5. The follow chip (+ FOLLOW · PART 33/50) appears after 'real'.",
             "Map table (dist 96), a slow 0.3°/s turn.", ("open checklist, follow chip", "faces turned up", "the valley"), "Day.", "5 THE GOD · written last · 5/5", "The card goes full.", "Anthem from 'Write'; a D-major hit on 'last'."),
    "lesson": ("The takeaway.", "The full card (BEFORE YOU WRITE A GOD · THE LAMPLIGHT, all five rows ticked) over the whole map in golden light, with 'Every god answers a fear.' in serif italic from the end of the first sentence.",
               "Map table, the whole Isle, rotating 3°/s: the only turn in the episode.", ("full card, follow chip", "the lit map", "stars"), "Golden hour.", "BEFORE YOU WRITE A GOD · THE LAMPLIGHT · Every god answers a fear.", "Block wipe to the end card.", "Anthem; the World Engine chime as the card lands."),
    "cta": ("Comment CTA: what would your people ask their gods?", "End card: logo, PART 33 / 50, the title, and a COMMENT panel where two starter questions pop (WHY DO WE DIE?, ARE YOU THERE?), then 'Ask it in their words.'",
            "Cut (under the block wipe) back to the hook pose, drifting into it.", ("end card", "the Isle", "void"),
            "Golden hour under the eclipse (the loop frame).", "COMMENT · WHY DO WE DIE? / ARE YOU THERE? · Ask it in their words.", "The card lifts on 'Part'.", "Outro."),
    "next": ("Say the part number, ask for the follow with a reason (part 34), open the next loop.",
             "The hook frame; PART 33/50; FOLLOW FOR PART 34, pressed on 'Follow'; NEXT RUN · 34 decodes from a locked crack in the ground to THE LIE · THE GODS ARE LYING. In the world, on 'lying', a crack of light opens across the meadow south of the lake for a breath (something under the Isle that the myth leaves out) and closes; the eclipse's shadow slides back onto frame 0's spot and the hook title returns.",
             "The hook frame.", ("progress bar, follow button, next-run card", "the crack of light", "the eclipse"), "Golden hour under the eclipse.",
             "PART 33/50 · FOLLOW FOR PART 34 · NEXT RUN: THE LIE · THE GODS ARE LYING.", "Loop to frame 0.", "Tease over a held A, a crack and a groan on 'lying', the engine chime on 'Follow'."),
}


def build():
    ep = {
        "id": "ep33", "number": 33, "season": 2,
        "title": "How Do You Invent a Believable Religion?",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.04},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same lab host, a cartographer this time. The hook is a gentle correction, then a real question. 'One job each' is the knowing setup; 'Nobody prays to a god they don't need' lands dry. "
                         "The rules are crisp, two beats each. 'That nobody is listening' is the quiet reveal; 'So they made someone who listens' is warm. The comment ask is a genuine invitation.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L3", "from": "twelve"}, {"line": "L5", "from": "Shrines"}, {"line": "L7", "from": "Real", "to": "Four"}, {"line": "L13", "from": "Rule"},
                        {"line": "L14", "from": "So"}],
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
             hit("towerBell", cue("L1", "gods."), -20), hit("eclipse", cue("L1", "fear?", -0.3), -17),
             hit("cardSlide", cue("L2", "Meet", -0.05), -18), hit("check", cue("L2", "empty"), -20)],
    "setup": [hit("rewind", RESET, -15), hit("lampOn", cue("L3", "twelve"), -19), hit("stamp", cue("L3", "one"), -20),
              hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "out.", 0.3), -22),
             hit("restore", cue("L5", "Shrines"), -17), hit("crownPass", cue("L5", "Nobody"), -19),
             bed("losses", cue("L5", "lamps", -0.1), cue("L5", "out.", 0.3), -19)],
    "drop": [hit("stamp", cue("L6", "god"), -10)],
    "rehook": [hit("rewind", cue("L6", "need.", 0.5), -11), bed("creep", cue("L7", "dark.", -0.15), cue("L7", "come", 0.1), -17), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "death": [hit("check", cue("L8", "death."), -13), hit("lampOn", cue("L8", "Candles"), -12)],
    "lake": [hit("check", cue("L9", "lake."), -13), hit("lampOn", cue("L9", "boat"), -12)],
    "hunger": [hit("check", cue("L10", "hunger."), -13), hit("lampOn", cue("L10", "Hoarding"), -12), hit("restore", cue("L10", "grain"), -18)],
    "eclipse": [hit("check", cue("L11", "eclipse."), -13), hit("lampOn", cue("L11", "Keepers"), -12), hit("towerBell", cue("L11", "sky."), -15)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L12", "burns."), -22),
             hit("eclipse", cue("L12", "again.", -0.1), -18), hit("towerBell", cue("L12", "again."), -18), hit("stamp", cue("L12", "burns."), -13)],
    "twist": [hit("unlock", cue("L13", "Rule"), -15), bed("creep", DEEP, cue("L13", "listening.", 0.3), -14),
              hit("stamp", cue("L13", "nobody"), -17), hit("lampOn", GOD, -10), hit("worldRipple", GOD, -16)],
    "role": [hit("restore", ROLE, -17), hit("unlock", cue("L15", "last,", -0.1), -10)],
    "lesson": [hit("engineWind", cue("L16", "Gods", -0.8), -15), hit("chime", cue("L16", "Gods", -0.3), -10), hit("cardSlide", cue("L16", "Gods", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("check", cue("L17", "question"), -17), hit("check", cue("L17", "people"), -17)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11), hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "34:", -0.1), -18), hit("unlock", cue("L18", "gods"), -15),
             hit("rift", cue("L18", "lying.", -0.2), -14),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score: the series theme stays (D minor for the problem, D major for the payoff). EP33's band is `vigil` (a bell
# tolling the theme's opening over bowed glass, a cello drone, a rain of celesta stars: a night under a dark sky) and
# `lantern` (a procession of lamps: celesta, then a dulcimer, a hand drum, the theme on ocarina and bells), one family
# per belief lit.
VIGIL_P = {"strings": 92, "mbox": 14}
LANTERN_P = {"strings": 92, "marimba": 15, "lead": 79, "mbox": 14}
BACK_P = {"strings": 48, "marimba": 12, "lead": 73, "mbox": 10}
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 96,
    "sections": [
        msec({"shot": "hook"}, "vigil", ["Dm", "Bb", "Gm", "A"], "D minor", programs=VIGIL_P),
        msec(RESET, "lantern", ["Dm", "Bb", "F", "C"], "D minor", layer=1, programs=LANTERN_P),
        msec(cue("L4", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.85, programs=BACK_P),
        msec(cue("L6", "Nobody", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "need.", 0.5), "vigil", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=4, programs=VIGIL_P),
        msec(cue("L8", "One:", -0.1), "lantern", ["Dm", "C", "Bb", "C"], "D minor", layer=1, programs=LANTERN_P),
        msec(cue("L9", "Two:", -0.1), "lantern", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "lantern", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L11", "Four:", -0.1), "lantern", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True, programs=BACK_P),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(cue("L14", "So", -0.1), "vigil", ["D", "G", "Bm", "A"], "D major", beatsPerChord=2, programs=VIGIL_P),
        msec(cue("L15", "Write", -0.1), "anthem", ["D", "G", "Bm", "A"], "D major", programs=BACK_P),
        msec(cue("L17", "What", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "fear?"), "chord": "Dm"},
        {"kind": "boom", "at": cue("L6", "need."), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "burns."), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "burns.")},
        {"kind": "boom", "at": cue("L13", "listening."), "chord": "Dm"},
        {"kind": "hit", "at": cue("L15", "last,"), "chord": "D"},
        {"kind": "boom", "at": cue("L18", "lying."), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #WritingTips #Lore #WorldcraftShorts"
IG_HOOK = "Don't invent gods first. Ask what your people fear."
BODY = (
    "Inventing a religion? Don't start with gods. What do people fear?\n\n"
    "Meet the Lamplight faith. They pray to an empty sky. The lazy version invents twelve gods first, one job each, "
    "and we ran it: shrines rise, nobody comes, the lamps go out. Nobody prays to a god they don't need.\n\n"
    "Real faith starts in the dark. Death: candles keep the dead company at the cairn. The lake: no boat leaves "
    "without a lamp. Hunger: hoarding grain becomes a sin. The eclipse: keepers rise to read the sky. Run it again: "
    "five hundred years, and every lamp still burns.\n\n"
    "Then the twist: the deepest fear is that nobody is listening. So they made someone who listens. A god. Write it "
    "last, and it feels real.\n\n"
    "Gods don't come first. Every god answers a fear.\n\n"
    "What question would the people of your world ask their gods?\n\n"
    "Part 33 of 50. Follow for part 34: the gods are lying."
)
METADATA = {
    "youtube": {
        "title": "How Do You Invent a Believable Religion? (Worldbuilding)",
        "titleAlternate": "Don't invent gods first. Ask what your people fear.",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 7: History and Mythology. The Lamplight faith and its god are "
        "invented for this video; no real religion is depicted.\n\n" + TAGS,
        "pinnedComment": "What question would the people of your world ask their gods? Why do we die? Are you there? Something stranger? (Part 34: the gods are lying.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated field-card sprite; the island, people, lamps and the fear map are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "Don't invent gods first. Ask what your people fear 🕯️ Four fears, four answers, and rule #5 is the one that makes a god feel real. "
                   "What would your people ask their gods? Part 33/50 · follow for part 34 🌑 " + TAGS,
        "pinnedComment": "What question would the people of your world ask their gods?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "What does the oldest fear in your world sound like when it's said as a prayer?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": IG_HOOK + "\n\n" + BODY + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": f"First {len(IG_HOOK)} characters: '{IG_HOOK}'",
        "pinnedComment": "Save the LIGHT THE DARK card, then tell us: what question would your people ask their gods?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep33] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots, loop span {loop_span():.2f} s")
