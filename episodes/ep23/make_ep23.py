"""Writes episodes/ep23/episode.json (EP23: Make Magic Expensive Without Using Mana).

Run from anywhere: `python episodes/ep23/make_ep23.py`. Plate geometry (plate px, 1080x1920) lives in GEOM below and was
measured from gridded plates. Keep cues word-addressed; `nth` picks a repeated word.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EP = ROOT / "episodes/ep23/episode.json"

MEMORY = "#f3b9c8"  # EP23 motif colour: memory, a pale rose (the spell's light and the memories it takes)

TAIL = "Painterly realism, atmospheric perspective, 35mm anamorphic look, soft film grain, original architecture and clothing. No text, no letters, no signage, no logos, no watermark."
SDXL = {
    "hook": "a young woman with short dark hair in a plum wool coat sits at a wooden desk by candlelight writing in a thick open leather journal with a quill, seen from the side, face half in shadow, shelves of glass jars behind her, small attic room at night, medium shot",
    "storm": "seen from behind, a lone young woman in a plum wool hooded cloak stands on a stone harbour wall raising one open hand toward a dark storm over the sea, huge grey waves, small fishing boats tied below, a break of pale light opening in the clouds above, wide shot",
    "door": "a weathered blue wooden cottage front door with black iron hinges and a small blank brass plate at eye level, climbing pink roses around the stone doorframe, a warm lit window beside it, evening light, quiet village lane, no people",
    "sister": "seen from behind in the foreground, a young woman in a plum wool hooded cloak stands in a village lane facing a smiling young woman in a green dress who waves warmly from an open wooden garden gate in front of a stone cottage, soft morning light, medium wide shot",
}

# Plate geometry (plate px), measured from the gridded plates.
GEOM = {
    "hook": {"hand": [600, 1080], "book": [560, 1150]},
    "storm": {"hand": [640, 760]},
    "door": {"plate": [540, 820], "window": [860, 900], "plateW": 220, "plateRot": 0},
    "sister": {"face": [700, 900]},
}


def ip(k):
    return f"(Generated locally: see sdxlPrompt; Figma credits are out until 1 Nov 2026.) Vertical 9:16 cinematic fantasy documentary still. {SDXL[k]}. {TAIL}"


def c(line, word=None, offset=0.0, nth=None):
    d = {"line": line}
    if word:
        d["word"] = word
    if offset:
        d["offset"] = round(offset, 3)
    if nth:
        d["nth"] = nth
    return d


def sh(shot, offset=0.0):
    d = {"shot": shot}
    if offset:
        d["offset"] = offset
    return d


lines = [
    ("L1", "hook", "What if every spell stole one of your memories?", 0.5, ["every", "memories?"]),
    ("L2", "ledger", "Wren keeps a ledger of what she still remembers.", 0.45, ["ledger", "remembers."]),
    ("L3", "storm", "She stills a storm. Her first snow is gone.", 0.45, ["storm.", "gone."]),
    ("L4", "door", "She breaks a fever. Her mother's name fades.", 0.45, ["fever.", "fades."]),
    ("L5", "sister", "One more spell, and her sister is a stranger.", 0.6, ["stranger."]),
    ("L6", "choice", "Only her own name is left. Is the next spell worth it?", 0.8, ["own", "worth"]),
    ("L7", "lesson", "Years, warmth, a sense: a real price makes every spell a choice.", 0.6, ["real", "choice."]),
    ("L8", "cta", "Comment the strangest price someone could pay for magic.", 0.0, ["comment", "strangest"]),
]

# The ledger: one line per memory, written on L2, struck one per spell.
LEDGER_LINES = [
    {"num": "I", "text": "My first snow", "at": c("L2", "ledger", -0.05), "strikeAt": c("L3", "gone.", -0.1)},
    {"num": "II", "text": "Mother's name", "at": c("L2", "what", -0.05), "strikeAt": c("L4", "fades.", -0.1)},
    {"num": "III", "text": "My sister's face", "at": c("L2", "still", -0.05), "strikeAt": c("L5", "stranger.", -0.15)},
    {"num": "IV", "text": "My own name", "at": c("L2", "remembers.", -0.05)},
]


def ledger(**kw):
    g = {"type": "memoryLedger", "kicker": "What I remember", "title": "Wren", "lines": LEDGER_LINES, "motif": MEMORY}
    g.update(kw)
    return g


CORNER = {"x": 90, "y": 336, "s": 0.6}
H, S, D, SI = GEOM["hook"], GEOM["storm"], GEOM["door"], GEOM["sister"]

shots = [
    {
        "id": "hook", "scene": "nightSky",
        "plateFrame": {"from": {"s": 1.0, "y": 0}, "to": {"s": 1.06, "y": 0}},
        "plateScrim": 0.5,
        "purpose": "Stop the scroll on the price: a caster writing down what she still remembers, and the hook's question.",
        "visual": "A young woman writes by candlelight in a thick journal; a pale rose glow (code) breathes at her hand. 'EVERY SPELL TAKES A MEMORY / Which one goes?'",
        "camera": "Slow push (1.00 to 1.06).",
        "layers": {"foreground": "title", "midground": "Wren and the journal", "background": "jars on shelves, the attic"},
        "lighting": "Candlelight; top scrim for the title.",
        "imagePrompt": ip("hook"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["hook"],
        "graphics": [
            {"type": "mendGlow", "local": True, "at": H["hand"], "r": 44, "color": MEMORY, "start": sh("hook", 0.1),
             "pulses": [c("L1", "spell", -0.05)], "ringMax": 200},
            {"type": "titleLockup", "kicker": "Every spell takes a memory", "text": "Which one goes?", "y": 340, "size": 120,
             "start": c("L1", "what", -0.1), "end": c("L1", "memories?", 0.45)},
        ],
        "onScreenText": "Kicker 'EVERY SPELL TAKES A MEMORY' + 'Which one goes?' (ember serif italic).",
        "transition": "Dissolve (0.35 s) on 'Wren' into the ledger.",
        "sfx": [
            {"sound": "hearth", "from": sh("hook"), "to": sh("ledger", 0.6), "gain": -36},
            {"sound": "recall", "at": c("L1", "spell", -0.05), "gain": -22},
        ],
        "music": "D minor, hushed.",
    },
    {
        "id": "ledger", "scene": "nightSky", "plateFrom": "hook",
        "transitionIn": {"type": "dissolve", "duration": 0.35},
        "plateFrame": {"from": {"s": 1.06, "y": 0}, "to": {"s": 1.08, "y": 0}},
        "plateScrim": 0.6, "plateLook": {"from": "saturate(0.7) brightness(0.55)"},
        "purpose": "Show the price as a list: the ledger of the four memories she has left, written in as she names them.",
        "visual": "The attic dims; the ledger card (code) fills the frame: 'WHAT I REMEMBER / Wren', four lines written in: I My first snow, II Mother's name, III My sister's face, IV My own name.",
        "camera": "Slow push (1.06 to 1.08).",
        "layers": {"foreground": "the ledger", "midground": "", "background": "the dimmed attic"},
        "lighting": "Dimmed candlelight.",
        "imagePrompt": "(Reuses the hook plate.)", "videoPrompt": "(Not used.)",
        "graphics": [ledger(at={"x": 140, "y": 400, "s": 1.0}, dim=0.55, start=sh("ledger", -0.1))],
        "onScreenText": "Ledger 'WHAT I REMEMBER / Wren' with four lines.",
        "transition": "Hard cut on 'She' to the harbour; the ledger glides to the corner.",
        "sfx": [{"sound": "quill", "at": l["at"], "gain": -27} for l in LEDGER_LINES],
        "music": "D minor; a pulse starts.",
    },
    {
        "id": "storm", "scene": "nightSky",
        "transitionIn": {"type": "cut"},
        "plateFrame": {"from": {"s": 1.04, "y": 0}, "to": {"s": 1.08, "y": 0}},
        "plateScrim": 0.4,
        "purpose": "Spell I and its price: the storm stills, and the first line is struck.",
        "visual": "Wren on a harbour wall, hand raised to a storm; a rose glow at her hand sends rings into the clouds. In the corner the ledger strikes I: My first snow, and a mote of light drifts away.",
        "camera": "Slow push (1.04 to 1.08).",
        "layers": {"foreground": "ledger", "midground": "Wren and the glow", "background": "the storm breaking"},
        "lighting": "Storm grey; pale light opening above.",
        "imagePrompt": ip("storm"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["storm"],
        "graphics": [
            {"type": "mendGlow", "local": True, "at": S["hand"], "r": 46, "color": MEMORY, "start": c("L3", "she", -0.1),
             "pulses": [c("L3", "stills", -0.05), c("L3", "storm.", -0.05)], "ringMax": 520, "ringDur": 1.5, "end": c("L3", "gone.", 0.4)},
            ledger(at=CORNER, start=sh("storm"), active=0, instant=True),
        ],
        "onScreenText": "Ledger in the corner; line I struck.",
        "transition": "Hard cut on 'She'.",
        "sfx": [
            {"sound": "wind", "from": sh("storm"), "to": c("L3", "storm.", 0.4), "gain": -32},
            {"sound": "recall", "at": c("L3", "stills", -0.05), "gain": -22},
            {"sound": "forget", "at": c("L3", "gone.", -0.1), "gain": -23},
        ],
        "music": "Bb major 7: the storm lifts, something goes with it.",
    },
    {
        "id": "door", "scene": "nightSky",
        "transitionIn": {"type": "cut"},
        "plateFrame": {"from": {"s": 1.04, "y": 0}, "to": {"s": 1.08, "y": 0}},
        "plateScrim": 0.4,
        "purpose": "Spell II and its price: a fever broken behind a warm window, and her mother's name fades from the door.",
        "visual": "A blue cottage door; the window beside it glows rose for a moment (the fever breaks). The name MAREN, painted on the door's plate in code, fades letter by letter; the ledger strikes II.",
        "camera": "Slow push (1.04 to 1.08).",
        "layers": {"foreground": "ledger", "midground": "the name on the door", "background": "the lit window"},
        "lighting": "Evening; warm window.",
        "imagePrompt": ip("door"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["door"],
        "graphics": [
            {"type": "mendGlow", "local": True, "at": D["window"], "r": 40, "color": MEMORY, "start": c("L4", "breaks", -0.15),
             "pulses": [c("L4", "fever.", -0.05)], "ringMax": 200, "end": c("L4", "name", 0.0)},
            {"type": "fadingName", "local": True, "text": "Maren", "at": D["plate"], "width": D["plateW"], "rotate": D["plateRot"],
             "start": sh("door"), "fadeAt": c("L4", "name", -0.05), "fadeDur": 1.2},
            ledger(at=CORNER, start=sh("door"), active=1, instant=True),
        ],
        "onScreenText": "The name 'Maren' on the door fades; ledger line II struck.",
        "transition": "Hard cut on 'One'.",
        "sfx": [
            {"sound": "room", "from": sh("door"), "to": sh("sister"), "gain": -38},
            {"sound": "recall", "at": c("L4", "fever.", -0.05), "gain": -23},
            {"sound": "forget", "at": c("L4", "fades.", -0.1), "gain": -23},
        ],
        "music": "G minor.",
    },
    {
        "id": "sister", "scene": "nightSky",
        "transitionIn": {"type": "cut"},
        "plateFrame": {"from": {"s": 1.04, "y": 0}, "to": {"s": 1.08, "y": 0}},
        "plateScrim": 0.4,
        "purpose": "Spell III and the cost made personal: her sister waves, and Wren doesn't know her. Shown with tenderness.",
        "visual": "A woman waves warmly from a garden gate; Wren, seen from behind, doesn't wave back. Callout 'HER SISTER' struck to 'A KIND STRANGER'; the ledger strikes III.",
        "camera": "Slow push (1.04 to 1.08).",
        "layers": {"foreground": "ledger, callout", "midground": "the sister at the gate", "background": "the cottage"},
        "lighting": "Soft morning.",
        "imagePrompt": ip("sister"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["sister"],
        "graphics": [
            ledger(at=CORNER, start=sh("sister"), active=2, instant=True),
            {"type": "callout", "at": SI["face"], "label": "Her sister", "note": "Waving hello", "side": "left", "reach": 110, "rise": -90,
             "backdrop": True, "start": c("L5", "sister", -0.1),
             "then": {"label": "A stranger", "note": "Who is she?", "color": "rust", "at": c("L5", "stranger.", -0.1)}},
        ],
        "onScreenText": "Callout 'HER SISTER / Ilse', struck to 'A STRANGER / Who is she?'; ledger line III struck.",
        "transition": "Dissolve (0.45 s) to the ledger.",
        "sfx": [
            {"sound": "market", "from": sh("sister"), "to": sh("choice", 0.3), "gain": -40},
            {"sound": "recall", "at": c("L5", "spell,", -0.05), "gain": -24},
            {"sound": "forget", "at": c("L5", "stranger.", -0.15), "gain": -22},
        ],
        "music": "Eb major 7, tender.",
    },
    {
        "id": "choice", "scene": "nightSky", "plateFrom": "hook",
        "transitionIn": {"type": "dissolve", "duration": 0.45},
        "plateFrame": {"from": {"s": 1.08, "y": 0}, "to": {"s": 1.1, "y": 0}},
        "plateScrim": 0.7, "plateLook": {"from": "saturate(0.5) brightness(0.45)"},
        "purpose": "The turn: one line is left, and it is her own name. The cost is now a choice.",
        "visual": "The ledger returns large over the dimmed attic: I–III struck, IV 'My own name' glowing and breathing. 'Worth it?' lands beneath.",
        "camera": "Slow push (1.08 to 1.10).",
        "layers": {"foreground": "the ledger, 'Worth it?'", "midground": "", "background": "the dimmed attic"},
        "lighting": "Nearly dark; the last line carries the light.",
        "imagePrompt": "(Reuses the hook plate.)", "videoPrompt": "(Not used.)",
        "graphics": [
            ledger(at={"x": 140, "y": 360, "s": 1.0}, from_=None, dim=0.6, start=sh("choice", -0.2), active=3, hoverAt=c("L6", "own", -0.1)),
            {"type": "oversizedWord", "text": "Worth it?", "y": 1010, "size": 170, "start": c("L6", "worth", -0.1)},
        ],
        "onScreenText": "Ledger: three struck lines, 'My own name' glowing; 'Worth it?'.",
        "transition": "Dissolve (0.45 s) to the lesson.",
        "sfx": [{"sound": "recall", "at": c("L6", "own", -0.1), "gain": -26}],
        "music": "D minor, held; ducked under the question.",
    },
    {
        "id": "lesson", "scene": "nightSky", "plateFrom": "storm",
        "transitionIn": {"type": "dissolve", "duration": 0.45},
        "plateFrame": {"from": {"s": 1.05, "y": 0}, "to": {"s": 1.03, "y": 0}},
        "plateScrim": 0.85, "plateLook": {"from": "saturate(0.4) brightness(0.38)"},
        "purpose": "The lesson: other prices than mana, then the principle: a real price turns each spell into a decision.",
        "visual": "The ledger lifts small; price chips land: YEARS · WARMTH · A SENSE · A MEMORY; then 'MAKE IT COST / A real price makes every spell a choice.'",
        "camera": "Slow pull (1.05 to 1.03).",
        "layers": {"foreground": "lesson type", "midground": "price chips", "background": "the dimmed harbour"},
        "lighting": "Night-dimmed; rose chips carry the light.",
        "imagePrompt": "(Reuses the storm plate.)", "videoPrompt": "(Not used.)",
        "graphics": [
            ledger(at={"x": 140, "y": 360, "s": 1.0}, start=sh("lesson", -0.45), instant=True,
                   liftAt=sh("lesson", 0.0), lift={"x": 330, "y": 336, "s": 0.55},
                   prices=[{"text": "Years", "at": c("L7", "years,", -0.05)}, {"text": "Warmth", "at": c("L7", "warmth,", -0.05)},
                           {"text": "A sense", "at": c("L7", "sense:", -0.05)}, {"text": "A memory", "at": c("L7", "sense:", 0.35)}],
                   pricesTop=760,
                   lessonKicker="Make it cost", lessonText=["A real price makes", "*every* *spell* *a* *choice.*"],
                   lessonAt=c("L7", "real", -0.1), lessonTop=980),
        ],
        "onScreenText": "Chips 'YEARS · WARMTH · A SENSE · A MEMORY'; 'MAKE IT COST' / 'A real price makes every spell a choice.'",
        "transition": "Dissolve (0.6 s) to the attic at dawn.",
        "sfx": [{"sound": "paper", "at": c("L7", "years,", -0.05), "gain": -30},
                {"sound": "paper", "at": c("L7", "warmth,", -0.05), "gain": -30},
                {"sound": "paper", "at": c("L7", "sense:", -0.05), "gain": -30},
                {"sound": "swell", "at": c("L7", "real", -0.3), "gain": -27}],
        "music": "Bb to D major: resolving.",
    },
    {
        "id": "cta", "scene": "nightSky", "plateFrom": "hook",
        "transitionIn": {"type": "dissolve", "duration": 0.6},
        "plateFrame": {"from": {"s": 1.06, "y": 0}, "to": {"s": 1.0, "y": 0}},
        "plateScrim": 0.45, "plateLook": {"from": "sepia(0.2) saturate(0.85) brightness(0.6)"},
        "captions": False, "hideLogoBug": True,
        "purpose": "Comment CTA over the opening attic, the glow still at her hand; loops back to the hook.",
        "visual": "The hook's attic, dimmed; the rose glow at her hand; CTA card with the 'Comment below' pill.",
        "camera": "Slow pull back (1.06 to 1.00) toward the hook framing for the loop.",
        "layers": {"foreground": "CTA card", "midground": "the glow", "background": "the attic"},
        "lighting": "Dim candlelight under the card.",
        "imagePrompt": "(Reuses the hook plate.)", "videoPrompt": "(Not used.)",
        "graphics": [
            {"type": "mendGlow", "local": True, "at": H["hand"], "r": 44, "color": MEMORY, "start": sh("cta", -0.6)},
            {"type": "ctaCard", "start": sh("cta"), "ctaAt": c("L8", "comment"), "episode": "Episode 23 / 50",
             "title": "Make magic expensive without mana", "kicker": "Your turn", "size": 72,
             "lines": ["Comment the strangest", "price someone could", "*pay* *for* *magic.*"], "button": "Comment below"},
        ],
        "onScreenText": "Full logo, 'EPISODE 23 / 50', title, 'YOUR TURN', 'Comment the strangest price someone could pay for magic.', pill 'Comment below'.",
        "transition": "Cross-fade into the hook's first frame for a seamless loop.",
        "sfx": [
            {"sound": "hearth", "from": sh("cta"), "to": c("L8", "magic.", 1.0), "gain": -37},
            {"sound": "swell", "at": sh("cta", -0.3), "gain": -26},
            {"sound": "chimes", "at": c("L8", "magic.", 0.2), "gain": -24},
        ],
        "music": "G to D major, warm; fades fully before the last frame.",
    },
]

# `from_` is a Python-keyword dodge; drop None entries.
for s in shots:
    for g in s["graphics"]:
        g.pop("from_", None)

music = {
    "key": "D minor, resolving to D major",
    "drone": ["D2", "A2"],
    "events": [
        {"type": "duck", "at": c("L6", "is", nth=2), "pre": 0.15, "dur": 1.8, "gain": 0.55},
        {"type": "duck", "at": c("L7", "real"), "pre": 0.15, "dur": 1.6, "gain": 0.6},
    ],
    "sections": {
        "hook": {"chords": [["D2", "A2", "F3", "A3", "E4"]], "level": 0.46, "dark": True},
        "ledger": {"chords": [["D2", "A2", "F3", "C4"]], "level": 0.5, "pulse": 66},
        "storm": {"chords": [["Bb1", "F2", "D3", "A3"]], "level": 0.54, "pulse": 72},
        "door": {"chords": [["G1", "D2", "Bb2", "F3"]], "level": 0.54, "pulse": 72},
        "sister": {"chords": [["Eb2", "Bb2", "G3", "D4"]], "level": 0.52, "pulse": 66},
        "choice": {"chords": [["D2", "A2", "F3", "A3"]], "level": 0.42, "dark": True},
        "lesson": {"chords": [["Bb1", "F2", "D3", "A3"], ["D2", "A2", "F#3", "A3", "E4"]], "level": 0.6, "bells": True},
        "cta": {"chords": [["G2", "D3", "B3", "D4"], ["D2", "A2", "F#3", "A3", "D4"]], "level": 0.58, "bells": True},
    },
}

DESC = (
    "What if every spell stole one of your memories?\n\n"
    "Wren keeps a ledger of what she still remembers. She stills a storm, and her first snow is gone. She breaks a fever, "
    "and her mother's name fades. One more spell, and her sister is a stranger. Now only her own name is left. Is the next spell worth it?\n\n"
    "Magic doesn't need mana to be expensive. It can cost strength, years of life, warmth, a sense, someone's standing, a rare "
    "material, or a memory. A real price makes every spell a choice, and choices make drama.\n\n"
    "Comment the strangest price someone could pay for magic.\n\n"
)
TAGS = "#Worldbuilding #FantasyWriting #MagicSystem #WritingTips #WorldcraftShorts"
UP_YT = "Altered or synthetic content: Yes (AI-generated stills and synthetic narration; see docs/DISTRIBUTION.md). Not made for kids. Category: Education."
metadata = {
    "youtube": {
        "title": "Make Magic Expensive Without Using Mana (Worldbuilding)",
        "titleAlternate": "What if every spell stole one of your memories?",
        "description": DESC + "Episode 23 of 50 in Worldcraft Shorts: Worldbuilding, from the ground up. Short lessons for fantasy writers, novelists, mapmakers and tabletop RPG creators.\n\n" + TAGS,
        "pinnedComment": "Your turn: what's the strangest price someone could pay for magic? Bonus points if it forces a hard choice.",
        "uploadSettings": UP_YT,
    },
    "tiktok": {
        "caption": "Every spell costs her a memory 🕯️ First snow, gone. Mother's name, gone. Her sister, a stranger. One line left: her own name. Is the next spell worth it? Comment the strangest price for magic. " + TAGS,
        "pinnedComment": "Drop the strangest price your magic could charge. Years? Warmth? Your shadow?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": DESC + "Episode 23 of 50.\n\n" + TAGS,
        "pinnedComment": "Which price would stop you casting: a memory, a year of your life, or your sense of taste?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": "Every spell takes a memory.\n\n" + DESC + "Episode 23 of 50 · Worldcraft Shorts\n\n" + TAGS,
        "hookCheck": "First 27 characters: 'Every spell takes a memory.'",
        "pinnedComment": "Name a price for magic that would make *you* hesitate. Strangest one wins.",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
    "cover": "Worldcraft_Short_E23_cover.jpg: Wren writing by candlelight, the rose glow at her hand, 'EVERY SPELL TAKES A MEMORY / Which one goes?' above, corner logo.",
    "followUpQuestion": "Pick a price for your magic system. What would your caster refuse to pay, and what would make them pay it anyway?",
}

ep = {
    "id": "ep23", "number": 23, "title": "Make Magic Expensive Without Using Mana",
    "voice": {
        "provider": "kokoro",
        "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.0},
        "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                       "settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}},
        "direction": "A calm, warm guide. The hook is a real, slightly uneasy question. Each spell line is two beats: the deed, then the price, softer. 'Her sister is a stranger' is tender, not tragic. 'Is the next spell worth it?' is a genuine question, left hanging. The lesson is clear and sure; the comment CTA friendly. No trailer voice.",
    },
    "timing": {"leadIn": 0.25, "tail": 1.5, "shotLead": 0.12},
    "lines": [{"id": i, "shot": s, "text": t, "pauseAfter": p, "emphasis": e} for i, s, t, p, e in lines],
    "shots": shots,
    "lesson": "Magic doesn't need mana to be expensive. A spell can cost strength, time, years of life, warmth, a sense, social standing, rare materials, emotional stability or a memory. The best price is one the caster truly values, so every spell becomes a decision: is this worth what it takes?",
    "captionReplace": {},
    "music": music,
    "metadata": metadata,
}

EP.write_text(json.dumps(ep, indent=1, ensure_ascii=False) + "\n")
print("wrote", EP)
