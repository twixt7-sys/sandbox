"""Original score + sound design, synthesized from the episode's cues (no licensed samples).

Usage: python pipeline/score.py ep01
Reads public/<ep>/timing.json, writes public/<ep>/music.wav and public/<ep>/sfx.wav (48 kHz stereo).
Swap in licensed stems later by dropping music.wav / sfx.wav in place and skipping this step.
"""
from __future__ import annotations

import json
import sys

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt
import soundfile as sf

from common import SR, load_episode, out_dir, resolve_cue

RNG = np.random.default_rng(7)
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6,
        "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


def hz(name: str) -> float:
    pitch, octave = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((NOTE[pitch] + 12 * (octave + 1) - 69) / 12)


def db(x: float) -> float:
    return 10 ** (x / 20)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def env(n, attack, release, total=None):
    """Linear-attack / exponential-release envelope of n samples."""
    t = np.arange(n) / SR
    total = total or n / SR
    e = np.minimum(1.0, t / max(attack, 1e-3))
    tail = np.clip((t - (total - release)) / max(release, 1e-3), 0, 1)
    return e * (1 - tail) ** 2


def reverb(x, seconds=3.2, decay=3.5, wet=0.35):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = RNG.standard_normal((n, 2)) * np.exp(-decay * t)[:, None]
    ir[:, 0], ir[:, 1] = lp(ir[:, 0], 5000), lp(ir[:, 1], 4200)
    ir /= np.sqrt((ir ** 2).sum(axis=0))
    out = np.stack([fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], axis=1)
    return (1 - wet) * x + wet * out


def pad_voice(freq, n, bright=10.0, detune_cents=7):
    """Soft additive 'string pad': three detuned voices, harmonics rolled off like a low-pass."""
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for k, cents in enumerate((-detune_cents, 0, detune_cents)):
        f = freq * 2 ** (cents / 1200)
        sig = np.zeros(n)
        for h in range(1, 16):
            if f * h > 9000:
                break
            sig += np.sin(2 * np.pi * f * h * t + RNG.uniform(0, 6.28)) * (1 / h) * np.exp(-h / bright)
        pan = (k - 1) * 0.6
        out[:, 0] += sig * (1 - pan) / 2
        out[:, 1] += sig * (1 + pan) / 2
    return out / 3


