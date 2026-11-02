"""Season 2 composed score: the "World Engine" theme, arranged from story cues and played on sampled instruments.

Used by pipeline/score.py when episode.json has `"music": {"engine": "s2-score", ...}`.

How it works
  1. Tempo map to picture. Each section starts on a spoken cue. Between two section starts the number of beats is
     rounded from the nominal tempo (default 100 BPM) and the beat is stretched to fit exactly, so every musical
     change lands *on* its story beat (the RUN press, the drop, the delete, "together") without the tempo wandering
     more than a few BPM.
  2. Arrangement. Each section names a style (hook, pulse, drive, drop, void, mystery, build 1-4, twist, rest, frenzy,
     crash, swell, anthem, outro), its chords and key. Styles write notes for a fixed band of General MIDI
     instruments (celesta, marimba, pizzicato and sustained strings, cello, acoustic bass, flute, horns, harp,
     glockenspiel, music box, timpani, taiko, a square "chip" lead for the World Engine colour, drums).
     The series theme (a 4-bar melody) recurs in minor for the problem and in major for the payoff.
  3. Accents. One-shots on exact cues: `hit` (timpani + string stab + crash), `boom` (taiko + low strings),
     `stab`, `cymbal`, `riser` (a reverse cymbal that peaks on the cue).
  4. Render. The MIDI is played by FluidSynth with the MuseScore General SoundFont (MIT; Debian package
     musescore-general-soundfont-small), then `rests` windows are silenced and the end fades out before the loop.

Install: apt-get install fluidsynth musescore-general-soundfont-small; pip install mido.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import mido
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

from common import SR, resolve_cue

SOUNDFONTS = [
    "/usr/share/sounds/sf3/MuseScore_General.sf3",
    "/usr/share/sounds/sf3/MuseScore_General_Lite.sf3",
    "/usr/share/sounds/sf2/FluidR3_GM.sf2",
]
PPQ = 480

# ---------------------------------------------------------------- pitch helpers

PC = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
      "A": 9, "A#": 10, "Bb": 10, "B": 11, "Cb": 11}


def chord_tones(name: str):
    """'Dm' -> (2, [2, 5, 9]); supports m, dim, aug, 7, maj7, m7, 7b9, sus4, sus2."""
    root = name[:2] if len(name) > 1 and name[1] in "#b" else name[:1]
    q = name[len(root):]
    r = PC[root]
    table = {"": [0, 4, 7], "m": [0, 3, 7], "dim": [0, 3, 6], "aug": [0, 4, 8], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11],
             "m7": [0, 3, 7, 10], "7b9": [0, 4, 7, 10, 13], "sus4": [0, 5, 7], "sus2": [0, 2, 7], "m9": [0, 3, 7, 10, 14]}
    return r, [(r + i) % 12 for i in table[q]], table[q]


def in_range(pc: int, lo: int, hi: int):
    return [p for p in range(lo, hi + 1) if p % 12 == pc]


def voicing(name: str, lo: int, hi: int):
    """All chord tones between lo and hi (MIDI), sorted."""
    _, pcs, _ = chord_tones(name)
    return sorted(p for p in range(lo, hi + 1) if p % 12 in pcs)


def nearest(pc: int, target: int):
    cands = [p for p in range(target - 6, target + 7) if p % 12 == pc]
    return min(cands, key=lambda p: abs(p - target))


MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]


def key_info(key: str):
    """'D minor' -> (tonic pc, scale steps)."""
    name, mode = key.split()
    return PC[name], (MINOR if mode.startswith("min") else MAJOR)


# The series theme: (scale degree, octave offset, beats). 4 bars of 4/4; bars 1-2 ask, bars 3-4 answer.
THEME = [(1, 0, 1.0), (5, -1, 0.5), (1, 0, 0.5), (3, 0, 1.0), (2, 0, 1.0),
         (1, 0, 0.5), (2, 0, 0.5), (3, 0, 1.0), (5, 0, 2.0),
         (6, 0, 1.0), (5, 0, 0.5), (3, 0, 0.5), (2, 0, 1.0), (1, 0, 1.0),
         (2, 0, 0.5), (3, 0, 0.5), (2, 0, 1.0), (1, 0, 2.0)]

# General MIDI band: name -> (channel, program, volume CC7)
BAND = {
    "lead": (0, 73, 100),       # flute (program can change per section)
    "marimba": (1, 12, 92),
    "pizz": (2, 45, 88),
    "strings": (3, 48, 82),
    "bass": (4, 32, 104),
    "glock": (5, 9, 72),
    "chip": (6, 80, 48),       # square lead: the World Engine colour, always quiet
    "harp": (7, 46, 86),
    "timp": (8, 47, 104),
    "drums": (9, 0, 100),
    "celesta": (10, 8, 96),
    "horns": (11, 60, 88),
    "cello": (12, 42, 96),
    "taiko": (13, 116, 104),
    "mbox": (14, 10, 84),
    "fx": (15, 119, 86),       # reverse cymbal
}
# Stereo seat for each part (CC10, 64 = centre): a small orchestra spread left to right, low end in the middle.
PAN = {"lead": 64, "marimba": 40, "pizz": 88, "strings": 64, "bass": 64, "glock": 84, "chip": 54, "harp": 34, "timp": 70,
       "drums": 64, "celesta": 92, "horns": 50, "cello": 58, "taiko": 64, "mbox": 96, "fx": 64}
KICK, STICK, SNARE, HAT, PHAT, OHAT, CRASH, RIDE, TAMB, SHAKER, LTOM, HTOM = 36, 37, 38, 42, 44, 46, 49, 51, 54, 82, 45, 50


class Score:
    """Notes on a tempo map fitted to picture."""

    def __init__(self, anchors: list[float], total: float, bpm: float = 100.0):
        beat0 = 60.0 / bpm
        self.secs = []
        pts = anchors + [total]
        tick = 0
        for a, b in zip(pts[:-1], pts[1:]):
            n = max(1, int(round((b - a) / beat0)))
            self.secs.append({"t0": a, "t1": b, "n": n, "beat": (b - a) / n, "tick0": tick})
            tick += n * PPQ
        self.total_ticks = tick
        self.events: list[tuple[int, int, mido.Message]] = []  # (tick, order, msg)
        self.rng = np.random.default_rng(26)

    def tick_at(self, t: float) -> int:
        for s in self.secs:
            if t < s["t1"] or s is self.secs[-1]:
                return s["tick0"] + int(round((t - s["t0"]) / s["beat"] * PPQ))
        return self.total_ticks

    def note(self, sec: int, beat: float, dur: float, part: str, pitch: int, vel: int, human=True):
        s = self.secs[sec]
        if beat >= s["n"] or pitch < 0 or pitch > 127:
            return
        dur = min(dur, s["n"] - beat + 0.5) if part not in ("strings", "cello", "timp", "mbox", "fx") else dur
        ch = BAND[part][0]
        jitter = int(self.rng.integers(-6, 7)) if human and part not in ("drums",) else int(self.rng.integers(-3, 4)) if human else 0
        v = int(np.clip(vel + (self.rng.integers(-5, 6) if human else 0), 1, 127))
        on = max(0, s["tick0"] + int(round(beat * PPQ)) + jitter)
        off = max(on + 10, s["tick0"] + int(round((beat + dur) * PPQ)) - 12)
        self.events.append((on, 2, mido.Message("note_on", channel=ch, note=pitch, velocity=v)))
        self.events.append((off, 1, mido.Message("note_off", channel=ch, note=pitch, velocity=0)))

    def at_time(self, t: float, dur_s: float, part: str, pitch: int, vel: int):
        """A note at an absolute time (accents), duration in seconds."""
        ch = BAND[part][0]
        on = self.tick_at(t)
        off = self.tick_at(t + dur_s)
        self.events.append((on, 2, mido.Message("note_on", channel=ch, note=pitch, velocity=int(np.clip(vel, 1, 127)))))
        self.events.append((max(off, on + 10), 1, mido.Message("note_off", channel=ch, note=pitch, velocity=0)))

    def program(self, sec: int, part: str, program: int):
        s = self.secs[sec]
        self.events.append((s["tick0"], 0, mido.Message("program_change", channel=BAND[part][0], program=program)))

    def cc(self, tick: int, part: str, num: int, val: int):
        self.events.append((tick, 0, mido.Message("control_change", channel=BAND[part][0], control=num, value=int(np.clip(val, 0, 127)))))

    def write(self, path: Path):
        mid = mido.MidiFile(ticks_per_beat=PPQ)
        tr = mido.MidiTrack()
        mid.tracks.append(tr)
        ev = []
        for s in self.secs:
            ev.append((s["tick0"], -1, mido.MetaMessage("set_tempo", tempo=int(round(s["beat"] * 1e6)))))
        for part, (ch, prog, vol) in BAND.items():
            if part != "drums":
                ev.append((0, -2, mido.Message("program_change", channel=ch, program=prog)))
            ev.append((0, -2, mido.Message("control_change", channel=ch, control=7, value=vol)))
            ev.append((0, -2, mido.Message("control_change", channel=ch, control=91, value=58 if part not in ("bass", "drums") else 30)))
            ev.append((0, -2, mido.Message("control_change", channel=ch, control=10, value=PAN[part])))
        ev += self.events
        ev.sort(key=lambda e: (e[0], e[1]))
        last = 0
        for tick, _, msg in ev:
            tr.append(msg.copy(time=tick - last))
            last = tick
        tr.append(mido.MetaMessage("end_of_track", time=PPQ * 4))
        mid.save(str(path))


# ---------------------------------------------------------------- arrangement styles

class Ctx:
    def __init__(self, score: Score, sec: int, spec: dict):
        self.s = score
        self.i = sec
        self.n = score.secs[sec]["n"]
        self.spec = spec
        self.chords = spec.get("chords", ["C"])
        self.bpc = spec.get("beatsPerChord", 4)
        self.key = spec.get("key", "D minor")
        self.I = spec.get("intensity", 0.7)

    def chord(self, beat: float) -> str:
        return self.chords[int(beat // self.bpc) % len(self.chords)]

    def chord_spans(self):
        b = 0
        while b < self.n:
            yield b, min(self.bpc, self.n - b), self.chord(b)
            b += self.bpc

    def add(self, part, beat, dur, pitch, vel):
        self.s.note(self.i, beat, dur, part, pitch, vel)

    # -- reusable layers
    def pad(self, part="strings", lo=50, hi=67, vel=48, max_notes=4):
        for b, d, ch in self.chord_spans():
            notes = voicing(ch, lo, hi)
            for p in notes[-max_notes:]:
                self.add(part, b, d + 0.15, p, vel)

    def root(self, part, octave_lo, octave_hi, vel, every=None, dur=None):
        for b, d, ch in self.chord_spans():
            r, _, _ = chord_tones(ch)
            p = in_range(r, octave_lo, octave_hi)[0]
            if every:
                k = 0.0
                while k < d - 1e-6:
                    self.add(part, b + k, dur or every * 0.9, p, vel)
                    k += every
            else:
                self.add(part, b, dur or d + 0.1, p, vel)

    def arp(self, part, step, lo, hi, vel, pattern=(0, 1, 2, 3, 2, 1), accent=1.0, start=0.0):
        k = 0
        b = start
        while b < self.n - 1e-6:
            notes = voicing(self.chord(b), lo, hi)
            if notes:
                p = notes[pattern[k % len(pattern)] % len(notes)]
                v = vel * (accent if (b % 1) < 1e-6 else 1.0)
                self.add(part, b, step * 0.95, p, int(v))
            b += step
            k += 1

    def drums(self, kick=(0, 2), snare=(1, 3), hats=0.5, hat_vel=42, kick_vel=92, snare_vel=74, shaker=None, sticks=False, from_beat=0.0):
        b = 0.0
        while b < self.n - 1e-6:
            pos = b % 4
            if b >= from_beat:
                if any(abs(pos - k) < 1e-6 for k in kick):
                    self.add("drums", b, 0.4, KICK, kick_vel)
                if any(abs(pos - k) < 1e-6 for k in snare):
                    self.add("drums", b, 0.4, STICK if sticks else SNARE, snare_vel)
                if hats and abs((b / hats) - round(b / hats)) < 1e-6:
                    off = (b % 1) > 1e-6
                    self.add("drums", b, 0.2, HAT, int(hat_vel * (1.15 if off else 0.85)))
                if shaker and abs((b / shaker) - round(b / shaker)) < 1e-6:
                    self.add("drums", b, 0.2, SHAKER, 34)
            b += 0.25

    def theme(self, part, tonic_midi=None, vel=88, start=0.0, bars=(0, 4), octave=0, legato=0.95):
        tpc, steps = key_info(self.key)
        if tonic_midi is None:
            tonic_midi = nearest(tpc, 74)
        tonic_midi += 12 * octave
        b = start
        bar_idx = 0
        acc = 0.0
        for deg, oc, dur in THEME:
            bar_idx = int(acc // 4)
            acc += dur
            if bar_idx < bars[0]:
                continue
            if bar_idx >= bars[1]:
                break
            p = tonic_midi + steps[(deg - 1) % 7] + 12 * (oc + (deg - 1) // 7)
            self.add(part, b, dur * legato, p, vel if (b % 1) < 1e-6 else vel - 8)
            b += dur


def style_hook(c: Ctx):
    c.pad("strings", 50, 69, 46)
    c.root("cello", 38, 50, 58)
    c.theme("celesta", vel=92, bars=(0, 2))
    c.theme("mbox", vel=50, bars=(0, 2), octave=1)
    for k, p in enumerate(voicing(c.chord(0), 62, 86)[:8]):  # opening harp sweep
        c.add("harp", k * 0.125, 1.5, p, 62)


def style_pulse(c: Ctx):
    c.pad("strings", 50, 67, 44)
    c.root("cello", 38, 50, 52)
    c.arp("pizz", 0.5, 50, 64, 62, pattern=(0, 2, 1, 2))
    c.drums(kick=(0,), snare=(), hats=0, kick_vel=70)
    c.theme("celesta", vel=78, bars=(2, 4))


def style_drive(c: Ctx):
    c.pad("strings", 52, 69, 40)
    c.arp("marimba", 0.25, 62, 81, 70, pattern=(0, 1, 2, 3, 2, 1, 0, 2), accent=1.15)
    c.arp("chip", 0.25, 74, 93, 40, pattern=(0, 2, 1, 3))
    c.arp("pizz", 0.5, 45, 60, 66, pattern=(0, 2))
    for b, d, ch in c.chord_spans():
        r, _, _ = chord_tones(ch)
        p = in_range(r, 33, 45)[0]
        k = 0.0
        while k < d - 1e-6:
            c.add("bass", b + k, 0.45, p + (12 if abs((k % 4) - 3.5) < 1e-6 else 0), 84)
            k += 0.5
    syncop = (0, 1.5, 2) if c.I > 0.75 else (0, 2)
    c.drums(kick=syncop, snare=(1, 3), hats=0.25 if c.I > 0.85 else 0.5, hat_vel=44, shaker=0.25 if c.I > 0.85 else None)
    if c.spec.get("theme"):
        c.theme("lead", vel=96, bars=(0, 4))
        c.theme("glock", vel=58, bars=(0, 4), octave=1)


def style_drop(c: Ctx):
    c.root("cello", 36, 47, 70)
    c.pad("strings", 45, 60, 34, max_notes=3)
    for b in range(0, c.n, 2):
        c.add("timp", b, 0.5, in_range(chord_tones(c.chord(b))[0], 40, 52)[0], 54)
        c.add("timp", b + 0.33, 0.5, in_range(chord_tones(c.chord(b))[0], 40, 52)[0], 40)
    tpc, steps = key_info(c.key)
    tonic = nearest(tpc, 86)
    for k, deg in enumerate((1, 5, 3, 2)):  # a slowed music-box echo of the theme
        if 2 * k < c.n:
            c.add("mbox", 2 * k + 1, 1.8, tonic + steps[deg - 1] - (12 if deg == 5 else 0), 46)


def style_void(c: Ctx):
    c.root("cello", 36, 47, 46)


def style_mystery(c: Ctx):
    c.pad("strings", 50, 67, 40)
    c.arp("celesta", 0.5, 62, 81, 64, pattern=(0, 1, 2, 3, 2, 1))
    c.root("cello", 38, 50, 48)
    c.arp("harp", 1.0, 55, 72, 50, pattern=(0, 2, 1))


def style_build(c: Ctx):
    layer = c.spec.get("layer", 1)
    c.pad("strings", 52, 69, 44)
    c.arp("marimba", 0.5, 60, 79, 62, pattern=(0, 1, 2, 1, 2, 3, 2, 1))
    if layer >= 2:
        c.root("bass", 33, 45, 78, every=1.0, dur=0.9)
        c.arp("pizz", 0.5, 50, 64, 50, pattern=(1, 2), start=0.5)
    if layer >= 3:
        c.drums(kick=(0, 2), snare=(1, 3), hats=0.5, hat_vel=36, kick_vel=74, snare_vel=56, sticks=True)
    if layer >= 4:
        c.theme("glock", vel=70, bars=(0, 2), octave=0)
        c.arp("celesta", 1.0, 72, 88, 44, pattern=(2, 1, 0))


def style_twist(c: Ctx):
    for p in voicing(c.chord(0), 45, 70):
        c.add("strings", 0, c.n + 0.1, p, 58)
    c.root("cello", 33, 45, 70)
    for k in range(int(c.n * 4)):
        c.add("timp", k * 0.25, 0.3, in_range(chord_tones(c.chord(0))[0], 40, 52)[0], 36 + k * 3)


def style_rest(c: Ctx):
    pass


def style_frenzy(c: Ctx):
    c.arp("marimba", 0.25, 62, 84, 78, pattern=(0, 1, 2, 3, 1, 2, 3, 4))
    c.arp("pizz", 0.25, 50, 67, 62, pattern=(0, 1, 2, 1))
    c.arp("chip", 0.25, 74, 93, 42, pattern=(0, 2, 3, 1))
    for b, d, ch in c.chord_spans():
        r, _, _ = chord_tones(ch)
        p = in_range(r, 33, 45)[0]
        k = 0.0
        while k < d - 1e-6:
            c.add("bass", b + k, 0.45, p, 86)
            k += 0.5
    b = 0.0
    while b < c.n - 1e-6:  # snare roll rising
        c.add("drums", b, 0.2, SNARE, int(40 + 50 * b / max(1, c.n)))
        if abs(b - round(b)) < 1e-6:
            c.add("drums", b, 0.4, KICK, 90)
        b += 0.25
    c.pad("strings", 52, 72, 52)


def style_crash(c: Ctx):
    # a chromatic slide down in the strings, a timpani roll, then nothing
    top = 79
    steps = int(c.n * 4)
    for k in range(steps):
        c.add("strings", k * 0.25, 0.3, top - k, max(30, 80 - k * 4))
        c.add("pizz", k * 0.25, 0.25, top - 12 - k, max(30, 70 - k * 4))
    for k in range(steps):
        c.add("timp", k * 0.25, 0.3, 38, 70 - k * 2)
    c.add("taiko", c.n - 0.5, 1.0, 50, 112)
    c.add("cello", 0, c.n, 38, 70)


def style_swell(c: Ctx):
    c.pad("strings", 50, 74, 50)
    c.root("cello", 36, 48, 60)
    c.arp("harp", 0.5, 55, 79, 56, pattern=(0, 1, 2, 3))
    n = int(c.n * 4)
    for k in range(max(0, n - 8), n):  # timpani roll into the next downbeat
        c.add("timp", k * 0.25, 0.3, in_range(chord_tones(c.chord(c.n - 1))[0], 40, 52)[0], 50 + (k - n + 8) * 7)
    tick0 = c.s.secs[c.i]["tick0"]
    for k in range(16):  # expression swell
        c.s.cc(tick0 + int(k / 16 * c.n * PPQ), "strings", 11, 70 + k * 3)
    c.s.cc(tick0 + c.n * PPQ, "strings", 11, 110)


def style_anthem(c: Ctx):
    c.pad("strings", 50, 74, 60)
    c.root("cello", 36, 48, 66)
    c.root("bass", 33, 45, 80, every=1.0, dur=0.9)
    c.theme("lead", vel=100, bars=(0, 4))
    c.theme("glock", vel=60, bars=(0, 4), octave=1)
    c.theme("horns", vel=70, bars=(0, 4), octave=-1)
    c.arp("harp", 0.5, 57, 81, 56, pattern=(0, 1, 2, 3, 2, 1))
    c.drums(kick=(0,), snare=(2,), hats=0, kick_vel=78, snare_vel=58, shaker=0.5)


def style_outro(c: Ctx):
    c.pad("strings", 50, 69, 46)
    c.theme("celesta", vel=82, bars=(2, 4))
    c.theme("mbox", vel=44, bars=(2, 4), octave=1)
    c.arp("harp", 1.0, 55, 79, 48, pattern=(0, 1, 2, 3))
    c.root("cello", 36, 48, 50)


STYLES = {"hook": style_hook, "pulse": style_pulse, "drive": style_drive, "drop": style_drop, "void": style_void,
          "mystery": style_mystery, "build": style_build, "twist": style_twist, "rest": style_rest, "frenzy": style_frenzy,
          "crash": style_crash, "swell": style_swell, "anthem": style_anthem, "outro": style_outro}


def accent(score: Score, kind: str, t: float, chord: str = "Dm"):
    r, pcs, _ = chord_tones(chord)
    low = in_range(r, 38, 50)[0]
    if kind in ("hit", "stab"):
        for p in voicing(chord, 55, 76):
            score.at_time(t, 0.35 if kind == "stab" else 0.6, "strings", p, 100)
            score.at_time(t, 0.35, "horns", p, 92)
    if kind == "hit":
        score.at_time(t, 1.2, "timp", low, 118)
        score.at_time(t, 1.5, "drums", CRASH, 96)
        score.at_time(t, 1.0, "taiko", 50, 100)
    if kind == "boom":
        score.at_time(t, 2.0, "taiko", 45, 120)
        score.at_time(t, 2.5, "cello", low - 12 if low - 12 >= 28 else low, 110)
        score.at_time(t, 1.5, "timp", low, 112)
    if kind == "cymbal":
        score.at_time(t, 1.5, "drums", CRASH, 100)
    if kind == "riser":
        # the GM reverse cymbal swells for ~1.6 s; start it so the swell peaks on the cue
        score.at_time(max(0.0, t - 1.55), 1.7, "fx", 60, 110)


def build_music_score(ep: dict, timing: dict) -> np.ndarray:
    spec = ep["music"]
    total = timing["duration"]
    secs = sorted(({**s, "t0": resolve_cue(s["from"], timing)} for s in spec["sections"]), key=lambda s: s["t0"])
    secs[0]["t0"] = 0.0
    score = Score([s["t0"] for s in secs], total, spec.get("bpm", 100))
    for i, s in enumerate(secs):
        for part, prog in s.get("programs", {}).items():
            score.program(i, part, prog)
        STYLES[s["style"]](Ctx(score, i, s))
    for a in spec.get("accents", []):
        accent(score, a["kind"], resolve_cue(a["at"], timing), a.get("chord", "Dm"))

    sf2 = next((p for p in SOUNDFONTS if Path(p).exists()), None)
    if not sf2:
        raise SystemExit("No General MIDI SoundFont found: apt-get install fluidsynth musescore-general-soundfont-small")
    with tempfile.TemporaryDirectory() as td:
        mid = Path(td) / "score.mid"
        wav = Path(td) / "score.wav"
        score.write(mid)
        if spec.get("keepMidi"):
            (Path(spec["keepMidi"])).write_bytes(mid.read_bytes())
        cmd = ["fluidsynth", "-ni", "-q", "-g", str(spec.get("gain", 0.55)), "-r", "48000", "-o", "synth.reverb.room-size=0.62",
               "-o", "synth.reverb.width=0.9", "-o", "synth.reverb.level=0.55", "-o", "synth.chorus.level=1.2", "-F", str(wav), sf2, str(mid)]
        subprocess.run(cmd, check=True, capture_output=True)
        audio, sr = sf.read(wav, always_2d=True)
    if sr != SR:
        audio = resample_poly(audio, SR, sr, axis=0)
    # clear sub-rumble below the kick (headroom for the voice; phone speakers can't play it anyway)
    from scipy.signal import butter, sosfilt
    audio = sosfilt(butter(2, 32, "high", fs=SR, output="sos"), audio, axis=0)
    n = int(total * SR)
    out = np.zeros((n, 2))
    m = min(n, len(audio))
    out[:m] = audio[:m, :2]
    # silence windows (e.g. the beat after "Delete"), with 25 ms fades
    for r in spec.get("rests", []):
        a, b = int(resolve_cue(r["from"], timing) * SR), int(resolve_cue(r["to"], timing) * SR)
        f = int(0.025 * SR)
        g = np.ones(n)
        g[max(0, a): max(0, b)] = 0
        g[max(0, a - f): a] = np.linspace(1, 0, min(f, a))
        g[b: min(n, b + f)] = np.linspace(0, 1, min(f, n - b))
        out *= g[:, None]
    fo = resolve_cue(spec["fadeOut"]["at"], timing) if spec.get("fadeOut") else total - 2.0
    i0 = int(fo * SR)
    i1 = min(n, int((fo + spec.get("fadeOut", {}).get("dur", 1.6)) * SR))
    if i0 < n:
        out[i0:i1] *= np.linspace(1, 0, i1 - i0)[:, None] ** 2
        out[i1:] = 0
    return out
