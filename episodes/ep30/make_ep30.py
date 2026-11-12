"""Generate episodes/ep30/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep30/make_ep30.py
EP30's own device is THE LEDGER: a pixel balance beam under the world. Every gift the Grimmaw gives the village (the
harvest it guards, the medicine of its shed plates) hangs on the left pan; every cost (fear, raided pens, the tithe)
hangs on the right. The beam tips toward whatever weighs more, and each ritual the village invents is a weight that
levels it: the episode's argument is in the device (worship is a deal with danger, kept in balance by custom). Camera
language: THE WORSHIPPER'S ANGLE, low among the people and looking up at the monster (EP26 orbited, EP27 rode a dragon,
EP28 sat at eye height, EP29 was a locked-off tripod). Motif colour: shrine madder #ef6f9c. Music band: `hymn` (choir,
drone, frame drum) and `rite` (kalimba, frame drums, the theme on pan flute).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep30" / "timing.json"
SCOUT = os.environ.get("SCOUT")  # an overhead camera for the whole episode (layout checks only)


def cue(line, word=None, offset=0.0, nth=None):
    c = {"line": line}
    if word:
        c["word"] = word
    if nth:
        c["nth"] = nth
    if offset:
        c["offset"] = round(offset, 3)
    return c


def timing():
    return json.loads(TIMING.read_text()) if TIMING.exists() else None


# The block wipe into the end card: the world resets to frame 0 under it (the shrine in full honour, the hook pose).
WIPE = cue("L17", "What", -0.3)

LINES = [
    ("L1", "hook", "What if the creature everyone fears is also the source of their harvest?", 0.3, ["fears", "harvest?"]),
    ("L2", "hook", "Meet the Grimmaw. It eats a sheep a moon.", 0.3, ["grimmaw.", "sheep"]),
    ("L3", "setup", "The lazy version: it's a monster, so drive it off.", 0.25, ["lazy", "monster,"]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "Ten years. No more lost sheep. Then the flocks eat the fields.", 0.35, ["lost", "fields."]),
    ("L6", "drop", "No monster. No harvest.", 0.4, ["monster.", "harvest."]),
    ("L7", "rehook", "Fear and need share one scale. Four rules level it. The fifth is the twist.", 0.25, ["scale.", "twist."]),
    ("L8", "offer", "One: offerings. A sheep each moon, so it never raids the pens.", 0.2, ["offerings.", "never"]),
    ("L9", "holy", "Two: holy ground. Nobody farms its meadow.", 0.2, ["holy", "nobody"]),
    ("L10", "harvest", "Three: harvest. It keeps grazers off the crops. It gets the first sheaf.", 0.2, ["grazers", "first"]),
    ("L11", "medicine", "Four: medicine. Keepers gather its shed plates for fevers.", 0.3, ["keepers", "fevers."]),
    ("L12", "run2", "Run it again. Ten years. Still feared. Still fed.", 0.3, ["feared.", "fed."]),
    ("L13", "twist", "Rule five? The keepers. Whoever speaks for it speaks for everyone.", 0.3, ["keepers.", "everyone."]),
    ("L14", "twist", "So it's always hungry. Unless everyone watches it eat.", 0.3, ["always", "watches"]),
    ("L15", "role", "An open rite. Nobody fakes its hunger.", 0.3, ["open", "hunger."]),
    ("L16", "lesson", "Worship isn't superstition. It's a deal with danger.", 0.35, ["superstition.", "danger."]),
    ("L17", "cta", "What creature would your civilization worship despite its danger?", 0.25, ["worship", "danger?"]),
    ("L18", "next", "Part 30 of 50. Follow for part 31: hero, or monster?", 0.25, ["follow", "monster?"]),
]

SHOTS = ["hook", "setup", "run1", "drop", "rehook", "offer", "holy", "harvest", "medicine", "run2", "twist", "role", "lesson", "cta", "next"]


# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle. EP27's humans live in the valley under the cliff (slate and turf, barns, the watchtower, the
# forest road); EP28's Fenn live in their open hall on the lake; the cairn stands on the meadow; the Undying Queen keeps
# her dais on the open east meadow (EP29). EP30 builds the Grimmaw's shrine at the edge of its north-east meadow, where
# EP29's candles were lit, and sows fields on the east meadow below it.
CAIRN = (8.95, -5.38)
LAKE_HALL = (6.0, 4.6)
HUMAN_B = [("hall", (-3.6, -4.6)), ("house", (-1.8, -2.4)), ("house", (-4.8, -2.4)), ("house", (-1.0, -5.8)),
           ("house", (-5.6, -0.9)), ("house", (-3.4, -0.7)), ("house", (0.4, -4.2))]
HUMAN_TOWER = (-6.4, -5.6)
HUMAN_ROAD = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
DAIS = (9.4, -2.2)
QUEEN = (9.1, -2.2)
SHRINE = (13.6, -1.2)                  # the shrine stands before its head, toward the village (south-west)
SHRINE_FACE = -100
G_HOME = (17.0, -3.0)                  # the Grimmaw keeps the east meadow, side-on to the hook camera
G_FACE = 165
G_FAR = (17.6, -9.6)                   # where the lazy version drives it (off the north-east edge)
FIELDS = [(14.2, -7.6, 4.0, 3.0), (17.8, -8.2, 3.0, 3.0), (11.8, -7.8, 2.5, 2.5)]   # north of its meadow
FLOCK = [[-7.2, -1.4], [-6.0, 0.4], [14.6, -11.0]]
CROWD = [[11.0, -0.6], [18.4, 1.8], [12.6, 3.2]]   # to the shrine's sides, not in front of the hook camera
MADDER = "#ef6f9c"
ROBE = "#b84a72"


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


# The lazy version: under a wipe the shrine is gone (nobody honours a monster), then they drive it off.
RESET = cue("L3", "lazy", -0.15)
REWIND = cue("L6", "harvest.", 0.55)
HOOK_DRIFT = 0.6


def loop_span():
    """Seconds from the wipe to the end: the loop camera key drifts this long and lands exactly on the hook pose."""
    tm = timing()
    if not tm:
        return 6.0
    from_line = next(l for l in tm["lines"] if l["id"] == WIPE["line"])
    w = next(w for w in from_line["words"] if w["text"].strip(".,?!:").lower() == WIPE["word"].strip(".,?!:").lower())
    return tm["duration"] - (w["start"] + WIPE.get("offset", 0.0))


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    step = lambda at, v: [at, v, "step"]
    lin = lambda at, v: [at, v, "linear"]
    # ---- the clock (YEARS) and the sim speed: two ten-year runs
    clock = [[shot("hook"), 0], step(RESET, 0), [cue("L4", "run."), 0], lin(cue("L5", "fields.", 0.3), 10), [REWIND, 10], step(cue("L6", "harvest.", 0.8), 0),
             step(cue("L12", "Run", -0.05), 0), [cue("L12", "Run", 0.1), 0], lin(cue("L12", "fed.", 0.2), 10), [cue("L13", "Rule"), 10], step(cue("L13", "Rule", 0.01), 10),
             [WIPE, 10], step(cue("L17", "What", -0.28), 0)]
    speed = [[shot("hook"), 1], [cue("L4", "run."), 1], [cue("L4", "run.", 0.35), 6], [cue("L5", "fields.", 0.3), 6], [cue("L6", "No"), 1],
             [cue("L12", "Run", 0.1), 1], [cue("L12", "Run", 0.4), 6], [cue("L12", "fed.", 0.2), 6], [cue("L13", "Rule"), 1]]

    # ---- the flock: grazes beside the fields while the Grimmaw is near; booms and strips them when it's gone
    herd = [[shot("hook"), 30], step(RESET, 30), [cue("L4", "run.", 0.3), 30], lin(cue("L5", "fields.", 0.2), 150), [REWIND, 150], step(cue("L6", "harvest.", 0.8), 30)]
    graze = [[shot("hook"), 0], [cue("L5", "Then", -0.4), 0], lin(cue("L5", "fields.", 0.4), 0.85), [REWIND, 0.85], step(cue("L6", "harvest.", 0.8), 0)]
    # crops: golden at frame 0 (the fixed village), green under the lazy version, eaten bare in run 1, golden after rule 3
    ripe = [[shot("hook"), 1], step(RESET, 0.62), [cue("L5", "Then"), 0.62], lin(cue("L5", "fields.", 0.4), 0), [REWIND, 0], step(cue("L6", "harvest.", 0.8), 0.62),
            [cue("L10", "grazers", -0.1), 0.62], [cue("L10", "crops.", 0.3), 1.0], [WIPE, 1.0], step(cue("L17", "What", -0.28), 1.0)]
    harvest = [[shot("hook"), 100], step(RESET, 62), [cue("L5", "Then"), 62], lin(cue("L5", "fields.", 0.4), 0), [REWIND, 0], step(cue("L6", "harvest.", 0.8), 62),
               [cue("L10", "grazers", -0.1), 62], [cue("L10", "crops.", 0.3), 100], [WIPE, 100], step(cue("L17", "What", -0.28), 100)]
    # the tithe the shrine shows and the ledger weighs (one world series, so the two always agree)
    tithe = [[shot("hook"), 1], step(RESET, 0), [cue("L8", "sheep", -0.1), 0], [cue("L8", "sheep", 0.3), 1, "out"],
             [cue("L14", "always", -0.1), 1], [cue("L14", "hungry.", 0.3), 5, "linear"], [cue("L14", "watches", -0.1), 5], [cue("L15", "rite.", 0.0), 1],
             [WIPE, 1], step(cue("L17", "What", -0.28), 1)]
    raids = [[shot("hook"), 0], step(RESET, 2), [cue("L5", "lost", -0.1), 2], [cue("L5", "lost", 0.3), 0], [REWIND, 0], step(cue("L6", "harvest.", 0.8), 2),
             [cue("L8", "raids", -0.1), 2], [cue("L8", "pens.", 0.1), 0], [WIPE, 0]]

    # ---- the Grimmaw: adorned (worshipped) in the hook and from rule 1; plain in the lazy version, run 1 and the re-hook
    g_sacred = [pk(shot("hook"), *G_HOME, "idle", face=G_FACE), pk(RESET, *G_HOME, "hidden"), pk(cue("L8", "offerings.", -0.2), *G_HOME, "idle", face=G_FACE),
                pk(cue("L8", "sheep", 0.2), SHRINE[0] + 1.2, SHRINE[1] - 0.6, "idle", dur=1.2), pk(cue("L8", "pens.", 0.0), *G_HOME, "idle", face=G_FACE, dur=1.4),
                pk(cue("L18", "monster?", -0.15), *G_HOME, "alert", face=G_FACE), pk(cue("L18", "monster?", 1.1), *G_HOME, "idle", face=G_FACE)]
    g_plain = [pk(shot("hook"), *G_HOME, "hidden"), pk(RESET, *G_HOME, "idle", face=G_FACE),
               pk(cue("L3", "monster,", 0.0), *G_HOME, "roar", face=-150), pk(cue("L3", "drive", 0.0), *G_HOME, "idle", face=60),
               pk(cue("L3", "off.", 0.0), *G_FAR, "idle", dur=1.6), pk(cue("L4", "run.", 0.2), *G_FAR, "despawn"),
               pk(REWIND, *G_HOME, "appear", face=G_FACE), pk(cue("L7", "Fear"), *G_HOME, "idle", face=G_FACE),
               pk(cue("L8", "offerings.", -0.2), *G_HOME, "hidden")]

    # ---- the people: villagers by the shrine; a share in madder robes (the keepers) who grow powerful in the twist
    count = [[shot("hook"), 20]]
    keepers = [[shot("hook"), 0.14], step(RESET, 0), [cue("L11", "Keepers", -0.1), 0], [cue("L11", "plates", 0.0), 0.14],
               [cue("L13", "keepers.", -0.1), 0.14], [cue("L13", "everyone.", 0.2), 0.6], [cue("L14", "Unless"), 0.6], [cue("L15", "rite.", 0.2), 0.14],
               [WIPE, 0.14], step(cue("L17", "What", -0.28), 0.14)]
    gather = [[shot("hook"), 0.4], step(RESET, 0), [cue("L8", "offerings.", 0.0), 0], [cue("L8", "pens.", 0.0), 0.4],
              [cue("L14", "Unless", 0.0), 0.4], [cue("L14", "eat.", 0.3), 1.0], [cue("L16", "Worship", -0.3), 1.0], [cue("L16", "danger.", 0.0), 0.4],
              [WIPE, 0.4], step(cue("L17", "What", -0.28), 0.4)]
    ruler = [pk(shot("hook"), *QUEEN, "idle", face=0), pk(cue("L18", "monster?", 0.0), *QUEEN, "alert", face=0), pk(cue("L18", "monster?", 1.2), *QUEEN, "idle", face=0)]

    # ---- the shrine: built on rule 1 (and there at frame 0), with candles, the tithe, the first sheaves and shed plates
    shrine_rise = [[shot("hook"), 1], step(RESET, 0), [cue("L8", "offerings.", -0.1), 0], [cue("L8", "offerings.", 0.6), 1, "out"], [WIPE, 1]]
    lights = [[shot("hook"), 1], step(RESET, 0), [cue("L8", "offerings.", 0.4), 0], [cue("L8", "pens.", 0.0), 1, "linear"],
              [cue("L14", "Unless"), 1], [cue("L14", "Unless", 0.01), 1], [WIPE, 1]]
    sheaves = [[shot("hook"), 3], step(RESET, 0), [cue("L10", "first", -0.1), 0], [cue("L10", "sheaf.", 0.5), 3, "linear"], [WIPE, 3], step(cue("L17", "What", -0.28), 3)]
    plates = [[shot("hook"), 2], step(RESET, 0), [cue("L11", "plates", -0.1), 0], [cue("L11", "fevers.", 0.2), 3, "linear"], [WIPE, 3], step(cue("L17", "What", -0.28), 2)]

    # ---- EP31's tease: two villages raise two stones to the same figure, one painted gold (a hero), one rust (a monster)
    # (the shrine's two standing stones are painted: a hero in gold on one, a beast in rust on the other; washed off
    # again before the loop so the last frame matches frame 0)
    paint = [[shot("hook"), 0], [cue("L18", "hero,", -0.05), 0], [cue("L18", "hero,", 0.5), 1, "out"], [cue("L18", "monster?", -0.05), 1],
             [cue("L18", "monster?", 0.5), 2, "out"], [cue("L18", "monster?", 1.1), 2], [cue("L18", "monster?", 1.5), 0]]

    # ---- the seasons flicker while the clock races
    def seasons(a_line, a_word, a_off, n, period, depth=0.5):
        out = []
        for k in range(n):
            b0 = a_off + k * period
            out += [[cue(a_line, a_word, b0), 0], [cue(a_line, a_word, b0 + period * 0.35), depth, "linear"], [cue(a_line, a_word, b0 + period * 0.8), 0, "linear"]]
        return out
    snow = [[shot("hook"), 0]] + seasons("L5", "Ten", 0.0, 6, 0.55) + seasons("L12", "Ten", -0.1, 4, 0.55) + [[cue("L13", "Rule"), 0]]
    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run")]
    rings = [{"x": G_HOME[0] + 1.0, "z": G_HOME[1] + 0.4, "r": 3.6, "on": cue("L9", "ground."), "off": cue("L10", "Three:", -0.2), "color": MADDER}]

    # Camera language: the worshipper's angle. Low among the people, looking UP at the monster over its shrine (a long
    # lens, so it towers); medium and wide only where the episode has to show land (holy ground, the two runs).
    # (every low pose was checked for a clear line of sight over the voxels and trees, and for a camera 1.2-2 units
    # above the grass; see BRIEF.md §6)
    hook_pose = dict(az=-12, el=7, dist=40, target=(15.2, 6.3, -2.1), fov=15)
    lazy_pose = dict(az=-60, el=10, dist=40, target=(17.0, 6.3, -3.0), fov=22)
    wide = dict(el=48, dist=196, target=(4.0, 10.5, 0.0), fov=26)
    span = loop_span()
    camera = [
        cam(shot("hook"), drift=HOOK_DRIFT, **hook_pose),
        cam(RESET, dur=0.01, cut=True, **lazy_pose),
        cam(cue("L4", "run.", 0.05), 18, dur=1.2, **wide),
        cam(cue("L6", "No", -0.2), -140, 8, 16, (14.2, 5.6, -7.6), fov=28, dur=0.01, cut=True),
        cam(REWIND, dur=0.01, cut=True, **lazy_pose),
        cam(cue("L8", "One:", -0.15), -40, 12, 32, (15.4, 6.0, -2.0), fov=20, dur=0.01, cut=True, drift=0.6),
        cam(cue("L9", "Two:", -0.15), 40, 40, 70, (16.0, 5.0, -3.0), fov=24, dur=0.01, cut=True),
        cam(cue("L10", "Three:", -0.15), 160, 16, 44, (15.4, 5.4, -6.0), fov=22, dur=0.01, cut=True, drift=0.6),
        cam(cue("L11", "Four:", -0.15), 25, 18, 34, (14.4, 5.6, -1.4), fov=20, dur=0.01, cut=True, drift=0.6),
        cam(cue("L12", "Run", -0.05), 20, dur=0.01, cut=True, **wide),
        cam(cue("L13", "Rule", -0.1), -25, 9, 30, (14.8, 6.2, -1.4), fov=20, dur=0.01, cut=True),
        cam(cue("L14", "Unless", -0.1), -60, 26, 34, (14.0, 5.4, -1.4), fov=26, dur=0.01, cut=True),
        cam(cue("L16", "Worship", -0.25), 15, 34, 190, (2.0, 3.0, 0.0), fov=26, dur=1.6, drift=2.0),
        cam(WIPE, hook_pose["az"] - HOOK_DRIFT * span, hook_pose["el"], hook_pose["dist"], hook_pose["target"], fov=hook_pose["fov"], cut=True, drift=HOOK_DRIFT),
    ]
    if SCOUT:
        camera = [cam(shot("hook"), 0, 89, 120, (4.0, 0.0, -2.0), fov=30)]
    if os.environ.get("HOOKCAM"):  # candidate hook poses (layout checks only): a JSON list, one pose per 2 s
        camera = [cam({"line": "L1", "offset": round(0.7 * i, 2)} if i else shot("hook"), cut=True, dur=0.01, **c) for i, c in enumerate(json.loads(os.environ["HOOKCAM"]))]
    light = [
        {"at": shot("hook"), "mood": "golden"},
        {"at": RESET, "mood": "day", "dur": 0.4},
        {"at": cue("L6", "No", -0.2), "mood": "gloom", "dur": 0.6},
        {"at": REWIND, "mood": "day", "dur": 0.8},
        {"at": cue("L13", "Rule", -0.2), "mood": "dusk", "dur": 0.6},
        {"at": cue("L14", "Unless", -0.1), "mood": "night", "dur": 0.4},
        {"at": cue("L16", "Worship", -0.3), "mood": "golden", "dur": 2.0},
    ]
    human_valley = {
        "buildings": [{"kind": k, "a": list(a), "face": 0} for k, a in HUMAN_B],
        "roof": [[shot("hook"), 1]],
        "pens": [{"a": [-6.4, -1.4], "r": 1.6}], "cover": [[shot("hook"), 1]],
        "roads": {"b": HUMAN_ROAD}, "route": [[shot("hook"), 1]],
        "tradeKey": "tradeH", "lanterns": [[shot("hook"), 0]],
        "tower": {"x": HUMAN_TOWER[0], "z": HUMAN_TOWER[1], "h": 6.0, "keys": [[shot("hook"), 1]]},
    }
    fenn_hall = {"buildings": [{"kind": "greathall", "a": list(LAKE_HALL), "b": list(LAKE_HALL), "stiltsB": 1.6, "face": 0}],
                 "place": [[shot("hook"), 1]], "open": [[shot("hook"), 1]], "glow": [[shot("hook"), 1]], "roof": [[shot("hook"), 1]], "pens": []}
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": herd, "max": 160, "base": 30, "centers": FLOCK, "skin": "sheep"},
        "pred": [[shot("hook"), 1]],
        "predators": [{"id": "g1", "scale": 1.3, "keys": g_sacred, "adorn": True}, {"id": "g0", "scale": 1.3, "keys": g_plain}],
        "series": {"harvest": harvest, "tithe": tithe, "tradeH": [[shot("hook"), 4]], "raids": raids},
        "settlement": human_valley,
        "settlements": [fenn_hall],
        "folk": {"count": [[shot("hook"), 9]], "centers": [list(LAKE_HALL)], "spread": 2.0, "site": [[shot("hook"), 0]],
                 "eyes": [[shot("hook"), 1]], "wet": [[shot("hook"), 1]], "glow": [[shot("hook"), 1]], "hero": []},
        "people": {"count": count, "centers": CROWD, "spread": 2.0, "life": 70, "royal": keepers, "robe": ROBE,
                   "gather": {"at": [SHRINE[0], SHRINE[1]], "r": 2.8, "keys": gather},
                   "ruler": {"keys": ruler, "dais": {"x": DAIS[0], "z": DAIS[1], "face": 0}}},
        "fields": {"plots": [{"x": x, "z": z, "w": w, "d": d} for x, z, w, d in FIELDS], "ripe": ripe},
        "props": [{"kind": "cairn", "x": CAIRN[0], "z": CAIRN[1], "stones": [[shot("hook"), 3]]},
                  {"kind": "shrine", "x": SHRINE[0], "z": SHRINE[1], "face": SHRINE_FACE, "r": 2.2, "rise": shrine_rise, "lights": lights,
                   "tithe": tithe, "sheaves": sheaves, "plates": plates, "paint": paint}],
        "clearTrees": [[d[0], d[1], 2.8] for d in [DAIS, SHRINE, G_HOME, *[tuple(c) for c in CROWD]]] + [[SHRINE[0] - 1.4, SHRINE[1] + 1.2, 4.6]],
        "layers": {"snow": snow, "graze": graze, "ripple": ripple, "rings": rings},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "TITHE", "text": "a sheep each moon", "at": cue("L8", "offerings.")},
    {"n": 2, "label": "HOLY", "text": "its meadow stays wild", "at": cue("L9", "holy")},
    {"n": 3, "label": "HARVEST", "text": "the first sheaf is its", "at": cue("L10", "harvest.")},
    {"n": 4, "label": "MEDICINE", "text": "keepers gather plates", "at": cue("L11", "medicine.")},
    {"n": 5, "label": "WITNESS", "text": "everyone watches it eat", "at": cue("L7", "level"), "locked": True, "unlockAt": cue("L15", "rite.")},
]
SPRITE = {"sprite": "ep30/grimmaw30_sprite.png", "spriteW": 168, "spriteH": 112}

# The ledger's weights. Gifts: the harvest it guards, the medicine of its plates. Costs: fear, raided pens, the tithe.
LEDGER_ITEMS = [
    {"side": "gift", "icon": "sheaf", "label": "HARVEST", "w": 2,
     "keys": [[cue("L3", "lazy"), 0.5], [cue("L5", "Then"), 0.5], [cue("L5", "fields.", 0.3), 0], [REWIND, 0], [cue("L6", "harvest.", 0.8), 0.5, "step"],
              [cue("L10", "grazers", -0.1), 0.5], [cue("L10", "crops.", 0.2), 1]]},
    {"side": "gift", "icon": "vial", "label": "MEDICINE", "w": 1, "keys": [[cue("L3", "lazy"), 0], [cue("L11", "plates", -0.1), 0], [cue("L11", "plates", 0.3), 1]]},
    {"side": "cost", "icon": "eye", "label": "FEAR", "w": 2,
     "keys": [[cue("L3", "lazy"), 1], [cue("L5", "lost", -0.1), 1], [cue("L5", "lost", 0.3), 0], [REWIND, 0], [cue("L6", "harvest.", 0.8), 1, "step"],
              [cue("L9", "ground.", -0.1), 1], [cue("L9", "meadow.", 0.1), 0.5]]},
    {"side": "cost", "icon": "sheep", "label": "RAIDS", "key": "raids", "w": 1},
    {"side": "cost", "icon": "sheep", "label": "TITHE", "key": "tithe", "w": 1},
]


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "THEY FEAR IT.", "size": 76}, {"text": "IT FEEDS THEM?", "color": MADDER, "size": 76}]
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 76, "start": {"shot": "hook"}, "end": cue("L2", "Meet", -0.1), "preShow": True},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 30 · CREATURES", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Meet", -0.05), "end": RESET, "dietAt": cue("L2", "eats"),
         "kicker": "FIELD CARD · NO. 005", "kind": "WORSHIPPED BEAST", "name": "GRIMMAW", "dietLabel": "TAKES", "diet": "a sheep a moon", **SPRITE},
    ]
    ledger = {"type": "ledger", "y": 1352, "start": cue("L3", "lazy", 0.1), "end": cue("L16", "Worship", -0.3), "items": LEDGER_ITEMS}
    G["setup"] += [
        {"type": "blockWipe", "at": RESET, "dur": 0.34, "color": "#3a1626"},
        {"type": "kinetic", "parts": [{"text": "IT'S A MONSTER", "at": cue("L3", "monster,"), "size": 70}, {"text": "DRIVE IT OFF", "at": cue("L3", "drive"), "color": "rust", "size": 84}],
         "y": 470, "size": 84, "start": cue("L3", "it's", -0.05), "end": cue("L4", "Press", -0.15)},
        ledger,
        {"type": "simBar", "counters": [{"icon": "sheaf", "label": "HARVEST", "key": "harvest", "color": "#e6c357", "digits": 3},
                                        {"icon": "sheep", "label": "FLOCK", "key": "herd", "color": "parchment", "digits": 3}],
         "compact": True, "start": cue("L4", "Press", -0.15), "end": cue("L16", "Worship", -0.3), "runAt": [cue("L4", "run."), cue("L12", "Run")]},
    ]
    G["run1"] += [
        {"type": "pin", "at": [FIELDS[0][0], 3.6, FIELDS[0][1]], "kicker": "THE FLOCKS", "text": "EAT THE FIELDS", "color": "ember", "lift": 80, "size": 28,
         "start": cue("L5", "flocks", -0.1), "end": cue("L6", "No", -0.25)},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "0 HARVEST", "sub": "NO MONSTER · NO FIELDS", "color": "rust", "y": 560, "size": 70, "start": cue("L6", "harvest."), "end": cue("L6", "harvest.", 0.5)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "harvest.", 0.55), "end": cue("L7", "Fear", 0.3)},
        {"type": "blockWipe", "at": cue("L6", "harvest.", 0.53), "dur": 0.34},
        {"type": "kinetic", "parts": [{"text": "FEAR AND NEED", "at": cue("L7", "Fear"), "size": 72}, {"text": "ONE SCALE", "at": cue("L7", "one"), "color": MADDER, "size": 96}],
         "y": 470, "size": 84, "start": cue("L7", "Fear", -0.05), "end": cue("L7", "Four", -0.15)},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L16", "Worship", -0.3),
         "kicker": "GRIMMAW · THE DEAL", "title": "KEEP IT LEVEL", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L9", "Two:", -0.3), 0], [cue("L9", "Two:", 0.05), 1], [cue("L12", "fed.", 0.4), 1], [cue("L12", "fed.", 0.7), 0],
                      [cue("L13", "Rule", -0.35), 0], [cue("L13", "Rule", -0.05), 1], [cue("L15", "rite.", 0.2), 1], [cue("L15", "rite.", 0.5), 0]]},
    ]
    G["run2"] += [
        {"type": "stamp", "text": "FEARED & FED", "sub": "10 HARVESTS · 0 RAIDS", "color": MADDER, "rotate": -4, "y": 880, "size": 80, "start": cue("L12", "fed."), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}, {"text": "THE KEEPERS", "at": cue("L13", "keepers."), "color": MADDER, "size": 88}],
         "size": 150, "y": 600, "start": cue("L13", "Rule", -0.02), "end": cue("L13", "Whoever", -0.1)},
        {"type": "kinetic", "parts": [{"text": "IT'S ALWAYS", "at": cue("L14", "always"), "size": 76}, {"text": "HUNGRY", "at": cue("L14", "hungry."), "color": "rust", "size": 110}],
         "size": 76, "y": 600, "start": cue("L14", "So", -0.05), "end": cue("L14", "Unless", -0.15)},
    ]
    G["role"] += [
        {"type": "pin", "at": [SHRINE[0], 6.0, SHRINE[1]], "kicker": "THE OPEN RITE", "text": "EVERYONE WATCHES", "color": MADDER, "lift": 120, "size": 28,
         "start": cue("L15", "open", 0.0), "end": cue("L16", "Worship", -0.35)},
        {"type": "followChip", "start": cue("L15", "hunger.", 0.3), "end": cue("L16", "danger.", 0.1), "text": "FOLLOW", "sub": "PART 30/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "Worship", -0.3), **({"unlockAt": cue("L16", "Worship", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "Worship", -0.3), "end": cue("L17", "What", -0.52), "kicker": "WHAT THE VILLAGE OWES", "title": "THE GRIMMAW", **SPRITE,
         "subtitle": "Worship is a deal with danger.", "subtitleAt": cue("L16", "danger.")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 30 / 50",
         "title": "Make a Monster That People Worship", "cta": "COMMENT", "icon": "bubble", "with": "What creature would your civilization worship despite its danger?"},
    ]
    gone = cue("L18", "monster?", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 30, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6, "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone, "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 31"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "31:", -0.1), "revealAt": cue("L18", "hero,"), "end": gone,
         "kicker": "NEXT RUN · 31", "title": "DISPUTED", "sub": "HERO, OR MONSTER?", "sprite": "stele", "spritePx": 9},
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 76, "start": cue("L18", "monster?", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("A worshipped monster isn't superstition: it's a deal a society makes with danger. When people depend on what "
          "they fear, they invent customs to keep the deal level (tithes, holy ground, first fruits, keepers), and then "
          "they need customs to keep the keepers honest.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Close EP29's loop (they pray to a monster) and stop the scroll on the question.",
             "Golden hour, low among the villagers and looking up: the Grimmaw, garlanded in wheat and painted in madder, stands framed between the two madder-banded standing stones of its shrine (an altar, a candle ring, a tithe sheep, sheaves, shed plates), villagers before it. THEY FEAR IT. / IT FEEDS THEM? Then the field card: GRIMMAW · WORSHIPPED BEAST · TAKES: a sheep a moon.",
             "Low, long lens (az -12, el 7, dist 40, fov 15), a slow 0.6°/s drift; the loop lands on the same frame.", ("kinetic, field card", "the Grimmaw over its shrine", "golden fields"),
             "Golden hour.", "THEY FEAR IT. / IT FEEDS THEM?", "Madder block wipe into the lazy version.", "Hymn: choir, drone, frame drum; the theme on voice oohs."),
    "setup": ("The lazy version: it's a monster, so drive it off.", "A madder block wipe: no shrine, no garland, a plain Grimmaw on its meadow; it calls, turns and is driven off the north-east edge. IT'S A MONSTER / DRIVE IT OFF. The ledger slides in under the world: HARVEST against FEAR and RAIDS, TIPPED. RUN.",
              "Medium, low (el 10, dist 40, fov 22): the beast against the sky.", ("kinetic, ledger, sim bar", "the Grimmaw leaving", "the meadow"), "Day.", "IT'S A MONSTER · DRIVE IT OFF", "Cut to the wide on 'run'.", "Rite, thin (kalimba)."),
    "run1": ("Run the lazy version: no monster, no harvest.", "Whole Isle; YEAR 0→10; FLOCK 030→150; the costs fall off the ledger ('no more lost sheep'), then the flocks spread over the fields and strip them bare: HARVEST 062→000, the ledger EMPTY.",
             "Wide (dist 196).", ("sim bar, ledger, pin", "the flock booming, the fields going bare", "island, seasons flickering"), "Day, winters flickering.", "THE FLOCKS · EAT THE FIELDS", "Cut to the bare field.", "Drive."),
    "drop": ("The punchline.", "Low on the stripped field, sheep everywhere: 0 HARVEST · NO MONSTER · NO FIELDS.", "Close on the field (el 8, dist 16).", ("stamp", "sheep on bare soil", "the empty meadow"), "Gloom.", "0 HARVEST", "Rewind + block wipe.", "Drop; a boom on 'harvest'."),
    "rehook": ("Re-hook: the thesis, then four easy fixes and one locked.", "REWIND: the Grimmaw back on its meadow; FEAR AND NEED / ONE SCALE; the checklist KEEP IT LEVEL, row 5 locked and blinking; the ledger TIPPED.",
               "Low medium.", ("kinetic, checklist, ledger", "the Grimmaw", "the meadow"), "Day.", "0/5", "Cut on 'One'.", "Mystery; a riser into 'the twist'."),
    "offer": ("Fix 1: a tithe instead of raids.", "The shrine rises out of the ground; the Grimmaw comes to it, garlanded; one sheep at the altar; the candles light one by one; villagers gather. On the ledger RAIDS lift off and one TITHE hangs instead.",
              "Low, long lens (el 6, dist 30, fov 20), a slow drift.", ("checklist, ledger", "shrine, Grimmaw, villagers", "meadow"), "Day.", "1 TITHE · a sheep each moon", "Cut.", "Rite 1: kalimba alone; a frame drum on the tithe."),
    "holy": ("Fix 2: holy ground.", "Medium-high: a madder ring is painted round the Grimmaw's meadow and the land outside dims: nobody farms it, nobody meets it by accident. FEAR halves on the ledger.",
             "Medium-high (el 40, dist 70).", ("checklist (folded), ledger", "the madder ring", "the meadow"), "Day.", "2 HOLY · its meadow stays wild", "Cut.", "Rite 2: frame drums join."),
    "harvest": ("Fix 3: the harvest is its gift.", "Low across the fields toward the Grimmaw: the green crop ripens to gold; three sheaves are laid at the shrine. HARVEST doubles on the ledger: LEVEL.",
                "Over the fields from the north (el 16, dist 44).", ("checklist (folded), ledger", "golden fields, sheaves", "the Grimmaw beyond"), "Day.", "3 HARVEST · the first sheaf is its", "Cut.", "Rite 3: drone bass joins."),
    "medicine": ("Fix 4: medicine, and the keepers.", "Low at the shrine: hooded keepers in madder robes lay shed plates on the altar. MEDICINE joins the gifts: WORTH IT.",
                 "Low, long lens (el 18, dist 34, fov 20), a slow drift.", ("checklist (folded), ledger", "keepers, plates, altar", "the Grimmaw"), "Day.", "4 MEDICINE · keepers gather plates", "Cut to the wide.", "Rite 4: the theme on pan flute, choir, glock."),
    "run2": ("Run with the rituals: feared and fed.", "Whole Isle; YEAR 0→10; HARVEST holds at 100; the flock stays 030; FEARED & FED · 10 HARVESTS · 0 RAIDS.",
             "Wide (dist 196).", ("stamp, ledger", "shrine, golden fields, the flock", "island"), "Day.", "FEARED & FED", "Cut to dusk.", "Drive with the theme; a stab and cymbal on 'fed'."),
    "twist": ("The locked rule: the keepers.", "Dusk, low on the shrine: RULE 5? THE KEEPERS. Madder robes spread through the crowd (whoever speaks for it speaks for everyone). IT'S ALWAYS / HUNGRY: the tithe piles up at the altar, one sheep after another, while the Grimmaw stands still; the ledger tips back: TIPPED.",
              "Low, long lens (el 9, dist 30, fov 20).", ("kinetic, ledger", "keepers, the growing tithe", "dusk"), "Dusk.", "RULE 5? THE KEEPERS · IT'S ALWAYS HUNGRY", "Cut.", "Twist, then hymn (choir, drone) under it."),
    "role": ("Unlock rule 5: an open rite.", "Night: the whole village walks to the shrine and rings it by candlelight; the extra tithe is gone, one sheep remains. THE OPEN RITE · EVERYONE WATCHES; row 5 unlocks (WITNESS · everyone watches it eat); the ledger: WORTH IT.",
             "Medium (el 26, dist 34).", ("pin, unlocked card, ledger, follow chip", "the village in a ring", "night"), "Night.", "THE OPEN RITE; 5/5", "Card goes full.", "A big D-major hit on 'rite'."),
    "lesson": ("The takeaway.", "The full card (WHAT THE VILLAGE OWES, all five rows) with 'Worship is a deal with danger.' in serif italic.",
               "Wide (dist 190), a slow drift.", ("full card", "the island at golden hour", "stars"), "Golden hour.", "Full card.", "Block wipe to the end card.", "Anthem; the World Engine chime as the card lands."),
    "cta": ("Comment CTA.", "End card: logo, PART 30 / 50, title, a speech-bubble COMMENT panel.", "Cut (under the block wipe) back to the hook pose, drifting into it.", ("end card", "the Isle", "void"),
            "Golden hour (the loop frame).", "End card.", "The card lifts on 'Part'.", "Outro."),
    "next": ("Say the part number, ask for the follow with a reason (part 31), open the next loop.",
             "The hook frame; PART 30/50; FOLLOW FOR PART 31; NEXT RUN 31 · DISPUTED from a locked standing stone; in the world two villages raise two stones to the same figure, one painted gold, one rust, and the Grimmaw and the Queen look up; then the hook title returns.",
             "The hook frame.", ("progress bar, follow button, next-run card", "the Grimmaw, the two stones", "the meadow"), "Golden hour.",
             "PART 30/50 · FOLLOW FOR PART 31 · NEXT RUN: DISPUTED · HERO, OR MONSTER?", "Loop to frame 0.", "Tease over a held A, a horn call, the engine chime on 'Follow'."),
}


def build():
    ep = {
        "id": "ep30",
        "number": 30,
        "season": 2,
        "title": "Make a Monster That People Worship",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.06},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same lab host, with a little awe in the hook. 'It's a monster, so drive it off' is the knowing setup. 'No monster. No harvest.' lands dry. "
                         "'Fear and need share one scale' is the thesis. The rules are crisp. 'Whoever speaks for it speaks for everyone' is quiet; 'An open rite' is the reveal. The comment ask is a genuine question.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L3", "from": "it's"}, {"line": "L6", "from": "No"}, {"line": "L7", "from": "Fear", "to": "Four"},
                        {"line": "L13", "from": "Rule", "to": "Whoever"}, {"line": "L14", "from": "So", "to": "Unless"}],
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
    "hook": [hit("chime", {"shot": "hook"}, -11), hit("worldRipple", {"shot": "hook", "offset": 0.05}, -17), hit("frameDrum", cue("L1", "harvest?", 0.05), -16),
             hit("cardSlide", cue("L2", "Meet", -0.05), -18), hit("check", cue("L2", "eats"), -20)],
    "setup": [hit("rewind", RESET, -15), hit("cardSlide", cue("L3", "lazy", 0.1), -18), hit("roar", cue("L3", "monster,", 0.0), -16), hit("stompHit", cue("L3", "monster,", 0.1), -20),
              hit("stamp", cue("L3", "drive"), -19), hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "fields.", 0.2), -22), bed("births", cue("L5", "Then", -0.2), cue("L5", "fields.", 0.2), -23),
             hit("beamTip", cue("L5", "lost", 0.0), -16), hit("cardSlide", cue("L5", "flocks", -0.1), -21), hit("beamTip", cue("L5", "fields.", 0.0), -16)],
    "drop": [hit("stamp", cue("L6", "harvest."), -10)],
    "rehook": [hit("rewind", cue("L6", "harvest.", 0.5), -11), hit("beamTip", cue("L7", "scale."), -15), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "offer": [hit("check", cue("L8", "offerings."), -13), hit("restore", cue("L8", "offerings.", 0.0), -15), hit("frameDrum", cue("L8", "sheep", 0.1), -13),
              hit("beamTip", cue("L8", "pens.", 0.0), -15)],
    "holy": [hit("check", cue("L9", "holy"), -13), hit("ringOn", cue("L9", "ground."), -14), hit("beamTip", cue("L9", "meadow.", 0.0), -15)],
    "harvest": [hit("check", cue("L10", "harvest."), -13), hit("restore", cue("L10", "crops.", -0.2), -16), hit("frameDrum", cue("L10", "sheaf.", 0.0), -14), hit("beamTip", cue("L10", "crops.", 0.2), -15)],
    "medicine": [hit("check", cue("L11", "medicine."), -13), hit("unlock", cue("L11", "plates", 0.0), -17), hit("beamTip", cue("L11", "plates", 0.3), -15)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L12", "fed.", 0.2), -22),
             hit("stamp", cue("L12", "fed."), -13)],
    "twist": [hit("frameDrum", cue("L13", "keepers."), -14), hit("morph", cue("L13", "speaks", 0.0), -18), bed("births", cue("L14", "always", 0.0), cue("L14", "hungry.", 0.3), -24),
              hit("beamTip", cue("L14", "hungry.", 0.2), -14)],
    "role": [hit("restore", cue("L15", "open", -0.1), -14), hit("unlock", cue("L15", "rite."), -10), hit("beamTip", cue("L15", "rite.", 0.1), -15)],
    "lesson": [hit("engineWind", cue("L16", "Worship", -0.8), -15), hit("chime", cue("L16", "Worship", -0.3), -10), hit("cardSlide", cue("L16", "Worship", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("cardSlide", cue("L17", "What", -0.1), -20)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11), hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "31:", -0.1), -18), hit("unlock", cue("L18", "hero,"), -15), hit("restore", cue("L18", "hero,", 0.1), -19),
             hit("restore", cue("L18", "monster?", 0.0), -19), hit("frameDrum", cue("L18", "monster?", 0.1), -19),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score: the series theme stays (D minor for the problem, D major for the payoff). EP30's band is `hymn` for the
# monster the village fears and honours (choir aahs on the strings channel, a cello drone, a deep frame drum, the theme
# on voice oohs) and `rite` for village life around the shrine (kalimba on the marimba channel, frame drums, a drone
# bass, the theme on pan flute), layering up as each ritual switches on. Programs are set where a colour starts and set
# back where it ends.
HYMN_P = {"strings": 52, "lead": 53}
RITE_P = {"marimba": 108, "lead": 75, "strings": 52}
BACK_P = {"marimba": 12, "strings": 48, "lead": 73}
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 92,
    "sections": [
        msec({"shot": "hook"}, "hymn", ["Dm", "Bb", "Gm", "A"], "D minor", programs=HYMN_P),
        msec(RESET, "rite", ["Dm", "Bb", "F", "C"], "D minor", layer=1, programs=RITE_P),
        msec(cue("L4", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.85, programs=BACK_P),
        msec(cue("L6", "No", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "harvest.", 0.5), "mystery", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=2),
        msec(cue("L8", "One:", -0.1), "rite", ["Dm", "C", "Bb", "C"], "D minor", layer=1, programs=RITE_P),
        msec(cue("L9", "Two:", -0.1), "rite", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "rite", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L11", "Four:", -0.1), "rite", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True, programs=BACK_P),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(cue("L13", "Whoever", -0.1), "hymn", ["Dm", "Bb", "Gm", "A"], "D minor", beatsPerChord=2, programs=HYMN_P),
        msec(cue("L15", "open", -0.05), "anthem", ["D", "G", "Bm", "A"], "D major", programs=BACK_P),
        msec(cue("L17", "What", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "harvest?"), "chord": "Dm"},
        {"kind": "boom", "at": cue("L6", "harvest."), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "fed."), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "fed.")},
        {"kind": "hit", "at": cue("L15", "rite."), "chord": "D"},
        {"kind": "call", "at": cue("L18", "hero,"), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #WritingTips #FantasyCreatures #WorldcraftShorts"
BODY = (
    "What if the creature everyone fears is also the source of their harvest?\n\n"
    "Meet the Grimmaw: it eats a sheep a moon. The lazy version treats it as just a monster and drives it off, and we "
    "ran it: ten years, no more lost sheep, and then the flocks ate the fields. No monster. No harvest.\n\n"
    "Fear and need share one scale. So the village makes offerings (a sheep each moon, so it never raids the pens), "
    "keeps its meadow holy, gives it the first sheaf of the harvest it guards, and lets keepers gather its shed plates "
    "for medicine. Run it again: still feared, still fed.\n\n"
    "Then the twist: the keepers. Whoever speaks for the monster speaks for everyone, so it's always hungry. Unless "
    "everyone watches it eat: an open rite.\n\n"
    "Worship isn't superstition. It's a deal with danger.\n\n"
    "What creature would your civilization worship despite its danger?\n\n"
    "Part 30 of 50. Follow for part 31: hero, or monster?"
)
METADATA = {
    "youtube": {
        "title": "Make a Monster That People Worship (Worldbuilding)",
        "titleAlternate": "Why would anyone worship a monster?",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 6: Creatures and Species (finale).\n\n" + TAGS,
        "pinnedComment": "What creature would your civilization worship despite its danger? (Part 31: hero, or monster?)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated field-card sprite; the island, creature, people and shrine are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "They drove the monster off. Then the harvest died 🌾 We ran it: 10 years, 0 harvest. Then we fixed it ritual by ritual. Rule #5 is about who speaks for it. "
                   "What creature would your civilization worship? Part 30/50 · follow for part 31 🗿 " + TAGS,
        "pinnedComment": "What creature would your civilization worship despite its danger?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "Which real-world danger would your fantasy culture turn into a god, and what would the tithe be?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": "They worship what eats their sheep.\n\n" + BODY + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": "First 34 characters: 'They worship what eats their sheep.'",
        "pinnedComment": "Save the KEEP IT LEVEL card, then tell us: what creature would your civilization worship?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep30] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots, loop span {loop_span():.2f} s")
