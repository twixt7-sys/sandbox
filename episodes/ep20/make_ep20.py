"""Writes episodes/ep20/episode.json (EP20: Make Two Nations Enemies Without Making One Evil)."""
import json
from pathlib import Path

ROOT = Path("/home/user/sandbox")
EP = ROOT / "episodes/ep20/episode.json"
old = json.loads(EP.read_text()) if EP.exists() else {}

# ---- Plate geometry (plate px, 1080x1920), measured from gridded plates ----
G = json.loads((Path(__file__).parent / "geom.json").read_text())

TAIL = "Painterly realism, atmospheric perspective, 35mm anamorphic look, soft film grain, original architecture and clothing. No text, no letters, no signage, no logos, no flags, no watermark."
SDXL = {
    "hook": "wide misty river valley at dawn, a calm river winding down the middle, on the left bank a tall weathered memorial standing stone, on the right bank a second tall memorial standing stone facing it across the water, green hills, low mist on the river, empty and quiet, no people, no buildings, no flags",
    "arvel": "a tall weathered memorial standing stone in the left foreground beside the charred black timber frames of a burned village, ash and empty doorways, grey morning, a wide river on the right side, on the far bank of the river many small stone cairns in a field, no people, no flags",
    "dunmere": "a field of many small stacked stone cairns on a dry cracked riverbank, a narrow shrunken river beside them, a tall memorial standing stone among the cairns, cold pale light, on the far hillside across the river the blackened ruins of a burned village, no people, no flags",
}
for k, v in G.get("sdxl", {}).items():
    SDXL[k] = v


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


lines = [
    ("L1", "hook", "What if both kingdoms are telling the truth about the same war?", 0.7, ["both", "truth"]),
    ("L2", "arvel", "Upstream, the stone says: they crossed the river and burned our town.", 0.45, ["burned"]),
    ("L3", "arvel", "True. Look what it leaves out.", 0.85, ["true.", "leaves"]),
    ("L4", "dunmere", "Downstream: they dammed the river, and we starved.", 0.35, ["dammed", "starved."]),
    ("L5", "dunmere", "True too. It leaves out the fire.", 0.85, ["true", "fire."]),
    ("L6", "both", "Different losses, stories and values. Enemies, but neither is evil.", 0.8, ["losses,", "neither"]),
    ("L7", "lesson", "Give each side a true story and a real loss, and you'll never need a villain.", 0.8, ["true", "real", "villain."]),
    ("L8", "cta", "Tag someone who loves morally complicated fantasy.", 0.0, ["tag", "complicated"]),
]

A, D, Hk = G["arvel"], G["dunmere"], G["hook"]

