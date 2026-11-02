"""Season 2 score + sound palette ("the World Engine"), synthesized from the episode's cues.

Used by pipeline/score.py only for episodes with "season": 2, so EP01–EP25 keep their exact audio.

Music: a light, rhythmic, chiptune-adjacent score on a continuous beat grid (so the groove never stumbles across
sections). Each section names its chords and which layers play: pad, arp (square plucks), bass, kick, hats, clap,
bells. The arc of every S2 episode: curious hook -> driving RUN -> drop-out on the failure -> layers stacking as
the fixes switch on -> full groove on the second run -> darker twist -> resolution -> soft outro that fades to
silence before the loop point.

SFX: one sound per World Engine event, reused every episode (see docs/STYLE_S2.md): sting, runPress, simTicks,
births, losses, stamp, rewind, ringOn, snowAir, sleepZ, cubPop, delete, restore, cardSlide, check, unlock,
worldRipple, stomp, crash.
"""
from __future__ import annotations

import numpy as np

from common import SR, resolve_cue
from score import RNG, bell, bp, env, events_gain, hp, hz, lp, pad_voice, place, reverb


def noise(n):
    return RNG.standard_normal(n)


def st(sig, width=0.0):
    if width:
        other = np.roll(sig, int(0.009 * SR))
        return np.stack([sig, sig * (1 - width) + other * width], axis=1)
    return np.stack([sig, sig], axis=1)


# ---------------------------------------------------------------- instruments