def bell(freq, dur=3.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    partials = [(1.0, 1.0, 1.2), (2.76, 0.5, 2.5), (5.4, 0.25, 4.0), (8.93, 0.12, 6.0)]
    sig = sum(a * np.sin(2 * np.pi * freq * r * t) * np.exp(-d * t) for r, a, d in partials)
    sig *= np.minimum(1, t / 0.004)
    return np.stack([sig, sig], axis=1) * 0.25


def pluck(freq, dur=1.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = sum(np.sin(2 * np.pi * freq * h * t) * np.exp(-t * (2.5 + h * 1.8)) / h for h in range(1, 7))
    sig *= np.minimum(1, t / 0.003)
    return np.stack([sig, sig], axis=1) * 0.3


def drum(dur=1.6, f0=70):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f0 * (1 + 1.2 * np.exp(-t * 18))
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.2)
    skin = lp(RNG.standard_normal(n), 900) * np.exp(-t * 30) * 0.3
    sig = body + skin
    return np.stack([sig, sig], axis=1) * 0.8


def place(buf, clip, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(clip))
    buf[max(i, 0):j] += clip[max(0, -i): j - i] * gain


# ---------------------------------------------------------------- music

def events_gain(events, timing, n):
    """Per-sample music gain from `music.events` cues.

    {"type": "duck", "at": cue, "pre": 0.3, "dur": 1.5, "gain": 0.35}: dip to `gain` from `pre` s before the cue,
    hold, and recover over the last 0.6 s of `dur` (e.g. let a silence or a sound-design hit land).
    """
    g = np.ones(n)
    for ev in events:
        if ev.get("type", "duck") != "duck":
            raise KeyError(f"unknown music event {ev['type']!r}")
        at = resolve_cue(ev["at"], timing)
        a = max(0, int((at - ev.get("pre", 0.3)) * SR))
        b = min(n, int((at + ev.get("dur", 1.5) - ev.get("pre", 0.3)) * SR))
        if b - a < int(0.9 * SR):
            continue
        depth = ev.get("gain", 0.35)
        g[a:b] = np.minimum(g[a:b], np.interp(np.arange(a, b), [a, a + 0.3 * SR, b - 0.6 * SR, b], [1, depth, depth, 1]))
    return g


def build_music(ep, timing):
    total = timing["duration"]
    n = int(total * SR)
    music = np.zeros((n, 2))
    sections = ep["music"]["sections"]
    for shot in timing["shots"]:
        sec = sections.get(shot["id"])
        if not sec:
            continue
        s0, s1 = shot["start"], shot["end"]
        chords = sec["chords"]
        span = (s1 - s0) / len(chords)
        for ci, chord in enumerate(chords):
            c0 = s0 + ci * span
            dur = span + 1.2  # overlap into the next chord / section
            m = int(dur * SR)
            block = np.zeros((m, 2))
            for note in chord:
                block += pad_voice(hz(note), m, bright=4.0 if sec.get("dark") else 8.0)
            block *= env(m, 0.9 if ci == 0 else 0.5, 1.4)[:, None] * sec["level"] / len(chord) * 2.2
            place(music, block, c0 - 0.25)
            if sec.get("arp"):
                pent = [hz(x) for x in chord[1:]] + [hz(chord[1]) * 2]
                step = 60 / sec["pulse"] / 2
                k = 0
                while c0 + k * step < c0 + span:
                    place(music, pluck(pent[(k * 3) % len(pent)] * 2), c0 + k * step, 0.18 * (0.6 + 0.4 * (k % 2 == 0)))
                    k += 1
            if sec.get("bells"):
                for bi, note in enumerate(chord[-3:]):
                    place(music, bell(hz(note) * 2), c0 + 0.35 + bi * 0.55, 0.22)
        if sec.get("pulse"):
            beat = 60 / sec["pulse"]
            k = 0
            while s0 + k * beat < s1 - 0.2:
                place(music, drum(f0=55), s0 + k * beat, 0.32 if k % 2 == 0 else 0.18)
                k += 1

    # Sub drone under everything except the final second (so the loop point is clean).
    t = np.arange(n) / SR
    root, fifth = ep["music"].get("drone", ["D1", "A1"])
    drone = np.sin(2 * np.pi * hz(root) * t) * 0.10 + np.sin(2 * np.pi * hz(fifth) * t) * 0.05
    music += np.stack([drone, drone], axis=1) * env(n, 2.0, 2.0)[:, None]

    music = reverb(music, wet=0.42)
    music *= events_gain(ep["music"].get("events", []), timing, n)[:, None]

    # Fade out fully before the end so the loop restarts from silence.
    fade = int(1.8 * SR)
    music[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    return music


# ---------------------------------------------------------------- sfx

def noise(n):
    return RNG.standard_normal(n)


def pink(n):
    w = noise(n)
    return lp(w, 800, 1) * 2 + lp(w, 4000, 1) * 0.5 + w * 0.05


def stereo(sig, width=0.0):
    if width:
        other = np.roll(sig, int(0.011 * SR))
        return np.stack([sig, sig * (1 - width) + other * width], axis=1)
    return np.stack([sig, sig], axis=1)


def sfx_bed(kind, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    if kind == "clock":
        # Steady escapement tick-tock, one per half second (a predictable rhythm, not a countdown).
        sig = np.zeros(n)
        m = int(0.025 * SR)
        for k, t0 in enumerate(np.arange(0.05, dur - 0.1, 0.5)):
            i = int(t0 * SR)
            click = bp(noise(m), 1800 if k % 2 else 2600, 6500) * np.exp(-np.arange(m) / SR * 260)
            sig[i:i + m] += click[: len(sig[i:i + m])]
        return stereo(sig / (np.abs(sig).max() + 1e-9), 0.2) * env(n, 0.02, 0.3)[:, None]
    if kind == "cave":
        # Cavern room tone: low rumble, slow airflow, sparse water drips with a long tail.
        sig = lp(pink(n), 260, 2) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.07 * t)) * 1.4
        sig += bp(noise(n), 400, 1200) * 0.08 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.13 * t + 2))
        for d in RNG.uniform(0.3, max(0.4, dur - 0.5), max(1, int(dur / 1.3))):
            i = int(d * SR)
            m = int(0.35 * SR)
            tt = np.arange(m) / SR
            f = RNG.uniform(1100, 1900) * (1 + 0.6 * np.exp(-tt * 40))
            drip = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 18) * 0.35
            sig[i:i + m] += drip[: len(sig[i:i + m])]
    elif kind == "market":
        # Restrained market activity: an unintelligible murmur (formant-filtered noise bursts) + wood and pottery knocks.
        murmur = np.zeros(n)
        for lo, hi, rate in ((300, 900, 3.1), (500, 1500, 4.3), (250, 700, 2.4)):
            syll = np.clip(lp(noise(n), rate, 1) * 9, 0, 1) ** 1.5
            murmur += bp(noise(n), lo, hi) * syll
        sig = murmur * 0.8 + lp(pink(n), 400) * 0.25
        for d in RNG.uniform(0.2, max(0.3, dur - 0.4), max(2, int(dur * 1.6))):
            i = int(d * SR)
            m = int(0.12 * SR)
            tt = np.arange(m) / SR
            knock = np.sin(2 * np.pi * RNG.uniform(180, 520) * tt) * np.exp(-tt * 45) * RNG.uniform(0.2, 0.5)
            sig[i:i + m] += knock[: len(sig[i:i + m])]
    elif kind == "hum":
        # Enchanted machinery: mains-like hum with harmonics, slow wobble, and irregular gear clanks.
        wob = 1 + 0.01 * np.sin(2 * np.pi * 0.3 * t)
        sig = sum(a * np.sin(2 * np.pi * 55 * k * np.cumsum(wob) / SR) for k, a in ((1, 1.0), (2, 0.6), (3, 0.35), (5, 0.15)))
        sig = sig * 0.5 + bp(noise(n), 900, 3000) * 0.05
        for d in np.arange(0.4, max(0.5, dur - 0.3), 0.9):
            i = int((d + RNG.uniform(-0.15, 0.15)) * SR)
            m = int(0.09 * SR)
            tt = np.arange(m) / SR
            clank = sum(np.sin(2 * np.pi * f * tt) for f in (620, 1130, 1810)) * np.exp(-tt * 40) * 0.25
            sig[max(0, i):i + m] += clank[: len(sig[max(0, i):i + m])]
    elif kind == "room":
        # Large stone room tone: low filtered air with a slow swell, very little detail.
        sig = lp(pink(n), 500, 2) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.09 * t)) + bp(noise(n), 2000, 5000) * 0.02
    elif kind == "rain":
        # Steady rain: soft broadband hiss with slow gusts, plus sparse close drops on stone and wood.
        # Opens as "first rain" (sparse drops) and fills in over the first ~3 s.
        build = np.clip(t / 3.0, 0.15, 1.0)
        hiss = bp(pink(n), 900, 7000) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.08 * t + 0.7)) * build
        sig = hiss * 0.5 + lp(pink(n), 300) * 0.15 * build
        for d in np.sort(RNG.uniform(0.05, max(0.1, dur - 0.1), int(dur * 9))):
            i = int(d * SR)
            m = int(0.04 * SR)
            tt = np.arange(m) / SR
            tap = bp(noise(m), RNG.uniform(1800, 4200), 9000) * np.exp(-tt * RNG.uniform(140, 260)) * RNG.uniform(0.15, 0.6)
            sig[i:i + m] += tap[: len(sig[i:i + m])]
    elif kind == "footsteps":
        # Unhurried footsteps on wet stone: a soft heel thud plus a short wet slap, ~1.8 steps a second.
        sig = np.zeros(n)
        for k, d in enumerate(np.arange(0.1, max(0.2, dur - 0.2), 0.56)):
            i = int((d + RNG.uniform(-0.03, 0.03)) * SR)
            m = int(0.16 * SR)
            tt = np.arange(m) / SR
            heel = lp(noise(m), 260) * np.exp(-tt * 38) * 1.4
            slap = bp(noise(m), 1200, 5000) * np.exp(-np.maximum(0, tt - 0.025) * 70) * (tt > 0.02) * 0.5
            step = (heel + slap) * (0.8 if k % 2 else 1.0)
            sig[i:i + m] += step[: len(sig[i:i + m])]
        sig = sig / (np.abs(sig).max() + 1e-9)
        return stereo(sig, 0.3) * env(n, 0.05, 0.3)[:, None]
    elif kind == "blizzard":
        # High-altitude blizzard: wind roar with whistling gusts and a fine icy hiss (EP06 snow).
        gust = (0.55 + 0.45 * np.sin(2 * np.pi * 0.17 * t + 0.4)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.53 * t))
        roar = bp(pink(n), 120, 900) * gust
        whistle = bp(noise(n), 700, 1100) * gust ** 3 * 0.5
        hiss = bp(noise(n), 4000, 11000) * gust * 0.12
        sig = roar + whistle + hiss
    elif kind == "caravan":
        # Pack animals on a stone road: slow hoof clops, small harness bells, creaking cart wood.
        sig = lp(pink(n), 400) * 0.08
        for d in np.arange(0.1, max(0.2, dur - 0.2), 0.42):
            i = int((d + RNG.uniform(-0.05, 0.05)) * SR)
            m = int(0.09 * SR)
            tt = np.arange(m) / SR
            clop = bp(noise(m), 400, 2500) * np.exp(-tt * 55) * RNG.uniform(0.4, 0.8)
            sig[i:i + m] += clop[: len(sig[i:i + m])]
        for d in RNG.uniform(0.2, max(0.3, dur - 0.5), max(2, int(dur * 1.6))):
            i = int(d * SR)
            m = int(0.8 * SR)
            tt = np.arange(m) / SR
            f = RNG.choice([1760.0, 2093.0, 2349.0])
            ting = (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tt)) * np.exp(-tt * 7) * 0.12
            sig[i:i + m] += ting[: len(sig[i:i + m])]
        for d in RNG.uniform(0.3, max(0.4, dur - 0.6), max(1, int(dur / 1.5))):
            i = int(d * SR)
            m = int(0.35 * SR)
            tt = np.arange(m) / SR
            creak = np.sin(2 * np.pi * np.cumsum(220 + 60 * np.sin(2 * np.pi * 9 * tt)) / SR) * bp(noise(m), 200, 1200) * np.interp(tt, [0, 0.1, 0.35], [0, 1, 0]) * 0.5
            sig[i:i + m] += creak[: len(sig[i:i + m])]
    elif kind == "hearth":
        # Winter hearth (EP09): a low fire roar with irregular wood crackles and pops, under faint outside wind.
        sig = lp(pink(n), 300, 2) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.21 * t)) * 0.9
        sig += bp(pink(n), 200, 900) * 0.25
        for d in np.sort(RNG.uniform(0.05, max(0.1, dur - 0.1), int(dur * 7))):
            i = int(d * SR)
            m = int(0.03 * SR)
            tt = np.arange(m) / SR
            pop = bp(noise(m), RNG.uniform(1500, 3500), 9000) * np.exp(-tt * RNG.uniform(150, 400)) * RNG.uniform(0.3, 1.0)
            sig[i:i + m] += pop[: len(sig[i:i + m])]
    elif kind == "procession":
        # Spring procession (EP09): slow round hide drums two to a bar, crunching steps on snow, distant bells.
        sig = lp(pink(n), 500) * 0.06
        for k, d in enumerate(np.arange(0.1, max(0.2, dur - 0.2), 0.43)):
            i = int((d + RNG.uniform(-0.02, 0.02)) * SR)
            m = int(0.5 * SR)
            tt = np.arange(m) / SR
            f0 = 82 if k % 2 == 0 else 98
            boom = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.5 * np.exp(-tt * 25))) / SR) * np.exp(-tt * 7) * (1.0 if k % 2 == 0 else 0.6)
            skin = bp(noise(m), 300, 1500) * np.exp(-tt * 45) * 0.3
            sig[i:i + m] += (boom + skin)[: len(sig[i:i + m])]
        for d in np.arange(0.3, max(0.4, dur - 0.2), 0.62):
            i = int((d + RNG.uniform(-0.05, 0.05)) * SR)
            m = int(0.12 * SR)
            tt = np.arange(m) / SR
            crunch = bp(noise(m), 1500, 6000) * np.exp(-tt * 30) * 0.18
            sig[i:i + m] += crunch[: len(sig[i:i + m])]
        for d in RNG.uniform(0.3, max(0.4, dur - 0.6), max(2, int(dur * 1.2))):
            i = int(d * SR)
            m = int(0.9 * SR)
            tt = np.arange(m) / SR
            f = RNG.choice([1568.0, 1760.0, 2349.0])
            ting = (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tt)) * np.exp(-tt * 6) * 0.08
            sig[i:i + m] += ting[: len(sig[i:i + m])]
    elif kind == "wind":
        sig = bp(pink(n), 180, 1400) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t + 1.3)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.37 * t))
    else:  # water
        burble = bp(noise(n), 500, 2600) * (0.5 + 0.5 * np.abs(lp(noise(n), 6, 1)) * 8).clip(0, 1.4)
        lap = lp(noise(n), 220) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.6 * t))
        sig = burble * 0.6 + lap * 1.5
    sig = sig / (np.abs(sig).max() + 1e-9)
    return stereo(sig, 0.7) * env(n, 0.8, 0.9)[:, None]


