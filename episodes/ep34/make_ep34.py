"""Generate episodes/ep34/episode.json (Season 2 format: the World Engine).

Run from the repo root: python episodes/ep34/make_ep34.py
EP34 is Arc 7's fourth episode (History and Mythology): "What If Your World's Creation Myth Is Wrong?". It closes
EP33's loop (on "the gods are lying" a crack of light opened in the meadow south of the lake for a breath): frame 0
has that crack open for good, a giant's bones lying in it, and above it a fresh hole torn in the sky.

Its own device is THE TWO SKIES: the Lamplight's creation myth (the First Lamp, which "fell from the sky, and the
world began") is a painted dome over the Isle, lapis and gilt, with the lamp falling across it; what the ground shows
tears holes in the paint, and the true sky (the night void) shows through. MYTH tags are pinned to the painting,
GROUND tags to the Isle. The lazy version makes the myth simply true (a perfect sky, a ground with no layers, nothing
to find). The four rules open the gap: proof in the ground (a giant's bones), a job for the myth (the Queen's crown),
someone who digs (the cliffs show ten thousand years) and someone who hides it (keepers paint over the holes). The
twist answers the hook: the myth isn't lying, it's remembering. A star really fell, and it made the lake.
Camera language: THE DOLLY ZOOM ("the ground holds, the sky moves"): every pose looks across the Isle at the painted
sky behind it, and every beat is a dolly zoom that keeps its subject the same size while the lens changes. The truth
dollies in on a wide lens, so the sky falls away behind the ground; the myth dollies out on a long lens, so the
painted sky looms over it (EP26 orbited, EP27 rode a dragon, EP28 sat at eye height, EP29 was a locked-off tripod,
EP30 looked up, EP31 split the frame, EP32 craned up and down the cut, EP33 looked down at a map table).
Motif colour: fresco ultramarine #4a68ff. Music band: `lullaby` (the myth as it is sung to children) and `excavate`
(the truth coming up out of the ground, one family per rule).
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMING = HERE.parent.parent / "public" / "ep34" / "timing.json"
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
    ("L1", "hook", "Every child learns the gods made the world. What if they're lying?", 0.3, ["gods", "lying?"]),
    ("L2", "hook", "Meet the First Lamp. It fell from the sky.", 0.3, ["first", "fell"]),
    ("L3", "setup", "The lazy version: the myth is simply true.", 0.25, ["lazy", "true."]),
    ("L4", "setup", "Press run.", 0.3, ["run."]),
    ("L5", "run1", "Five hundred years. Nobody digs. Nothing to find.", 0.35, ["nobody", "nothing"]),
    ("L6", "drop", "A myth that's just true is a textbook.", 0.4, ["true", "textbook."]),
    ("L7", "rehook", "Wrong myths build better worlds. Four rules. The fifth is the twist.", 0.25, ["wrong", "twist."]),
    ("L8", "bones", "One: bury proof. Bones older than the gods.", 0.25, ["proof.", "older"]),
    ("L9", "crown", "Two: give it a job. The Queen's crown rests on it.", 0.25, ["job.", "crown"]),
    ("L10", "cliff", "Three: let someone dig. The cliffs count ten thousand years.", 0.25, ["dig.", "thousand"]),
    ("L11", "keepers", "Four: let someone hide it. Keepers paint over the holes.", 0.3, ["hide", "paint"]),
    ("L12", "run2", "Run it again. Five hundred years. They're still arguing.", 0.35, ["hundred", "arguing."]),
    ("L13", "twist", "Rule five? The myth isn't lying at all. It's remembering.", 0.35, ["lying", "remembering."]),
    ("L14", "twist", "A star really fell here. It made the lake.", 0.4, ["star", "lake."]),
    ("L15", "role", "So hide the truth inside the myth.", 0.4, ["truth", "inside"]),
    ("L16", "lesson", "Myths aren't lies. Every myth is a memory, told wrong.", 0.35, ["lies.", "memory,"]),
    ("L17", "cta", "Would you tell them the truth, or keep the myth?", 0.25, ["tell", "keep"]),
    ("L18", "next", "Part 34 of 50. Follow for part 35: the ruins are older than us.", 0.25, ["follow", "us."]),
]
SHOTS = ["hook", "setup", "run1", "drop", "rehook", "bones", "crown", "cliff", "keepers", "run2", "twist", "role", "lesson", "cta", "next"]

# The block wipe into the end card: the world resets to frame 0 under it (today, the sky torn over the crack).
WIPE = cue("L17", "Would", -0.3)
RESET = cue("L3", "lazy", -0.15)          # the lazy version: the myth is simply true
REWIND = cue("L6", "textbook.", 0.6)      # back to the pristine sky, before anything is found
RULES = cue("L8", "One:", -0.1)
RUN2 = cue("L12", "Run", -0.05)
TWIST = cue("L13", "Rule", -0.1)
REMEMBER = cue("L13", "remembering.", -0.05)  # the paint thins: the true sky behind the myth
STAR = cue("L14", "star", -0.1)           # the real star falls
ROLE = cue("L15", "So", -0.15)
HOOK_DRIFT = 0.0
END = {"end": True}

# ---------------------------------------------------------------- the world (Season 2 timeline)

# Landmarks on the Isle (it remembers): EP27's valley village and watchtower (west), the cairn (east of the lake),
# EP29's Queen on her dais, EP30's Grimmaw (north-east), EP31's split statue and EP32's boundary stones and relic
# (south-east), EP33's Lamplight faith (candles at the cairn, boats with lamps, the sheaves, the keepers, the crowd's
# lamps) and EP33's crack of light in the meadow south of the lake. EP28's Fenn hall stays out (it covers the lake).
CAIRN = (8.95, -5.38)
HUMAN_B = [("hall", (-3.6, -4.6)), ("house", (-1.8, -2.4)), ("house", (-4.8, -2.4)), ("house", (-1.0, -5.8)),
           ("house", (-5.6, -0.9)), ("house", (-3.4, -0.7)), ("house", (0.4, -4.2))]
HUMAN_TOWER = (-6.4, -5.6)
HUMAN_ROAD = [[-3.4, -1.6], [-5.6, 2.0], [-8.2, 6.0], [-11.0, 10.0], [-13.0, 14.0], [-14.6, 17.0]]
DAIS = (9.4, -2.2)
QUEEN = (9.1, -2.2)
G_NOW = (13.0, -10.5)                               # EP30's Grimmaw, a few steps east of its EP33 spot (it stood behind the Queen in the crown rule's line of sight)
STATUE = (18.0, 1.5)
LINE_A, LINE_B = (18.0, -7.0), (18.0, 8.3)
RELIC = (20.3, 5.4)
LAKE = (6.5, 4.5)
FIELD = (3.0, -11.0, 4.0, 3.4)
CROWD = [[-2.4, -3.2], [-0.4, -1.6], [-4.2, -1.8]]

# The ground's proof
RIFT_A, RIFT_B = (-0.5, 10.6), (12.0, 8.8)         # EP33's crack of light, open for good
BONES = (6.5, 12.2)                                 # a giant's skeleton dug out along the crack's south lip
BONES_FACE = 8.2                                    # its spine along the crack, the skull to the east
RUIN = (12.8, 13.4)                                 # EP35's tease: pillars older than anyone
DIGGER = (3.2, 13.4)                                # one figure with a torch at the crack's south lip

# The painted sky: a dome of radius 56 centred 2 below the grass; the First Lamp hangs on its north wall
SKY_R, SKY_Y = 56.0, -2.0
ULTRA = "#4a68ff"
GILT = "#e6be5e"
BONE = "#e8dec4"
ROBE = "#efe2b0"


def shift(c, d):
    """The same cue, `d` seconds later."""
    return {**c, "offset": round(c.get("offset", 0.0) + d, 3)}


def jump(at, before, after):
    """A hard change of value on a cut: hold `before` until just before the cue, then step to `after`."""
    return [[shift(at, -0.02), before], [at, after, "step"]]


def cam(at, az, el, dist, target, fov=24, dur=1.4, drift=0.0, cut=False, dolly=False):
    c = {"at": at, "az": az, "el": el, "dist": round(dist, 3), "target": list(target), "fov": fov, "dur": dur, "drift": drift}
    if cut:
        c["cut"] = True
    if dolly:
        c["dolly"] = True
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


# ---- the dolly zoom. A pose is a subject (target), an angle (az, el) and `h`, the frame's half-height at the target
# (dist · tan(fov / 2)): change the lens with the same h and the subject keeps its size while the sky behind it moves.
def dist_for(h, fov):
    return h / math.tan(math.radians(fov / 2))


def pose(target, az, el, h, fov):
    return dict(target=target, az=az, el=el, dist=dist_for(h, fov), fov=fov)


def lens(p, fov):
    """The same pose through another lens (a dolly zoom's other end)."""
    h = p["dist"] * math.tan(math.radians(p["fov"] / 2))
    return dict(p, dist=dist_for(h, fov), fov=fov)


def behind(p, pt):
    """Where the line from a pose's camera through the world point `pt` meets the dome: (az, el) on the dome, so a
    tear torn there (or the painted lamp) shows right behind that point in that pose."""
    az, el = math.radians(p["az"]), math.radians(p["el"])
    t = p["target"]
    c = (t[0] + math.sin(az) * math.cos(el) * p["dist"], t[1] + math.sin(el) * p["dist"], t[2] + math.cos(az) * math.cos(el) * p["dist"])
    d = (pt[0] - c[0], pt[1] - c[1], pt[2] - c[2])
    n = math.sqrt(sum(v * v for v in d))
    d = tuple(v / n for v in d)
    o = (c[0], c[1] - SKY_Y, c[2])
    b = sum(o[i] * d[i] for i in range(3))
    cc = sum(v * v for v in o) - SKY_R ** 2
    s = -b + math.sqrt(max(0.0, b * b - cc))
    q = tuple(o[i] + d[i] * s for i in range(3))
    return round(math.degrees(math.atan2(q[0], q[2])) % 360, 2), round(math.degrees(math.asin(q[1] / SKY_R)), 2)


# Poses (planned with pipeline/camprobe.ts; BRIEF.md §6). Myth poses are long lenses, truth poses wide ones.
HOOK_POSE = pose((5.0, 8.0, 3.0), 4, 16, 18.0, 22)        # the crack, the bones, the torn sky over the lake
WIDE = pose((1.0, 2.0, 0.0), 0, 20, 31.0, 22)             # the whole Isle under its painted sky
P_BONES = pose((BONES[0] + 1.0, 5.0, BONES[1] - 1.0), -6, 12, 9.0, 14)
P_CROWN = pose((QUEEN[0], 6.2, QUEEN[1]), 6, 12, 7.5, 30)
P_CLIFF = pose((4.0, 3.4, 18.0), -16, 10, 10.0, 14)
P_KEEP = pose((-1.0, 4.0, -2.0), -21, 18, 15.0, 26)
TEAR1, TEAR2 = (167.0, 7.0), (153.0, 8.0)              # behind the bones and the cliff, and both in sight of the keepers
P_TWIST = pose((5.0, 2.0, 2.0), 2, 16, 24.0, 18)
# the painted First Lamp hangs on the dome right above the Queen's head in the crown rule's long lens
LAMP_AZ, LAMP_EL = behind(lens(P_CROWN, 11), (QUEEN[0], 8.8, QUEEN[1]))

def tear(az, el, r, open_, patch=None, seed=None):
    t = {"az": az, "el": el, "r": r, "open": open_}
    if patch:
        t["patch"] = patch
    if seed is not None:
        t["seed"] = seed
    return t


def world():
    shot = lambda sid, off=0.0: {"shot": sid, **({"offset": round(off, 3)} if off else {})}
    lin = lambda at, v: [at, v, "linear"]
    H = shot("hook")
    span = loop_span()

    # ---- the clock (YEARS since the First Lamp fell). Today is year 500.
    R1A, R1B = cue("L4", "run.", 0.3), cue("L5", "find.", 0.3)            # run 1: 500 years of a myth that is simply true
    R2A, R2B = cue("L12", "Run", 0.25), cue("L12", "arguing.", 0.1)        # run 2: 500 years of digging and patching
    clock = [[H, 500], *jump(RESET, 500, 0), [R1A, 0], lin(R1B, 500), *jump(REWIND, 500, 0),
             [R2A, 0], lin(R2B, 500), [REMEMBER, 500], lin(shift(REMEMBER, 1.1), 0), *jump(ROLE, 0, 500), [WIPE, 500]]
    speed = [[H, 1], [cue("L4", "run."), 1], [R1A, 6], [R1B, 6], [cue("L6", "A"), 1],
             [R2A, 1], [cue("L12", "Run", 0.5), 6], [R2B, 6], [cue("L13", "Rule"), 1]]

    # ---- rule cues
    B_OPEN, B_UP, B_TEAR = cue("L8", "bury"), cue("L8", "Bones"), cue("L8", "older")
    C_JOB, C_LOOM = cue("L9", "job."), cue("L9", "Queen's")
    D_DIG, D_COUNT, D_TEAR = cue("L10", "dig."), cue("L10", "cliffs"), cue("L10", "thousand")
    K_HIDE, K_KEEP, K_P1, K_P2 = cue("L11", "hide"), cue("L11", "Keepers"), cue("L11", "paint"), cue("L11", "holes.")

    # ---- the painted sky. Tear 1 opens behind the bones, tear 2 behind the cliff; the keepers patch both; run 2 tears
    # and patches eleven more around the dome; the last one (tear 0, over the crack) stays open: frame 0's tear.
    T1, T2 = TEAR1, TEAR2
    T0 = (round(LAMP_AZ - 8, 2), round(LAMP_EL - 2.5, 2))
    gone = lambda: [*jump(RESET, 1, 0)]
    tears = []
    # tear 0: open on frame 0 (it widens on "lying?"), gone for the lazy version and the rules, torn again at the end of run 2
    t0_open = [[H, 0.82], [cue("L1", "lying?", -0.05), 0.82], [cue("L1", "lying?", 0.35), 1, "out"], *jump(RESET, 1, 0),
               [cue("L12", "arguing.", -0.5), 0], [cue("L12", "arguing.", -0.1), 1, "out"], *jump(WIPE, 1, 0.82)]
    tears.append(tear(T0[0], T0[1], 7.5, t0_open, seed=11))
    tears.append(tear(T1[0], T1[1], 5.5, [[H, 1], *jump(RESET, 1, 0), [B_TEAR, 0], [shift(B_TEAR, 0.5), 1, "out"], [WIPE, 1]],
                      [[H, 1], *jump(RESET, 1, 0), [K_P1, 0], lin(shift(K_P1, 0.55), 1), [WIPE, 1]], seed=23))
    tears.append(tear(T2[0], T2[1], 5.5, [[H, 1], *jump(RESET, 1, 0), [D_TEAR, 0], [shift(D_TEAR, 0.5), 1, "out"], [WIPE, 1]],
                      [[H, 1], *jump(RESET, 1, 0), [K_P2, 0], lin(shift(K_P2, 0.55), 1), [WIPE, 1]], seed=37))
    # run 2: eleven more tears around the dome, each patched half a second after it opens
    R2_TEARS = [(170, 26, 4.5), (205, 8, 5.0), (150, 12, 4.0), (222, 30, 5.5), (186, 38, 4.0), (240, 14, 4.5),
                (128, 28, 5.0), (196, 2, 3.5), (160, 44, 4.5), (262, 26, 4.0), (110, 10, 4.5)]
    r2a = tcue(cue("L12", "Run", 0.4)) or 34.0
    r2b = tcue(cue("L12", "arguing.", -0.7)) or 37.0
    for k, (az, el, r) in enumerate(R2_TEARS):
        on = shift(cue("L12", "Run", 0.4), (r2b - r2a) * k / (len(R2_TEARS) - 1))
        tears.append(tear(az, el, r, [[H, 1], *jump(RESET, 1, 0), [on, 0], [shift(on, 0.25), 1, "out"], [WIPE, 1]],
                          [[H, 1], *jump(RESET, 1, 0), [shift(on, 0.45), 0], lin(shift(on, 0.85), 1), [WIPE, 1]], seed=51 + 13 * k))
    # the twist: the paint thins to show the true sky (the lamp stays longest), then comes back for "hide it inside"
    sheer = [[H, 0], [REMEMBER, 0], lin(shift(REMEMBER, 0.8), 0.92), [ROLE, 0.92], [shift(ROLE, 0.9), 0], [WIPE, 0]]
    star_from = [round(SKY_R * 0.9 * math.sin(math.radians(200)) * math.cos(math.radians(30)), 2), round(SKY_Y + SKY_R * 0.9 * math.sin(math.radians(30)), 2),
                 round(SKY_R * 0.9 * math.cos(math.radians(200)) * math.cos(math.radians(30)), 2)]
    fall = [[H, 0], [shift(STAR, -0.35), 0], lin(shift(STAR, 0.9), 1), [shift(STAR, 0.95), 0, "step"], [WIPE, 0]]
    sky = {"r": SKY_R, "y": SKY_Y, "lamp": {"az": LAMP_AZ, "el": LAMP_EL}, "tears": tears, "sheer": sheer,
           "star": {"from": star_from, "to": [LAKE[0], 2.2, LAKE[1]], "fall": fall}}
    IMPACT = shift(STAR, 0.9)

    # ---- the HUD: holes torn in the painted sky, and how many the keepers have patched (both read from the tears)
    holes = [[H, 14], *jump(RESET, 14, 0), *jump(B_TEAR, 0, 1), *jump(D_TEAR, 1, 2)]
    patched = [[H, 13], *jump(RESET, 13, 0), *jump(K_P1, 0, 1), *jump(K_P2, 1, 2)]
    for k in range(len(R2_TEARS)):
        on = shift(cue("L12", "Run", 0.4), (r2b - r2a) * k / (len(R2_TEARS) - 1))
        holes += jump(on, 2 + k, 3 + k)
        patched += jump(shift(on, 0.45), 2 + k, 3 + k)
    holes += jump(cue("L12", "arguing.", -0.5), 13, 14) + [[WIPE, 14]]
    patched += [[WIPE, 13]]

    # ---- the ground: the crack (open for good), the bones in it, the cliffs' layers (a callback to EP32's strata)
    rift = [[H, 1], *jump(RESET, 1, 0), [B_OPEN, 0], [shift(B_OPEN, 0.6), 1, "out"], [WIPE, 1]]
    fears = [{"id": "rift", "x": RIFT_A[0], "z": RIFT_A[1], "r": 0.0, "kind": "rift", "to": list(RIFT_B), "dark": rift}]
    bones = [[H, 1], *jump(RESET, 1, 0), [B_UP, 0], lin(shift(B_UP, 0.9), 1), [WIPE, 1]]
    layers_n = [[H, 12], *jump(RESET, 12, 0), [D_COUNT, 0], lin(cue("L10", "years.", 0.1), 12), [WIPE, 12]]
    strata = {"war": {"y0": [[H, -4.4]], "y1": [[H, -4.0]]}, "surface": 2.55, "max": 12, "centuries": layers_n, "fade": [[H, 1]], "flood": [[H, 0]]}
    # the crater: the lake's rim lights as the star lands
    rings = [{"x": LAKE[0], "z": LAKE[1], "r": 6.6, "on": shift(IMPACT, 0.05), "off": ROLE, "color": "#fff3c4"}]
    dust = [{"at": IMPACT, "x": LAKE[0], "z": LAKE[1], "r": 5.0}]

    # ---- people: the crowd keeps the Lamplight's lamps; keepers among them; the Queen on her dais; one digger
    keepers = [[H, 0.22], *jump(RESET, 0.22, 0), [K_KEEP, 0], lin(shift(K_KEEP, 0.5), 0.22), [WIPE, 0.22]]
    look = [[H, 1], *jump(RESET, 1, 0), [STAR, 0], [shift(STAR, 0.5), 1], [ROLE, 1], [shift(ROLE, 0.6), 0], *jump(WIPE, 0, 1)]
    ruler = [pk(H, *QUEEN, "idle", face=0), pk(C_LOOM, *QUEEN, "alert", face=0), pk(cue("L9", "it.", 0.2), *QUEEN, "idle", face=0),
             pk(cue("L18", "ruins"), *QUEEN, "alert", face=0), pk(cue("L18", "us.", 0.7), *QUEEN, "idle", face=0)]
    digger = [pk(H, *DIGGER, "hidden", face=90), pk(D_DIG, *DIGGER, "idle", face=90), pk(cue("L11", "Four:", -0.1), *DIGGER, "hidden", face=90)]
    g_now = [pk(H, *G_NOW, "idle", face=160)]
    # EP35's tease: on "ruins" broken pillars rise out of the ground beside the bones, hold, and sink back for the loop
    ruin = [[H, 0], [cue("L18", "ruins", -0.05), 0], [cue("L18", "older", 0.1), 1, "out"], [cue("L18", "us.", 0.55), 1], [cue("L18", "us.", 1.0), 0]]
    # the lake's lamp boats withdraw for the flashback (year 0: the star falls into an empty lake) and come back with the day
    boats = [[H, 1], [REMEMBER, 1], lin(shift(REMEMBER, 0.6), 0), [ROLE, 0], lin(shift(ROLE, 0.8), 1), [WIPE, 1]]
    ripple = [shot("hook", 0.05), cue("L4", "run."), cue("L12", "Run"), IMPACT]
    bells = [cue("L9", "crown"), cue("L12", "again.")]

    # Camera language: the dolly zoom. Truth: in on a wide lens (the sky falls away); myth: out on a long lens.
    dz = lambda at, p, dur=1.2, **kw: cam(at, p["az"], p["el"], p["dist"], p["target"], fov=p["fov"], dur=dur, dolly=True, **kw)
    cut = lambda at, p, **kw: cam(at, p["az"], p["el"], p["dist"], p["target"], fov=p["fov"], dur=0.01, cut=True, **kw)
    LESSON_AT = cue("L16", "Myths", -0.25)
    camera = [
        cam(H, HOOK_POSE["az"], HOOK_POSE["el"], HOOK_POSE["dist"], HOOK_POSE["target"], fov=HOOK_POSE["fov"], drift=HOOK_DRIFT),
        dz(cue("L2", "Meet", -0.1), lens(HOOK_POSE, 20), dur=3.2),
        cut(RESET, lens(HOOK_POSE, 20)),
        # the lazy version: a long lens, the perfect sky looming (the myth is all there is)
        dz(cue("L3", "simply", -0.1), lens(HOOK_POSE, 13), dur=1.6),
        cut(cue("L4", "run.", 0.05), WIDE),
        dz(cue("L5", "Nobody", -0.1), lens(WIDE, 15), dur=2.4),
        dz(cue("L6", "A", -0.2), lens(WIDE, 12), dur=1.6),
        cut(REWIND, lens(WIDE, 26)),
        dz(cue("L7", "Four", -0.1), lens(WIDE, 18), dur=1.4),
        # each rule: a cut to its subject, then a dolly zoom on its word
        cut(RULES, P_BONES),
        dz(B_TEAR, lens(P_BONES, 40), dur=1.3),
        cut(cue("L9", "Two:", -0.1), P_CROWN),
        dz(C_LOOM, lens(P_CROWN, 11), dur=1.5),
        cut(cue("L10", "Three:", -0.1), P_CLIFF),
        dz(D_TEAR, lens(P_CLIFF, 38), dur=1.3),
        cut(cue("L11", "Four:", -0.1), P_KEEP),
        dz(K_P1, lens(P_KEEP, 14), dur=1.6),
        cut(RUN2, WIDE),
        dz(cue("L12", "hundred", -0.1), lens(WIDE, 30), dur=2.4),
        cut(TWIST, P_TWIST),
        dz(REMEMBER, lens(P_TWIST, 34), dur=1.4),
        dz(cue("L14", "lake.", -0.2), lens(P_TWIST, 30), dur=1.2),
        dz(ROLE, lens(P_TWIST, 12), dur=1.4),
        # the lesson: one slow dolly zoom across the whole Isle in golden light
        cut(LESSON_AT, lens(WIDE, 14)),
        dz(cue("L16", "Every", -0.1), lens(WIDE, 22), dur=2.4),
        cam(WIPE, HOOK_POSE["az"] - HOOK_DRIFT * span, HOOK_POSE["el"], HOOK_POSE["dist"], HOOK_POSE["target"], fov=HOOK_POSE["fov"], cut=True, drift=HOOK_DRIFT),
    ]
    if SCOUT:
        camera = [cam(H, WIDE["az"], WIDE["el"], WIDE["dist"], WIDE["target"], fov=WIDE["fov"])]
    light = [
        {"at": H, "mood": "golden"},
        {"at": RESET, "mood": "day", "dur": 0.4},
        {"at": cue("L6", "A", -0.2), "mood": "gloom", "dur": 0.6},
        {"at": REWIND, "mood": "day", "dur": 0.3},
        {"at": K_HIDE, "mood": "dusk", "dur": 0.8},
        {"at": RUN2, "mood": "day", "dur": 0.4},
        {"at": TWIST, "mood": "dusk", "dur": 0.6},
        {"at": ROLE, "mood": "day", "dur": 0.5},
        {"at": cue("L16", "Myths", -0.3), "mood": "golden", "dur": 1.4},
    ]
    human_valley = {
        "buildings": [{"kind": k, "a": list(a), "face": 0} for k, a in HUMAN_B],
        "roof": [[H, 1]], "pens": [{"a": [-6.4, -1.4], "r": 1.6}], "cover": [[H, 1]],
        "roads": {"b": HUMAN_ROAD}, "route": [[H, 1]], "tradeKey": "tradeH", "lanterns": [[H, 0]],
        "tower": {"x": HUMAN_TOWER[0], "z": HUMAN_TOWER[1], "h": 6.0, "keys": [[H, 1]], "rings": bells},
    }
    clear = [BONES, (BONES[0] - 4, BONES[1]), (BONES[0] + 4, BONES[1] - 0.5), CAIRN, (FIELD[0], FIELD[1]), *[tuple(c) for c in CROWD], DIGGER, RUIN, (2.5, 19.6), (4.0, 19.0), (0.5, 19.0), (6.5, 19.5)]
    rift_lane = [[RIFT_A[0] + (RIFT_B[0] - RIFT_A[0]) * k / 8, RIFT_A[1] + (RIFT_B[1] - RIFT_A[1]) * k / 8 + dz, 2.2] for k in range(9) for dz in (0.0, 2.6)]
    return {
        "clock": {"label": "YEAR", "keys": clock},
        "speed": speed,
        "camera": camera,
        "light": light,
        "herd": {"count": [[H, 24]], "max": 30, "base": 24, "centers": [[-9.5, -1.0], [-8.4, 1.2]], "skin": "sheep"},
        "pred": [[H, 1]],
        "predators": [{"id": "g1", "scale": 1.3, "keys": g_now, "adorn": True}],
        "series": {"holes": holes, "patched": patched, "tradeH": [[H, 4]]},
        "settlement": human_valley,
        "people": {"count": [[H, 30], [WIPE, 30]], "centers": CROWD, "spread": 1.6, "life": 70, "royal": keepers, "robe": ROBE,
                   "look": look, "lamps": [[H, 1]],
                   "figures": [{"keys": digger, "tunic": "#7a5a3a", "torch": True}],
                   "ruler": {"keys": ruler, "dais": {"x": DAIS[0], "z": DAIS[1], "face": 0}}},
        "fields": {"plots": [{"x": FIELD[0], "z": FIELD[1], "w": FIELD[2], "d": FIELD[3]}], "ripe": [[H, 1]]},
        "props": [{"kind": "cairn", "x": CAIRN[0], "z": CAIRN[1], "stones": [[H, 3]]},
                  {"kind": "offerings", "x": CAIRN[0], "z": CAIRN[1], "r": 1.7, "lights": [[H, 1]]},
                  {"kind": "lanterns", "x": LAKE[0], "z": LAKE[1], "r": 3.8, "n": 9, "lights": boats},
                  {"kind": "sheaves", "x": FIELD[0], "z": FIELD[1], "r": 2.7, "n": 8, "sheaves": [[H, 8]]},
                  {"kind": "statue", "x": STATUE[0], "z": STATUE[1], "face": -90, "rise": [[H, 1]], "gild": [[H, 1]], "tar": [[H, 1]], "grow": [[H, 1.35]], "torch": [[H, 0]]},
                  {"kind": "border", "x": LINE_A[0], "z": LINE_A[1], "to": list(LINE_B), "skip": [0.46, 0.65], "rise": [[H, 1]]},
                  {"kind": "relic", "x": RELIC[0], "z": RELIC[1], "face": -90, "rise": [[H, 1]]},
                  {"kind": "bones", "x": BONES[0], "z": BONES[1], "face": BONES_FACE, "r": 1.7, "rise": bones},
                  {"kind": "ruin", "x": RUIN[0], "z": RUIN[1], "face": 20, "r": 2.2, "rise": ruin}],
        "fears": fears,
        "strata": strata,
        "sky": sky,
        "clearTrees": [[d[0], d[1], 2.2] for d in clear] + rift_lane,
        "layers": {"ripple": ripple, "rings": rings, "dust": dust},
        "ambient": {"birds": 9, "motes": 40, "glints": True},
        "simLoop": WIPE,
    }


# ---------------------------------------------------------------- overlays per shot

ROWS = [
    {"n": 1, "label": "PROOF", "text": "bones older than gods", "at": cue("L8", "proof.")},
    {"n": 2, "label": "A JOB", "text": "the Queen's crown", "at": cue("L9", "job.")},
    {"n": 3, "label": "A DIGGER", "text": "the cliffs count", "at": cue("L10", "dig.")},
    {"n": 4, "label": "A KEEPER", "text": "paints over holes", "at": cue("L11", "hide")},
    {"n": 5, "label": "THE MEMORY", "text": "the truth inside", "at": cue("L7", "Four"), "locked": True, "unlockAt": cue("L15", "inside", -0.1)},
]
SPRITE = {"sprite": "ep34/firstlamp_sprite.png", "spriteW": 76, "spriteH": 124}


def stag(kind, text, at, end, lift=70, dx=0, **kw):
    return {"kind": kind, "text": text, "at": at, "end": end, "lift": lift, "dx": dx, **kw}


def overlays():
    G = {s: [] for s in SHOTS}
    hook_text = [{"text": "THE GODS MADE IT", "color": GILT, "size": 60, "pulseAt": cue("L1", "gods")},
                 {"text": "ARE THEY LYING?", "color": BONE, "size": 64, "pulseAt": cue("L1", "lying?")}]
    G["hook"] += [
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 60, "start": {"shot": "hook"}, "end": cue("L2", "Meet", -0.1), "preShow": True},
        {"type": "sting", "label": "WORLD ENGINE", "run": "RUN 34 · MYTH", "dur": 1.4, "start": {"shot": "hook"}, "front": True},
        {"type": "skyTags", "start": cue("L1", "lying?", 0.1), "end": RESET, "tags": [stag("ground", "SOMETHING BURIED", cue("L1", "lying?", 0.1), cue("L2", "Meet", -0.1), pos=[BONES[0], BONES[1], 0.4], lift=110)]},
        {"type": "fieldCard", "mode": "intro", "y": 440, "start": cue("L2", "Meet", -0.05), "end": RESET, "dietAt": cue("L2", "fell"),
         "kicker": "FIELD CARD · NO. 009", "kind": "CREATION MYTH", "name": "THE FIRST LAMP", "dietLabel": "SAYS", "diet": "it fell from the sky", **SPRITE},
    ]
    G["setup"] += [
        {"type": "blockWipe", "at": RESET, "dur": 0.34, "color": "#1b2766"},
        {"type": "kinetic", "parts": [{"text": "THE MYTH", "at": cue("L3", "myth"), "size": 80, "color": GILT}, {"text": "IS SIMPLY TRUE", "at": cue("L3", "simply"), "color": "parchment", "size": 60}],
         "y": 470, "size": 80, "start": cue("L3", "myth", -0.05), "end": cue("L4", "Press", -0.15)},
        {"type": "simBar", "counters": [{"icon": "tear", "label": "HOLES", "key": "holes", "color": ULTRA, "digits": 2},
                                        {"icon": "brush", "label": "PATCHED", "key": "patched", "color": "parchment", "digits": 2}],
         "compact": True, "start": cue("L4", "Press", -0.15), "end": cue("L16", "Myths", -0.3), "runAt": [cue("L4", "run."), cue("L12", "Run")]},
    ]
    G["run1"] += [
        {"type": "kinetic", "parts": [{"text": "500 YEARS", "at": cue("L5", "Five"), "color": "parchment", "size": 56},
                                      {"text": "NOBODY DIGS", "at": cue("L5", "Nobody"), "color": "parchment", "size": 56},
                                      {"text": "NOTHING TO FIND", "at": cue("L5", "Nothing"), "color": "rust", "size": 56}],
         "y": 468, "size": 56, "start": cue("L5", "Five", -0.05), "end": cue("L6", "A", -0.25)},
    ]
    G["drop"] += [
        {"type": "stamp", "text": "TEXTBOOK", "sub": "0 HOLES · 0 SECRETS · 0 STORIES", "color": "rust", "y": 560, "size": 84, "start": cue("L6", "true"), "end": cue("L6", "textbook.", 0.55)},
    ]
    G["rehook"] += [
        {"type": "rewind", "y": 620, "start": cue("L6", "textbook.", 0.6), "end": cue("L7", "Wrong", 0.3)},
        {"type": "blockWipe", "at": cue("L6", "textbook.", 0.58), "dur": 0.34},
        {"type": "kinetic", "parts": [{"text": "WRONG MYTHS", "at": cue("L7", "Wrong"), "size": 78, "color": GILT}, {"text": "BUILD BETTER WORLDS", "at": cue("L7", "build"), "color": "parchment", "size": 56}],
         "y": 470, "size": 84, "start": cue("L7", "Wrong", -0.05), "end": cue("L7", "Four", -0.15)},
        {"type": "fieldCard", "mode": "checklist", "y": 448, "rows": ROWS, "start": cue("L7", "Four", -0.1), "end": cue("L16", "Myths", -0.3),
         "kicker": "THE FIRST LAMP · WHAT IT HIDES", "title": "TEAR THE SKY", "blinkAt": cue("L7", "twist."), "lockedText": "the twist", **SPRITE,
         "collapse": [[cue("L8", "bury", -0.3), 0], [cue("L8", "bury", 0.0), 1], [ROLE, 1], [shift(ROLE, 0.3), 0]]},
    ]
    G["bones"] += [{"type": "skyTags", "start": cue("L8", "Bones", 0.2), "end": cue("L9", "Two:", -0.15), "tags": [
        stag("ground", "BONES · 9,000 YEARS", cue("L8", "Bones", 0.2), cue("L9", "Two:", -0.15), pos=[BONES[0] + 2.2, BONES[1], 0.5], lift=80),
        stag("myth", "THE WORLD IS 500", cue("L8", "older", 0.3), cue("L9", "Two:", -0.15), tear=1, lift=-50, band=[600, 760])]}]
    G["crown"] += [{"type": "skyTags", "start": cue("L9", "Queen's"), "end": cue("L10", "Three:", -0.15), "tags": [
        stag("ground", "HER RIGHT TO RULE", cue("L9", "Queen's"), cue("L10", "Three:", -0.15), pos=[QUEEN[0], QUEEN[1], 1.6], lift=-30, dx=250),
        stag("myth", "THE GODS CROWNED HER", cue("L9", "rests", -0.1), cue("L10", "Three:", -0.15), lift=-150, dx=-200)]}]
    G["cliff"] += [{"type": "skyTags", "start": cue("L10", "cliffs"), "end": cue("L11", "Four:", -0.15), "tags": [
        stag("ground", "10,000 YEARS", cue("L10", "count"), cue("L11", "Four:", -0.15), pos=[4.0, 17.5, -2.5], lift=90, dx=200),
        stag("myth", "MADE IN ONE NIGHT", cue("L10", "thousand", 0.3), cue("L11", "Four:", -0.15), tear=2, lift=-50, band=[600, 760])]}]
    G["keepers"] += [{"type": "skyTags", "start": cue("L11", "Keepers"), "end": cue("L12", "Run", -0.15), "tags": [
        stag("ground", "THE KEEPERS", cue("L11", "Keepers"), cue("L12", "Run", -0.15), pos=[-2.4, -3.2, 1.6], lift=90),
        stag("myth", "PAINTED OVER", cue("L11", "holes.", 0.2), cue("L12", "Run", -0.15), tear=2, lift=-50, band=[600, 760])]}]
    G["run2"] += [
        {"type": "stamp", "text": "STILL ARGUING", "sub": "500 YEARS · 14 HOLES · 13 PATCHED", "color": ULTRA, "rotate": -4, "y": 880, "size": 90, "start": cue("L12", "arguing."), "end": cue("L13", "Rule", -0.1)},
    ]
    G["twist"] += [
        {"type": "kinetic", "parts": [{"text": "RULE 5?", "at": cue("L13", "Rule"), "color": "ember"}, {"text": "NOT LYING", "at": cue("L13", "isn't"), "color": BONE, "size": 72}],
         "size": 150, "y": 520, "start": cue("L13", "Rule", -0.02), "end": cue("L13", "It's", -0.1)},
        {"type": "kinetic", "parts": [{"text": "REMEMBERING", "at": cue("L13", "remembering."), "color": GILT, "size": 84}],
         "size": 84, "y": 560, "start": cue("L13", "remembering.", -0.05), "end": STAR},
        {"type": "skyTags", "start": STAR, "end": ROLE, "tags": [
            stag("myth", "A LAMP FELL", shift(STAR, 0.1), ROLE, lift=-90, dx=-240),
            stag("ground", "A STAR FELL", shift(STAR, 0.95), cue("L14", "lake.", -0.1), pos=[LAKE[0], LAKE[1], 0.3], lift=110, dx=230),
            stag("ground", "THE CRATER", cue("L14", "lake.", -0.1), ROLE, pos=[LAKE[0], LAKE[1], 0.3], lift=110, dx=230)]},
    ]
    G["role"] += [
        {"type": "followChip", "start": cue("L15", "myth.", 0.2), "end": cue("L16", "Every", 0.3), "text": "FOLLOW", "sub": "PART 34/50"},
    ]
    G["lesson"] += [
        {"type": "fieldCard", "mode": "full", "y": 452, "rows": [dict(r, at=cue("L16", "Myths", -0.3), **({"unlockAt": cue("L16", "Myths", -0.3)} if r.get("locked") else {})) for r in ROWS],
         "start": cue("L16", "Myths", -0.3), "end": WIPE, "kicker": "BEFORE YOU WRITE A MYTH", "title": "THE FIRST LAMP", **SPRITE,
         # the line to keep: on screen from the end of the first sentence until the wipe covers the card
         "subtitle": "Every myth is a memory, told wrong.", "subtitleAt": cue("L16", "lies.")},
    ]
    G["cta"] += [
        {"type": "blockWipe", "at": WIPE, "dur": 0.34},
        {"type": "endCardS2", "start": WIPE, "end": cue("L18", "Part", -0.12), "fadeOut": 0.3, "kicker": "PART 34 / 50",
         "title": "What If Your World's Creation Myth Is Wrong?", "cta": "COMMENT", "icon": "bubble", "with": "Which would you choose?", "withAt": cue("L17", "myth?", -0.05), "choiceSize": 30,
         "choices": [{"text": "TELL THEM", "color": BONE, "at": cue("L17", "tell")}, {"text": "KEEP THE MYTH", "color": GILT, "at": cue("L17", "keep")}]},
    ]
    gone = cue("L18", "us.", 0.6)
    G["next"] += [
        {"type": "seasonBar", "y": 350, "part": 34, "of": 50, "start": cue("L18", "Part", -0.1), "fillAt": cue("L18", "Part", -0.05), "fillDur": 0.6, "ofAt": cue("L18", "50."), "end": gone},
        {"type": "followButton", "y": 556, "start": cue("L18", "Follow", -0.6), "pressAt": cue("L18", "Follow"), "end": gone, "text": "FOLLOW", "doneText": "FOLLOWING", "sub": "FOR PART 35"},
        {"type": "nextRun", "y": 772, "start": cue("L18", "35:", -0.1), "revealAt": cue("L18", "ruins"), "end": gone,
         "kicker": "NEXT RUN · 35", "title": "THE RUINS", "sub": "OLDER THAN US.", "sprite": "ruins", "spritePx": 8},
        {"type": "kinetic", "parts": hook_text, "y": 440, "size": 60, "start": cue("L18", "us.", 0.92), "fadeIn": 0.35, "preShow": True},
    ]
    return G