def square_pluck(freq, dur=0.32, bright=1.0, duty_harm=9):
    """Soft band-limited square pluck (odd harmonics, each decaying faster): 8-bit colour without the harshness."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for h in range(1, duty_harm * 2, 2):
        if freq * h > 11000:
            break
        sig += np.sin(2 * np.pi * freq * h * t) / h * np.exp(-t * (7 + h * 3.2 / max(bright, 0.2)))
    sig *= np.minimum(1, t / 0.002)
    return sig * 0.5


def tri_bass(freq, dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = (freq * t) % 1.0
    tri = 4 * np.abs(ph - 0.5) - 1
    sig = (tri * 0.7 + np.sin(2 * np.pi * freq * t) * 0.6) * np.exp(-t * 3.2) * np.minimum(1, t / 0.004)
    return sig


def kick(dur=0.45):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 52 * (1 + 2.2 * np.exp(-t * 32))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    click = hp(noise(n), 2000) * np.exp(-t * 300) * 0.25
    return body + click


def hat(dur=0.05, open_=False):
    n = int((0.16 if open_ else dur) * SR)
    t = np.arange(n) / SR
    return hp(noise(n), 7000) * np.exp(-t * (28 if open_ else 110)) * 0.35


def clap(dur=0.22):
    n = int(dur * SR)
    t = np.arange(n) / SR
    burst = sum(np.exp(-np.clip(t - d, 0, None) * 60) * (t >= d) for d in (0.0, 0.012, 0.024))
    return bp(noise(n), 900, 4200) * burst * 0.45


ARP_PATTERNS = {
    8: [0, 1, 2, 1, 0, 2, 1, 2],
    16: [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 3, 1, 2, 0, 2],
}


def build_music_s2(ep, timing):
    """Music for a Season 2 episode from ep["music"]: {bpm, sections: [{from, chords, beatsPerChord, level, layers}], fadeOut}."""
    spec = ep["music"]
    total = timing["duration"]
    n = int(total * SR)
    pads = np.zeros((n, 2))
    rhythm = np.zeros((n, 2))
    beat = 60.0 / spec.get("bpm", 100)
    secs = sorted(({**s, "t0": resolve_cue(s["from"], timing)} for s in spec["sections"]), key=lambda s: s["t0"])
    for i, s in enumerate(secs):
        s["t1"] = secs[i + 1]["t0"] if i + 1 < len(secs) else total
    for s in secs:
        L = s.get("layers", {})
        lvl = s.get("level", 0.5)
        chords = s["chords"]
        bpc = s.get("beatsPerChord", 4)
        # chord spans on the global beat grid
        k0 = int(np.ceil(s["t0"] / beat - 1e-6))
        k1 = int(np.floor((s["t1"] - 1e-6) / beat))
        # pads: one block per chord span (start at the section start even off-grid)
        ci = 0
        tc = s["t0"]
        while tc < s["t1"] - 0.05:
            nxt = (np.floor(tc / beat + 1e-6) + bpc) * beat if tc > s["t0"] or s["t0"] % beat < 1e-3 else (k0 + bpc) * beat
            nxt = min(nxt, s["t1"])
            chord = chords[ci % len(chords)]
            if L.get("pad", 0) > 0:
                m = int((nxt - tc + 1.0) * SR)
                block = sum(pad_voice(hz(note), m, bright=4.0 if s.get("dark") else 7.0) for note in chord)
                block *= env(m, 0.35, 0.9)[:, None] * L["pad"] * lvl / len(chord) * 2.0
                place(pads, block, tc - 0.08)
            if L.get("bells"):
                for bi, note in enumerate(chord[-2:]):
                    place(pads, bell(hz(note) * 2, 2.4), tc + 0.05 + bi * beat * 0.5, 0.16 * lvl * L["bells"])
            ci += 1
            tc = nxt
        # rhythm on the beat grid
        for k in range(k0, k1 + 1):
            tb = k * beat
            if tb < s["t0"] - 1e-6 or tb >= s["t1"]:
                continue
            bi = k - k0
            chord = chords[(bi // bpc) % len(chords)]
            root = hz(chord[0])
            pos = k % 4
            kd = L.get("kick")
            if kd == "four" or (kd == "half" and pos in (0, 2)) or (kd == "one" and pos == 0):
                place(rhythm, st(kick()), tb, 0.55 * lvl)
            if kd == "heart" and pos == 0:
                place(rhythm, st(kick()), tb, 0.45 * lvl)
                place(rhythm, st(kick()), tb + 0.18, 0.28 * lvl)
            if L.get("clap") and pos in (1, 3):
                place(rhythm, st(clap(), 0.3), tb, 0.38 * lvl * L["clap"])
            if L.get("bass"):
                for sub in ((0, 0.5) if L.get("bassEighths") else (0,)):
                    place(rhythm, st(tri_bass(root / 2 if root > 90 else root, beat * 0.9)), tb + sub * beat, 0.42 * lvl * L["bass"])
            hats = L.get("hats")
            if hats:
                steps = 4 if hats == 16 else 2
                for j in range(steps):
                    if hats == 8 and j == 0:
                        continue
                    place(rhythm, st(hat(), 0.5), tb + j * beat / steps, (0.18 if j % 2 else 0.1) * lvl)
            arp = L.get("arp")
            if arp:
                rate = L.get("arpRate", 8)
                pat = ARP_PATTERNS[rate]
                steps = rate // 4
                tones = [hz(x) for x in chord[1:]] + [hz(chord[1]) * 2]
                for j in range(steps):
                    idx = pat[(bi * steps + j) % len(pat)] % len(tones)
                    f = tones[idx] * (2 if L.get("arpHigh", True) else 1)
                    acc = 1.0 if j == 0 else 0.7
                    place(rhythm, st(square_pluck(f, beat / steps * 1.6, bright=s.get("bright", 1.0)), 0.4), tb + j * beat / steps, 0.2 * lvl * arp * acc)
    music = reverb(pads, seconds=2.8, decay=3.2, wet=0.4) + reverb(rhythm, seconds=1.2, decay=6.0, wet=0.16)
    # optional low drone (dark sections)
    for d in spec.get("drones", []):
        a, b = resolve_cue(d["from"], timing), resolve_cue(d["to"], timing)
        m = int((b - a) * SR)
        t = np.arange(m) / SR
        sig = sum(np.sin(2 * np.pi * hz(note) * t) for note in d["notes"]) * 0.12 * d.get("level", 1.0)
        place(music, st(sig * env(m, 1.0, 1.2)), a)
    music *= events_gain(spec.get("events", []), timing, n)[:, None]
    # Fade to silence before the loop point.
    fo = resolve_cue(spec["fadeOut"]["at"], timing) if spec.get("fadeOut") else total - 2.0
    i0 = int(fo * SR)
    i1 = min(n, int((fo + spec.get("fadeOut", {}).get("dur", 1.6)) * SR))
    if i0 < n:
        music[i0:i1] *= np.linspace(1, 0, i1 - i0)[:, None] ** 2
        music[i1:] = 0
    return music


# ---------------------------------------------------------------- the World Engine sound palette

def blip(f0, f1, dur, bright=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = np.geomspace(f0, f1, n)
    ph = np.cumsum(f) / SR
    sig = sum(np.sin(2 * np.pi * h * ph) / h for h in (1, 3, 5) if f1 * h < 12000) * np.exp(-t * (5 / dur)) * np.minimum(1, t / 0.002)
    return sig * bright


S2_HITS = {"roar", "stompHit", "sting", "runPress", "stamp", "rewind", "ringOn", "snowAir", "sleepZ", "cubPop", "delete", "restore", "cardSlide", "check", "unlock", "worldRipple", "crash", "boomPop"}
S2_BEDS = {"simTicks", "births", "losses", "stomp"}


def s2_hit(kind):
    if kind == "roar":
        # The Grimmaw's display call: a low, rough growl (saw with vibrato through two moving formants) that swells and
        # drops away. A call, not an attack.
        n = int(1.4 * SR)
        t = np.arange(n) / SR
        f = 78 * (1 + 0.18 * np.interp(t, [0, 0.3, 0.9, 1.4], [0, 1, 0.7, -0.2])) * (1 + 0.025 * np.sin(2 * np.pi * 7.5 * t))
        ph = np.cumsum(f) / SR
        saw = 2 * (ph % 1) - 1
        rough = saw * (1 + 0.35 * lp(noise(n), 60, 1) * 8)
        body = bp(rough, 120, 900) * 1.2 + bp(rough, 900, 2400) * np.interp(t, [0, 0.35, 1.0, 1.4], [0.1, 0.6, 0.3, 0])
        breath = bp(noise(n), 300, 3000) * 0.25
        shape = np.interp(t, [0, 0.18, 0.95, 1.4], [0, 1, 0.7, 0])
        return st((body + breath) * shape, 0.5)
    if kind == "stompHit":
        n = int(1.0 * SR)
        t = np.arange(n) / SR
        thud = np.sin(2 * np.pi * np.cumsum(46 * (1 + 0.9 * np.exp(-t * 26))) / SR) * np.exp(-t * 8)
        grit = bp(noise(n), 200, 2500) * np.exp(-t * 14) * 0.5
        return st(thud + grit, 0.4)
    if kind == "sting":
        # Series sting: a rising four-note square arpeggio (D5 F#5 A5 D6) over a soft low "power-on" swell + sparkle.
        out = np.zeros(int(1.5 * SR))
        for i, f in enumerate((587.3, 740.0, 880.0, 1174.7)):
            c = square_pluck(f, 0.5, 1.2)
            i0 = int(i * 0.085 * SR)
            out[i0:i0 + len(c)] += c[: len(out) - i0] * (0.8 + i * 0.1)
        n = len(out)
        t = np.arange(n) / SR
        swell = np.sin(2 * np.pi * np.cumsum(np.geomspace(70, 140, n)) / SR) * np.interp(t, [0, 0.25, 0.6, 1.4], [0, 0.6, 0.3, 0])
        spark = hp(noise(n), 6000) * np.interp(t, [0, 0.3, 0.5, 1.2], [0, 0.0, 0.12, 0])
        return st(out + swell * 0.5 + spark, 0.5)
    if kind == "runPress":
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        click = bp(noise(n), 1500, 6000) * np.exp(-t * 400) * 0.8
        rise = np.zeros(n)
        b = blip(330, 1320, 0.32)
        rise[int(0.03 * SR):int(0.03 * SR) + len(b)] += b
        whoosh = bp(noise(n), 800, 5000) * np.interp(t, [0, 0.1, 0.35, 0.9], [0, 0.25, 0.15, 0])
        return st(click + rise * 0.7 + whoosh, 0.6)
    if kind == "stamp":
        n = int(1.0 * SR)
        t = np.arange(n) / SR
        thud = np.sin(2 * np.pi * np.cumsum(60 * (1 + np.exp(-t * 25))) / SR) * np.exp(-t * 7)
        crush = np.round(bp(noise(n), 200, 3000) * 6) / 6 * np.exp(-t * 18) * 0.6
        return st(thud + crush, 0.3)
    if kind == "rewind":
        n = int(1.0 * SR)
        t = np.arange(n) / SR
        f = 1400 * np.exp(-t * 2.2) * (1 + 0.04 * np.sin(2 * np.pi * 14 * t))
        warble = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.12 * np.interp(t, [0, 0.1, 0.8, 1.0], [0, 1, 0.7, 0])
        sweep = bp(noise(n), 600, 6000) * np.interp(t, [0, 0.7, 0.95, 1.0], [0.05, 0.4, 0.5, 0])
        return st(lp(warble, 4000) + sweep * 0.6, 0.7)
    if kind == "ringOn":
        n = int(1.6 * SR)
        t = np.arange(n) / SR
        chord = sum(square_pluck(f, 1.6, 0.8) for f in (587.3, 740.0, 880.0))
        shimmer = sum(np.sin(2 * np.pi * f * t) for f in (1760, 2217)) * np.interp(t, [0, 0.5, 1.6], [0, 0.08, 0]) * (1 + np.sin(2 * np.pi * 9 * t)) / 2
        return st(chord * 0.6 + shimmer, 0.7)
    if kind == "snowAir":
        n = int(2.2 * SR)
        t = np.arange(n) / SR
        air = hp(noise(n), 3000) * np.interp(t, [0, 0.9, 2.2], [0, 0.25, 0])
        tinkle = np.zeros(n)
        for g in RNG.uniform(0.2, 1.9, 14):
            c = np.sin(2 * np.pi * RNG.choice([2349, 2637, 3136]) * np.arange(int(0.3 * SR)) / SR) * np.exp(-np.arange(int(0.3 * SR)) / SR * 14) * 0.08
            i = int(g * SR)
            tinkle[i:i + len(c)] += c[: n - i]
        return st(air + tinkle, 0.8)
    if kind == "sleepZ":
        n = int(1.0 * SR)
        out = np.zeros(n)
        for i, f in enumerate((220, 196)):
            b = blip(f * 1.02, f, 0.28, 0.8)
            j = int(i * 0.34 * SR)
            out[j:j + len(b)] += b
        return st(lp(out, 2500), 0.3)
    if kind == "cubPop":
        n = int(0.6 * SR)
        out = np.zeros(n)
        for i, (a, b2) in enumerate(((900, 1400), (1200, 1900))):
            b = blip(a, b2, 0.12)
            j = int(i * 0.1 * SR)
            out[j:j + len(b)] += b
        return st(out, 0.4)
    if kind == "delete":
        # 8-bit deletion: a square that jumps between random pitches, crushed, then a falling zap.
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        steps = RNG.choice([1046, 1568, 523, 2093, 784, 392], size=20)
        f = steps[np.minimum(19, (t / 0.025).astype(int))] * np.where(t > 0.5, np.exp(-(t - 0.5) * 6), 1)
        sq = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.22 * np.interp(t, [0, 0.02, 0.7, 0.9], [0, 1, 0.6, 0])
        crush = np.round(hp(noise(n), 1500) * 3) / 3 * np.exp(-t * 6) * 0.15
        return st(lp(sq, 6000) + crush, 0.5)
    if kind == "restore":
        n = int(1.4 * SR)
        out = np.zeros(n)
        for i, f in enumerate((293.7, 370.0, 440.0, 587.3, 740.0, 880.0)):
            c = square_pluck(f * 2, 0.6, 1.1)
            j = int(i * 0.07 * SR)
            out[j:j + len(c)] += c[: n - j] * 0.6
        t = np.arange(n) / SR
        pad = sum(np.sin(2 * np.pi * f * t) for f in (293.7, 440, 587.3)) * np.interp(t, [0, 0.4, 1.4], [0, 0.12, 0])
        return st(out + pad, 0.6)
    if kind == "cardSlide":
        n = int(0.45 * SR)
        t = np.arange(n) / SR
        out = bp(noise(n), 1200, 6000) * np.interp(t, [0, 0.12, 0.45], [0, 0.35, 0])
        b = blip(500, 760, 0.1) * 0.3
        out[: len(b)] += b
        return st(out, 0.6)
    if kind == "check":
        n = int(0.4 * SR)
        out = np.zeros(n)
        for i, f in enumerate((1046.5, 1568.0)):
            b = blip(f, f, 0.14)
            j = int(i * 0.07 * SR)
            out[j:j + len(b)] += b * 0.6
        return st(out, 0.3)
    if kind == "unlock":
        n = int(1.0 * SR)
        out = np.zeros(n)
        for i, f in enumerate((784.0, 987.8, 1174.7, 1568.0)):
            c = square_pluck(f, 0.5, 1.2)
            j = int(i * 0.09 * SR)
            out[j:j + len(c)] += c[: n - j] * 0.8
        return st(out, 0.5)
    if kind == "worldRipple":
        n = int(1.2 * SR)
        t = np.arange(n) / SR
        whomp = np.sin(2 * np.pi * np.cumsum(np.geomspace(90, 45, n)) / SR) * np.exp(-t * 4) * 0.8
        rise = bp(noise(n), 2000, 8000) * np.interp(t, [0, 0.4, 1.2], [0, 0.12, 0])
        return st(whomp + rise, 0.6)
    if kind == "crash":
        n = int(1.4 * SR)
        t = np.arange(n) / SR
        glide = np.sign(np.sin(2 * np.pi * np.cumsum(np.geomspace(880, 110, n)) / SR)) * 0.12 * np.exp(-t * 1.4)
        thud = np.sin(2 * np.pi * 55 * t) * np.exp(-np.clip(t - 1.0, 0, None) * 8) * (t >= 1.0) * 0.8
        return st(lp(glide, 3500) + thud, 0.4)
    if kind == "boomPop":
        n = int(1.2 * SR)
        out = np.zeros(n)
        for g in np.sort(RNG.uniform(0, 1.0, 40)):
            b = blip(RNG.uniform(700, 1100), RNG.uniform(1300, 2000), 0.06, 0.5)
            i = int(g * SR)
            out[i:i + len(b)] += b[: n - i]
        return st(out, 0.8)
    raise KeyError(kind)


def s2_bed(kind, dur):
    n = int(dur * SR)
    out = np.zeros(n)
    if kind == "simTicks":
        # a soft tick every 0.12 s while the simulation fast-forwards
        k = 0
        while k * 0.12 < dur - 0.1:
            b = blip(1700 + (k % 4) * 90, 1700 + (k % 4) * 90, 0.03, 0.35)
            i = int(k * 0.12 * SR)
            out[i:i + len(b)] += b[: n - i]
            k += 1
    elif kind in ("births", "losses"):
        rate = 9 if kind == "births" else 6
        for g in np.sort(RNG.uniform(0, max(0.1, dur - 0.15), int(rate * dur))):
            b = blip(800, 1500, 0.07, 0.4) if kind == "births" else blip(900, 420, 0.1, 0.3)
            i = int(g * SR)
            out[i:i + len(b)] += b[: n - i]
    elif kind == "stomp":
        k = 0
        while k * 0.5 < dur - 0.2:
            m = int(0.4 * SR)
            t = np.arange(m) / SR
            thud = np.sin(2 * np.pi * np.cumsum(48 * (1 + 0.8 * np.exp(-t * 30))) / SR) * np.exp(-t * 11) + lp(noise(m), 300) * np.exp(-t * 30) * 0.4
            i = int(k * 0.5 * SR)
            out[i:i + m] += thud[: n - i] * (0.8 + 0.2 * (k % 2))
            k += 1
    else:
        raise KeyError(kind)
    return st(out, 0.5)
