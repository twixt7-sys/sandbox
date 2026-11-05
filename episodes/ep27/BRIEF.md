# EP27 production brief: What Would Dragons Actually Change?

**Series:** Worldcraft Shorts, Episode 27 / 50. Season 2, "The World Engine", **Arc 6: Creatures and Species** (second episode).

**Plan entry** (`docs/SERIES_PLAN.md`):
- Hook: "If dragons existed, your world's architecture would look very different."
- Topic: the societal consequences of creatures.
- Core: flying predators change roof design, livestock protection, military strategy, settlement placement and travel. What must ordinary people do differently because dragons exist?
- CTA (a comment CTA): "What would your civilization invent to survive dragons?"

**Deliverable:** a 61.31 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. The AI disclosure is on everywhere.

**Shot list and timings:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`. The script that writes `episode.json`, including the whole world timeline, is `make_ep27.py` (copied from `make_ep26.py` and adapted).

## The brief

The request: produce EP27 following EP26's patterns, style and vibe exactly, closing EP26's open loop ("a dragon lands here") and growing the Isle by its first village. EP26's §11 hand-off was the plan, and every Season 2 rule in `docs/STYLE_S2.md` applies: the Isle, ▶ RUN twice, the field card with a locked row, golden-hour bookends, the World Engine chime at its three moments, the ending formula and the seamless loop.

### How EP27 uses the format

| Time | Beat |
|---|---|
| 0–4.2 s | **Hook (closes EP26's loop):** the dragon perched on the Grimmaw's meadow in golden light, the Grimmaw looking up at it, the naive village behind; IF DRAGONS / EXISTED on frame 0. On "dragons" it rears (wings up, dust ring) |
| 4.2–8.6 s | **Setup:** the dragon takes off ("built before the dragon came"); the DRAGON field card (HUNTS: anything in the open) over the village: thatch, open pens, the hall at the top of the slope, the trade road; RUN |
| 8.6–14.6 s | **Run 1:** WEEK 0→3. The dragon circles the open village; roofs char one by one and smoke (ROOFS 07→00), FLOCK 60→9, carts leave the road (TRADE 06→00) |
| 14.6–17.5 s | **The drop:** close on the burnt, empty village in gloom; COLLAPSED · NO WAR; IT JUST STOPPED. |
| 17.5–21.3 s | **Re-hook:** rewind; the DRAGON-PROOF checklist with four easy rows and a locked fifth |
| 21.3–32.4 s | **The changes, each visible in the world:** ROOFS (thatch → slate and turf), PENS (a covered barn rises), PLACE (every building unbuilds and rises again in the valley under the cliff; the flock follows), TRAVEL (night; carts with lanterns on a forest road) |
| 32.4–36.6 s | **Run 2:** the dragon circles the valley and finds NOTHING IN THE OPEN; roofs hold, FLOCK 60→92, TRADE 6→9; THRIVING |
| 36.6–47.2 s | **The twist (rule five):** "Someone has to watch the sky." A watchtower with a bell rises on the cliff, its watch ring covers the valley; the dragon passes, the bell rings, the carts vanish (everyone hides); THE BELL-RINGER DECIDES WHEN WE HIDE. Row 5 unlocks: POWER · whoever rings the bell |
| 47.2–51.1 s | **Lesson:** the full card in golden light, *Ask what ordinary people change.* |
| 51.1–55.0 s | **Comment CTA:** end card with a speech-bubble COMMENT panel |
| 55.0–61.3 s | **The ending formula, then loop:** PART 27 / 50, FOLLOW FOR PART 28, NEXT RUN · 28 BUILDERS; on the lake shore a cairn's stones stack themselves; the hook title returns on frame 0's pose |

No people appear and no one is harmed on screen: roofs char with nobody in them, livestock loss is a falling counter and sheep shrinking away, and "everyone hides" is the carts leaving the road.

**Twist choice.** BRIEF 26 §11 offered three twists. *Burns clear farmland* was rejected because it pre-empts EP30 ("a monster that is also the source of the harvest"). *The sky becomes a border* reads mainly as tunnels, which overlaps change 4. *Towers and bells change who holds power* is the most surprising social consequence, it shows well (a tower rising, a ring, a bell swinging), and it pays off the plan's "military strategy" point without showing violence.

## 1. Research note

No new research was needed. The why is in `docs/SEASON2_RESEARCH.md` (hook in the first second, re-hooks every 10–15 s, the follow ask after the payoff, part numbers, sound logo). EP27 also applies two items from EP26's §10 experiments:
- **The golden hook again**, so EP26 and EP27 can be compared on "viewed vs swiped away" as a pair.
- **A comment CTA instead of a share CTA**, as the plan asks. Compare comments per 1,000 views with EP26.

## 2. Stack

Unchanged from EP26 (Remotion 4 + `@remotion/three` + three.js in software WebGL, `swangle`). New this episode, all additive (EP01–EP26 render as before; see §6):
- `src/s2/world/Dragon.tsx`: the voxel dragon (perch / roar / fly / glide / hidden, wing flap, banking, outline).
- `src/s2/world/Settlement.tsx`: the village layer (roofs, char, smoke, pens and barns, the site move, roads, carts, lanterns, tower and bell, the cairn).
- `timeline.ts`: `dragons`, `settlement`, `series`, `props`, `herd.skin` / `herd.centersB`, `dragonAt`, `seriesAt`; the `gaze` predator state.
- `Creatures.tsx`: the `sheep` skin and a second set of herd homes.
- Overlays: `simBar.counters` + `compact`, graph series by key, sprite size on the field card, `pin.dragon`, `endCardS2.icon`, `nextRun.sprite`, sprites `sheep`, `house`, `cart`, `bubble`, `cairn`.
- Sound: `towerBell` and `burn` in `score_s2.py`.
- Environment note: Kokoro 0.9.4 needs Python ≤ 3.12 (the container's default is 3.13), so the pipeline ran in a Python 3.12 venv with `pipeline/requirements.txt`.

## 3. Narration (170 words, 61.31 s total)

> If dragons existed, your world's architecture would look very different. Let's test it. This village was built before the dragon came. Press run. Week one: thatch burns. Week two: open pens, empty. Week three: no one travels. Nobody fought a war. The village just stopped working. So rebuild it. Four changes are easy. The fifth is the twist. One: roofs. Slate and turf don't burn. Two: pens. Flocks sleep in covered barns. Three: place. Move into the valley, out of sight. Four: travel. Trade moves at night, under the trees. Run it again. Now the roofs hold, the flocks grow, and trade returns. Rule five? Someone has to watch the sky. A tower rises, with a bell. Whoever rings it decides when everyone hides. Rule five is power. The dragon changed who's in charge. Don't just add a dragon. Ask what ordinary people do differently. What would your civilization invent to survive dragons? Comment below. Part 27 of 50. Follow for part 28: something on the Isle learns to build.

- **Measured with the real TTS** (Kokoro `af_heart`, speed 1.07) before any cue was set. The first draft (173 words) ran 62.22 s, over the window. "out of its sight lines" became "out of sight", "comes back" became "returns", and five pauses were trimmed, giving **61.29 s**.
- **G2P checked:** "Isle" → ˈIl (misaki's `I` = aɪ, so "aisle", not "ill"); "thatch" → θˈæʧ; "27", "50", "28:" read as numbers.
- **Landmarks:** "run" 8.13 s; re-hook "the twist" 20.46 s; "Rule five?" 36.73 s; "power" 44.47 s; "What" (wipe −0.3) 51.21 s; "Part" 55.14 s; "Follow" 56.95 s; "learns" 59.36 s; the line ends at 60.19 s, then the cairn and the wind-up into the loop.

## 4. Timed storyboard

See [`STORYBOARD.md`](STORYBOARD.md) (per shot: purpose, visual, camera, layers, light, on-screen text, transition, music, graphics and SFX cues).

## 5. Generated assets

- **Figma** (file "Worldcraft Shorts EP26 art", `7wHdle0cigAS8MhVmZzZYJ`): **1 generation** with `gpt-image-2.5-sunburst`. The user approved up to 2 for EP27, and the first was right. The prompt is in [`art/PROMPT.md`](art/PROMPT.md): an original lean wyvern-like dragon, rust-red with bone wing fingers, side view, wings raised. Saved as `art/dragon_sunburst.png` and re-gridded to `assets/dragon_sprite.png` (168×116, 28 colours, transparent).
- **Code-drawn:** everything else. The voxel dragon was built to match the sprite. Also code: the village and its changes, the sheep, the cairn, the HUD icons (`sheep`, `house`, `cart`, `bubble`, `cairn`), and the tower bell and burn sounds.
- **No readable text in any generated image.** The dragon design is original.

## 6. Final video and verification

- **QA:** `qa.py` **passed** on all four copies, each 61.31 s, −14.0 LUFS, TP −1.3 dB:
  - master: 47.7 MB;
  - compat (H.264 Main, CRF 20, `+faststart`): 40.9 MB;
  - download (two-pass 1,600k): 14.3 MB;
  - player (two-pass 1,300k): 12.0 MB.
- **The loop:** frame 0 against the master's last frame differs by **1.35/255** on average (EP26 v3: about 1.4). Everything that changes resets under the CTA wipe: the camera, the dragon on its perch, the Grimmaw's gaze, the naive village, 60 sheep and 6 carts.
- **Preview page:** https://claude.ai/artifact/Hb2nZKR7ReFhXi7hvGyJ2s (new; EP26's page is untouched).
  - The page declares `downloads` and `assets`, and has a Download MP4 button.
  - The download reads back byte-identical (sha256 `6762864c…`) and passes `qa.py`.
  - The player is asset `/_blob/aef978bdfb86c18cd90a214cd0abb00c`.
- **Render:** 22 min 0 s with `--gl=swangle` (1,839 frames; EP26 v3 took 19 min). The village, the dragon and the extra shadow casters cost about 15 %.
- **Inspected:**
  - the QA contact sheet;
  - beat stills across every beat (three rounds; fixes below);
  - frame 0 against the last frame;
  - the cover.
- **Fixes made after looking:**
  1. **The hook was too tight.** The dragon's wings filled the frame as a red slab, and the Grimmaw stood in front of it. Re-shot at fov 18 from 88 units across the lake (az 20), with the dragon in profile on the left facing the Grimmaw on the right, and the dragon at scale 1.35 so it dwarfs the houses.
  2. **An az −40 hook looked into the sun.** It came out dark and backlit, with forest filling the foreground. I went back to EP26's front-lit angle.
  3. **The dragon blocked the village in the setup.** It now takes off on "Let's test it" ("built before the dragon came") and returns on "run".
  4. **The village was hidden behind the field card.** The camera target was raised.
  5. **Village A was first placed in the north-east forest.** It moved to the open meadow on the slope. Trees on building sites, pens and roads are now cleared in code.
  6. **The night road was invisible under the canopy.** A lane is cleared along it, and the lanterns are bigger and on poles.
  7. **ROOFS dipped to 04 while buildings moved to the valley.** It read as a loss, so the counter now counts standing roofs whether or not a building is mid-move.
  8. **The tower pin overlapped the card.** The camera was raised. The lesson card's title is VILLAGE, because DRAGON-PROOF ran under 5/5 at full size.
  9. **The cairn hid behind the Grimmaw.** It moved to the right and toward the camera and is drawn at 1.5×.
  10. **The first render was stopped.** The audio had been built before two SFX cues moved, so it was rebuilt (`score.py` + `mix.py`) and the render restarted.
- **Sound (measured):**
  - −14.06 LUFS, voice/music 14.0 LU;
  - the three chime windows (frame 0, the lesson card, the follow press) measure within about 1 dB of EP26's, which sat 6–7 LU under the voice;
  - all score sections, accents and the 80 ms fade to the loop point are as in EP26's plan.
- **Season 1 and EP26 regression:**
  - with the narration and timing fixed (Kokoro output isn't bit-identical between runs), EP25's and EP26's `music.wav`, `sfx.wav` and `mix.wav` rebuild **bit-identical** to `main`;
  - EP26 stills at 0, 22, 43.5 and 59.5 s are **pixel-identical** to `main` (mean difference 0.0);
  - `src/Episode.tsx` (Season 1) is untouched.
- **Cover:** `Worldcraft_Short_E27_cover.jpg`, the golden hook at 0.75 s, mid-roar, with the sting.
- **Not verifiable by me:** how anything sounds. In particular, listen to the tower bell, the burn crackle, the roar on "dragons", and the last 6 seconds into the loop.
- **Accepted compromises:**
  - at hook distance the dragon's raised wings read as large flat panels: voxel-faithful, but less detailed than the sprite;
  - the night road is dark green, and the carts read mainly by their lanterns;
  - at the place move, the trade road still starts at the old site until the travel change moves it into the forest.

## 7. Reusable components added

All are documented in `README.md` (Season 2 building blocks) and `docs/STYLE_S2.md` (motion vocabulary, settlements).
- **World:** `dragons` / `Dragon` (perch, roar, fly, glide, hidden; flight keys with altitude; banking; `orbit()` in `make_ep27.py` writes circling keys). `settlement` / `SettlementLayer`: buildings with a `roof` switch, `char` and `smoke`; `pens` + `cover` barns; the `place` move from site A to site B with the herd following (`herd.centersB`); `roads` A / B with `route`, carts counted by a `series`, `lanterns`; a `tower` with a bell on `rings` cues. Trees on building sites and roads are cleared automatically. Also `herd.skin: "sheep"`, `props` (the cairn), and the `gaze` state (alert held from the first frame, for frame 0 and the loop).
- **HUD:** `simBar.counters` (any keys: `herd`, `pred`, `roofs` read from the village itself, or a `series`) with a `compact` layout for three counters plus the clock; `simGraph` on the same keys; `fieldCard.spriteW` / `spriteH` / `dietLabel`; `pin.dragon`; `endCardS2.icon` (`bubble` for a comment CTA); `nextRun.sprite`.
- **Sound:** `towerBell` (a low cast bell, unlike the chime) and `burn` (flame and crackle bed with its own seed).

## 8. Cost (₱63.35 = $1)

**$0 cash.** One Figma AI generation (of the 2 approved). Everything else is free and open. Details in `docs/COSTS.md`.

## 9. Platform metadata

In `episode.json → metadata`, and ready to paste in `docs/DISTRIBUTION.md` ("Episode 27 captions").
- YouTube title: *What Would Dragons Actually Change? (Worldbuilding)*. Alternate: *Your village wouldn't survive a dragon*.
- TikTok caption: 329 characters, ending "Part 27/50 · follow for part 28".
- Instagram hook: "Dragons change architecture."
- Pinned comments repeat the comment ask ("What would your civilization invent to survive dragons?").
- Every description ends with the ending formula: "Part 27 of 50. Follow for part 28: something on the Isle learns to build."
- AI label ON on all four platforms.

## 10. Experiments and metrics

- **Comment CTA vs share CTA:** comments per 1,000 views on EP27 against EP26, and shares per 1,000 views (expect lower). If comments rise without a big share loss, use comment CTAs on "what would you invent" episodes.
- **Closing the loop:** EP27's "viewed vs swiped away" for viewers arriving from EP26 (YouTube's "related video" traffic). Was the open loop worth it?
- **The re-hook:** check for a dip at about 17 s (the drop) and a recovery after "The fifth is the twist" at 20.5 s.
- **The twist:** retention around 37–44 s. If it holds better than EP26's delete experiment, social twists work as well as ecological ones.
- **Follows per 1,000 views:** EP26–EP30 against EP21–EP25 (unchanged from EP26).

## 11. How to produce EP28 ("Intelligent Species Need More Than Different Ears", Arc 6)

1. **Branch:** `claude/worldcraft-ep28` from `main` once EP27 is merged (or from `claude/worldcraft-ep27`). Read `CLAUDE.md`, `docs/STYLE_S2.md` and this brief (§6, and §7 for the new pieces).
2. **Plan entry:**
   - Hook: "Giving elves pointy ears doesn't make them a distinct civilization."
   - Core: biology shapes senses, lifespans, family structures, communication and environmental needs, and those should shape how a species builds.
   - CTA: "Invent one biological trait that would completely change a species' society."
3. **Close EP27's loop first.** EP27 ends on "something on the Isle learns to build" with a cairn stacking itself on the lake shore beside the Grimmaw (`CAIRN = (11.8, -0.8)` in `make_ep27.py`, 3 stones, `props` kind `cairn`). EP28's frame 0 should show *who* stacked it: a new intelligent species at the cairn, in golden light, the same hook pose (`az 20, el 8, dist 88, fov 18, target (6.4, 10, -1.4)`), so returning viewers recognise the spot.
4. **Story idea on the Isle:**
   - **Naive:** "humans with pointy ears", whose new village is a copy of EP27's (reuse `settlement`, same buildings, nothing changed).
   - **Run 1:** nothing about their biology is used, so nothing about their world changes. A flat result is the point: it looks like every other fantasy village.
   - **The fixes**, one trait at a time, each visibly changing the build:
     - senses (e.g. they see heat, so houses are built to be dark and cold);
     - lifespan (towns built for centuries: stone, not timber);
     - family (one great hall instead of houses, which is already a `hall` building kind);
     - communication (e.g. the bell tower from EP27 becomes their language).
   - **Twist:** a need that changes *where* they live (they must stay by water, so the village moves onto the lake: re-use `place` with a site B on the lake shore).
5. **New pieces it needs:** a small voxel builder species (a two-legged creature, outlined like the Grimmaw, with a carry pose for a stone); building variants (round huts, a long hall, stilts) as new `kind`s in `Settlement.tsx`; maybe a `water` site variant. Field card sprite: ask the user before using Figma credits (1–2 generations), as for EP26 and EP27.
6. **Reuse:** everything in §7, the counters (`compact`, three keys), `orbit()` for any flyer, the dragon itself if a cameo helps (it lives on its rock shoulder under the peak, `LAIR = (-2.5, -12.5)`).
7. **Ending formula:** "Part 28 of 50. Follow for part 29: <tease>". EP29 is immortality ("a ruler who lives ten thousand years"). In-world tease idea: one tree on the Isle that never changes season while everything else does, or a figure that never moves while the clock races.
8. **Pipeline notes from this episode:**
   - Kokoro needs Python ≤ 3.12: `uv venv -p 3.12` and install `pipeline/requirements.txt` with the CPU torch index.
   - Kokoro output is not bit-identical between runs. For the Season 1 regression, copy `main`'s `narration.wav` + `timing.json` into both trees and rebuild only `score.py` + `mix.py`, then compare.
   - **Rebuild the audio (`score.py` + `mix.py`) after any SFX or music cue change, before rendering.** Remotion bundles `public/` when the render starts.
9. **Then** the same delivery as EP26 and EP27: stills, a `--gl=swangle` render (about 22 min), `qa.py`, encodes, SRT, storyboard, cover, this 11-section brief, docs, a new preview page with the Download button, push.