LESSON = ("A creation myth that is simply true leaves nothing to find. Let yours be wrong about the past and still do a "
          "job: bury proof that it can't explain, give it something to hold up (a crown), let someone dig and someone "
          "hide what they find. Then hide a real event inside it, told wrong, so a reader can decode it. Every myth "
          "is a memory, told wrong.")

# Per-shot production notes (STORYBOARD.md). (purpose, visual, camera, layers fg/mid/bg, lighting, onScreen, transition, music)
NOTES = {
    "hook": ("Close EP33's loop (a crack of light opened on 'the gods are lying') and stop the scroll on the question.",
             "Golden hour, looking north across the Isle: EP33's crack of light lies open for good in the meadow south of the lake, a giant's bones half out of it; behind the island the sky is a painted dome (lapis, gilt stars, a gold horizon band, the First Lamp falling with its trail) mended with old patches, and a fresh ragged hole torn in it right above the crack shows the true night sky. THE GODS MADE IT / ARE THEY LYING? from frame 0, each line pulsing on its word; the hole widens on 'lying?'. Then the field card: THE FIRST LAMP · CREATION MYTH · SAYS: it fell from the sky.",
             "From the south over the crack (el 16, fov 22), dolly-zooming to a longer lens (fov 20) under the field card.", ("kinetic, sting, ground tag, field card", "the crack, the bones, the crowd with lamps", "the painted sky, torn"),
             "Golden hour.", "THE GODS MADE IT / ARE THEY LYING? · FIELD CARD NO. 009 · THE FIRST LAMP", "Ultramarine block wipe into the lazy version.", "Lullaby: a harp rocking in triplets, the theme on music box; a hit on 'lying?'."),
    "setup": ("The lazy version: the myth is simply true.",
              "A wipe to a perfect sky: no holes, no patches; the ground closed, no bones, the cliffs one plain colour (a world made in one night has no layers). THE MYTH / IS SIMPLY TRUE as the lens lengthens and the painted lamp looms. The sim bar arrives (HOLES 00, PATCHED 00) and RUN is pressed.",
              "Dolly zoom out to fov 13 (the myth looms).", ("kinetic, sim bar", "the closed ground", "the perfect painted sky"), "Day.", "THE MYTH IS SIMPLY TRUE", "A cut to the whole Isle on 'run'.", "Lullaby, in major."),
    "run1": ("Run the lazy version: 500 years and nothing to find.",
             "The whole Isle under its unbroken painted sky; YEAR 0→500; nobody digs; HOLES 00. 500 YEARS, NOBODY DIGS, NOTHING TO FIND; tags: THE MYTH · MADE IN ONE NIGHT and THE GROUND · AGREES.",
             "Wide (dist 160, fov 22), dolly-zooming to a long lens (fov 15): the painted sky swells around the Isle.", ("sim bar, kinetic, tags", "the unchanging Isle", "the painted sky"), "Day.", "500 YEARS / NOBODY DIGS / NOTHING TO FIND", "Gloom.", "Drive."),
    "drop": ("The punchline: a myth that's just true is a textbook.", "Gloom over the perfect sky: TEXTBOOK · 0 HOLES · 0 SECRETS · 0 STORIES.",
             "The longest lens of the episode (fov 12, dist 292): the painted sky fills the frame.", ("stamp", "the Isle", "the painted sky"), "Gloom.", "TEXTBOOK · 0 HOLES · 0 SECRETS · 0 STORIES", "Rewind + block wipe.", "Drop; a boom on 'textbook'."),
    "rehook": ("Re-hook: the thesis, four rules, one locked.",
               "REWIND to the pristine sky. WRONG MYTHS / BUILD BETTER WORLDS; then the checklist TEAR THE SKY, row 5 locked (the twist).",
               "Wide, dolly-zooming from fov 26 to 18.", ("rewind, kinetic, checklist", "the Isle", "the painted sky"), "Day.",
               "WRONG MYTHS · BUILD BETTER WORLDS · TEAR THE SKY 0/5", "Cut to the meadow south of the lake.", "Excavate, bare (kalimba and wood blocks); a riser into 'the twist'."),
    "bones": ("Rule 1: bury proof.", "The meadow south of the lake on a long lens, the painted lamp behind it; on 'bury' the crack of light opens along the meadow; on 'Bones' a giant's skeleton rises half out of it (THE GROUND · BONES · 9,000 YEARS); on 'older' the sky tears open right behind it (THE MYTH · THE WORLD IS 500) as the camera dolly-zooms in to a wide lens and the sky falls away. HOLES 01.",
              "Cut, then a dolly zoom in (fov 15 → 40).", ("tags, checklist (folded)", "the bones in the crack", "the sky tearing"), "Day.", "1 PROOF · bones older than gods", "Cut to the Queen.", "Excavate 1: kalimba and wood blocks."),
    "crown": ("Rule 2: give the myth a job.", "The Queen on her dais close on a wide lens; on 'Queen's' a dolly zoom out to a long lens swells the painted First Lamp behind her (THE GROUND · HER RIGHT TO RULE; THE MYTH · THE GODS CROWNED HER); the tower bell rings on 'crown'.",
              "Cut, then a dolly zoom out (fov 34 → 11): the myth looms over her.", ("tags, checklist (folded)", "the Queen", "the painted lamp"), "Day.", "2 A JOB · the Queen's crown", "Cut to the south cliff.", "Excavate 2: a pizzicato walk over a bowed bass."),
    "cliff": ("Rule 3: let someone dig.", "The island's south cliff, low and close, a digger with a torch at its lip; on 'cliffs' twelve layers stack up the cut side from the bottom (a callback to EP32's strata; THE GROUND · 10,000 YEARS); on 'thousand' the sky tears behind it (THE MYTH · MADE IN ONE NIGHT). HOLES 02.",
              "Cut, then a dolly zoom in (fov 14 → 38): the sky falls away behind the layered cliff.", ("tags, checklist (folded)", "the layered cliff, the digger", "the sky tearing"), "Day.", "3 A DIGGER · the cliffs count", "Cut to the valley.", "Excavate 3: a low hand drum and a shaker."),
    "keepers": ("Rule 4: let someone hide it.", "Dusk over the valley: robed keepers appear among the crowd (THE GROUND · THE KEEPERS); on 'paint' and 'holes' both tears are brushed over with fresher paint, a visible patch with a dark seam (THE MYTH · PAINTED OVER). PATCHED 02.",
                "Cut, then a dolly zoom out (fov 30 → 14): the mended sky looms.", ("tags, checklist (folded)", "the keepers", "the patches"), "Dusk.", "4 A KEEPER · paints over holes", "Cut to the whole Isle.", "Excavate 4: the theme on clarinet, glockenspiel on the roots."),
    "run2": ("Run with the gap open: 500 years of digging and patching.",
             "The whole Isle; YEAR 0→500; eleven more holes tear around the painted sky and each is patched half a second later; the last, over the crack, stays open: STILL ARGUING · 500 YEARS · 14 HOLES · 13 PATCHED, stamped in ultramarine.",
             "Wide, dolly-zooming in to a wide lens (fov 22 → 30).", ("sim bar, stamp", "the tearing and mending sky", "the true sky in the holes"), "Day.", "STILL ARGUING · 500 YEARS · 14 HOLES · 13 PATCHED", "Cut to dusk.", "Drive with the theme; a stab and a cymbal on 'arguing'."),
    "twist": ("The locked rule: the myth isn't lying, it's remembering.",
              "Dusk: RULE 5? NOT LYING; on 'remembering' the clock runs back to year 0 and the paint thins until the true night sky shows through the whole dome, the painted lamp fading last. On 'star' a real star falls out of the sky behind the painted lamp into the lake: a flash, a ripple, a ring of dust, and the lake's rim lights as a crater (THE MYTH · A LAMP FELL; THE GROUND · A STAR FELL, then THE CRATER); every face turns up.",
              "Cut, a dolly zoom in to a wide lens (fov 18 → 34) on 'remembering'.", ("kinetic, tags", "the falling star, the crater", "the sheer painted sky"), "Dusk.",
              "RULE 5? NOT LYING · REMEMBERING · A LAMP FELL / A STAR FELL · THE CRATER", "A dolly zoom out on 'So'.", "Twist (a held A7♭9), then the lullaby in D major (the myth was a memory); a boom as the star lands."),
    "role": ("Unlock rule 5: hide the truth inside the myth.",
             "Day returns and the paint with it; a dolly zoom out to a long lens brings the painted lamp back over the lake (the star, remembered as a lamp); the checklist opens and row 5 unlocks on 'inside': THE MEMORY · the truth inside · 5/5. The follow chip (+ FOLLOW · PART 34/50) after 'myth'.",
             "Dolly zoom out (fov 34 → 12).", ("open checklist, follow chip", "the lake", "the painted lamp"), "Day.", "5 THE MEMORY · the truth inside · 5/5", "The card goes full.", "Anthem from 'So'; a D-major hit on 'inside'."),
    "lesson": ("The takeaway.", "The full card (BEFORE YOU WRITE A MYTH · THE FIRST LAMP, all five rows ticked) over the whole Isle in golden light under its mended, torn sky, with 'Every myth is a memory, told wrong.' in serif italic from the end of the first sentence.",
               "Wide: one slow dolly zoom (fov 14 → 22).", ("full card, follow chip", "the Isle", "the painted sky"), "Golden hour.", "BEFORE YOU WRITE A MYTH · THE FIRST LAMP · Every myth is a memory, told wrong.", "Block wipe to the end card.", "Anthem; the World Engine chime as the card lands."),
    "cta": ("Comment CTA: would you tell them, or keep the myth?", "End card: logo, PART 34 / 50, the title, and a COMMENT panel where TELL THEM and KEEP THE MYTH pop on their words, then 'Which would you choose?'",
            "Cut (under the block wipe) back to the hook pose.", ("end card", "the Isle", "the torn sky"),
            "Golden hour (the loop frame).", "COMMENT · TELL THEM / KEEP THE MYTH · Which would you choose?", "The card lifts on 'Part'.", "Outro."),
    "next": ("Say the part number, ask for the follow with a reason (part 35), open the next loop.",
             "The hook frame; PART 34/50; FOLLOW FOR PART 35, pressed on 'Follow'; NEXT RUN · 35 decodes from locked pillars to THE RUINS · OLDER THAN US. In the world, on 'ruins', broken pillars older than anyone rise out of the ground beside the bones and the Queen looks across at them; they sink back before the hook title returns.",
             "The hook frame.", ("progress bar, follow button, next-run card", "the ruins rising", "the torn sky"), "Golden hour.",
             "PART 34/50 · FOLLOW FOR PART 35 · NEXT RUN: THE RUINS · OLDER THAN US.", "Loop to frame 0.", "Tease over a held A; stones grinding on 'ruins'; the engine chime on 'Follow'."),
}


