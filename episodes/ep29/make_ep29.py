"""Generate episodes/ep29/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep29/make_ep29.py
EP29's own device is the LINEAGE STRIP: a generations timeline under the world. The Undying Queen's cell never changes
(AGE 30, forever) while one cell per generation is born, greys and is gone, 25 years apart, as the clock races. Every
rule the episode switches on shows up in the strip as a badge on every generation (heirs who waited, land at fifty,
a council seat each century, titles capped, who still remembers year zero). Camera language: LOCKED-OFF TABLEAUX, a
tripod that never moves while centuries pass in front of it (EP26 orbited, EP27 rode a dragon, EP28 sat at eye
height). Motif colour: ageless violet #b48cff. Music band: `clockwork` (harpsichord, woodblock tick-tock) and `reign`
(church organ, timpani processional).
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep29" / "timing.json"


def cue(line, word=None, offset=0.0, nth=None):
    c = {"line": line}
    if word:
        c["word"] = word
    if nth:
        c["nth"] = nth
    if offset:
        c["offset"] = round(offset, 3)
    return c


# The block wipe into the end card: the world resets to frame 0 under it (year 0, the naive court, the hook pose).
WIPE = cue("L17", "Would", -0.3)

LINES = [
    ("L1", "hook", "What happens when a ruler can live for ten thousand years?", 0.3, ["ruler", "thousand"]),
    ("L2", "hook", "Meet the Undying Queen. She never ages.", 0.3, ["undying", "never"]),
    ("L3", "setup", "The lazy version: she's immortal, and nothing else changes.", 0.25, ["lazy", "nothing"]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "A thousand years. Forty generations wait for her crown.", 0.35, ["forty", "crown."]),
    ("L6", "drop", "Forty heirs. Not one coronation.", 0.4, ["heirs.", "coronation."]),
    ("L7", "rehook", "Forever breaks every rule built for death. Four fixes are easy. The fifth is the twist.", 0.25, ["forever", "twist."]),
    ("L8", "inherit", "One: inheritance. Heirs inherit at fifty, not at a funeral.", 0.2, ["fifty,", "funeral."]),
    ("L9", "power", "Two: power. Her crown is lent: a new council every century.", 0.2, ["lent:", "century."]),
    ("L10", "marriage", "Three: marriage. She outlives every husband, so vows last one lifetime.", 0.2, ["outlives", "lifetime."]),
    ("L11", "family", "Four: family. Forty generations of princes? Titles stop at grandchildren.", 0.3, ["princes?", "grandchildren."]),
    ("L12", "run2", "Run it again. The valley keeps changing. She doesn't.", 0.3, ["changing.", "doesn't."]),
    ("L13", "twist", "Rule five? Memory. Nobody else remembers year zero.", 0.3, ["memory.", "zero."]),
    ("L14", "twist", "So history is whatever she says. Unless it's written down.", 0.3, ["whatever", "written"]),
    ("L15", "role", "A library she can't rewrite.", 0.3, ["library", "rewrite."]),
    ("L16", "lesson", "Immortality isn't a trait. It's a society.", 0.35, ["trait.", "society."]),
    ("L17", "cta", "Would you want an immortal ruler? Explain why.", 0.25, ["immortal", "why."]),
    ("L18", "next", "Part 29 of 50. Follow for part 30: they pray to a monster.", 0.25, ["follow", "monster."]),
]

SHOTS = ["hook", "setup", "run1", "drop", "rehook", "inherit", "power", "marriage", "family", "run2", "twist", "role", "lesson", "cta", "next"]


# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle. EP27's humans live in the valley under the cliff (slate and turf, barns, the watchtower, the
# forest road); EP28's Fenn live in their open hall on the lake; the cairn stands on the meadow; the Grimmaw grazes the
# south-east meadow. EP29 adds the Undying Queen's dais at the valley's edge, and the court that grows around it.
G1_HOME = (15.5, -10.0)           # the Grimmaw grazes the north-east meadow (behind the court, in the hook frame)
CAIRN = (8.95, -5.38)
LAKE_HALL = (6.0, 4.6)
HUMAN_B = [("hall", (-3.6, -4.6)), ("house", (-1.8, -2.4)), ("house", (-4.8, -2.4)), ("house", (-1.0, -5.8)),
           ("house", (-5.6, -0.9)), ("house", (-3.4, -0.7)), ("house", (0.4, -4.2))]
HUMAN_TOWER = (-6.4, -5.6)
HUMAN_ROAD = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
DAIS = (9.4, -2.2)                    # the Queen's dais, on the open east meadow north of the lake, facing east
QUEEN = (9.1, -2.2)                   # she stands on it, in front of the throne
QUEUE_FROM = (11.4, -2.0)              # the heir line runs east from the dais steps
QUEUE_DIR = (1.0, 0.3)
CONSORT = (9.4, -1.2)                 # beside her, on the dais
COUNCIL = (12.8, -6.8)                 # the council hall (power)
LIBRARY = (4.6, -6.4)                 # the library (the twist's payoff)
PLOTS = [(13.2, 1.8), (15.8, 2.6), (14.6, -5.4), (17.4, -3.6), (18.4, -0.4), (16.6, -7.0)]   # heirs' land (inheritance)
CROWD = [[11.8, -6.8], [8.0, -5.4], [14.2, -4.4], [12.4, -8.6]]
OFFER = (11.2, -4.0)                  # the EP30 tease: a ring of candles lit on the meadow behind the court (for something they fear)


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


# The lazy version: under the rewind wipe the world goes back to year 0 and the valley keeps every mortal rule.
RESET = cue("L3", "lazy", -0.15)
REWIND = cue("L6", "coronation.", 0.55)


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    step = lambda at, v: [at, v, "step"]
    lin = lambda at, v: [at, v, "linear"]

    # ---- the clock (YEARS): every tableau is a time-lapse; the camera never moves while it runs
    clock = [[shot("hook"), 0], [shot("hook", 0.35), 0], lin(cue("L1", "years?", 0.3), 260), [cue("L2", "Meet", 0.0), 260],
             lin(cue("L2", "ages.", 0.4), 300), step(RESET, 0),
             [cue("L4", "run."), 0], lin(cue("L5", "crown.", 0.3), 1000), [REWIND, 1000], lin(cue("L7", "Forever", 0.4), 0),
             [cue("L8", "inheritance."), 0], lin(cue("L8", "funeral.", 0.4), 150),
             [cue("L9", "power."), 150], lin(cue("L9", "century.", 0.5), 350),
             [cue("L10", "marriage."), 350], lin(cue("L10", "lifetime.", 0.4), 560),
             [cue("L11", "family."), 560], lin(cue("L11", "grandchildren.", 0.3), 760),
             step(cue("L12", "Run", -0.05), 0), [cue("L12", "Run", 0.1), 0], lin(cue("L12", "doesn't.", 0.2), 1000),
             [cue("L13", "Rule"), 1000], lin(cue("L15", "rewrite.", 0.3), 1450),
             [WIPE, 1450], step(cue("L17", "Would", -0.28), 0)]
    gens = [[k[0], round(k[1] / 25.0, 3), *k[2:]] for k in clock]
    crowned = [[shot("hook"), 0], [cue("L12", "Run", 0.1), 0], lin(cue("L12", "doesn't.", 0.2), 10), [WIPE, 10], step(cue("L17", "Would", -0.28), 0)]
    speed = [[shot("hook"), 1], [cue("L4", "run."), 1], [cue("L4", "run.", 0.35), 6], [cue("L5", "crown.", 0.3), 6], [cue("L6", "Forty"), 1],
             [cue("L12", "Run", 0.1), 1], [cue("L12", "Run", 0.4), 6], [cue("L12", "doesn't.", 0.2), 6], [cue("L13", "Rule"), 1]]

    # ---- the people: a crowd on the clock, the heir line, the consort, royal titles
    count = [[shot("hook"), 34], step(RESET, 34), [cue("L4", "run."), 34], lin(cue("L5", "crown.", 0.3), 52), [REWIND, 52], lin(cue("L7", "Forever", 0.4), 34),
             [cue("L11", "family."), 34], lin(cue("L11", "princes?", 0.2), 52), [cue("L11", "Titles"), 52], lin(cue("L11", "grandchildren.", 0.3), 44),
             [WIPE, 44], step(cue("L17", "Would", -0.28), 34)]
    royal = [[shot("hook"), 0.08], [cue("L4", "run."), 0.08], lin(cue("L5", "crown.", 0.3), 0.45), [REWIND, 0.45], lin(cue("L7", "Forever", 0.4), 0.08),
             [cue("L11", "family."), 0.08], lin(cue("L11", "princes?", 0.2), 0.7), [cue("L11", "Titles", 0.1), 0.7], lin(cue("L11", "grandchildren.", 0.2), 0.06),
             [WIPE, 0.06], step(cue("L17", "Would", -0.28), 0.08)]
    queue = [[shot("hook"), 1], [cue("L4", "run."), 1], lin(cue("L5", "crown.", 0.3), 12), [REWIND, 12], lin(cue("L7", "Forever", 0.4), 3),
             [cue("L8", "inherit"), 3], lin(cue("L8", "funeral.", 0.0), 0), [WIPE, 0], step(cue("L17", "Would", -0.28), 1)]
    consort = [[shot("hook"), 0], [cue("L10", "marriage.", -0.1), 0], [cue("L10", "marriage.", 0.3), 1], [cue("L11", "Four:", -0.2), 1], [cue("L11", "Four:", 0.1), 0]]
    ruler = [pk(shot("hook"), *QUEEN, "idle", face=0), pk(cue("L18", "monster.", -0.1), *QUEEN, "alert", face=0), pk(cue("L18", "monster.", 1.3), *QUEEN, "idle", face=0)]

    # ---- the court that grows around her (its own settlement): heirs' houses, the council hall, the library
    plots = []
    for i, a in enumerate(PLOTS):
        show = [[shot("hook"), 0], [cue("L8", "inherit", 0.1 + i * 0.22), 0], [cue("L8", "inherit", 0.5 + i * 0.22), 1, "out"],
                [WIPE, 1], step(cue("L17", "Would", -0.28), 0)]
        plots.append({"kind": "house", "a": list(a), "face": 0, "show": show})
    council = {"kind": "hall", "a": list(COUNCIL), "face": 0, "w": 3.6, "d": 2.4, "h": 1.9,
               "show": [[shot("hook"), 0], [cue("L9", "lent:", -0.1), 0], [cue("L9", "council", 0.0), 1, "out"], [WIPE, 1], step(cue("L17", "Would", -0.28), 0)]}
    library = {"kind": "library", "a": list(LIBRARY), "face": 0,
               "show": [[shot("hook"), 0], [cue("L14", "written", -0.1), 0], [cue("L15", "library", 0.1), 1, "out"], [WIPE, 1], step(cue("L17", "Would", -0.28), 0)]}
    court = {"buildings": plots + [council, library], "roof": [[shot("hook"), 1]], "stone": [[shot("hook"), 0]], "pens": []}

    # ---- EP27's human valley (sky-proof, unchanged) and EP28's Fenn hall on the lake (open walls, speaking in light)
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

    # ---- time passing in the tableaux: the seasons flicker (snow) while the clock races; the forest thins and returns
    def seasons(a_line, a_word, a_off, n, period, depth=0.55):
        out = []
        for k in range(n):
            b0 = a_off + k * period
            out += [[cue(a_line, a_word, b0), 0], [cue(a_line, a_word, b0 + period * 0.35), depth, "linear"], [cue(a_line, a_word, b0 + period * 0.8), 0, "linear"]]
        return out
    snow = [[shot("hook"), 0]] + seasons("L1", "What", 0.25, 6, 0.48) + seasons("L5", "A", 0.0, 6, 0.5) + seasons("L12", "valley", -0.3, 4, 0.5) + [[cue("L13", "Rule"), 0]]
    forest = [[shot("hook"), 1], [cue("L1", "ruler", 0.0), 1], [cue("L1", "thousand", 0.0), 0.6, "linear"], [cue("L1", "years?", 0.4), 1, "linear"],
              [cue("L5", "A"), 1], [cue("L5", "Forty"), 0.55, "linear"], [cue("L5", "crown.", 0.3), 1, "linear"]]
    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run")]
    rings = [{"x": LIBRARY[0], "z": LIBRARY[1], "r": 3.0, "on": cue("L15", "library"), "off": cue("L16", "Immortality", -0.3), "color": "#8fc8ff"}]

    # Camera language: a locked-off tripod. Each tableau holds one frame (drift 0) while the years race through it.
    hook_pose = dict(az=20, el=8, dist=44, target=(10.0, 6.4, -3.0), fov=13)
    setup_pose = dict(az=20, el=12, dist=64, target=(12.4, 6.2, -2.6), fov=20)
    wide = dict(el=48, dist=196, target=(4.0, 10.5, 0.0), fov=26)
    camera = [
        cam(shot("hook"), **hook_pose),
        cam(RESET, dur=0.01, cut=True, **setup_pose),
        cam(cue("L4", "run.", 0.05), 18, dur=1.2, **wide),
        cam(cue("L6", "Forty", -0.2), -17, 12, 40, (14.0, 6.0, -1.2), fov=24, dur=0.01, cut=True),
        cam(REWIND, dur=0.01, cut=True, **setup_pose),
        cam(cue("L8", "One:", -0.15), 30, 26, 60, (14.2, 6.0, -1.6), fov=24, dur=0.01, cut=True),
        cam(cue("L9", "Two:", -0.15), 50, 18, 48, (11.2, 6.0, -4.6), fov=24, dur=0.01, cut=True),
        cam(cue("L10", "Three:", -0.15), 70, 6, 22, (9.3, 5.4, -1.7), fov=24, dur=0.01, cut=True),
        cam(cue("L11", "Four:", -0.15), 10, 30, 70, (11.4, 5.5, -5.4), fov=24, dur=0.01, cut=True),
        cam(cue("L12", "Run", -0.05), 20, dur=0.01, cut=True, **wide),
        cam(cue("L13", "Rule", -0.1), 40, 10, 26, (9.6, 6.3, -2.4), fov=26, dur=0.01, cut=True),
        cam(cue("L14", "Unless", -0.1), -30, 16, 40, (5.6, 7.0, -5.2), fov=26, dur=0.01, cut=True),
        cam(cue("L16", "Immortality", -0.25), 15, 34, 190, (2.0, 3.0, 0.0), fov=26, dur=1.6, drift=2.0),
        cam(WIPE, cut=True, **hook_pose),
    ]
    light = [
        {"at": shot("hook"), "mood": "golden"},
        {"at": RESET, "mood": "day", "dur": 0.4},
        {"at": cue("L6", "Forty", -0.2), "mood": "gloom", "dur": 0.6},
        {"at": REWIND, "mood": "day", "dur": 0.8},
        {"at": cue("L10", "Three:", -0.15), "mood": "dusk", "dur": 0.4},
        {"at": cue("L11", "Four:", -0.15), "mood": "day", "dur": 0.4},
        {"at": cue("L13", "Rule", -0.2), "mood": "dusk", "dur": 0.6},
        {"at": cue("L14", "Unless", -0.1), "mood": "night", "dur": 0.4},
        {"at": cue("L16", "Immortality", -0.3), "mood": "golden", "dur": 2.0},
    ]
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": [[shot("hook"), 30]], "max": 40, "base": 30, "centers": [[-7.2, -1.4], [-6.0, 0.4]], "skin": "sheep"},
        "pred": [[shot("hook"), 1]],
        "predators": [{"id": "g1", "keys": [pk(shot("hook"), *G1_HOME, "idle", face=200)]}],
        "series": {"gens": gens, "crowned": crowned, "tradeH": [[shot("hook"), 4]]},
        "settlement": human_valley,
        "settlements": [fenn_hall, court],
        "folk": {"count": [[shot("hook"), 9]], "centers": [list(LAKE_HALL)], "spread": 2.0, "site": [[shot("hook"), 0]],
                 "eyes": [[shot("hook"), 1]], "wet": [[shot("hook"), 1]], "glow": [[shot("hook"), 1]], "hero": []},
        "people": {"count": count, "centers": CROWD, "spread": 2.2, "life": 70, "royal": royal,
                   "queue": {"from": list(QUEUE_FROM), "dir": list(QUEUE_DIR), "count": queue, "gap": 0.72},
                   "consort": {"x": CONSORT[0], "z": CONSORT[1], "face": 0, "show": consort, "life": 60},
                   "ruler": {"keys": ruler, "dais": {"x": DAIS[0], "z": DAIS[1], "face": 0}}},
        "props": [{"kind": "cairn", "x": CAIRN[0], "z": CAIRN[1], "stones": [[shot("hook"), 3]]},
                  {"kind": "offerings", "x": OFFER[0], "z": OFFER[1],
                   "r": 0.8, "lights": [[shot("hook"), 0], [cue("L18", "monster.", -0.2), 0], [cue("L18", "monster.", 0.5), 1, "linear"], [cue("L18", "monster.", 1.0), 1], [cue("L18", "monster.", 1.3), 0]]}],
        "clearTrees": [[d[0], d[1], 2.8] for d in [DAIS, QUEUE_FROM, *[tuple(c) for c in CROWD], (15.0, -0.8), (11.0, -7.0)]],
        "layers": {"snow": snow, "forest": forest, "ripple": ripple, "rings": rings},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "HEIRS", "text": "inherit at fifty", "at": cue("L8", "inheritance.")},
    {"n": 2, "label": "POWER", "text": "the crown is lent", "at": cue("L9", "power.")},
    {"n": 3, "label": "MARRIAGE", "text": "vows for one life", "at": cue("L10", "marriage.")},
    {"n": 4, "label": "TITLES", "text": "end at grandkids", "at": cue("L11", "family.")},
    {"n": 5, "label": "MEMORY", "text": "write it down", "at": cue("L7", "easy."), "locked": True, "unlockAt": cue("L15", "library")},
]
SPRITE = {"sprite": "ep29/queen_sprite.png", "spriteW": 56, "spriteH": 107}
VIOLET = "#b48cff"


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "A RULER WHO", "size": 84}, {"text": "NEVER DIES?", "color": VIOLET, "size": 96}]
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 96, "start": {"shot": "hook"}, "end": cue("L2", "Meet", -0.1), "preShow": True},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 29 · CREATURES", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Meet", -0.05), "end": RESET, "dietAt": cue("L2", "never"),
         "kicker": "FIELD CARD · NO. 004", "kind": "IMMORTAL RULER", "name": "THE UNDYING", "dietLabel": "AGE", "diet": "30, since year 0", **SPRITE},
    ]
    lineage = {"type": "lineage", "y": 1352, "start": cue("L3", "lazy", 0.1), "end": cue("L16", "Immortality", -0.3), "stat": {"label": "CROWNED", "key": "crowned", "color": VIOLET},
               "badges": [[cue("L3", "lazy"), "none"], [cue("L5", "Forty", -0.3), "waited"], [REWIND, "none"], [cue("L8", "inherit"), "land"], [cue("L9", "lent:"), "council"],
                          [cue("L10", "marriage."), "none"], [cue("L11", "Forty"), "titles"], [cue("L11", "Titles"), "cap"], [cue("L12", "Run"), "council"],
                          [cue("L13", "remembers"), "memory"], [cue("L15", "library"), "record"]]}
    G["setup"] += [
        {"type": "blockWipe", "at": RESET, "dur": 0.34, "color": "#2a1a44"},
        {"type": "kinetic", "parts": [{"text": "NOTHING ELSE", "at": cue("L3", "nothing"), "size": 76}, {"text": "CHANGES", "at": cue("L3", "changes."), "color": "rust", "size": 92}],
         "y": 470, "size": 92, "start": cue("L3", "nothing", -0.05), "end": cue("L4", "Press", -0.15)},
        lineage,
        {"type": "simBar", "counters": [{"icon": "mortal", "label": "GENERATIONS", "key": "gens", "color": "parchment", "digits": 2},
                                        {"icon": "crown", "label": "CROWNED", "key": "crowned", "color": VIOLET, "digits": 2}],
         "compact": True, "start": cue("L4", "Press", -0.15), "end": cue("L16", "Immortality", -0.3), "runAt": [cue("L4", "run."), cue("L12", "Run")]},
    ]
    G["run1"] += [
        {"type": "pin", "at": [QUEUE_FROM[0] + 4.0, 3.6, QUEUE_FROM[1] + 1.0], "kicker": "THE HEIRS", "text": "STILL WAITING", "color": "ember", "lift": 80, "size": 28,
         "start": cue("L5", "wait", -0.1), "end": cue("L6", "Forty", -0.25)},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "0 CORONATIONS", "sub": "40 HEIRS WAITED", "color": "rust", "y": 560, "size": 58, "start": cue("L6", "coronation."), "end": cue("L6", "coronation.", 0.5)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "coronation.", 0.55), "end": cue("L7", "Forever", 0.4)},
        {"type": "blockWipe", "at": cue("L6", "coronation.", 0.53), "dur": 0.34},
        {"type": "kinetic", "parts": [{"text": "FOREVER BREAKS", "at": cue("L7", "Forever"), "color": VIOLET, "size": 72}, {"text": "EVERY RULE", "at": cue("L7", "every"), "size": 84},
                                      {"text": "BUILT FOR DEATH", "at": cue("L7", "built"), "color": "rust", "size": 70}],
         "y": 470, "size": 84, "start": cue("L7", "Forever", -0.05), "end": cue("L7", "Four", -0.15)},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L16", "Immortality", -0.3),
         "kicker": "UNDYING · WHAT MUST CHANGE", "title": "BUILT FOR FOREVER", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L10", "Three:", -0.3), 0], [cue("L10", "Three:", 0.05), 1], [cue("L12", "doesn't.", 0.4), 1], [cue("L12", "doesn't.", 0.7), 0],
                      [cue("L13", "Rule", -0.35), 0], [cue("L13", "Rule", -0.05), 1], [cue("L15", "rewrite.", 0.2), 1], [cue("L15", "rewrite.", 0.5), 0]]},
    ]
    G["run2"] += [
        {"type": "stamp", "text": "MOVING ON", "sub": "10 CROWNS · 40 GENERATIONS", "color": VIOLET, "rotate": -4, "y": 880, "size": 88, "start": cue("L12", "doesn't."), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}, {"text": "MEMORY", "at": cue("L13", "Memory."), "color": VIOLET, "size": 96}],
         "size": 150, "y": 600, "start": cue("L13", "Rule", -0.02), "end": cue("L13", "Nobody", -0.1)},
        {"type": "kinetic", "parts": [{"text": "HISTORY =", "at": cue("L14", "history"), "size": 76}, {"text": "WHAT SHE SAYS", "at": cue("L14", "whatever"), "color": "rust", "size": 76}],
         "size": 76, "y": 600, "start": cue("L14", "history", -0.05), "end": cue("L14", "Unless", -0.15)},
    ]
    G["role"] += [
        {"type": "pin", "at": [LIBRARY[0], 7.6, LIBRARY[1]], "kicker": "THE RECORD", "text": "SHE CAN'T REWRITE IT", "color": "sky", "lift": 110, "size": 28,
         "start": cue("L15", "library", 0.2), "end": cue("L16", "Immortality", -0.35)},
        {"type": "followChip", "start": cue("L15", "rewrite.", 0.4), "end": cue("L16", "society.", 0.1), "text": "FOLLOW", "sub": "PART 29/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "Immortality", -0.3), **({"unlockAt": cue("L16", "Immortality", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "Immortality", -0.3), "end": cue("L17", "Would", -0.52), "kicker": "BEFORE YOU WRITE ONE", "title": "THE UNDYING", **SPRITE,
         "subtitle": "Immortality is a society.", "subtitleAt": cue("L16", "society.")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 29 / 50",
         "title": "Immortality Would Break Your Society", "cta": "COMMENT", "icon": "bubble", "with": "Would you want an immortal ruler? Explain why."},
    ]
    gone = cue("L18", "monster.", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 29, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6, "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone, "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 30"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "30:", -0.1), "revealAt": cue("L18", "pray"), "end": gone,
         "kicker": "NEXT RUN · 30", "title": "WORSHIPPED", "sub": "THEY PRAY TO A MONSTER.", "sprite": "shrine", "spritePx": 9},
        {"type": "kinetic", "parts": hook_text, "y": 452, "size": 96, "start": cue("L18", "monster.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("An immortal isn't a character trait, it's a change to the whole society around them: who inherits, who holds "
          "power and for how long, what marriage means, how far titles spread, and who gets to remember the past.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Close EP28's loop (who never dies?) and stop the scroll on the question.",
             "Golden hour, a locked-off frame: the Undying Queen in violet on her stone dais, still, while behind her the valley's people are born, grey and are replaced, winters flicker and the forest thins and returns. A RULER WHO / NEVER DIES? Then the field card: THE UNDYING · IMMORTAL RULER · AGE: 30, since year 0.",
             "Locked off (az 12, el 9, dist 30, fov 22), no drift; the loop lands on the same frame.", ("kinetic, field card", "the Queen on her dais", "the valley ageing"),
             "Golden hour.", "A RULER WHO / NEVER DIES?", "Rewind wipe into the lazy version.", "Reign: organ chorale, timpani, the theme on horns."),
    "setup": ("The lazy version: she's immortal and every mortal rule stays.", "A violet block wipe back to year 0: the court as it is, one heir at the dais steps. NOTHING ELSE / CHANGES. The lineage strip slides in under the world: THE QUEEN · AGE 30 beside the generations. RUN.",
              "Locked medium on the dais and the heir (dist 44).", ("kinetic, lineage strip, sim bar", "Queen, heir, crowd", "valley"), "Day.", "NOTHING ELSE CHANGES", "Cut to the wide on 'run'.", "Clockwork, thin."),
    "run1": ("Run the lazy version: forty generations wait for a crown that never passes.", "Whole Isle, locked off; YEAR 0→1000, GENERATIONS 00→40, CROWNED 00; the heir line grows to twelve, each heir greying in line; the strip marks every passing generation with a rust ✗.",
             "Wide (dist 196), locked.", ("sim bar, strip, pin", "the heir line, the crowd turning over", "island, seasons flickering"), "Day, winters flickering.", "THE HEIRS · STILL WAITING", "Cut to the heir line.", "Clockwork at full."),
    "drop": ("The punchline.", "Close on the heir line before the dais, every heir grey: 0 CORONATIONS · 40 HEIRS WAITED.", "Locked close (dist 34).", ("stamp", "grey heirs", "the dais"), "Gloom.", "0 CORONATIONS", "Rewind + block wipe.", "Drop; a boom on 'coronation'."),
    "rehook": ("Re-hook: the thesis, then four easy fixes and one locked.", "REWIND to year 0; FOREVER BREAKS / EVERY RULE / BUILT FOR DEATH; the checklist BUILT FOR FOREVER, row 5 locked and blinking.",
               "Locked medium.", ("kinetic, checklist", "the court at year 0", "valley"), "Day.", "0/5", "Cut on 'One'.", "Mystery; a riser into 'the twist'."),
    "inherit": ("Fix 1: inheritance without a funeral.", "Tableau: the heir line at the dais dissolves as each heir is given land; six houses rise on the meadow one by one; the strip marks a house under every generation at fifty. YEAR 0→150.",
                "Locked (az 30, el 22, dist 46).", ("checklist, strip", "heirs' houses rising", "meadow"), "Day.", "1 INHERITANCE · land at fifty", "Cut.", "Clockwork 1: harpsichord alone."),
    "power": ("Fix 2: a lent crown.", "Tableau from the other side: a council hall rises beside the dais; a council seat marks every fourth generation in the strip. YEAR 150→350.",
              "Locked (az -20, el 18, dist 46).", ("checklist, strip", "the council hall", "valley"), "Day.", "2 POWER · the crown is lent", "Cut.", "Clockwork 2: tick-tock joins."),
    "marriage": ("Fix 3: vows for one lifetime.", "Close tableau at dusk: the Queen and her consort on the dais; he greys and is replaced, again and again, while she doesn't change. YEAR 350→560.",
                 "Locked close, low (az 70, el 7, dist 18).", ("checklist, strip", "Queen and consort", "dusk valley"), "Dusk.", "3 MARRIAGE · vows for one life", "Cut.", "Clockwork 3: bass joins."),
    "family": ("Fix 4: titles end.", "Medium tableau on the crowd: violet (royal) spreads through the generations until most of the valley is royal; on 'Titles stop' it drains back to a few. YEAR 560→760.",
               "Locked (el 30, dist 70).", ("checklist (folded), strip", "royal violet spreading and receding", "valley"), "Day.", "4 FAMILY · titles end", "Cut to the wide.", "Clockwork 4: the theme on celesta, bells."),
    "run2": ("Run with the fixes: the valley moves on, she doesn't.", "Whole Isle, locked; YEAR 0→1000; CROWNED 00→10; MOVING ON · 10 CROWNS · 40 GENERATIONS.",
             "Wide (dist 196), locked.", ("stamp, strip", "the court, the council hall, the heirs' houses", "island"), "Day.", "MOVING ON", "Cut to night.", "Drive with the theme; a stab and cymbal on 'doesn't'."),
    "twist": ("The locked rule: memory.", "Night, close on the Queen as the crowd keeps turning over around her: RULE 5? MEMORY. The strip's lamps: only the generations alive at year zero remember it, and they're long gone; only hers stays lit. HISTORY = WHAT SHE SAYS.",
              "Locked close (az 40, el 10, dist 26).", ("kinetic, strip", "the Queen, the crowd", "night"), "Night.", "RULE 5? MEMORY · HISTORY = WHAT SHE SAYS", "Cut.", "Twist, then reign (organ) under it."),
    "role": ("Unlock rule 5: a record she can't rewrite.", "A stone library rises in the valley, its windows lit; THE RECORD · SHE CAN'T REWRITE IT; every lamp in the strip lights; row 5 unlocks (MEMORY · write it down).",
             "Locked (az -30, el 16, dist 40).", ("pin, unlocked card, strip, follow chip", "the library", "the valley at night"), "Night.", "THE RECORD; 5/5", "Card goes full.", "A big D-major hit on 'library'."),
    "lesson": ("The takeaway.", "The full card (BEFORE YOU WRITE AN IMMORTAL, all five rows) with 'Immortality is a society.' in serif italic.",
               "Wide (dist 190), the one slow drift of the episode.", ("full card", "the island at golden hour", "stars"), "Golden hour.", "Full card.", "Block wipe to the end card.", "Anthem; the World Engine chime as the card lands."),
    "cta": ("Comment CTA.", "End card: logo, PART 29 / 50, title, a speech-bubble COMMENT panel.", "Cut (under the block wipe) back to the hook frame.", ("end card", "the Isle", "void"),
            "Golden hour (the loop frame).", "End card.", "The card lifts on 'Part'.", "Outro."),
    "next": ("Say the part number, ask for the follow with a reason (part 30), open the next loop.",
             "The hook frame; PART 29/50; FOLLOW FOR PART 30; NEXT RUN 30 · WORSHIPPED from a locked shrine; on the meadow behind, candles light one by one around the Grimmaw and the Queen looks up; then the hook title returns.",
             "The hook frame, locked.", ("progress bar, follow button, next-run card", "the Queen, the candles", "the Grimmaw's meadow"), "Golden hour.",
             "PART 29/50 · FOLLOW FOR PART 30 · NEXT RUN: WORSHIPPED · THEY PRAY TO A MONSTER.", "Loop to frame 0.", "Tease over a held A, a horn call, the engine chime on 'Follow'."),
}


def build():
    ep = {
        "id": "ep29",
        "number": 29,
        "season": 2,
        "title": "Immortality Would Break Your Society",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.07},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same lab host, a little slower and more thoughtful for a story told across centuries. The hook is a real question. "
                         "'Nothing else changes' is the knowing setup. 'Forty heirs. Not one coronation.' lands dry. 'Forever breaks every rule built for death' is the thesis. "
                         "The fixes are crisp. 'Nobody else remembers year zero' is quiet; 'A library she can't rewrite' is the reveal. The comment ask is a genuine question.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L3", "from": "nothing"}, {"line": "L6", "from": "Not"}, {"line": "L7", "from": "Forever", "to": "Four"},
                        {"line": "L13", "from": "Rule", "to": "Nobody"}, {"line": "L14", "from": "history", "to": "Unless"}],
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
             bed("clockTicks", {"shot": "hook", "offset": 0.35}, cue("L1", "years?", 0.3), -24),
             hit("cardSlide", cue("L2", "Meet", -0.05), -18), hit("check", cue("L2", "never"), -20)],
    "setup": [hit("rewind", RESET, -15), hit("cardSlide", cue("L3", "lazy", 0.1), -18), hit("stamp", cue("L3", "changes."), -19),
              hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "crown.", 0.2), -22), bed("clockTicks", cue("L4", "run.", 0.3), cue("L5", "crown.", 0.2), -22),
             hit("crownPass", cue("L5", "Forty"), -19), hit("cardSlide", cue("L5", "wait", -0.1), -21)],
    "drop": [hit("stamp", cue("L6", "coronation."), -10)],
    "rehook": [hit("rewind", cue("L6", "coronation.", 0.5), -11), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "inherit": [hit("check", cue("L8", "inheritance."), -13), hit("delete", cue("L8", "inherit", 0.0), -20),
                bed("births", cue("L8", "inherit", 0.1), cue("L8", "funeral.", 0.0), -24), hit("restore", cue("L8", "fifty,", 0.0), -15)],
    "power": [hit("check", cue("L9", "power."), -13), hit("restore", cue("L9", "lent:", -0.1), -14), hit("crownPass", cue("L9", "century."), -14)],
    "marriage": [hit("check", cue("L10", "marriage."), -13), hit("crownPass", cue("L10", "husband,"), -17), hit("crownPass", cue("L10", "lifetime."), -17)],
    "family": [hit("check", cue("L11", "family."), -13), hit("morph", cue("L11", "princes?", -0.2), -15), hit("restore", cue("L11", "Titles", 0.1), -15)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L12", "doesn't.", 0.2), -22),
             bed("clockTicks", cue("L12", "Run", 0.3), cue("L12", "doesn't.", 0.2), -22), hit("stamp", cue("L12", "doesn't."), -13)],
    "twist": [hit("ringOn", cue("L13", "remembers"), -18), hit("unlock", cue("L14", "whatever"), -19)],
    "role": [hit("restore", cue("L15", "library", -0.1), -12), hit("unlock", cue("L15", "library"), -10), hit("ringOn", cue("L15", "library"), -18)],
    "lesson": [hit("engineWind", cue("L16", "Immortality", -0.8), -15), hit("chime", cue("L16", "Immortality", -0.3), -10), hit("cardSlide", cue("L16", "Immortality", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("cardSlide", cue("L17", "Would", -0.1), -20)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11), hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "30:", -0.1), -18), hit("unlock", cue("L18", "pray"), -15), hit("crownPass", cue("L18", "monster.", 0.0), -18), hit("roar", cue("L18", "monster.", 0.15), -27),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score: the series theme stays (D minor for the problem, D major for the payoff). EP29's band is `reign` for the
# Queen who never changes (church organ on the strings channel, timpani, the theme on horns) and `clockwork` for the
# centuries racing past her (harpsichord on the marimba channel, woodblock tick-tock, tubular bells), layering up as the
# fixes switch on. Programs are set where a colour starts and set back where it ends.
REIGN_P = {"strings": 19}
CLOCK_P = {"marimba": 6, "glock": 14, "strings": 48}
BACK_P = {"marimba": 12, "strings": 48, "glock": 9}
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 96,
    "sections": [
        msec({"shot": "hook"}, "reign", ["Dm", "Bb", "Gm", "A"], "D minor", programs=REIGN_P),
        msec(RESET, "clockwork", ["Dm", "Bb", "F", "C"], "D minor", layer=1, programs=CLOCK_P),
        msec(cue("L4", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.85),
        msec(cue("L6", "Forty", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8, programs=BACK_P),
        msec(cue("L6", "coronation.", 0.5), "mystery", ["Dm", "C", "Bb", "A"], "D minor", beatsPerChord=2),
        msec(cue("L8", "One:", -0.1), "clockwork", ["Dm", "C", "Bb", "C"], "D minor", layer=1, programs=CLOCK_P),
        msec(cue("L9", "Two:", -0.1), "clockwork", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "clockwork", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L11", "Four:", -0.1), "clockwork", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True, programs=BACK_P),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(cue("L13", "Nobody", -0.1), "reign", ["Dm", "Bb", "Gm", "A"], "D minor", beatsPerChord=2, programs=REIGN_P),
        msec(cue("L15", "library", -0.05), "anthem", ["D", "G", "Bm", "A"], "D major", programs=BACK_P),
        msec(cue("L17", "Would", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "years?"), "chord": "Dm"},
        {"kind": "boom", "at": cue("L6", "coronation."), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "doesn't."), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "doesn't.")},
        {"kind": "hit", "at": cue("L15", "library"), "chord": "D"},
        {"kind": "call", "at": cue("L18", "pray"), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #WritingTips #Immortality #WorldcraftShorts"
BODY = (
    "What happens when a ruler can live for ten thousand years?\n\n"
    "Meet the Undying Queen: she never ages. The lazy version makes her immortal and changes nothing else, and we ran "
    "it: a thousand years, forty generations of heirs waiting for a crown that never passes. Forty heirs. Not one coronation.\n\n"
    "Forever breaks every rule built for death. So heirs inherit at fifty, not at a funeral. Her crown is lent: a new "
    "council every century. She outlives every husband, so vows last one lifetime. And forty generations of princes? "
    "Titles stop at grandchildren. Run it again, and the valley keeps changing while she doesn't.\n\n"
    "Then the twist: memory. Nobody else remembers year zero, so history is whatever she says, unless it's written "
    "down. A library she can't rewrite.\n\n"
    "Immortality isn't a trait. It's a society.\n\n"
    "Would you want an immortal ruler? Explain why.\n\n"
    "Part 29 of 50. Follow for part 30: they pray to a monster."
)
METADATA = {
    "youtube": {
        "title": "Immortality Would Break Your Society (Worldbuilding)",
        "titleAlternate": "What if your queen never died?",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 6: Creatures and Species.\n\n" + TAGS,
        "pinnedComment": "Would you want an immortal ruler? Explain why. (Part 30: they pray to a monster.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated field-card sprite; the island, people and buildings are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "Your immortal queen just broke inheritance 👑 We ran it: 1,000 years, 40 generations of heirs, 0 coronations. Then we fixed it rule by rule. Rule #5 is about who remembers. "
                   "Would you want an immortal ruler? Part 29/50 · follow for part 30 🕯️ " + TAGS,
        "pinnedComment": "Would you want an immortal ruler? Explain why.",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "If your ruler never died, what's the first law you'd change?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": "Your queen never dies. Now what?\n\n" + BODY + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": "First 32 characters: 'Your queen never dies. Now what?'",
        "pinnedComment": "Save the BUILT FOR FOREVER card, then tell us: would you want an immortal ruler?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep29] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots")