def sfx_hit(kind, dur=None):
    if kind == "ticks":
        return None
    if kind == "swell":
        n = int(2.6 * SR)
        t = np.arange(n) / SR
        rise = np.minimum(1, t / 1.0) ** 3 * np.exp(-np.maximum(0, t - 1.0) * 2.0)
        sig = bp(noise(n), 300, 3000) * rise * 0.5 + np.sin(2 * np.pi * 38 * t) * rise
        return stereo(sig, 0.5)
    if kind == "impact":
        n = int(2.4 * SR)
        t = np.arange(n) / SR
        sig = np.sin(2 * np.pi * np.cumsum(42 * (1 + 0.8 * np.exp(-t * 12))) / SR) * np.exp(-t * 2.2)
        sig += lp(noise(n), 1200) * np.exp(-t * 9) * 0.7
        return stereo(sig, 0.4)
    if kind == "rumble":
        n = int(2.8 * SR)
        t = np.arange(n) / SR
        sig = lp(noise(n), 160, 4) * 3 * env(n, 0.15, 1.6)
        grains = np.zeros(n)
        for g in RNG.uniform(0.1, 1.6, 14):
            i = int(g * SR)
            m = int(0.06 * SR)
            grains[i:i + m] += bp(noise(m), 600, 3000) * np.exp(-np.arange(m) / SR * 60) * RNG.uniform(0.2, 0.6)
        return stereo(sig + grains, 0.6)
    if kind == "whoosh":
        n = int(1.2 * SR)
        t = np.arange(n) / SR
        shape = np.sin(np.pi * np.clip(t / 1.1, 0, 1)) ** 2
        sig = sum(bp(noise(n), lo, lo * 2.2) * np.interp(t, [0, 0.55, 1.1], [0, 1, 0]) for lo in (250, 600, 1400))
        return stereo(sig * shape, 0.8)
    if kind == "paper":
        n = int(0.7 * SR)
        sig = hp(noise(n), 2000) * (np.abs(lp(noise(n), 30, 1)) * 12).clip(0, 1) * env(n, 0.02, 0.4)
        return stereo(sig, 0.5)
    if kind == "ink":
        n = int(1.0 * SR)
        t = np.arange(n) / SR
        sig = bp(noise(n), 1500, 6000) * np.interp(t, [0, 0.15, 1.0], [0, 1, 0]) * 0.6
        return stereo(sig, 0.7)
    if kind == "coin":
        n = int(1.8 * SR)
        t = np.arange(n) / SR
        sig = sum(a * np.sin(2 * np.pi * 2350 * r * t) * np.exp(-t * d) for r, a, d in [(1, 1, 4), (1.47, 0.6, 6), (2.13, 0.4, 9), (2.87, 0.25, 12)])
        sig *= np.minimum(1, t / 0.002)
        return stereo(sig * 0.6, 0.3)
    if kind == "drum":
        return drum(2.0, 62) * 1.2
    if kind == "powerDown":
        # Machinery losing power: hum pitch sags and stutters out.
        n = int(1.8 * SR)
        t = np.arange(n) / SR
        f = 110 * (1 - 0.45 * np.minimum(1, t / 1.2))
        sig = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 2) / SR)
        gate = np.ones(n)
        for a, b in ((0.0, 0.07), (0.14, 0.21), (0.31, 0.38), (0.62, 0.69)):
            gate[int(a * SR):int(b * SR)] = 0.15
        e = np.exp(-t * 1.4) * np.minimum(1, t / 0.01)
        return stereo(sig * gate * e, 0.4)
    if kind == "shimmer":
        # Celestial shimmer: rising cluster of high partials with slow beating, bright air on top.
        n = int(1.6 * SR)
        t = np.arange(n) / SR
        e = np.minimum(1, t / 0.35) * np.exp(-np.maximum(0, t - 0.35) * 2.6)
        sig = sum(np.sin(2 * np.pi * f * (1 + 0.04 * t) * t + RNG.uniform(0, 6.28)) / (k + 1)
                  for k, f in enumerate((1568, 2093, 2349, 3136, 3520, 4186)))
        sig = sig * e + hp(noise(n), 6000) * e * 0.15
        return stereo(sig, 0.8)
    if kind == "relook":
        # EP11 "look again": a soft swept breath rising into a warm major-triad bloom, as the cold read turns warm.
        n = int(2.4 * SR)
        t = np.arange(n) / SR
        sweep = bp(noise(n), 400, 3200) * np.minimum(1, t / 0.7) * np.exp(-np.maximum(0, t - 0.7) * 5)
        bloom_e = np.clip((t - 0.55) / 0.25, 0, 1) * np.exp(-np.maximum(0, t - 0.8) * 1.6)
        bloom = sum(np.sin(2 * np.pi * f * t + RNG.uniform(0, 6.28)) / (k + 1)
                    for k, f in enumerate((293.66, 369.99, 440.0, 587.33)))
        return reverb(stereo(sweep * 0.5 + bloom * bloom_e * 0.6, 0.6), 2.4, 3.0, 0.3)
    if kind == "tonalDrop":
        # Low atmospheric tonal shift: a sub tone gliding down a fourth, with a soft filtered body.
        n = int(3.2 * SR)
        t = np.arange(n) / SR
        f = 98 * 2 ** (-5 / 12 * np.minimum(1, t / 1.2))
        body = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(2 * np.pi * np.cumsum(f * 2) / SR)
        e = np.minimum(1, t / 0.08) * np.exp(-t * 0.9)
        sig = body * e + lp(noise(n), 300) * e * 0.4
        return stereo(sig, 0.5)
    if kind == "doors":
        # Heavy stone doors: low grinding friction that swells and settles, ending in a soft thud.
        n = int(2.0 * SR)
        t = np.arange(n) / SR
        grind = bp(noise(n), 80, 700) * (np.abs(lp(noise(n), 18, 1)) * 10).clip(0, 1.2)
        e = np.interp(t, [0, 0.3, 1.2, 1.5], [0, 1, 0.8, 0])
        thud = np.sin(2 * np.pi * 52 * t) * np.exp(-np.maximum(0, t - 1.35) * 9) * (t > 1.35)
        return stereo(grind * e + thud * 0.8, 0.6)
    if kind == "ritualBell":
        # Temple bell: inharmonic partials, long decay.
        n = int(5.0 * SR)
        t = np.arange(n) / SR
        f0 = 207.65  # G#3
        sig = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-d * t)
                  for r, a, d in [(0.5, 0.6, 0.6), (1.0, 1.0, 0.8), (1.19, 0.5, 1.1), (1.56, 0.4, 1.5), (2.0, 0.35, 1.8), (2.74, 0.2, 2.6), (3.76, 0.1, 3.5)])
        sig *= np.minimum(1, t / 0.003)
        return stereo(sig, 0.4)
    if kind == "sunrise":
        # Sunrise swell: a major chord blooming out of noise, peaking at about 2 s.
        n = int(4.0 * SR)
        t = np.arange(n) / SR
        e = np.minimum(1, t / 2.0) ** 2 * np.exp(-np.maximum(0, t - 2.0) * 1.4)
        tone = sum(np.sin(2 * np.pi * hz(nm) * t) for nm in ("C4", "E4", "G4", "C5")) / 4
        sig = tone * e + bp(noise(n), 1500, 7000) * e * 0.12
        return stereo(sig, 0.7)
    if kind == "bowlKnock":
        # Wooden bowl set down upside down on stone: hollow wood resonance + a dull contact click.
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        body = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in [(210, 1.0, 22), (480, 0.6, 30), (930, 0.3, 45), (1650, 0.15, 60)])
        click = bp(noise(n), 1500, 6000) * np.exp(-t * 300) * 0.6
        sig = (body + click) * np.minimum(1, t / 0.001)
        return stereo(sig, 0.2)
    if kind == "ladle":
        # Ladle pour: a short liquid stream (modulated band noise) settling into a ceramic bowl, with a soft clink.
        n = int(1.4 * SR)
        t = np.arange(n) / SR
        e = np.interp(t, [0, 0.08, 0.7, 1.1], [0, 1, 0.7, 0])
        gurgle = 0.6 + 0.4 * np.sin(2 * np.pi * (9 + 6 * np.sin(2 * np.pi * 1.3 * t)) * t)
        stream = bp(noise(n), 400, 2600) * gurgle * e
        clink = sum(np.sin(2 * np.pi * f * t) for f in (2900, 4300)) * np.exp(-t * 25) * 0.12
        return stereo(stream + clink, 0.5)
    if kind == "chimes":
        out = np.zeros((int(3.6 * SR), 2))
        for i, note in enumerate(["A5", "C6", "E6", "G5"]):
            place(out, bell(hz(note)), i * 0.33, 0.5)
        return out
    if kind == "stoneShift":
        # Distant stone settling: a short low grind, then a few small crumbles trickling down.
        n = int(2.0 * SR)
        t = np.arange(n) / SR
        grind = bp(noise(n), 70, 500) * (np.abs(lp(noise(n), 14, 1)) * 9).clip(0, 1.1) * np.interp(t, [0, 0.15, 0.7, 1.0], [0, 1, 0.6, 0])
        grains = np.zeros(n)
        for g in RNG.uniform(0.35, 1.6, 10):
            i = int(g * SR)
            m = int(0.05 * SR)
            grains[i:i + m] += bp(noise(m), 900, 4000) * np.exp(-np.arange(m) / SR * 70) * RNG.uniform(0.1, 0.35)
        return stereo(grind + grains, 0.6)
    if kind == "resonance":
        # Dormant mechanism: faint inharmonic bronze resonance with slow beating, struck softly.
        n = int(3.4 * SR)
        t = np.arange(n) / SR
        sig = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-d * t) for f, a, d in [(146.8, 1.0, 0.9), (148.1, 0.8, 0.9), (403, 0.35, 1.6), (689, 0.2, 2.4), (1012, 0.1, 3.2)])
        sig *= np.minimum(1, t / 0.04)
        sig += bp(noise(n), 1500, 5000) * np.exp(-t * 12) * 0.08
        return stereo(sig, 0.5)
    if kind == "rebuild":
        # Reconstruction lines drawing in: a soft rising fifth with fine "drafting" grains on top.
        n = int(3.0 * SR)
        t = np.arange(n) / SR
        e = np.minimum(1, t / 1.4) ** 2 * np.exp(-np.maximum(0, t - 1.6) * 1.8)
        tone = sum(np.sin(2 * np.pi * hz(nm) * (1 + 0.01 * t) * t) for nm in ("E4", "B4", "E5")) / 3
        scratch = hp(noise(n), 3500) * (np.abs(lp(noise(n), 25, 1)) * 10).clip(0, 1) * 0.12
        return stereo((tone + scratch) * e, 0.7)
    if kind == "warHorn":
        # Distant war horn, half lost in the wind: a low brassy fifth that sags at the end.
        n = int(2.6 * SR)
        t = np.arange(n) / SR
        f = 98 * (1 - 0.04 * np.clip((t - 1.4) / 0.8, 0, 1))
        ph = 2 * np.pi * np.cumsum(f) / SR
        tone = sum(a * np.sin(k * ph) for k, a in [(1, 1), (2, 0.6), (3, 0.45), (4, 0.25), (5, 0.15), (1.5, 0.35)])
        e = np.interp(t, [0, 0.35, 1.6, 2.4], [0, 1, 0.8, 0])
        return stereo(lp(tone * e, 1400), 0.3)
    if kind == "mountainRise":
        # A range drawing onto the map: a deep tectonic swell with gravel grains, rising then settling.
        n = int(2.6 * SR)
        t = np.arange(n) / SR
        e = np.minimum(1, t / 1.1) ** 2 * np.exp(-np.maximum(0, t - 1.2) * 2.2)
        body = lp(noise(n), 120, 4) * 3 + np.sin(2 * np.pi * np.cumsum(36 + 10 * np.minimum(1, t / 1.2)) / SR) * 0.6
        grains = np.zeros(n)
        for g in RNG.uniform(0.2, 1.6, 18):
            i = int(g * SR)
            m = int(0.05 * SR)
            grains[i:i + m] += bp(noise(m), 700, 3500) * np.exp(-np.arange(m) / SR * 70) * RNG.uniform(0.1, 0.4)
        return stereo(body * e + grains * 0.7, 0.6)
    if kind == "tally":
        # A reason checked off: a dry wooden tick and a soft high bell a fifth above (EP07 tally icons).
        n = int(1.6 * SR)
        t = np.arange(n) / SR
        tick = bp(noise(n), 900, 4000) * np.exp(-t * 90) * 0.8
        ring = (np.sin(2 * np.pi * 1318.5 * t) + 0.5 * np.sin(2 * np.pi * 1975.5 * t)) * np.exp(-t * 3.2) * 0.35
        return stereo(tick + ring * np.minimum(1, t / 0.004), 0.3)
    if kind == "stake":
        # A survey stake driven into turf: a soft low thump with a little earth crunch.
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        thump = np.sin(2 * np.pi * np.cumsum(90 * (1 + 0.6 * np.exp(-t * 30))) / SR) * np.exp(-t * 14)
        crunch = bp(noise(n), 700, 3500) * np.exp(-t * 40) * 0.4
        return stereo(thump + crunch, 0.2)
    if kind == "drop":
        # One drop of water into a full cup: a short rising "plink" with a soft wet tail (EP08 water motif).
        n = int(1.2 * SR)
        t = np.arange(n) / SR
        f = 900 * (1 + 1.4 * (1 - np.exp(-t * 60)))
        plink = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 28) * np.minimum(1, t / 0.002)
        tail = bp(noise(n), 1200, 5000) * np.exp(-t * 22) * 0.12
        return stereo(plink + tail, 0.3)
    if kind == "lock":
        # An iron padlock snapping shut: a dull body knock and two bright metallic clicks (EP08 wells).
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        knock = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 35) * 0.6
        out = knock.copy()
        for at, a in ((0.0, 1.0), (0.055, 0.7)):
            i = int(at * SR)
            m = n - i
            tt = np.arange(m) / SR
            ring = sum(w * np.sin(2 * np.pi * fr * tt) for fr, w in ((2350, 1.0), (3710, 0.6), (5280, 0.3))) * np.exp(-tt * 45)
            out[i:] += (ring * 0.5 + bp(noise(m), 2500, 8000) * np.exp(-tt * 160)) * a
        return stereo(out, 0.2)
    if kind == "strike":
        # A wrong idea struck out (EP09 reverseCard): a fast dry pen scratch with a low muted thud.
        n = int(0.8 * SR)
        t = np.arange(n) / SR
        scratch = bp(noise(n), 1800, 7000) * np.interp(t, [0, 0.02, 0.22, 0.3], [0, 1, 0.7, 0]) * 0.6
        thud = np.sin(2 * np.pi * np.cumsum(70 * (1 + 0.8 * np.exp(-t * 30))) / SR) * np.exp(-t * 16) * 0.8
        return stereo(scratch + thud, 0.25)
    if kind == "gateSlam":
        # A bridge gate shut for good (EP10): a short chain rattle running down, then a deep timber-and-iron boom.
        n = int(2.4 * SR)
        t = np.arange(n) / SR
        chain = np.zeros(n)
        for k in range(14):
            i = int((0.02 + k * 0.026 * (1 - k / 30)) * SR)
            m = int(0.04 * SR)
            chain[i:i + m] += bp(noise(m), 2200, 7000) * np.exp(-np.arange(m) / SR * 90) * RNG.uniform(0.25, 0.5)
        hit = 0.42
        th = np.clip(t - hit, 0, None)
        boom = np.sin(2 * np.pi * np.cumsum(48 * (1 + 0.8 * np.exp(-th * 25))) / SR) * np.exp(-th * 4.5) * (t >= hit)
        clang = (np.sin(2 * np.pi * 311 * th) + 0.6 * np.sin(2 * np.pi * 467 * th)) * np.exp(-th * 9) * 0.25 * (t >= hit)
        crack = bp(noise(n), 300, 2500) * np.exp(-th * 35) * 0.7 * (t >= hit)
        return stereo(chain + boom + clang + crack, 0.4)
    if kind == "timeFold":
        # Centuries folding (EP12 eraShift): a bell played backwards swells up out of a cold wind gust, then a soft low settle.
        n = int(2.2 * SR)
        t = np.arange(n) / SR
        m = int(1.5 * SR)
        tt = np.arange(m) / SR
        b = sum(a * np.sin(2 * np.pi * 523.25 * r * tt) * np.exp(-tt * d) for r, a, d in [(1, 1, 2.2), (2.76, 0.5, 3.5), (5.4, 0.25, 6)])
        sig = np.zeros(n)
        sig[:m] += b[::-1] * 0.6
        gust = bp(noise(n), 400, 2500) * np.interp(t, [0, 1.3, 1.6, 2.2], [0, 0.5, 0.15, 0])
        th = np.clip(t - 1.5, 0, None)
        settle = np.sin(2 * np.pi * 55 * th) * np.exp(-th * 5) * 0.7 * (t >= 1.5)
        return stereo(sig + gust + settle, 0.6)
    if kind == "headCount":
        # A quiet roll-call (EP12): twenty soft wooden taps accelerating slightly over 1.1 s, like a staff counting heads.
        n = int(1.6 * SR)
        out = np.zeros(n)
        for k in range(20):
            i = int((k / 19) ** 0.92 * 1.1 * SR)
            m = int(0.05 * SR)
            tt = np.arange(m) / SR
            tap = (np.sin(2 * np.pi * 820 * tt) * 0.5 + bp(noise(m), 900, 3000)) * np.exp(-tt * 90) * (0.5 + 0.2 * (k % 2))
            out[i:i + m] += tap[: len(out[i:i + m])]
        return stereo(out, 0.3)
    if kind == "giftSet":
        # The gift offered (EP13 signature): a glazed ceramic lid settling on its box, a soft bright ring and a cloth brush.
        n = int(1.6 * SR)
        t = np.arange(n) / SR
        ring = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in [(1240, 1.0, 6), (2010, 0.55, 8), (3170, 0.3, 11), (4630, 0.15, 15)])
        settle = np.zeros(n)
        for at, a in ((0.0, 1.0), (0.07, 0.45), (0.12, 0.25)):
            i = int(at * SR)
            settle[i:] += ring[: n - i] * a
        brush = bp(noise(n), 600, 3000) * np.interp(t, [0, 0.05, 0.25], [0.3, 0.15, 0])
        return stereo(settle * 0.35 * np.minimum(1, t / 0.002) + brush, 0.35)
    if kind == "seam":
        # A split frame drawn across like a border (EP13): a soft rising air sweep that ends in a low muted tap.
        n = int(1.1 * SR)
        t = np.arange(n) / SR
        sweep = bp(noise(n), 500, 4000) * np.interp(t, [0, 0.3, 0.38, 0.6], [0, 0.6, 0.2, 0])
        tap = np.sin(2 * np.pi * 110 * np.clip(t - 0.32, 0, None)) * np.exp(-np.clip(t - 0.32, 0, None) * 18) * (t >= 0.32) * 0.7
        return stereo(sweep + tap, 0.6)
    if kind == "benchSet":
        # The bench carried out (EP15 signature): a short scrape on cobbles, then two hollow timber knocks as each end lands.
        n = int(1.3 * SR)
        t = np.arange(n) / SR
        scrape = bp(noise(n), 700, 3500) * np.interp(t, [0, 0.04, 0.22, 0.3], [0, 0.35, 0.25, 0])
        out = scrape.copy()
        for at, a, f in ((0.3, 1.0, 196), (0.42, 0.75, 174)):
            th = np.clip(t - at, 0, None)
            body = sum(w * np.sin(2 * np.pi * f * r * th) for r, w in ((1, 1.0), (2.41, 0.45), (3.9, 0.2))) * np.exp(-th * 22)
            out += (body * 0.8 + bp(noise(n), 300, 1800) * np.exp(-th * 60) * 0.5) * a * (t >= at)
        return stereo(out, 0.3)
    if kind == "inferSeal":
        # A value inferred (EP15 inferChain): a dry pen tick, then a warm rising fifth, quiet, like a thought clicking into place.
        n = int(1.8 * SR)
        t = np.arange(n) / SR
        tick = bp(noise(n), 2000, 7000) * np.exp(-t * 120) * 0.5
        out = tick.copy()
        for at, f in ((0.06, 587.33), (0.16, 880.0)):
            th = np.clip(t - at, 0, None)
            tone = (np.sin(2 * np.pi * f * th) + 0.35 * np.sin(2 * np.pi * 2 * f * th) + 0.12 * np.sin(2 * np.pi * 3.01 * f * th)) * np.exp(-th * 3.2)
            out += tone * np.minimum(1, th / 0.004) * 0.3 * (t >= at)
        return stereo(out, 0.35)
    if kind == "scaleTip":
        # A verdict scale tipping (EP14 signature): a short wooden creak, two chain chinks, then a soft knock as the pan settles.
        n = int(1.4 * SR)
        t = np.arange(n) / SR
        creak = bp(noise(n), 300, 1400) * (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t)) * np.interp(t, [0, 0.05, 0.35, 0.5], [0, 0.35, 0.25, 0])
        chink = np.zeros(n)
        for at, a in ((0.08, 1.0), (0.21, 0.6)):
            th = np.clip(t - at, 0, None)
            chink += a * (t >= at) * sum(b * np.sin(2 * np.pi * f * th) * np.exp(-th * d) for f, b, d in [(2890, 1.0, 26), (4410, 0.5, 34), (6120, 0.25, 42)])
        th = np.clip(t - 0.42, 0, None)
        knock = np.sin(2 * np.pi * 150 * th) * np.exp(-th * 22) * (t >= 0.42)
        return stereo(creak + chink * 0.22 + knock * 0.6, 0.4)
    if kind == "grainPour":
        # Grain on the move (EP16 signature): a dry hiss of kernels poured from a sack, thinning out, over a soft cloth thump.
        n = int(1.8 * SR)
        t = np.arange(n) / SR
        hiss = bp(noise(n), 2500, 9000) * np.interp(t, [0, 0.12, 0.9, 1.5], [0, 0.5, 0.35, 0])
        grains = np.zeros(n)
        for g in RNG.uniform(0.05, 1.4, 160):
            i = int(g * SR)
            m = int(0.008 * SR)
            grains[i:i + m] += bp(noise(m), 3000, 8000) * RNG.uniform(0.1, 0.5) * (1.4 - g)
        thump = lp(noise(n), 300) * np.exp(-t * 14) * 1.5
        return stereo(hiss + grains + thump, 0.5)
    if kind == "crownShift":
        # The crown changes hands (EP16 signature): a gold ring lifted (bright partials gliding up), carried on a breath of air,
        # then set down with a soft low chord-tap: the power arriving somewhere new.
        n = int(2.2 * SR)
        t = np.arange(n) / SR
        glide = 1 + 0.06 * np.minimum(1, t / 0.9)
        ring = sum(a * np.sin(2 * np.pi * np.cumsum(np.full(n, f) * glide) / SR) * np.exp(-t * d) for f, a, d in [(1318.5, 1.0, 2.0), (1975.5, 0.5, 2.6), (2637.0, 0.25, 3.4)])
        air = bp(noise(n), 600, 4000) * np.interp(t, [0, 0.4, 0.9, 1.2], [0, 0.35, 0.2, 0])
        th = np.clip(t - 1.0, 0, None)
        land = sum(np.sin(2 * np.pi * f * th) for f in (146.83, 220.0, 293.66)) * np.exp(-th * 4) * (t >= 1.0) * np.minimum(1, th / 0.01)
        return stereo(ring * 0.3 * np.minimum(1, t / 0.01) + air + land * 0.35, 0.5)
    if kind == "pillarSet":
        # A stone pillar set in place (EP17 pillarStack signature): a short grit scrape, then a low, dry stone thud.
        n = int(1.2 * SR)
        t = np.arange(n) / SR
        grit = bp(noise(n), 900, 4200) * np.interp(t, [0, 0.03, 0.1, 0.14], [0, 0.3, 0.2, 0])
        th = np.clip(t - 0.1, 0, None)
        thud = np.sin(2 * np.pi * np.cumsum(70 * (1 + 0.5 * np.exp(-th * 30))) / SR) * np.exp(-th * 14) * (t >= 0.1)
        thud += lp(noise(n), 700) * np.exp(-th * 40) * 0.6 * (t >= 0.1)
        return stereo(grit + thud, 0.25)
    if kind == "doorKnock":
        # Three knuckle knocks on a wooden door down the street (EP17's implied fear): muffled, unhurried, a little room tail.
        n = int(1.6 * SR)
        t = np.arange(n) / SR
        out = np.zeros(n)
        for at, a in ((0.0, 0.9), (0.24, 1.0), (0.48, 0.85)):
            th = np.clip(t - at, 0, None)
            body = sum(w * np.sin(2 * np.pi * f * th) for f, w in ((118, 1.0), (241, 0.5), (377, 0.25))) * np.exp(-th * 30)
            out += (body + bp(noise(n), 400, 2200) * np.exp(-th * 90) * 0.7) * a * (t >= at)
        out = lp(out, 1600)
        return stereo(out + np.roll(out, int(0.045 * SR)) * 0.25, 0.3)
    if kind == "crackTick":
        # A strain spreading (EP19 crackLoop signature): a dry, brittle snap like glaze crazing, with a short low knock under it.
        n = int(0.7 * SR)
        t = np.arange(n) / SR
        snap = bp(noise(n), 2200, 9000) * np.exp(-t * 90) * 0.7
        for at in (0.012, 0.03):
            th = np.clip(t - at, 0, None)
            snap += bp(noise(n), 3000, 8000) * np.exp(-th * 140) * 0.35 * (t >= at)
        knock = np.sin(2 * np.pi * np.cumsum(95 * (1 + 0.4 * np.exp(-t * 40))) / SR) * np.exp(-t * 26) * 0.6
        return stereo(snap + knock, 0.35)
    if kind == "sealSplit":
        # The empire's seal breaks in two (EP19): a sharp stone crack, a dropping low boom, and fragments settling.
        n = int(2.6 * SR)
        t = np.arange(n) / SR
        crack = bp(noise(n), 1200, 9000) * np.exp(-t * 35) * 1.1
        boom = np.sin(2 * np.pi * np.cumsum(58 * (1 + 0.9 * np.exp(-t * 9))) / SR) * np.exp(-t * 1.9)
        boom += lp(noise(n), 220, 3) * np.exp(-t * 3.5) * 1.4
        bits = np.zeros(n)
        for g in RNG.uniform(0.15, 1.3, 18):
            i = int(g * SR)
            m = int(0.05 * SR)
            bits[i:i + m] += bp(noise(m), 1500, 6000) * np.exp(-np.arange(m) / SR * 80) * RNG.uniform(0.1, 0.35)
        return stereo(crack + boom * 0.9 + bits, 0.55)
    if kind == "quill":
        # A clause written into the law (EP18 lawText signature): three quick nib strokes on vellum, then a dry dot.
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        out = np.zeros(n)
        for at, d, a in ((0.0, 0.16, 0.8), (0.2, 0.12, 0.6), (0.36, 0.2, 0.7)):
            th = t - at
            shape = np.clip(th / d, 0, 1) * (th < d) * np.sin(np.pi * np.clip(th / d, 0, 1))
            out += bp(noise(n), 2500, 8000) * shape * a * (0.7 + 0.3 * np.sin(2 * np.pi * 55 * t))
        th = np.clip(t - 0.62, 0, None)
        out += bp(noise(n), 1500, 5000) * np.exp(-th * 80) * (t >= 0.62) * 0.6
        return stereo(out * 0.6, 0.4)
    if kind == "clauseLight":
        # A clause lit by the fear behind it (EP18): a soft breath of flame catching, under a low, warm open fifth.
        n = int(2.0 * SR)
        t = np.arange(n) / SR
        catch = bp(noise(n), 400, 2500) * np.interp(t, [0, 0.08, 0.5, 1.0], [0, 0.5, 0.2, 0])
        tone = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((110.0, 1.0), (164.81, 0.6), (220.0, 0.35), (329.63, 0.15)))
        tone *= np.minimum(1, t / 0.06) * np.exp(-t * 2.2)
        return stereo(catch + tone * 0.35, 0.4)
    if kind == "chisel":
        # A memorial inscription cut into stone (EP20 tablet signature): a run of light chisel taps with grit, slowing at the end.
        n = int(1.6 * SR)
        t = np.arange(n) / SR
        out = np.zeros(n)
        hits = np.cumsum(np.linspace(0.085, 0.16, 11))
        for i, at in enumerate(hits[hits < 1.4]):
            th = np.clip(t - at, 0, None)
            f = 2300 + 260 * np.sin(i * 1.7)
            ring = (np.sin(2 * np.pi * f * th) + 0.4 * np.sin(2 * np.pi * 2.76 * f * th)) * np.exp(-th * 70)
            out += (ring * 0.35 + bp(noise(n), 1500, 6500) * np.exp(-th * 55) * 0.6 + lp(noise(n), 500) * np.exp(-th * 45) * 0.4) * (t >= at) * RNG.uniform(0.6, 1.0)
        return stereo(out, 0.3)
    if kind == "frameOpen":
        # A chronicle's frame opening onto what it left out (EP20 chronicleFrame signature): a breath of air widening as its
        # low-pass opens, under a low hollow fifth that swells and fades, unresolved.
        n = int(2.4 * SR)
        t = np.arange(n) / SR
        k = np.minimum(1, t / 1.1)
        air = bp(noise(n), 200, 900) * (1 - k) + bp(noise(n), 700, 5200) * k
        air *= np.interp(t, [0, 0.5, 1.2, 2.2], [0, 0.4, 0.3, 0])
        tone = sum(np.sin(2 * np.pi * f * t + RNG.uniform(0, 6.28)) for f in (110.0, 164.81, 220.0)) * np.interp(t, [0, 0.7, 1.4, 2.4], [0, 0.22, 0.16, 0])
        return stereo(air + tone, 0.6)
    if kind == "mendKnit":
        # The mend (EP21 signature magic): a fine crackle of pieces drawing together under a glassy cluster gliding up a
        # fourth, settling on a soft open fifth. Reused whenever the mending magic (or the spell page's sigil) works.
        n = int(2.2 * SR)
        t = np.arange(n) / SR
        grains = np.zeros(n)
        for g in RNG.uniform(0.0, 0.8, 70):
            i = int(g * SR)
            m = int(0.006 * SR)
            grains[i:i + m] += bp(noise(m), 2500, 8000) * RNG.uniform(0.1, 0.4) * (0.9 - g)
        glide = 1 + (4 / 3 - 1) * np.minimum(1, t / 0.8) ** 0.7
        glass = sum(a * np.sin(2 * np.pi * np.cumsum(np.full(n, f) * glide) / SR) for f, a in ((523.25, 1.0), (784.0, 0.5), (1046.5, 0.3)))
        glass *= np.interp(t, [0, 0.3, 0.8, 2.2], [0, 0.35, 0.5, 0])
        th = np.clip(t - 0.8, 0, None)
        settle = sum(np.sin(2 * np.pi * f * th) for f in (349.23, 523.25, 698.46)) * np.exp(-th * 2.2) * (t >= 0.8) * np.minimum(1, th / 0.02)
        return stereo(grains + glass * 0.5 + settle * 0.3, 0.5)
    if kind == "mendFizzle":
        # A mend that fails (EP21's limit): the glassy tone sags a semitone, sputters and dies on a dull thump.
        n = int(1.2 * SR)
        t = np.arange(n) / SR
        f = 698.46 * (1 - 0.06 * np.minimum(1, t / 0.5))
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
        gate = (lp(noise(n), 18, 1) > -0.02).astype(float) * 0.7 + 0.3
        tone *= gate * np.interp(t, [0, 0.05, 0.5, 0.75], [0, 0.6, 0.35, 0])
        th = np.clip(t - 0.55, 0, None)
        thump = lp(noise(n), 400) * np.exp(-th * 18) * (t >= 0.55) * 1.2
        return stereo(tone + thump, 0.3)
    if kind == "costCrack":
        # The price of a mend (EP21): a brittle crack racing across glass or stone, a few splitting ticks, a low creak.
        n = int(1.4 * SR)
        t = np.arange(n) / SR
        snap = hp(noise(n), 1800) * np.exp(-t * 40) * 0.9
        ticks = np.zeros(n)
        for g in np.sort(RNG.uniform(0.02, 0.4, 12)):
            i = int(g * SR)
            m = int(0.004 * SR)
            ticks[i:i + m] += hp(noise(m), 3000) * RNG.uniform(0.3, 0.8)
        creak = bp(noise(n), 120, 500) * np.interp(t, [0, 0.05, 0.5, 1.0], [0, 0.6, 0.3, 0])
        return stereo(snap + ticks + creak, 0.5)
    if kind == "mend":
        # A wound closing at a touch (EP22 mendGlow signature): a soft breath, then glassy A-major partials that bloom and
        # drift a few cents upward, like warmth spreading under the hand. No attack transient: healing never clicks.
        n = int(2.0 * SR)
        t = np.arange(n) / SR
        breath = bp(noise(n), 500, 3000) * np.interp(t, [0, 0.18, 0.5, 0.9], [0, 0.25, 0.12, 0])
        glide = 1 + 0.004 * np.minimum(1, t / 1.2)
        bloom = np.interp(t, [0, 0.12, 0.35], [0, 0.6, 1.0]) * np.exp(-np.maximum(0, t - 0.35) * 2.4)
        tone = sum(a * np.sin(2 * np.pi * np.cumsum(np.full(n, f) * glide) / SR + p) for f, a, p in [(880.0, 1.0, 0.0), (1108.73, 0.6, 1.1), (1318.51, 0.45, 2.3), (2217.46, 0.15, 0.7)])
        return stereo(breath + tone * bloom * 0.28, 0.5)
    if kind == "ripple":
        # The consequence spreading outward (EP22 rippleMap ring): a low, round water-like swell whose pitch sinks as the ring
        # widens, with a faint airy shimmer on top, so each ring sounds farther away than the last hit.
        n = int(1.8 * SR)
        t = np.arange(n) / SR
        f = 150 * (1 - 0.35 * np.minimum(1, t / 1.2))
        body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.interp(t, [0, 0.08, 0.5, 1.6], [0, 1.0, 0.45, 0])
        air = bp(noise(n), 1500, 6000) * np.interp(t, [0, 0.15, 0.7, 1.3], [0, 0.18, 0.08, 0])
        return stereo(lp(body, 900) + air, 0.6)
    if kind == "recall":
        # The memory spell (EP23 signature): a soft breath, then a quick rising music-box arpeggio (D, F#, A, E) whose notes
        # ring on and shimmer, like something remembered for the last time. Gentle attacks: the spell itself never hurts.
        n = int(2.4 * SR)
        t = np.arange(n) / SR
        breath = bp(noise(n), 700, 4000) * np.interp(t, [0, 0.15, 0.45, 1.0], [0, 0.18, 0.08, 0])
        tone = np.zeros(n)
        for k, f in enumerate([587.33, 739.99, 880.0, 1318.51]):
            st = 0.06 + k * 0.085
            th = np.clip(t - st, 0, None)
            amp = (t >= st) * (1 - np.exp(-th * 60)) * np.exp(-th * 1.9)
            tone += amp * (np.sin(2 * np.pi * f * th) + 0.3 * np.sin(2 * np.pi * 2.01 * f * th) * np.exp(-th * 4)) * (0.9 - 0.12 * k)
        shimmer = 1 + 0.04 * np.sin(2 * np.pi * 5.5 * t)
        return stereo(breath + tone * shimmer * 0.22, 0.55)
    if kind == "forget":
        # A memory struck from the ledger (EP23 price): a short dry quill stroke, then one music-box note that sags a
        # quarter-tone as it fades, and an airy whisper rising away (the mote of light drifting off the page).
        n = int(2.2 * SR)
        t = np.arange(n) / SR
        stroke = bp(noise(n), 2500, 7500) * np.interp(t, [0, 0.02, 0.22, 0.3], [0, 0.35, 0.22, 0])
        f = 880.0 * (1 - 0.028 * np.minimum(1, t / 1.6))
        th = np.clip(t - 0.12, 0, None)
        note = (t >= 0.12) * np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - np.exp(-th * 50)) * np.exp(-th * 1.7)
        air = bp(noise(n), 3000, 9000) * np.interp(t, [0, 0.3, 0.9, 1.8], [0, 0.0, 0.1, 0])
        return stereo(stroke + note * 0.3 + air, 0.6)
    if kind == "gaze":
        # Her sight touching something (EP25 gazeBeam / sightPlan signature): a cold glassy hum on a tritone-free open fifth
        # (C5 + G5) that swells in and hangs, with a faint high whistle drifting a few cents, like a wet finger on crystal.
        n = int(1.8 * SR)
        t = np.arange(n) / SR
        shape = np.interp(t, [0, 0.35, 1.0, 1.8], [0, 1.0, 0.6, 0])
        drift = 1 + 0.003 * np.sin(2 * np.pi * 0.9 * t)
        hum = sum(a * np.sin(2 * np.pi * np.cumsum(np.full(n, f) * drift) / SR) for f, a in ((523.25, 1.0), (783.99, 0.55), (1567.98, 0.18)))
        whistle = np.sin(2 * np.pi * np.cumsum(np.full(n, 3135.96) * (1 + 0.006 * t)) / SR) * 0.06
        air = bp(noise(n), 2000, 7000) * 0.05
        return stereo((hum * 0.3 + whistle + air) * shape, 0.6)
    if kind == "unmake":
        # Something erased (EP25 unmake): an inward rush (filtered noise that swells *up* to the moment, like a reversed
        # breath), a sine that falls an octave as the thing dissolves, and a spray of fine crackles thinning to silence.
        # No impact and no thud: what she unmakes just stops being there.
        n = int(2.2 * SR)
        t = np.arange(n) / SR
        rush = bp(noise(n), 400, 4000) * np.interp(t, [0, 0.5, 0.62, 1.2], [0, 0.6, 0.15, 0])
        f = 440 * 2 ** (-np.clip(t - 0.5, 0, 1.2) / 1.2)
        fall = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.interp(t, [0, 0.45, 0.6, 1.9], [0, 0.1, 0.45, 0])
        crackle = np.zeros(n)
        for g in RNG.uniform(0.5, 1.9, 160):
            i = int(g * SR)
            m = int(0.003 * SR)
            crackle[i:i + m] += hp(noise(m), 4000) * RNG.uniform(0.1, 0.5) * (1.9 - g) / 1.4
        return stereo(rush + fall * 0.5 + crackle * 0.6, 0.6)
    raise KeyError(kind)