def build():
    ep = {
        "id": "ep34", "number": 34, "season": 2,
        "title": "What If Your World's Creation Myth Is Wrong?",
        "lesson": LESSON,
        "format": {"version": "s2", "qa": {"min": 55.0, "max": 62.0}},
        "voice": {
            "provider": "kokoro",
            "kokoro": {"voice": "af_heart", "lang": "a", "speed": 0.98},
            "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                           "settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.2, "use_speaker_boost": True}},
            "direction": "The same lab host, a little conspiratorial this time. The hook is a question asked of the viewer's childhood. 'Simply true' is the knowing setup; 'a textbook' lands dry. "
                         "The rules are crisp, two beats each. 'It's remembering' is the quiet reveal; 'A star really fell here' is wonder. The comment ask is a genuine dilemma.",
        },
        "timing": {"leadIn": 0.2, "tail": 0.85, "shotLead": 0.12},
        "captionY": 1238,
        "captionsOff": [{"line": "L3", "from": "myth"}, {"line": "L5", "from": "Five"}, {"line": "L7", "from": "Wrong", "to": "Four"}, {"line": "L13", "from": "Rule"}],
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
             hit("towerBell", cue("L1", "gods"), -20), hit("tear", cue("L1", "lying?", -0.05), -15),
             hit("cardSlide", cue("L2", "Meet", -0.05), -18), hit("check", cue("L2", "fell"), -20)],
    "setup": [hit("rewind", RESET, -15), hit("restore", cue("L3", "simply"), -19),
              hit("runPress", cue("L4", "run."), -11), hit("worldRipple", cue("L4", "run."), -16)],
    "run1": [bed("simTicks", cue("L4", "run.", 0.3), cue("L5", "find.", 0.3), -22), hit("crownPass", cue("L5", "Nobody"), -20), hit("stamp", cue("L5", "Nothing"), -21)],
    "drop": [hit("stamp", cue("L6", "true"), -10)],
    "rehook": [hit("rewind", cue("L6", "textbook.", 0.55), -11), hit("cardSlide", cue("L7", "Four", -0.1), -17)],
    "bones": [hit("check", cue("L8", "proof."), -13), hit("rift", cue("L8", "bury"), -15), hit("dig", cue("L8", "Bones"), -14), hit("tear", cue("L8", "older"), -11)],
    "crown": [hit("check", cue("L9", "job."), -13), hit("towerBell", cue("L9", "crown"), -16), hit("morph", cue("L9", "Queen's"), -20)],
    "cliff": [hit("check", cue("L10", "dig."), -13), bed("rumble", cue("L10", "cliffs"), cue("L10", "years.", 0.1), -16), hit("tear", cue("L10", "thousand"), -11)],
    "keepers": [hit("check", cue("L11", "hide"), -13), hit("restore", cue("L11", "Keepers"), -18), hit("brush", cue("L11", "paint"), -12), hit("brush", cue("L11", "holes."), -12)],
    "run2": [hit("runPress", cue("L12", "Run"), -11), hit("worldRipple", cue("L12", "Run"), -16), bed("simTicks", cue("L12", "Run", 0.3), cue("L12", "arguing."), -22),
             hit("tear", cue("L12", "again.", 0.05), -19), hit("brush", cue("L12", "Five", 0.1), -19), hit("tear", cue("L12", "years.", -0.1), -19), hit("brush", cue("L12", "still", -0.05), -19),
             hit("towerBell", cue("L12", "again."), -20), hit("stamp", cue("L12", "arguing."), -13)],
    "twist": [hit("unlock", cue("L13", "Rule"), -15), hit("rewind", REMEMBER, -15), hit("starfall", STAR, -10), hit("worldRipple", shift(STAR, 0.9), -15)],
    "role": [hit("restore", ROLE, -17), hit("unlock", cue("L15", "inside", -0.1), -10)],
    "lesson": [hit("engineWind", cue("L16", "Myths", -0.8), -15), hit("chime", cue("L16", "Myths", -0.3), -10), hit("cardSlide", cue("L16", "Myths", -0.3), -18)],
    "cta": [hit("restore", WIPE, -21), hit("check", cue("L17", "tell"), -17), hit("check", cue("L17", "keep"), -17)],
    "next": [bed("simTicks", cue("L18", "Part", -0.05), cue("L18", "Part", 0.55), -22),
             hit("engineWind", cue("L18", "Follow", -0.5), -15), hit("followPress", cue("L18", "Follow"), -11), hit("chime", cue("L18", "Follow", 0.02), -11),
             hit("cardSlide", cue("L18", "35:", -0.1), -18), hit("unlock", cue("L18", "ruins"), -15),
             hit("stoneRise", cue("L18", "ruins", -0.1), -13),
             hit("engineWind", {"end": True, "offset": -0.54}, -14)],
}


