# EP28 production brief: Intelligent Species Need More Than Different Ears

**Series:** Worldcraft Shorts, Episode 28 / 50. Season 2, "The World Engine", **Arc 6: Creatures and Species** (third episode).

**Plan entry** (`docs/SERIES_PLAN.md`):
- Hook: "Giving elves pointy ears doesn't make them a distinct civilization."
- Topic: species-specific worldbuilding.
- Core: biology influences senses, lifespans, family structures, communication and environmental needs; these should change how a species builds and understands its world.
- CTA (a comment CTA): "Invent one biological trait that would completely change a species' society."

**Deliverable:** a 60.50 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. The AI disclosure is on everywhere.

**Shot list and timings:** [`STORYBOARD.md`](STORYBOARD.md). The script that writes `episode.json`, including the whole world timeline, is `make_ep28.py`.

## The brief

The user's request (verbatim): "do episode 28 please". The standing direction is from the EP27 review: each episode must be **unique in its own sense**, at EP26's level of style and content value (`docs/STYLE_S2.md` → "Make every episode its own"). EP27's hand-off (§11 of its brief) was the plan.

### EP28's own idea: the species editor

A **character-creator panel** whose trait sliders run from HUMAN to the species' own biology. The lazy version of a fantasy species moves one slider, EARS, and nothing in the world changes. Every real trait moves a slider, and the village and the bodies rebuild themselves on screen, while a **HUMAN-LIKE meter** falls from 96 % to 0 %. The episode's argument is in the device: *a species is defined by what its biology forces it to build, not by its costume.*

- **Camera language:** at the species' eye height (low, long lenses). EP27 rode on a dragon; EP26 stood back on the ground.
- **Motif colour:** bioluminescent teal `#5fe0c0` (the sliders, the meter at low values, the glow).
- **Music band** around the series theme:
  - `folk`: kalimba ostinato, the theme on ocarina, hand drums; it gains one family per trait;
  - `glow`: a choir pad, vibraphone ripples, the theme high on celesta, for the twist.
- **Fresh wording for the recurring beats:**
  - the drop: "Spot the difference. There isn't one.", stamped 0 DIFFERENCES · HUMANS + EARS;
  - the checklist: SPECIES EDITOR · HUMAN → FENN;
  - run 2's verdict: ORIGINAL · NOTHING COPIED;
  - the twist's payoff: GHOST LIGHTS.