shots = [
    {
        "id": "hook", "scene": "nightSky",
        "plateFrame": {"from": {"s": 1.0, "y": 0}, "to": {"s": 1.06, "y": 0}},
        "plateScrim": 0.5,
        "purpose": "Stop the scroll on the paradox: one river, two memorial stones facing each other across it, and the question of how both can be true.",
        "visual": "A misty river valley at dawn; a tall memorial stone on each bank, facing each other. 'ONE RIVER · ONE WAR / Two truths.'",
        "camera": "Slow push (1.00 to 1.06).",
        "layers": {"foreground": "title", "midground": "the two stones", "background": "the valley"},
        "lighting": "Cold dawn mist; top scrim for the title.",
        "imagePrompt": ip("hook"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["hook"],
        "graphics": [
            {"type": "titleLockup", "kicker": "One river · one war", "text": "Two truths.", "y": 340, "size": 124,
             "start": c("L1", "what", -0.1), "end": c("L1", "war?", 0.55)},
        ],
        "onScreenText": "Kicker 'ONE RIVER · ONE WAR' + 'Two truths.' (ember serif italic).",
        "transition": "Hard cut on 'Upstream' to the first stone.",
        "sfx": [
            {"sound": "water", "from": {"shot": "hook"}, "to": {"shot": "arvel", "offset": 0.8}, "gain": -34},
            {"sound": "wind", "from": {"shot": "hook"}, "to": {"shot": "arvel", "offset": 0.5}, "gain": -36},
            {"sound": "swell", "at": c("L1", "war?", -1.0), "gain": -24},
            {"sound": "drum", "at": c("L1", "war?"), "gain": -22},
        ],
        "music": "A minor, low and open.",
    },
    {
        "id": "arvel", "scene": "nightSky", "transitionIn": {"type": "cut"},
        "plateFrame": A["plateFrame"],
        "plateScrim": 0.35,
        "purpose": "Kingdom 1 (Arvel, upstream): its memorial is true (the raid burned their town), and its frame crops out the river running downstream to Dunmere, whose dead it never mentions.",
        "visual": "Arvel's memorial stone beside the burned village, inside a gilt frame that darkens the rest; the tablet is cut: 'THEY CROSSED THE RIVER / AND BURNED OUR TOWN'. On 'Look' the frame opens and the camera pulls back down the river: LEFT OUT · DOWNSTREAM / Their dead.",
        "camera": "Pull back as the frame opens.",
        "layers": {"foreground": "tablet", "midground": "the stone and the burned village", "background": "the river downstream"},
        "lighting": "Grey morning, ash.",
        "imagePrompt": ip("arvel"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["arvel"],
        "graphics": [
            {"type": "chronicleFrame", "local": True, "frame": A["frame"], "dim": 0.82, "label": "What Arvel keeps",
             "start": {"shot": "arvel"}, "openAt": c("L3", "look", -0.1)},
            *A.get("props", []),
            {"type": "tablet", "at": A["tablet"], "width": 760, "size": 52, "kicker": "Arvel's stone · upstream",
             "lines": ["They crossed the river", "and burned our town"], "start": c("L2", "they", -0.05, nth=1), "dur": 1.9,
             "sealAt": c("L3", "true.", -0.05)},
            {"type": "callout", "local": True, "at": A["leftOut"], "side": A["leftOutSide"], "rise": A["rise"], "dx": A["dx"], "noteSize": 48,
             "label": "Left out · downstream", "note": "Their dead.", "color": "rust", "backdrop": True,
             "start": c("L3", "leaves", 0.05)},
        ],
        "onScreenText": "Tablet 'ARVEL'S STONE · UPSTREAM / THEY CROSSED THE RIVER AND BURNED OUR TOWN', ember TRUE seal; then callout 'LEFT OUT · DOWNSTREAM / Their dead.'",
        "transition": "Hard cut on 'Downstream'.",
        "sfx": [
            {"sound": "wind", "from": {"shot": "arvel"}, "to": {"shot": "dunmere"}, "gain": -35},
            {"sound": "chisel", "at": c("L2", "they", -0.05, nth=1), "gain": -27},
            {"sound": "inferSeal", "at": c("L3", "true.", -0.05), "gain": -26},
            {"sound": "frameOpen", "at": c("L3", "look", -0.15), "gain": -23},
        ],
        "music": "A minor; F major colour under the stone.",
    },
    {
        "id": "dunmere", "scene": "nightSky", "transitionIn": {"type": "cut"},
        "plateFrame": D["plateFrame"],
        "plateScrim": 0.35,
        "purpose": "Kingdom 2 (Dunmere, downstream): its cairns are true too (the dam starved the valley), and its frame crops out the river running upstream to Arvel's burned town.",
        "visual": "Dunmere's cairn field on the cracked riverbank, framed and cut: 'THEY DAMMED THE RIVER / AND WE STARVED'. On 'leaves' the frame opens on the river winding upstream: LEFT OUT · UPSTREAM / Their burned town.",
        "camera": "Pull back as the frame opens.",
        "layers": {"foreground": "tablet", "midground": "the cairns", "background": "the river upstream"},
        "lighting": "Cold, pale, dry.",
        "imagePrompt": ip("dunmere"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["dunmere"],
        "graphics": [
            {"type": "chronicleFrame", "local": True, "frame": D["frame"], "dim": 0.82, "label": "What Dunmere keeps",
             "start": {"shot": "dunmere"}, "openAt": c("L5", "leaves", -0.1)},
            *D.get("props", []),
            {"type": "tablet", "at": D["tablet"], "width": 760, "size": 52, "kicker": "Dunmere's cairns · downstream",
             "lines": ["They dammed the river", "and we starved"], "start": c("L4", "they", -0.05), "dur": 1.6,
             "sealAt": c("L5", "true", -0.05)},
            {"type": "callout", "local": True, "at": D["leftOut"], "side": D["leftOutSide"], "rise": D["rise"], "dx": D["dx"], "noteSize": 48,
             "label": "Left out · upstream", "note": "Their burned town.", "color": "rust", "backdrop": True,
             "start": c("L5", "fire.", -0.1)},
        ],
        "onScreenText": "Tablet 'DUNMERE'S CAIRNS · DOWNSTREAM / THEY DAMMED THE RIVER AND WE STARVED', ember TRUE seal; then callout 'LEFT OUT · UPSTREAM / Their burned town.'",
        "transition": "Dissolve (0.45 s) back to the valley.",
        "sfx": [
            {"sound": "wind", "from": {"shot": "dunmere"}, "to": {"shot": "both", "offset": 0.4}, "gain": -35},
            {"sound": "chisel", "at": c("L4", "they", -0.05), "gain": -27},
            {"sound": "inferSeal", "at": c("L5", "true", -0.05), "gain": -26},
            {"sound": "frameOpen", "at": c("L5", "leaves", -0.15), "gain": -23},
        ],
        "music": "A minor; D minor colour.",
    },
    {
        "id": "both", "scene": "nightSky", "plateFrom": "hook", "transitionIn": {"type": "dissolve", "duration": 0.45},
        "plateFrame": {"from": {"s": 1.06, "y": 0}, "to": {"s": 1.03, "y": 0}},
        "plateScrim": 0.55,
        "plateLook": {"from": "saturate(0.6) brightness(0.55)"},
        "purpose": "Both truths in one frame: the opening valley again, both tablets side by side, each stamped TRUE, and the reasons the two memories differ.",
        "visual": "The hook valley, dimmed, a stone on each bank; both tablets side by side with TRUE seals; rows 'Different losses. / Different stories. / Different values.', then 'ENEMIES / Neither is evil.'",
        "camera": "Gentle pull (1.06 to 1.03).",
        "layers": {"foreground": "tablets and rows", "midground": "the two stones", "background": "the valley"},
        "lighting": "Dimmed dawn.",
        "graphics": [
            {"type": "tablet", "at": Hk["tabletL"], "width": 490, "size": 35, "kickerSize": 21, "kicker": "Arvel remembers", "align": "center",
             "lines": ["They crossed the river", "and burned our town"], "instant": False, "start": {"shot": "both", "offset": 0.1}, "dur": 0.01,
             "sealAt": {"shot": "both", "offset": 0.35}, "sealSize": 22},
            {"type": "tablet", "at": Hk["tabletR"], "width": 490, "size": 35, "kickerSize": 21, "kicker": "Dunmere remembers", "align": "center",
             "lines": ["They dammed the river", "and we starved"], "start": {"shot": "both", "offset": 0.3}, "dur": 0.01,
             "sealAt": {"shot": "both", "offset": 0.55}, "sealSize": 22},
            {"type": "truthRows", "y": Hk.get("rowsY", 800), "size": 66,
             "rows": [{"text": "Different *losses.*", "at": c("L6", "losses,")},
                      {"text": "Different *stories.*", "at": c("L6", "stories")},
                      {"text": "Different *values.*", "at": c("L6", "values.")}],
             "sumKicker": "Enemies", "sum": ["*Neither* is evil."], "sumAt": c("L6", "neither", -0.1), "sumSize": 84},
        ],
        "onScreenText": "Both tablets, TRUE; 'Different losses. / Different stories. / Different values.'; 'ENEMIES / Neither is evil.'",
        "transition": "Dissolve (0.45 s) to the dark valley for the payoff.",
        "sfx": [
            {"sound": "water", "from": {"shot": "both"}, "to": {"shot": "lesson", "offset": 0.5}, "gain": -38},
            {"sound": "inferSeal", "at": {"shot": "both", "offset": 0.35}, "gain": -29},
            {"sound": "inferSeal", "at": {"shot": "both", "offset": 0.55}, "gain": -29},
            {"sound": "tally", "at": c("L6", "losses,"), "gain": -30},
            {"sound": "tally", "at": c("L6", "stories"), "gain": -30},
            {"sound": "tally", "at": c("L6", "values."), "gain": -30},
            {"sound": "tonalDrop", "at": c("L6", "neither", -0.1), "gain": -25},
        ],
        "music": "F major → A minor, settling.",
        "imagePrompt": "", "videoPrompt": "",
    },
    {
        "id": "lesson", "scene": "nightSky", "plateFrom": "hook", "transitionIn": {"type": "dissolve", "duration": 0.45},
        "plateFrame": {"from": {"s": 1.08, "y": 0}, "to": {"s": 1.04, "y": 0}},
        "plateScrim": 0.88,
        "plateLook": {"from": "saturate(0.45) brightness(0.42)"},
        "purpose": "The shareable thought, word by word.",
        "visual": "The valley almost dark; 'Give each side / a true story / and a real loss, / and you'll never / need a villain.' lands word by word.",
        "camera": "Gentle pull (1.08 to 1.04).",
        "layers": {"foreground": "statement", "midground": "", "background": "the valley, dark"},
        "lighting": "Dimmed and cooled under the type.",
        "graphics": [
            {"type": "statement", "lines": ["Give each side", "a *true* story", "and a *real* loss,", "and you'll never", "need a *villain.*"]},
        ],
        "captions": False,
        "onScreenText": "'Give each side a true story and a real loss, and you'll never need a villain.' (word-synced; true / real / villain in amber).",
        "transition": "Dissolve (0.6 s) to the valley at dusk, a lantern lit at each stone.",
        "sfx": [
            {"sound": "swell", "at": c("L7", "real", -0.6), "gain": -26},
            {"sound": "drum", "at": c("L7", "villain.", -0.05), "gain": -22},
        ],
        "music": "A major with bells: the answer.",
        "imagePrompt": "", "videoPrompt": "",
    },
    {
        "id": "cta", "scene": "nightSky", "plateFrom": "hook", "transitionIn": {"type": "dissolve", "duration": 0.6},
        "plateFrame": {"from": {"s": 1.04, "y": 0}, "to": {"s": 1.0, "y": 0}},
        "plateScrim": 0.4,
        "plateLook": {"from": "saturate(0.85) brightness(0.8) sepia(0.25)"},
        "captions": False, "hideLogoBug": True,
        "purpose": "Tag CTA over the opening valley in a changed state: dusk, a lantern lit at the foot of each stone. Both sides mourn. Loops back to the grey dawn hook.",
        "visual": "The same valley at dusk, a small lantern glowing at each stone. Full logo, Episode 20 / 50, the CTA, a 'Tag a friend' pill.",
        "camera": "Settles (1.04 to 1.00).",
        "layers": {"foreground": "logo and CTA type", "midground": "the stones and lanterns", "background": "the valley at dusk"},
        "lighting": "Dusk; the last 0.6 s cross-fades to the dawn hook.",
        "graphics": [
            {"type": "emberDusk", "horizon": Hk.get("horizon", 700)},
            *[{"type": "lanterns", "at": [pt], "size": sz, "start": {"shot": "cta", "offset": 0.2 + 0.5 * i}} for i, (pt, sz) in enumerate(zip(Hk["lanterns"], Hk["lanternSizes"]))],
            {"type": "ctaCard", "start": {"shot": "cta"}, "ctaAt": c("L8", "tag"), "episode": "Episode 20 / 50",
             "title": "Two nations, one war, no villain", "kicker": "Pass it on", "size": 80,
             "lines": ["Tag someone who loves", "morally complicated", "*fantasy.*"], "button": "Tag a friend", "icon": "share"},
        ],
        "onScreenText": "Full logo, 'EPISODE 20 / 50', title, 'PASS IT ON', 'Tag someone who loves morally complicated fantasy.', pill 'Tag a friend'.",
        "transition": "Cross-fade into the hook's first frame (the dawn valley) for a seamless loop.",
        "sfx": [
            {"sound": "water", "from": {"shot": "cta"}, "to": c("L8", "fantasy.", 1.0), "gain": -36},
            {"sound": "swell", "at": {"shot": "cta", "offset": -0.3}, "gain": -25},
            {"sound": "chimes", "at": c("L8", "fantasy.", 0.2), "gain": -24},
        ],
        "music": "D to A major, warm; fades fully before the last frame.",
        "imagePrompt": "", "videoPrompt": "",
    },
]

ep = {
    "id": "ep20", "number": 20, "title": "Make Two Nations Enemies Without Making One Evil",
    "voice": {
        "provider": "kokoro", "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.0},
        "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                       "settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}},
        "direction": "A calm, fair guide who takes neither side. A real question on the hook. Each inscription is read plainly, as a quote, never as an accusation; 'True.' is said with weight, then 'Look what it leaves out' quietly, like noticing something. 'Downstream' mirrors 'Upstream'. The lesson is clear and even; 'neither is evil' lands softly. The tag CTA is friendly. No trailer voice.",
    },
    "timing": {"leadIn": 0.25, "tail": 1.5, "shotLead": 0.12},
    "lines": [{"id": i, "shot": s, "text": t, "pauseAfter": p, "emphasis": e} for i, s, t, p, e in lines],
    "shots": shots,
    "lesson": "Two nations can remember the same war truthfully and still disagree, because each lost something different, inherited a different story about it, and holds a different value sacred; each memorial frames out the other side's dead. Enemies are more interesting when both sides have a true story and a real loss: then no villain is needed.",
    "captionReplace": {},
    "music": {
        "key": "A minor, resolving to A major",
        "drone": ["A1", "E2"],
        "events": [
            {"type": "duck", "at": c("L3", "look"), "pre": 0.15, "dur": 1.4, "gain": 0.6},
            {"type": "duck", "at": c("L5", "it", nth=1), "pre": 0.15, "dur": 1.4, "gain": 0.6},
            {"type": "duck", "at": c("L7", "give"), "pre": 0.15, "dur": 1.2, "gain": 0.65},
        ],
        "sections": {
            "hook": {"chords": [["A1", "E2", "C3", "E3", "B3"]], "level": 0.46, "dark": True},
            "arvel": {"chords": [["F1", "C2", "A2", "E3"], ["A1", "E2", "C3", "E3"]], "level": 0.5, "pulse": 64},
            "dunmere": {"chords": [["D2", "A2", "F3", "A3"], ["A1", "E2", "C3", "E3"]], "level": 0.5, "pulse": 64},
            "both": {"chords": [["F1", "C2", "A2", "E3", "G3"], ["G1", "D2", "B2", "D3"]], "level": 0.56, "pulse": 64},
            "lesson": {"chords": [["F1", "C2", "A2", "C3"], ["A1", "E2", "C#3", "E3", "B3"]], "level": 0.62, "bells": True},
            "cta": {"chords": [["D2", "A2", "F#3", "A3"], ["A1", "E2", "C#3", "E3", "A3"]], "level": 0.58, "bells": True},
        },
    },
}

DESC = (
    "What if both kingdoms are telling the truth about the same war?\n\n"
    "Upstream, Arvel's memorial stone says: they crossed the river and burned our town. True. Downstream, Dunmere's cairns say: "
    "they dammed the river, and we starved. Also true. Each memorial frames out the other side's dead.\n\n"
    "Nations remember the same event differently because they lost different things, inherited different stories and hold "
    "different values sacred. That is how two peoples stay enemies without either being evil. Give each side a true story and "
    "a real loss, and you'll never need a villain.\n\n"
    "Tag someone who loves morally complicated fantasy.\n\n"
)
TAGS = "#Worldbuilding #FantasyWriting #WritingTips #FantasyWar #WorldcraftShorts"
ep["metadata"] = {
    "youtube": {
        "title": "Two Kingdoms, One War, Both Telling the Truth (Worldbuilding)",
        "titleAlternate": "Make two nations enemies without making one evil",
        "description": DESC + "Episode 20 of 50 in Worldcraft Shorts: Worldbuilding, from the ground up. Short lessons for fantasy writers, novelists, mapmakers and tabletop RPG creators.\n\n" + TAGS,
        "pinnedComment": "Your turn: two nations in your world, one shared event. What does each side carve on its memorial, and what does it leave out?",
        "uploadSettings": "Altered or synthetic content: Yes (AI-generated stills and synthetic narration; see docs/DISTRIBUTION.md). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "One war, two memorials, both true 🪨 One remembers the fire, the other the famine. Neither is the villain. Tag someone who loves morally complicated fantasy. " + TAGS,
        "pinnedComment": "What does the other side's memorial leave out in your world?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": DESC + "Episode 20 of 50.\n\n" + TAGS,
        "pinnedComment": "Which loss does each nation in your world remember, and which one does it forget?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": "Both true. Neither evil.\n\n" + DESC + "Episode 20 of 50 · Worldcraft Shorts\n\n" + TAGS,
        "hookCheck": "First 24 characters: 'Both true. Neither evil.'",
        "pinnedComment": "Fire or famine: which memory would your nation carve in stone, and who did it leave out?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
}
EP.write_text(json.dumps(ep, indent=1, ensure_ascii=True) + "\n")
words = sum(len(t.split()) for _, _, t, _, _ in lines)
print("words", words, "tiktok", len(ep["metadata"]["tiktok"]["caption"]), "yt title", len(ep["metadata"]["youtube"]["title"]))