def msec(at, style, chords, key, **kw):
    return {"from": at, "style": style, "chords": chords, "key": key, **kw}


# The score: the series theme stays (D minor for the problem, D major for the payoff). EP34's band is `lullaby` (the
# myth as it is sung to children: a harp rocking in triplets, the theme on music box) and `excavate` (the truth coming
# up out of the ground: kalimba and wood blocks, then a pizzicato walk over a bowed bass, a low hand drum and a shaker,
# the theme on clarinet with glockenspiel), one family per rule. At the twist the lullaby returns in D major: the myth
# was a memory all along.
LULL_P = {"harp": 46, "mbox": 10}
EXC_P = {"marimba": 108, "lead": 71}
BACK_P = {"strings": 48, "marimba": 12, "lead": 73, "mbox": 10}
MUSIC = {
    "engine": "s2-score",
    "key": "D minor, resolving to D major",
    "bpm": 96,
    "sections": [
        msec({"shot": "hook"}, "lullaby", ["Dm", "Bb", "Gm", "A"], "D minor", programs=LULL_P),
        msec(RESET, "lullaby", ["F", "C", "Bb", "F"], "F major", bars=(0, 2), octave=1),
        msec(cue("L4", "run."), "drive", ["Dm", "Bb", "Gm", "A"], "D minor", intensity=0.85, programs=BACK_P),
        msec(cue("L6", "A", -0.2), "drop", ["Dm"], "D minor", beatsPerChord=8),
        msec(cue("L6", "textbook.", 0.55), "excavate", ["Dm", "C", "Bb", "A"], "D minor", layer=1, programs=EXC_P),
        msec(cue("L8", "One:", -0.1), "excavate", ["Dm", "C", "Bb", "C"], "D minor", layer=1),
        msec(cue("L9", "Two:", -0.1), "excavate", ["Dm", "C", "Bb", "C"], "D minor", layer=2),
        msec(cue("L10", "Three:", -0.1), "excavate", ["F", "C", "Dm", "Bb"], "F major", layer=3),
        msec(cue("L11", "Four:", -0.1), "excavate", ["F", "C", "Dm", "Bb"], "F major", layer=4),
        msec(cue("L12", "Run"), "drive", ["F", "C", "Bb", "F"], "F major", intensity=1.0, theme=True, programs=BACK_P),
        msec(cue("L13", "Rule", -0.05), "twist", ["A7b9"], "D minor"),
        msec(cue("L14", "A", -0.1), "lullaby", ["D", "G", "Bm", "A"], "D major", programs=LULL_P),
        msec(cue("L15", "So", -0.1), "anthem", ["D", "G", "Bm", "A"], "D major", programs=BACK_P),
        msec(cue("L17", "Would", -0.2), "outro", ["G", "D"], "D major"),
        msec(cue("L18", "Part", -0.1), "tease", ["A5"], "D minor", beatsPerChord=32),
    ],
    "accents": [
        {"kind": "hit", "at": cue("L1", "lying?"), "chord": "Dm"},
        {"kind": "boom", "at": cue("L6", "textbook."), "chord": "Dm"},
        {"kind": "riser", "at": cue("L7", "twist."), "chord": "A"},
        {"kind": "stab", "at": cue("L12", "arguing."), "chord": "F"},
        {"kind": "cymbal", "at": cue("L12", "arguing.")},
        {"kind": "boom", "at": shift(STAR, 0.9), "chord": "D"},
        {"kind": "hit", "at": cue("L15", "inside"), "chord": "D"},
        {"kind": "boom", "at": cue("L18", "older"), "chord": "A"},
        {"kind": "roll", "at": {"end": True, "offset": -0.05}, "chord": "A"},
    ],
    "fadeOut": {"fromEnd": 0.08},
    "gain": 0.55,
}

