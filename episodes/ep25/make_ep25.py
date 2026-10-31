"""Writes episodes/ep25/episode.json (EP25: The Strongest Magic System Has Weaknesses).

Run from anywhere: `python episodes/ep25/make_ep25.py`. Plate geometry (plate px, 1080x1920) lives in GEOM below and was
measured from gridded plates. The courtyard plan is in screen px (PLAN). Keep cues word-addressed; `nth` picks a repeated word.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
from prompts_ep25 import SDXL  # noqa: E402

EP = HERE / "episode.json"
GAZE = "#c7b8f5"  # EP25 motif colour: her sight, a pale lilac
TAIL = "Painterly realism, atmospheric perspective, 35mm anamorphic look, soft film grain, original architecture and clothing. No text, no letters, no signage, no logos, no watermark."

# Plate geometry (plate px), measured from the gridded plates.
GEOM = {
    "hook": {"eye": [540, 1005], "look": [565, 560], "sway": [170, 20, 4.5]},
    "erase": {"from": [-200, 200], "gate": [[272, 588], [806, 600], [806, 1662], [272, 1662]], "land": [540, 1000]},
    "heroes": {"from": [1300, -150], "to": [-250, 760]},
    "mirror": {"eye": [578, 1045], "mirror": [330, 590], "down": [1220, 1380], "lanterns": [[240, 1062]]},
}

# The courtyard plan (screen px). The eye sits on the top wall; cover casts blind spots below it.
YARD = [150, 500, 930, 1140]
EYE = [540, 500]
PILLARS = [
    {"rect": [300, 640, 360, 700]},
    {"rect": [720, 640, 780, 700]},
    {"circle": [540, 820, 48]},
]


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
    ("L1", "hook", "The secret to a terrifying wizard isn't making them unbeatable.", 0.6, ["terrifying", "unbeatable."]),
    ("L2", "erase", "Meet the Unmaker. Anything she can see, she can erase.", 0.55, ["unmaker.", "erase."]),
    ("L3", "plan", "But only what she can see.", 0.8, ["only", "see."]),
    ("L4", "heroes", "So the heroes stop fighting, and start thinking.", 0.5, ["stop", "thinking."]),
    ("L5", "path", "Smoke. Fog. A wall. Every shadow becomes a path.", 0.7, ["shadow", "path."]),
    ("L6", "mirror", "And she has to plan too: mirrors, lanterns, a higher tower.", 0.6, ["she", "too:"]),
    ("L7", "lesson", "Unbeatable is boring. A weakness turns a fight into a puzzle.", 0.6, ["boring.", "puzzle."]),
    ("L8", "cta", "Follow for more ways to make fictional powers interesting.", 0.0, ["follow", "interesting."]),
]

SMOKE = {"circle": [770, 925, 82], "kind": "smoke", "label": "Smoke"}
FOG = {"circle": [320, 985, 96], "kind": "fog", "label": "Fog"}
WALL = {"rect": [470, 1012, 690, 1036], "kind": "wall", "label": "Wall", "labelAt": [580, 1070]}
ROUTE = [[540, 1128], [600, 1080], [790, 1080], [830, 1010], [800, 760], [905, 700], [905, 540]]


def plan(**kw):
    g = {"type": "sightPlan", "yard": YARD, "eye": EYE, "spread": 30, "range": 900, "sweep": [62, 118, 4.6], "blocks": [dict(b) for b in PILLARS]}
    g.update(kw)
    return g


H, E, HE, M = GEOM["hook"], GEOM["erase"], GEOM["heroes"], GEOM["mirror"]

shots = [
    {
        "id": "hook", "scene": "nightSky",
        "plateFrame": {"from": {"s": 1.0, "y": 0}, "to": {"s": 1.06, "y": 0}},
        "plateScrim": 0.5,
        "purpose": "Stop the scroll on the caster: a cloaked figure on a high balcony whose sight sweeps the misty castle like a searchlight, and the hook's promise that her terror isn't invincibility.",
        "visual": "A cloaked woman on a high arched balcony, seen from behind, over a misty castle at dusk; a pale lilac beam (code) reaches from her hood into the mist and slowly sweeps. 'THE TERRIFYING WIZARD / isn\'t unbeatable.'",
        "camera": "Slow push (1.00 to 1.06).",
        "layers": {"foreground": "title", "midground": "the Unmaker and her sight", "background": "the misty castle"},
        "lighting": "Cold dusk; top scrim for the title.",
        "imagePrompt": ip("hook"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["hook"],
        "graphics": [
            {"type": "gazeBeam", "local": True, "points": [H["eye"], H["look"]], "widths": [22, 420], "sway": H["sway"], "opacity": 1.0, "start": sh("hook", 0.15), "flares": [c("L1", "terrifying", -0.05)]},
            {"type": "titleLockup", "kicker": "The terrifying wizard", "text": "isn't unbeatable.", "y": 340, "size": 120,
             "start": c("L1", "the", -0.1), "end": c("L1", "unbeatable.", 0.5)},
        ],
        "onScreenText": "Kicker 'THE TERRIFYING WIZARD' + 'isn\'t unbeatable.' (ember serif italic).",
        "transition": "Hard cut on 'Meet' to the gate.",
        "sfx": [
            {"sound": "wind", "from": sh("hook"), "to": sh("erase", 0.5), "gain": -34},
            {"sound": "gaze", "at": sh("hook", 0.1), "gain": -24},
            {"sound": "gaze", "at": c("L1", "terrifying", -0.05), "gain": -26},
        ],
        "music": "C minor, hushed and cold.",
    },
    {
        "id": "erase", "scene": "nightSky",
        "transitionIn": {"type": "cut"},
        "plateFrame": {"from": {"s": 1.04, "y": 0}, "to": {"s": 1.08, "y": 0}},
        "plateScrim": 0.4,
        "plateLook": {"from": "saturate(0.75) brightness(0.62) hue-rotate(-6deg)"},
        "purpose": "Show the power once, on a thing: her sight lands on the courtyard gate and the gate simply stops existing. Threat by implication.",
        "visual": "The great iron-strapped wooden gate at dusk; the lilac beam slants in from her tower, the gate's edge lights, and on 'erase' it dissolves cell by cell into the dark, shedding motes. Tag 'THE UNMAKER / Sees it. Erases it.'",
        "camera": "Slow push (1.04 to 1.08).",
        "layers": {"foreground": "tag", "midground": "the gate dissolving", "background": "the wall, the lantern"},
        "lighting": "Dusk; the beam is the brightest thing in frame.",
        "imagePrompt": ip("erase"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["erase"],
        "graphics": [
            {"type": "gazeBeam", "local": True, "points": [E["from"], E["land"]], "widths": [60, 340], "sway": [12, 6, 3], "start": c("L2", "anything", -0.15), "draw": 0.5, "flares": [c("L2", "erase.", -0.1)], "opacity": 0.7},
            {"type": "unmake", "local": True, "poly": E["gate"], "from": E["land"], "at": c("L2", "she", -0.05, nth=2), "edge": 0.45, "dur": 1.1},
            {"type": "tag", "kicker": "The Unmaker", "text": "Sees it. Erases it.", "start": c("L2", "meet", -0.1)},
        ],
        "onScreenText": "Tag 'THE UNMAKER' + 'Sees it. Erases it.'",
        "transition": "Dissolve (0.35 s) on 'But' to the courtyard plan.",
        "sfx": [
            {"sound": "gaze", "at": c("L2", "anything", -0.15), "gain": -23},
            {"sound": "unmake", "at": c("L2", "she", -0.05, nth=2), "gain": -20},
        ],
        "music": "C minor; a slow pulse begins.",
    },
    {
        "id": "plan", "scene": "nightSky",
        "transitionIn": {"type": "dissolve", "duration": 0.35},
        "purpose": "The weakness, made visible: on a top-down plan her sight is a cone, ray-cast against the cover, so every pillar and the well throw a blind spot.",
        "visual": "Top-down courtyard plan on dark midnight: walls, two pillars, a well, her lilac eye on the top wall. Her sight cone opens and sweeps; black blind spots trail behind each piece of cover. 'BLIND SPOT' chips pin behind the well and in the corner beside her. Tag 'THE WEAKNESS / Line of sight'.",
        "camera": "Static diagram; the cone does the moving.",
        "layers": {"foreground": "tag, chips", "midground": "the cone and its shadows", "background": "the plan"},
        "lighting": "Midnight board; the cone carries the light.",
        "imagePrompt": "(Code-drawn plan; no plate.)", "videoPrompt": "(Not used.)",
        "graphics": [
            plan(start=sh("plan", -0.2), sweepZero=sh("plan", -0.2), labels=[
                {"text": "Blind spot", "at": [540, 945], "cue": c("L3", "what", -0.05)},
                {"text": "Blind spot", "at": [835, 560], "cue": c("L3", "see.", -0.1)},
            ]),
            {"type": "tag", "kicker": "The weakness", "text": "Line of sight", "start": c("L3", "but", -0.1)},
        ],
        "onScreenText": "Tag 'THE WEAKNESS' + 'Line of sight'; 'BLIND SPOT' chips.",
        "transition": "Hard cut on 'So' to the heroes.",
        "sfx": [
            {"sound": "gaze", "at": sh("plan", 0.05), "gain": -24},
            {"sound": "ink", "at": c("L3", "what", -0.05), "gain": -28},
            {"sound": "ink", "at": c("L3", "see.", -0.1), "gain": -28},
        ],
        "music": "Ab major 7 under a held C: the first crack of hope.",
    },
    {
        "id": "heroes", "scene": "nightSky",
        "transitionIn": {"type": "cut"},
        "plateFrame": {"from": {"s": 1.2, "y": 185}, "to": {"s": 1.23, "y": 185}},
        "plateScrim": 0.4,
        "purpose": "What the weakness does to the other side: the heroes stop charging and start planning. They wait in the column's shadow while her sight passes over.",
        "visual": "Three hooded adventurers, faces unseen, wait in the shadow of a great column at night; a lilac sweep of sight passes above them across the arches. Tag 'THE HEROES / Think, don't fight'.",
        "camera": "Slow push (1.04 to 1.08).",
        "layers": {"foreground": "tag", "midground": "the heroes by the column", "background": "the sweep of light, the yard"},
        "lighting": "Night; cold light from above, the heroes in shadow.",
        "imagePrompt": ip("heroes"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["heroes"],
        "graphics": [
            {"type": "gazeBeam", "local": True, "points": [HE["from"], HE["to"]], "widths": [80, 420], "sway": [0, 260, 3.2], "start": sh("heroes"), "draw": 0.01, "instant": True, "opacity": 0.55},
            {"type": "tag", "kicker": "The heroes", "text": "Think, don't fight", "start": c("L4", "so", -0.1)},
        ],
        "onScreenText": "Tag 'THE HEROES' + 'Think, don't fight'.",
        "transition": "Hard cut on 'Smoke' back to the plan.",
        "sfx": [
            {"sound": "wind", "from": sh("heroes"), "to": sh("path", 0.3), "gain": -36},
            {"sound": "gaze", "at": sh("heroes", 0.2), "gain": -27},
        ],
        "music": "F minor, the pulse quickens.",
    },
    {
        "id": "path", "scene": "nightSky",
        "transitionIn": {"type": "cut"},
        "purpose": "The puzzle solved in three moves: each piece of cover they add (smoke, fog, a wall) cuts a new blind spot out of her cone, until a route through the shadows reaches her door.",
        "visual": "The plan again. On 'Smoke' a smoke cloud blooms, on 'Fog' a fog bank rolls in, on 'A wall' a wall drops; each casts a new shadow in the sweeping cone. On 'Every shadow becomes a path' an amber dotted route draws from the gate through the shadows to the tower door, and three hero tokens move along it. Tag 'THE PUZZLE / Make your own shadows'.",
        "camera": "Static diagram.",
        "layers": {"foreground": "tag, labels", "midground": "cone, cover, route, tokens", "background": "the plan"},
        "lighting": "Midnight board.",
        "imagePrompt": "(Code-drawn plan; no plate.)", "videoPrompt": "(Not used.)",
        "graphics": [
            plan(start=sh("path"), instantBoard=True, sweepZero=sh("plan", -0.2),
                 blocks=[dict(b) for b in PILLARS] + [
                     dict(SMOKE, at=c("L5", "smoke.", -0.05)),
                     dict(FOG, at=c("L5", "fog.", -0.05)),
                     dict(WALL, at=c("L5", "wall.", -0.05)),
                 ],
                 route=ROUTE, routeAt=c("L5", "shadow", -0.1), tokensAt=sh("path", 0.1),
                 moves=[{"at": c("L5", "becomes", -0.1), "p": 0.42}, {"at": c("L5", "path.", 0.05), "p": 1.0}]),
            {"type": "tag", "kicker": "The puzzle", "text": "Make your own shadows", "start": c("L5", "smoke.", -0.1)},
        ],
        "onScreenText": "Tag 'THE PUZZLE' + 'Make your own shadows'; labels SMOKE / FOG / WALL; dotted route to the door.",
        "transition": "Hard cut on 'And' to her terrace.",
        "sfx": [
            {"sound": "whoosh", "at": c("L5", "smoke.", -0.1), "gain": -26},
            {"sound": "whoosh", "at": c("L5", "fog.", -0.1), "gain": -29},
            {"sound": "stoneShift", "at": c("L5", "wall.", -0.1), "gain": -26},
            {"sound": "ink", "at": c("L5", "shadow", -0.1), "gain": -27},
            {"sound": "footsteps", "from": c("L5", "becomes", -0.1), "to": c("L5", "path.", 0.9), "gain": -33},
        ],
        "music": "Bb major: the plan works.",
    },
    {
        "id": "mirror", "scene": "nightSky",
        "transitionIn": {"type": "cut"},
        "plateFrame": {"from": {"s": 1.04, "y": 0}, "to": {"s": 1.08, "y": -30}},
        "plateScrim": 0.4,
        "purpose": "The weakness cuts both ways: she plans too. A mirror bends her sight around corners, lanterns burn the fog away, and she climbs higher. She is more frightening, not less.",
        "visual": "The Unmaker on a terrace at night beside a huge oval iron mirror frame; her lilac sight strikes the frame and bends away across the castle; the lantern beside her flares on 'lanterns'. Tag 'HER MOVE / She plans too'.",
        "camera": "Slow push with a slight rise (1.04 to 1.08).",
        "layers": {"foreground": "tag", "midground": "her, the mirror, the bent beam", "background": "lanterns, the yard below"},
        "lighting": "Night; lanterns warm, her sight cold.",
        "imagePrompt": ip("mirror"), "videoPrompt": "(Not used.)", "sdxlPrompt": SDXL["mirror"],
        "graphics": [
            {"type": "gazeBeam", "local": True, "points": [M["eye"], M["mirror"], M["down"]], "widths": [12, 70, 300], "sway": [60, 0, 3.5], "start": c("L6", "mirrors,", -0.25), "draw": 0.55, "flares": [c("L6", "tower.", -0.1)]},
            *[{"type": "mendGlow", "local": True, "at": p, "r": 34, "color": "amber", "start": c("L6", "lanterns,", -0.1 + 0.1 * i), "pulses": [c("L6", "lanterns,", -0.1 + 0.1 * i)], "ringMax": 160, "ringDur": 0.8} for i, p in enumerate(M["lanterns"])],
            {"type": "tag", "kicker": "Her move", "text": "She plans too", "start": c("L6", "and", -0.1)},
        ],
        "onScreenText": "Tag 'HER MOVE' + 'She plans too'.",
        "transition": "Dissolve (0.45 s) to the plan for the lesson.",
        "sfx": [
            {"sound": "wind", "from": sh("mirror"), "to": sh("lesson", 0.4), "gain": -36},
            {"sound": "gaze", "at": c("L6", "mirrors,", -0.25), "gain": -22},
            {"sound": "shimmer", "at": c("L6", "lanterns,", -0.1), "gain": -28},
            {"sound": "gaze", "at": c("L6", "tower.", -0.1), "gain": -25},
        ],
        "music": "G7: tension returns, she answers.",
    },
    {
        "id": "lesson", "scene": "nightSky",
        "transitionIn": {"type": "dissolve", "duration": 0.45},
        "purpose": "The lesson: the solved puzzle lifts, a one-line nod to the whole arc (can, can't, costs, consequences, weakness), then the principle.",
        "visual": "The plan, solved (smoke, fog, wall, the route to the door), lifts to the top. A small row: CAN · CAN'T · COSTS · CONSEQUENCES · WEAKNESS (the last in ember). Then 'UNBEATABLE IS BORING / A weakness turns a fight into a puzzle.'",
        "camera": "Static; the plan lifts.",
        "layers": {"foreground": "lesson type", "midground": "the arc row", "background": "the lifted plan"},
        "lighting": "Midnight board.",
        "imagePrompt": "(Code-drawn plan; no plate.)", "videoPrompt": "(Not used.)",
        "graphics": [
            plan(start=sh("lesson", -0.45), instant=True, instantP=1.0, sweep=[62, 118, 6], sweepZero=sh("plan", -0.2),
                 blocks=[dict(b) for b in PILLARS] + [dict(SMOKE), dict(FOG), dict(WALL)], route=ROUTE,
                 liftAt=sh("lesson", -0.1), lift={"to": [540, 605], "s": 0.6},
                 arcRow=["Can", "Can't", "Costs", "Consequences", "Weakness"], arcAt=c("L7", "is", -0.05), arcTop=850,
                 lessonKicker="Unbeatable is boring", lessonText=["A weakness turns", "a fight into *a* *puzzle.*"],
                 lessonAt=c("L7", "boring.", -0.1), lessonTop=915, lessonSize=88),
        ],
        "onScreenText": "Arc row 'CAN · CAN'T · COSTS · CONSEQUENCES · WEAKNESS'; 'UNBEATABLE IS BORING' / 'A weakness turns a fight into a puzzle.'",
        "transition": "Dissolve (0.6 s) to the hook balcony by night.",
        "sfx": [
            {"sound": "resonance", "at": sh("lesson", 0.1), "gain": -27},
        ],
        "music": "Ab to C major: resolved.",
    },
    {
        "id": "cta", "scene": "nightSky", "plateFrom": "hook",
        "transitionIn": {"type": "dissolve", "duration": 0.6},
        "plateFrame": {"from": {"s": 1.06, "y": 0}, "to": {"s": 1.0, "y": 0}},
        "plateScrim": 0.45,
        "plateLook": {"from": "saturate(0.7) brightness(0.55) hue-rotate(8deg)"},
        "captions": False, "hideLogoBug": True,
        "purpose": "Follow CTA over the opening balcony at night, her sight still sweeping the castle; the halfway mark of the series; loops back to the hook.",
        "visual": "The hook's balcony and castle, darker, her beam still sweeping; CTA card with the Follow pill.",
        "camera": "Slow pull back (1.06 to 1.00) toward the hook framing for the loop.",
        "layers": {"foreground": "CTA card", "midground": "her sight", "background": "the night courtyard"},
        "lighting": "Night; dimmed under the card.",
        "imagePrompt": "(Reuses the hook plate.)", "videoPrompt": "(Not used.)",
        "graphics": [
            {"type": "gazeBeam", "local": True, "points": [H["eye"], H["look"]], "widths": [14, 300], "sway": H["sway"], "start": sh("cta", -0.6), "instant": True, "draw": 0.01, "opacity": 0.6},
            {"type": "ctaCard", "start": sh("cta"), "ctaAt": c("L8", "follow"), "episode": "Episode 25 / 50", "title": "The strongest magic system has weaknesses",
             "kicker": "Halfway there", "size": 74, "lines": ["Follow for more ways", "to make fictional", "*powers* *interesting.*"], "button": "Follow", "icon": "follow"},
        ],
        "onScreenText": "Full logo, 'EPISODE 25 / 50', title, 'HALFWAY THERE', 'Follow for more ways to make fictional powers interesting.', pill 'Follow'.",
        "transition": "Cross-fade into the hook's first frame for a seamless loop.",
        "sfx": [
            {"sound": "wind", "from": sh("cta"), "to": c("L8", "interesting.", 1.0), "gain": -38},
            {"sound": "swell", "at": sh("cta", -0.3), "gain": -26},
            {"sound": "chimes", "at": c("L8", "interesting.", 0.2), "gain": -24},
        ],
        "music": "F to C major, warm; fades fully before the last frame.",
    },
]

music = {
    "key": "C minor, resolving to C major",
    "drone": ["C2", "G2"],
    "events": [
        {"type": "duck", "at": c("L5", "every"), "pre": 0.15, "dur": 1.6, "gain": 0.6},
        {"type": "duck", "at": c("L7", "unbeatable"), "pre": 0.15, "dur": 2.2, "gain": 0.55},
    ],
    "sections": {
        "hook": {"chords": [["C2", "G2", "Eb3", "G3", "D4"]], "level": 0.46, "dark": True},
        "erase": {"chords": [["C2", "G2", "Eb3", "Bb3"]], "level": 0.5, "pulse": 72},
        "plan": {"chords": [["Ab1", "Eb2", "C3", "G3"]], "level": 0.52, "pulse": 72},
        "heroes": {"chords": [["F1", "C2", "Ab2", "Eb3"]], "level": 0.54, "pulse": 84},
        "path": {"chords": [["Bb1", "F2", "D3", "F3"]], "level": 0.56, "pulse": 84},
        "mirror": {"chords": [["G1", "D2", "B2", "F3"]], "level": 0.52, "pulse": 84, "dark": True},
        "lesson": {"chords": [["Ab1", "Eb2", "C3", "G3"], ["C2", "G2", "E3", "G3", "D4"]], "level": 0.62, "bells": True},
        "cta": {"chords": [["F2", "C3", "A3", "C4"], ["C2", "G2", "E3", "G3", "C4"]], "level": 0.58, "bells": True},
    },
}

TAGS = "#Worldbuilding #FantasyWriting #MagicSystem #WritingTips #WorldcraftShorts"
BODY = (
    "The secret to a terrifying wizard isn't making them unbeatable.\n\n"
    "Meet the Unmaker. Anything she can see, she can erase. But only what she can see. So the heroes stop fighting and start thinking: "
    "smoke, fog, a wall. Every shadow becomes a path. And she has to plan too: mirrors, lanterns, a higher tower.\n\n"
    "Unbeatable is boring. A weakness turns a fight into a puzzle. Can, can't, costs, consequences, and now weakness: that's Arc 5, Magic and Its Rules.\n\n"
    "Follow for more ways to make fictional powers interesting."
)
metadata = {
    "youtube": {
        "title": "The Strongest Magic System Has Weaknesses (Worldbuilding)",
        "titleAlternate": "Why the scariest wizard isn't unbeatable",
        "description": BODY + "\n\nEpisode 25 of 50 in Worldcraft Shorts: Worldbuilding, from the ground up. Short lessons for fantasy writers, novelists, mapmakers and tabletop RPG creators.\n\n" + TAGS,
        "pinnedComment": "Your turn: give your strongest caster one weakness. Silence, line of sight, preparation or a rare ingredient. What would your heroes do with it?",
        "uploadSettings": "Altered or synthetic content: Yes (AI-generated stills and synthetic narration; see docs/DISTRIBUTION.md). Not made for kids. Category: Education.",
    },
    "tiktok": {
        "caption": "The scariest wizard isn't unbeatable 👁️ She erases anything she can see, so the heroes fight with smoke, fog and walls. A weakness turns a fight into a puzzle. Follow for more. " + TAGS,
        "pinnedComment": "Line of sight, silence, or a rare ingredient: which weakness makes the scariest caster?",
        "uploadSettings": "Turn on 'AI-generated content' under More options before posting.",
    },
    "facebook": {
        "caption": BODY + "\n\nEpisode 25 of 50.\n\n" + TAGS,
        "pinnedComment": "What weakness would make your most powerful caster more frightening, not less?",
        "uploadSettings": "Turn on the AI label ('AI info') when posting (see docs/DISTRIBUTION.md).",
    },
    "instagram": {
        "caption": "Unbeatable is boring.\n\n" + BODY + "\n\nEpisode 25 of 50 · Worldcraft Shorts\n\n" + TAGS,
        "hookCheck": "First 21 characters: 'Unbeatable is boring.'",
        "pinnedComment": "Name a caster from your world and the one thing that stops them. How would a clever hero use it?",
        "uploadSettings": "Turn on 'AI label' under Advanced settings before sharing. 5 hashtags (Instagram's limit).",
    },
    "cover": "Worldcraft_Short_E25_cover.jpg: the Unmaker on her balcony, her lilac sight reaching into the misty castle, 'THE TERRIFYING WIZARD / isn\'t unbeatable.' above, corner logo.",
    "followUpQuestion": "Take your strongest caster. What one condition must be true for their power to work, and what would a clever enemy do to break it?",
}

ep = {
    "id": "ep25",
    "number": 25,
    "title": "The Strongest Magic System Has Weaknesses",
    "voice": {
        "provider": "kokoro",
        "kokoro": {"voice": "af_heart", "lang": "a", "speed": 1.0},
        "elevenlabs": {"voiceId": "REPLACE_WITH_LIBRARY_VOICE_ID", "model": "eleven_multilingual_v2",
                       "settings": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}},
        "direction": "A calm guide with a hint of relish. The hook is a quiet secret, not a trailer line. 'Meet the Unmaker' is cool and level; 'she can erase' lands softly, more chilling for it. 'But only what she can see' is the turn: slower, a small smile. 'Smoke. Fog. A wall.' are three placed pieces, a beat each. 'And she has to plan too' warns. The lesson is clear and sure, and the CTA is warm.",
    },
    "timing": {"leadIn": 0.25, "tail": 1.5, "shotLead": 0.12},
    "lines": [{"id": i, "shot": s, "text": tx, "pauseAfter": p, "emphasis": em} for i, s, tx, p, em in lines],
    "shots": shots,
    "lesson": "A caster isn't frightening because nothing can stop them; they are frightening when the story has to work around them. Give a powerful caster one strategic weakness (line of sight, silence, preparation, a rare resource) and every encounter becomes a puzzle: the heroes must think instead of charge, and the caster must plan to cover the gap. Tension without powerlessness.",
    "captionReplace": {},
    "music": music,
    "metadata": metadata,
}

EP.write_text(json.dumps(ep, indent=1, ensure_ascii=False) + "\n")
print(f"wrote {EP.relative_to(ROOT)}: {sum(len(x[2].split()) for x in lines)} words, {len(shots)} shots")