def ticks(t0, t1):
    """Accelerating clock ticks across [t0, t1] to sell 'a thousand years'."""
    n = int((t1 - t0 + 0.3) * SR)
    out = np.zeros((n, 2))
    t, gap = 0.0, 0.22
    while t < t1 - t0:
        m = int(0.03 * SR)
        click = bp(noise(m), 2500, 7000) * np.exp(-np.arange(m) / SR * 220)
        place(out, stereo(click), t, 1.0)
        t += gap
        gap = max(0.045, gap * 0.86)
    return out


def build_sfx(ep, timing):
    n = int(timing["duration"] * SR)
    out = np.zeros((n, 2))
    for shot in ep["shots"]:
        for cue in shot.get("sfx", []):
            gain = db(cue.get("gain", -18))
            if "from" in cue:
                t0 = resolve_cue(cue["from"], timing)
                t1 = resolve_cue(cue["to"], timing)
                clip = ticks(t0, t1) if cue["sound"] == "ticks" else sfx_bed(cue["sound"], t1 - t0 + 0.6)
                place(out, clip / (np.abs(clip).max() + 1e-9), t0, gain)
            else:
                clip = sfx_hit(cue["sound"])
                place(out, clip / (np.abs(clip).max() + 1e-9), resolve_cue(cue["at"], timing), gain)
    return reverb(out, seconds=2.0, decay=4.5, wet=0.2)


def main():
    ep_id = sys.argv[1]
    ep = load_episode(ep_id)
    d = out_dir(ep_id)
    timing = json.loads((d / "timing.json").read_text())
    music = build_music(ep, timing)
    sfx = build_sfx(ep, timing)
    sf.write(d / "music.wav", (music / (np.abs(music).max() + 1e-9) * 0.7).astype(np.float32), SR, subtype="PCM_16")
    sf.write(d / "sfx.wav", np.clip(sfx, -1, 1).astype(np.float32), SR, subtype="PCM_16")
    print(f"[score] music + sfx written ({timing['duration']:.2f}s)")


if __name__ == "__main__":
    main()