| Time | Beat |
|---|---|
| 0–4.0 s | **Hook (closes EP27's loop):** at a Fenn's eye height in golden light, the small teal Fenn who stacked EP27's cairn lifts a stone; POINTY EARS / AREN'T A / CIVILIZATION. |
| 4.0–6.5 s | **"Meet the Fenn. They stacked these stones."** Field card: FENN · INTELLIGENT SPECIES · BUILT: these stones |
| 6.5–9.4 s | **"Now the lazy version: humans, with different ears."** A teal RESET wipe: the Fenn become humans with pointy ears in a copy of a human village. The SPECIES EDITOR: only EARS slides (ROUND → POINTY); EYES, LIFESPAN, FAMILY, SKIN and VOICE stay on HUMAN. **HUMAN-LIKE 96 %** |
| 9.4–14.6 s | **Run 1:** a hundred years: the copy grows like a human village (same houses, same barns, the bell tower rings); the graph's HUMAN-LIKE line is flat |
| 14.6–16.8 s | **The drop:** both villages side by side, pinned HUMANS and FENN: **0 DIFFERENCES · HUMANS + EARS** |
| 16.8–21.4 s | **Re-hook:** rewind; the editor as the checklist, every slider still on HUMAN, row 5 locked |
| 21.4–34.6 s | **Four traits, each rebuilding the world:** **SENSES** (night; their eyes grow huge, the houses sink into turf mounds with glowing doors, 96→78), **LIFESPAN** (400 years: stone walls, taller, 78→60), **FAMILY** (one clan: the houses give way to one great hall, 60→42), **NEEDS** (wet skin: teal skin and fins replace pointy ears, and the hall moves onto the lake on stilts, 42→22) |
| 34.6–37.1 s | **Run 2:** a hundred years of the real Fenn: **ORIGINAL · NOTHING COPIED** |
| 37.1–45.5 s | **The twist: "Rule five? How they talk. The Fenn speak in light."** Night on the hall's deck: their spots glow; "So their hall has no walls, only windows": the walls open into pillars and waves of light travel along them. "And from the human valley? **Ghost lights on the lake.**" Row 5 unlocks (VOICE · they speak in light); HUMAN-LIKE **00 %** |
| 45.5–49.0 s | **Lesson:** the full editor card in golden light, *Biology is a blueprint.* |
| 49.0–54.4 s | **Comment CTA:** "Invent one biological trait that would completely change a species' society." |
| 54.4–60.5 s | **The ending formula:** PART 28 / 50, FOLLOW FOR PART 29, NEXT RUN · 29 UNDYING (a locked hourglass); behind, years race (winters flicker, the forest thins and grows back) while the Fenn lifts its stone; the hook title returns on frame 0 |

**Why this twist:** the plan asks how biology changes how a species *understands* its world. Speaking in light makes the Fenn build without walls, and their ordinary conversation becomes another species' ghost story. It connects to the human village from EP27, and it's the most surprising consequence of the five.

**The Isle remembers:** EP27's humans live in their sky-proof valley village (slate and turf, barns, the watchtower, the forest road, the sheep), unchanged; the cairn stands where it was; the Grimmaw grazes the south-east meadow. The dragon is away hunting this episode, which keeps it out of the low shots.

## 1. Research note

No new research was needed (`docs/SEASON2_RESEARCH.md`). The craft point is the plan's own: in fantasy, "different species" often means humans with cosmetic changes, and a species reads as distinct when its biology drives its culture and its built environment. The episode demonstrates that directly instead of saying it.

## 2. Stack

Unchanged (Remotion 4 + `@remotion/three` + three.js in software WebGL, `swangle`). New this episode, all additive (EP01–EP27 render as before; see §6):
- **World:**
  - `src/s2/world/Folk.tsx`: the Fenn (a morphing voxel body, a crowd, a keyed hero, decks over water);
  - `Settlement.tsx`: building `show` keys, `greathall`, stilts at site B, `sink`, `stone`, `open`, wall light patterns;
  - `timeline.ts`: `settlements` (more than one village), `folk`, `clearTrees`.
- **Overlays:** `editor` (the species editor), `readout` (the HUMAN-LIKE meter), `fieldCard.sliders`, sprites `fenn` and `hourglass`.
- **Sound:**
  - music: `folk` and `glow` styles, using section `programs` (kalimba, ocarina, choir and vibraphone from the same SoundFont);
  - SFX: `morph` and `slide`.

## 3. Narration (171 words, 60.50 s total)

> Giving elves pointy ears doesn't make them a distinct civilization. Meet the Fenn. They stacked these stones. Now the lazy version: humans, with different ears. Press run. A hundred years later: same houses, same barns, same bell tower. Spot the difference. There isn't one. Biology should change the build. Four traits are easy. The fifth is the twist. One: senses. They see in the dark, so they live underground. Two: lifespan. Four hundred years, so they build in stone. Three: family. One clan, one great hall. Four: needs. Their skin must stay wet, so they build on the lake. Run it again. Nothing here looks human now. Rule five? How they talk. The Fenn speak in light. So their hall has no walls, only windows. And from the human valley? Ghost lights on the lake. Pointy ears are a costume. Biology is a blueprint. Invent one biological trait that would completely change a species' society. Comment it. Part 28 of 50. Follow for part 29: someone on the Isle never dies.

- **Measured with the real TTS** (Kokoro `af_heart`, speed 1.07) before any cue was set: 60.47 s, inside the window on the first draft.
- **G2P checked:** "Fenn" → fˈɛn; "Isle" → ˈIl ("aisle"); "light" → lˈIt; "28", "50", "29:" read as numbers.
- **Landmarks:**
  - "lazy" 6.82 s (the reset);
  - "run" 9.96 s;
  - "isn't" 16.11 s;
  - "the twist" 20.78 s;
  - "Rule five?" 37.51 s;
  - "light" 39.66 s;
  - "Ghost lights" 44.23 s;
  - "Invent" (wipe −0.3) 49.33 s;
  - "Part" 54.64 s;
  - "Follow" 56.23 s;
  - "never" 58.56 s.

## 4. Timed storyboard

See [`STORYBOARD.md`](STORYBOARD.md).

## 5. Generated assets

- **Figma** (file "Worldcraft Shorts EP26 art", `7wHdle0cigAS8MhVmZzZYJ`): **1 generation** with `gpt-image-2.5-sunburst` (the user approved up to 2 for EP28).
  - The result is an original small amphibious species: teal skin, big night eyes, fin frills instead of ears, glow spots, a reed sash. Prompt: [`art/PROMPT.md`](art/PROMPT.md).
  - Saved as `art/fenn_sunburst.png` and re-gridded to `assets/fenn_sprite.png` (52×127).
- **Code-drawn:** everything else (the voxel Fenn built to match the sprite, both villages, the hall, the lights, the editor).
- **No readable text in any generated image.**

## 6. Final video and verification

- **QA:** `qa.py` **passed** on all four copies, each 60.50 s, −14.0 LUFS, TP −1.4 dB:
  - master: 35.6 MB;
  - compat: 30.7 MB;
  - download (two-pass 1,600k): 14.2 MB;
  - player (two-pass 1,300k): 11.9 MB.
- **The loop:** the last frame against frame 0 differs by **0.76/255**, the same as an ordinary frame step (0.62). Stills at t = 0 and at the last frame differ by 0.02.
  - The first full render had a seam of 5.1/255. The two houses built during run 1 had their show keys out of order, so they came back at run 2 and stood for the rest of the episode, with a house roof in front of the camera on the last frame.
  - Fixed: they're rewound at the re-hook and never rebuilt.
- **Preview page:** https://claude.ai/artifact/1P2Jh9J9ubwGgAXtKbnVid (new; EP26's and EP27's pages are untouched).
  - The download reads back byte-identical (sha256 `fecfd2c8…`) and passes `qa.py`.
  - The player is asset `/_blob/3b2a3dbc6db602c90332eb494ddfd86a`.
- **Render:** 12 min 43 s with `--gl=swangle` (1,815 frames).
- **Inspected:**
  - beat stills on five rounds;
  - three hook candidates, then two more after the first failed (the chosen frame: the camera east of the cairn with the sun at its back, the Fenn in profile lifting its stone, the human valley and the peak behind);
  - the QA contact sheet;
  - frame 0 against the last frame;
  - the cover.
- **Fixes made after looking:**
  1. **The hook went through five framings.** A foreground tree was cleared with the new `clearTrees`. The lens was too narrow, so the cairn filled the frame. From the south, the great hall on the lake sat in front of the camera. Shooting from the north would have backlit the hero.
  2. **POINTY EARS wrapped onto the next line** at 96 px; it's now 84.
  3. **The copied bell tower stood in front of two shots,** so it moved north.
  4. **The Grimmaw blocked the lazy-version shot,** so it moved to the south-east meadow.
  5. **The dragon's perch kept appearing at the top of low shots,** so it's away hunting this episode.
  6. **The editor's unmoved rows were too dim to read.**
  7. **The twist camera sat inside the shoreline trees.**
  8. **The ghost-lights camera was first inside a house,** then too close to the hall. It now looks across the valley.
  9. **The great hall sank with the houses.** `sink` now skips it.
  10. **The Fenn's teal read too dark** in daylight.
- **Sound (measured):**
  - −14.05 LUFS, voice/music 13.9 LU;
  - the chime windows are within about 1 dB of EP26's (−26.1 / −25.4 / −27.4 against −26.0 / −24.4 / −26.5 LUFS), so the chime still sits about 6–7 LU under the voice;
  - the score follows the story: folk hook −19.1, the lazy version's pulse −27.1, run 1 −21.5, folk 1 −32.5 growing to folk 4 −21.3 as traits return, run 2 −17.7, glow −29.1 (soft, for the light-speech), anthem −18.8, tease −25.1.
- **Regression, all with the final EP28 code:**
  - EP25's and EP26's `music.wav`, `sfx.wav` and `mix.wav` are bit-identical to `main`;
  - EP27's are bit-identical to `claude/worldcraft-ep27` (narration and timing fixed);
  - EP26 stills at 0, 22, 43.5 and 59.5 s are pixel-identical to `main`;
  - EP27 stills at 0, 8.8, 26.8, 41.6 and 60.85 s are pixel-identical to `claude/worldcraft-ep27`;
  - `src/Episode.tsx` (Season 1) is untouched.
- **Cover:** `Worldcraft_Short_E28_cover.jpg`, the hall with no walls at 42.55 s (the Fenn inside, the light patterns, "ONLY WINDOWS.").
- **Not verifiable by me:** how anything sounds. In particular, listen to the kalimba / ocarina / hand-drum band, the choir under "they speak in light", the slider ticks and the morph shimmer.
- **Accepted compromises:**
  - at village distance, the Fenn's night eyes are a few pixels, so the SENSES slider and the night mood carry that trait;
  - the ghost lights are cyan squares in the dark rather than a soft glow (no bloom in the pixel stage);
  - in the drop, both villages are small in the medium shot; the pins and the stamp carry the comparison.

## 7. Reusable components added

All are documented in `README.md` (Season 2 building blocks) and `docs/STYLE_S2.md`.
- **`folk` / `Fenn`:** a people on the Isle, as a crowd plus a hero, whose body morphs by trait keys. Reuse it for any humanoid species and swap the palette per species.
- **Multiple `settlements`;** building `show` keys, `greathall`, `stiltsB`; village keys `sink`, `stone`, `open`, `glow`; `clearTrees` for a shot's line of sight.
- **`editor` + `fieldCard.sliders` + `readout`:** the species editor and its meter. It reuses for any "design X" episode (a culture editor, a magic-system editor).
- **Music:** `folk`, `glow`, and per-section `programs` (the band can change instruments without new MIDI channels).
- **SFX:** `morph`, `slide`.

## 8. Cost (₱63.35 = $1)

**$0 cash.** One Figma AI generation (of the 2 approved). Everything else is free and open. Details in `docs/COSTS.md`.

## 9. Platform metadata

In `episode.json → metadata`, and ready to paste in `docs/DISTRIBUTION.md` ("Episode 28 captions").
- YouTube title: *Intelligent Species Need More Than Different Ears (Worldbuilding)*. Alternate: *Your elves are just humans with ears*.
- Instagram hook: "Your elves are just humans." TikTok opens with the same idea.
- Pinned comments repeat the comment ask.
- Every description ends with "Part 28 of 50. Follow for part 29: someone on the Isle never dies."
- AI label ON on all four platforms.

## 10. Experiments and metrics

- **The device:** retention at 6.5–9.5 s (the lazy editor) and 21–35 s (the traits rebuilding the village). If both hold, "editor" devices become a series tool for "design X" topics.
- **Comments:** this CTA asks viewers to *invent*. Compare comment count and length with EP27's CTA ("what would your civilization invent").
- **Three distinct episodes in a row:** compare EP26, EP27 and EP28 on average view duration and follows per 1,000 views.
- **The re-hook:** check for a dip around 15 s (the drop) and a recovery after "The fifth is the twist" at 20.8 s.

## 11. How to produce EP29 ("Immortality Would Break Your Society", Arc 6)

1. **Branch:** `claude/worldcraft-ep29` from `main` once EP27 and EP28 are merged (or from `claude/worldcraft-ep28`). Read `CLAUDE.md`, `docs/STYLE_S2.md` ("Make every episode its own") and this brief.
2. **Plan entry:**
   - Hook: "What happens when a ruler can live for ten thousand years?"
   - Core: long lifespans transform inheritance, education, marriage, political turnover, population growth and the preservation of knowledge.
   - CTA: "Would you want an immortal ruler? Explain why."
3. **Close EP28's loop:** EP28 ends "someone on the Isle never dies", with years racing past (winters flicker, the forest thins and regrows). EP29's frame 0 should show *who*: one figure on the Isle unchanged while everything around it ages.
4. **Give EP29 its own device** (not an editor, not a point of view). A natural one: **a family tree / generations timeline**. A strip of generations scrolls under the world, and the immortal stays at the top while every row below turns over. The fixes ("what breaks") are inheritance (heirs who never inherit), education (the same teacher for 300 years), turnover (one ruler forever) and population. Give it its own camera language (e.g. locked-off, time-lapse tableaux: the same frame across centuries), motif colour and music band.
5. **Reuse:**
   - the human valley and the Fenn on the lake (both live on the Isle now);
   - `folk` for a crowd, with a new palette;
   - `settlements` for towns that age (`stone`, `show`);
   - `snow` and `forest` for time passing.
6. **Pipeline notes:**
   - Kokoro needs Python ≤ 3.12.
   - Regressions: fix `narration.wav` + `timing.json` and compare `score.py` + `mix.py`.
   - Rebuild the audio after any cue change, before rendering.
   - Plan the hook's line of sight early (`clearTrees`, nothing between the camera and the subject; the sun at the camera's back: golden is az 58).
7. **Then** the same delivery: stills, a `--gl=swangle` render (about 13 min), `qa.py`, encodes, SRT, storyboard, cover, this 11-section brief, docs, a new preview page with the Download button, push.