TAGS = "#Worldbuilding #FantasyWriting #WritingTips #Lore #WorldcraftShorts"
IG_HOOK = "Every child learns the gods made the world. What if they're lying?"
BODY = (
    "Every child learns the gods made the world. What if they're lying?\n\n"
    "Meet the First Lamp, the creation myth of the Lamplight faith: it fell from the sky, and the world began. The lazy "
    "version makes the myth simply true, and we ran it: five hundred years, nobody digs, nothing to find. A myth that's "
    "just true is a textbook.\n\n"
    "Wrong myths build better worlds. Bury proof: bones older than the gods. Give it a job: the Queen's crown rests on "
    "it. Let someone dig: the cliffs count ten thousand years. Let someone hide it: keepers paint over the holes. Run it "
    "again: five hundred years, and they're still arguing.\n\n"
    "Then the twist: the myth isn't lying. It's remembering. A star really fell here, and it made the lake. So hide the "
    "truth inside the myth.\n\n"
    "Myths aren't lies. Every myth is a memory, told wrong.\n\n"
    "Would you reveal the truth to a civilization built on a lie?\n\n"
    "Part 34 of 50. Follow for part 35: the ruins are older than us."
)
METADATA = {
    "youtube": {
        "title": "What If Your World's Creation Myth Is Wrong? (Worldbuilding)",
        "titleAlternate": "Every child learns the gods made the world. What if they're lying?",
        "description": BODY + "\n\nWorldcraft Shorts: Worldbuilding, from the ground up. Season 2, The World Engine: "
        "every idea gets tested on one living island. Arc 7: History and Mythology. The Lamplight faith, its creation "
        "myth and its gods are invented for this video; no real religion or creation story is depicted.\n\n" + TAGS,
        "pinnedComment": "Would you reveal the truth to a civilization built on a lie? Tell them, or keep the myth? One word, then your reason. (Part 35: the ruins are older than us.)",
        "uploadSettings": "Altered or synthetic content: Yes (synthetic narration and an AI-generated field-card sprite; the island, the painted sky, the bones and the people are drawn in code). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "Every child learns the gods made the world. What if they're lying? 🌌 Four rules for a creation myth that's wrong (in a useful way), and rule #5 is the twist. "
                   "Would you tell them the truth, or keep the myth? Part 34/50 · follow for part 35 🏛️ " + TAGS,
        "pinnedComment": "Would you reveal the truth to a civilization built on a lie? Tell them, or keep the myth?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nWorldcraft Shorts · Season 2: The World Engine.\n\n" + TAGS,
        "pinnedComment": "What real event is hiding inside your world's creation myth, told wrong?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": IG_HOOK + "\n\n" + BODY.split("\n\n", 1)[1] + "\n\nWorldcraft Shorts · Season 2\n\n" + TAGS,
        "hookCheck": f"First {len(IG_HOOK)} characters: '{IG_HOOK}'",
        "pinnedComment": "Save the TEAR THE SKY card, then tell us: would you reveal the truth to a civilization built on a lie?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}

if __name__ == "__main__":
    ep = build()
    (HERE / "episode.json").write_text(json.dumps(ep, indent=1))
    words = sum(len(t.split()) for _, _, t, _, _ in LINES)
    print(f"[make_ep34] wrote episode.json: {len(LINES)} lines, {words} words, {len(SHOTS)} shots, loop span {loop_span():.2f} s")
