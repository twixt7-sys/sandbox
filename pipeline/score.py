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
    drone = np.sin(2 * np.pi * hz("D1") * t) * 0.10 + np.sin(2 * np.pi * hz("A1") * t) * 0.05
    music += np.stack([drone, drone], axis=1) * env(n, 2.0, 2.0)[:, None]

    music = reverb(music, wet=0.42)

    # Duck the music under the hook's "empty." moment so the silence lands.
    hook_empty = resolve_cue({"line": "L2", "word": "empty"}, timing) if any(l["id"] == "L2" for l in timing["lines"]) else None
    if hook_empty:
        g = np.ones(n)
        a, b = int((hook_empty - 0.3) * SR), int((hook_empty + 1.2) * SR)
        g[a:b] = np.interp(np.arange(a, b), [a, a + 0.3 * SR, b - 0.6 * SR, b], [1, 0.35, 0.35, 1])
        music *= g[:, None]

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
    if kind == "wind":
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
    if kind == "chimes":
        out = np.zeros((int(3.6 * SR), 2))
        for i, note in enumerate(["A5", "C6", "E6", "G5"]):
            place(out, bell(hz(note)), i * 0.33, 0.5)
        return out
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
