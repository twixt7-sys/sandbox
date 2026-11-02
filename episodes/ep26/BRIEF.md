# EP26 production brief: Don't Design a Monster. Design an Ecosystem.

**Series:** Worldcraft Shorts, Episode 26 / 50. Opens **Arc 6: Creatures and Species**, and **relaunches the series as Season 2, "The World Engine."**

**Plan entry** (`docs/SERIES_PLAN.md`):
- Hook: "If your giant predator eats everything, why hasn't everything gone extinct?"
- Topic: creature ecology.
- CTA (a share CTA): "Share this with someone designing fantasy monsters."

**Deliverable:** a 60.3 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. The AI disclosure is on everywhere.

**Shot list and timings:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`. The script that writes `episode.json`, including the whole world timeline, is `make_ep26.py`.

## v2 (2 Nov 2026): after the first review

The user's response to v1 (verbatim): "it's okay but I feel like music would work good, or I don't know can you look through things that can make it even better than it is now?"

What changed in v2:

1. **Real music.** v1's score was synthesised tones on a beat grid (pads, square plucks, drum synthesis): functional, but it didn't sound like music. v2 is a **composed score played on sampled instruments**:
   - FluidSynth with the MuseScore General SoundFont (MIT, from the Ubuntu archive), arranged in the new `pipeline/music_s2.py`.
   - It has a **series theme**: a 4-bar melody that plays in D minor over the problem and returns in D major for the payoff.
   - The instruments: celesta, marimba, pizzicato and full strings, cello, bass, flute, horns, harp, glockenspiel, music box, timpani, taiko, a quiet square-wave lead for the World Engine colour, and drums.
   - A **tempo map fitted to the narration** puts every musical change exactly on its story beat:
     - the drive starts on "run";
     - the music drops out for "It ends it." with a low boom;
     - one instrument family joins per rule;
     - a full groove on the second run;
     - a hard stop on "Delete";
     - a frenzy and crash for the boom;
     - a big hit on "together";
     - the theme as an anthem for the lesson, and a soft outro faded out before the loop.
2. **A mix that lets the music be heard:**
   - **Music level:** music −25 LUFS before ducking, ducking −8 dB under speech. The music is now about **14 LU** under the voice (v1: 15.3 LU) and swells in every pause.
   - **Narration polish (`voiceFx`):** high-pass, presence lift, air and gentle compression for phone speakers.
   - **Stereo:** instruments are panned across the field and sub-rumble is filtered out.
3. **A stronger first two seconds.** On "eats everything" the Grimmaw now gives a **display call**: head up, jaw open, body rocks back, with a voxel **dust ring** from its feet (`roar` + `stompHit` sounds), and the camera slowly pushes in through the hook. Frame 0 is unchanged, so the loop still matches.
4. **Captions:** the word pop is softer (1.12× instead of 1.22×), so a popping word no longer overlaps its neighbour.

Checked objectively, since I can't hear:
- all 16 instrument channels render (927 notes, no missing presets);
- the theme is checked against every chord it plays over;
- the score's loudness envelope follows the story arc;
- EP25's audio is still bit-identical.

## The brief

The user's direction (1 Nov 2026), verbatim:

> "Improve style and animations drastically starting wit episode 26. make them 60 seconds and make them more valuable, engaging, stimulating, and do deep research. use all the best tools available and make it based on the most popular trend patterns. Maybe do it as an animated 3d or pixel art or invent a whole new sweet gimmick. surprise me but make it so good."

What that became:
- **60 seconds** from EP26 on. The QA window (55–62 s) is now per episode.
- **A new signature format**, built as reusable infrastructure (`src/s2/`, `pipeline/score_s2.py`, `docs/STYLE_S2.md`). EP01–EP25 still render as before, proven bit-identical where it matters (§6).
- **Research first:** `docs/SEASON2_RESEARCH.md`.

### The Season 2 decision

- **What the research found** (details and sources in the research doc):
  - The swipe decision happens in about the first second.
  - 30–60 s is the consensus, and completion and total watch time are the signals. 60 s has to *earn* its extra 30 s.
  - Re-hooks every 10–15 s, visible change every 3–5 s.
  - Word-by-word burst captions are the baseline.
  - Miniature dioramas, low-poly and pixel nostalgia, and cozy motion are named 2026 visual trends.
  - In the worldbuilding niche, channels either *talk* (essays) or *show a finished world* (maps, lore). Nobody I found *demonstrates* a principle as a running system.
- **Chosen: "THE WORLD ENGINE."** One persistent pixel-voxel island (the Isle), rendered as real 3D at ⅓ resolution and upscaled with hard pixel edges. Every episode tests a worldbuilding idea by pressing **▶ RUN**: the naive design visibly breaks, the fix visibly works, a twist shows what most people miss, and a field card checklist is the takeaway.
  - It combines all three directions the user named: animated 3D, pixel art, and a gimmick of its own (the simulation).
  - It reads on a phone and is ownable.
  - It extends to the remaining arcs: dragons changing settlements, species, immortal rulers, a worshipped monster, then history, war, economy and endings run on the same island.
- **Rejected:**
  - a recurring guide character: expensive to animate well in code, and it puts a face on an AI-voiced channel;
  - hand-drawn ink and paper cut-out: not convincing in code, and AI "ink" reads as AI;
  - flat 2D pixel art: less depth, less of a "world";
  - Blender (not installable here, and too slow on CPU) and the open music models (non-commercial weights, or a GPU needed).

### How EP26 uses the new format

| Time | Beat |
|---|---|
| 0–4.6 s | **Hook:** the Grimmaw among its herd, with IF IT EATS EVERYTHING / WHY ISN'T EVERYTHING EXTINCT? on screen from frame 0. The WORLD ENGINE sting boots over it |
| 4.6–9.2 s | **Setup:** the Grimmaw's field card (DIET: anything that moves), then "Press run." |
| 9.2–20.9 s | **Run 1 and the drop:** five years in four seconds. The herd counter falls 120→0 on a live graph, the Grimmaw walks an empty meadow and lies down, then EXTINCT and IT ENDS IT. |
| 20.9–25.6 s | **Re-hook:** a rewind; the checklist shows four easy rules and a **locked fifth row** ("the twist") |
| 25.6–38.0 s | **Fixes, one per beat:** prey breeding (lambs pop in), territory (three rings, three Grimmaws), energy (it sleeps at its den), slow breeding (winter, one cub) |
| 38.0–42.4 s | **Run 2:** twenty years. The populations cycle; STABLE |
| 42.4–51.4 s | **Twist (rule five):** DELETE the monster. The mossbacks boom to 380, strip the meadow to dirt, thin the forest and crash; then "the Grimmaw holds the island together", and the island heals |
| 51.4–54.7 s | **Lesson:** the full field card, 5/5, *Design its place in the world.* |
| 54.7–60.3 s | **CTA, then loop:** SHARE THIS end card, which lifts onto the exact opening frame |

No kills on screen. Prey loss is a falling counter and agents shrinking away. Hunger is an empty range. The starving predator lies down, greys and dissolves out of the simulation. "Delete" is clearly an experiment on the simulation, not a death.

## 1. Research note

Everything is in `docs/SEASON2_RESEARCH.md` (sources read 1 Nov 2026, with unverified claims marked). Two findings changed production directly:
- **AI labels:** YouTube's own help page requires disclosure only for *realistic* content and exempts clearly animated work. Meta names *realistic AI voice-overs* as label-worthy. Kokoro narration is a synthetic voice, so the series policy (label ON everywhere) stays.
- **WebGL in this container:** `--gl=angle` (the series default) can't create a WebGL context in the headless shell, and `angle-egl`, `swiftshader` and `vulkan` fail too. **`--gl=swangle` works.** Season 2 renders pass `--gl=swangle`; Season 1 keeps `angle`.

## 2. Stack

- **Picture:** Remotion 4.0.536 + `@remotion/three` + three.js 0.180 + React Three Fiber 9.3, in software WebGL (`swangle`).
  - `src/s2/EpisodeS2.tsx` is selected by `"season": 2`, so `src/Episode.tsx` is untouched for EP01–EP25.
  - The 3D canvas renders at 360×640 and is upscaled ×3 with `image-rendering: pixelated`.
- **The world:** `src/s2/world/`:
  - the seeded Isle (`island.ts`, 46×46 columns with strata) and its renderer (`IslandMesh.tsx`, with per-frame graze, forest, snow, ring and ripple layers);
  - the voxel Grimmaw and the instanced mossback herd (`Creatures.tsx`, with outlines);
  - the timeline: camera, light moods, clock, sim speed, populations and predator states, all keyed to spoken words (`timeline.ts`, `keys.ts`);
  - the scene (`WorldScene.tsx`).
- **Overlays:** `src/s2/overlays/`: sim bar, graph, field card, kinetic type, stamp, world-pinned labels, Zs, delete brackets, rewind, block wipe, sting, end card. Captions: `src/s2/CaptionsS2.tsx`.
- **Sound:**
  - Narration: Kokoro `af_heart` at speed 1.05.
  - Score (v2): `pipeline/music_s2.py`, a composed score (the series theme, D minor → D major, about 100 BPM on a tempo map fitted to the narration) played by FluidSynth on the MuseScore General SoundFont. v1 used the synth beat grid in `pipeline/score_s2.py`.
  - SFX: the World Engine palette in `pipeline/score_s2.py`, plus `roar` and `stompHit` in v2.
  - Mix: `mix.py` with a per-episode override: v2 sets `musicLufs` −25, `duckDb` −8, `sfxLufs` −29 and `voiceFx`; v1 used −28 / −6.
- **Art:** one Figma generation (§5), re-gridded by the new `pipeline/pixelate.py`.
- **Fonts** (Fontsource, SIL OFL, self-hosted in `public/fonts/`): Silkscreen, Pixelify Sans and Inter 900 are new; Cormorant Garamond is kept for the two serif lines.

## 3. Narration (159 words, measured 51.55 s of speech, 60.3 s total)

> If your giant predator eats everything, why hasn't everything gone extinct? Let's test it. This is the Grimmaw. It eats anything that moves. Press run. Year one: mossbacks everywhere. Year three: thinning. Year five: gone. With nothing left to hunt, the Grimmaw starves too. A monster that eats everything doesn't rule your world. It ends it. Real predators live inside limits. Four are easy. The fifth is the twist. One: prey that breeds faster than it's eaten. Two: territory. One Grimmaw needs a whole valley. Three: energy. A body this big hunts rarely and sleeps a lot. Four: slow breeding. One cub every few winters. Run it again. Now the numbers rise and fall, but nothing vanishes. Rule five? Delete the monster. The mossbacks boom, strip the meadow bare, then starve. Rule five is its job. The Grimmaw holds the island together. Don't design a monster. Design its place in the world. Share this with someone designing fantasy monsters.

- **Measured with the real TTS** before any cue was set. At speed 1.0 it ran 61.86 s; at **1.05** it runs **60.30 s**, a brisker host read.
- **G2P checked:** "Grimmaw" → ɡɹˈɪmɔ (GRIM-aw), "mossbacks" → mˈɔsbˌæks.
- **Landmarks:**
  - re-hook "The fifth is the twist" at **24.1 s**;
  - "Delete" at **43.24 s**;
  - "together" at **50.56 s**;
  - CTA ends at **57.6 s**, then a 2.4 s tail under the end card and the loop.

## 4. Timed storyboard

| Time | Shot | Narration | Picture |
|---|---|---|---|
| 0:00.0–0:04.6 | `hook` | If your giant predator eats everything, why hasn't everything gone extinct? | The Grimmaw in profile on the meadow of the Isle, mossbacks grazing around it; WORLD ENGINE boots top-right as the island ripples. |
| 0:04.6–0:09.2 | `setup` | Let's test it. This is the Grimmaw. It eats anything that moves. Press run. | Field card intro (sprite x3, GRIMMAW, APEX PREDATOR, DIET anything that moves) over the Grimmaw walking in profile; the sim bar slides in and RUN is pressed. |
| 0:09.2–0:13.8 | `run1` | Year one: mossbacks everywhere. Year three: thinning. Year five: gone. | The whole Isle; clock 0→5, MOSSBACKS 120→0 while the graph falls; herds thin everywhere. |
| 0:13.8–0:16.7 | `starve` | With nothing left to hunt, the Grimmaw starves too. | The Grimmaw walks an empty meadow at dusk, then lies down and greys. Pin: FOOD IN RANGE / NONE. |
| 0:16.7–0:20.9 | `ends` | A monster that eats everything doesn't rule your world. It ends it. | The whole island desaturated and empty; EXTINCT stamp; 'IT ENDS IT.' in rust. |
| 0:20.9–0:25.6 | `rehook` | Real predators live inside limits. Four are easy. The fifth is the twist. | REWIND chip and scanlines; clock and herd run back; the checklist card with a blinking locked row 5. |
| 0:25.6–0:27.9 | `prey` | One: prey that breeds faster than it's eaten. | Close on a herd; lambs pop in small and grow; pin SPRING +55 BORN; row 1 ticks. |
| 0:27.9–0:30.9 | `range` | Two: territory. One Grimmaw needs a whole valley. | Top-down Isle; three territory rings painted on the voxels (outside dimmed); two more Grimmaws appear, one per valley; card folds. |
| 0:30.9–0:34.6 | `energy` | Three: energy. A body this big hunts rarely and sleeps a lot. | The Grimmaw walks to its den at the foot of the peak and lies down to sleep; Zs. |
| 0:34.6–0:38.0 | `breed` | Four: slow breeding. One cub every few winters. | Winter falls over the den (snow on voxels and trees); one cub pops in beside the sleeping Grimmaw. |
| 0:38.0–0:42.4 | `run2` | Run it again. Now the numbers rise and fall, but nothing vanishes. | Wide Isle, winters flicker past, years 3→23; graph shows prey and predators rising and falling; STABLE stamp. |
| 0:42.4–0:47.6 | `twist` | Rule five? Delete the monster. The mossbacks boom, strip the meadow bare, then starve. | RULE 5? then selection brackets + DEL: the three Grimmaws fly apart into voxels; mossbacks boom to 380, strip the meadow to dirt, the forest thins, then the herd crashes. |
| 0:47.6–0:51.4 | `role` | Rule five is its job. The Grimmaw holds the island together. | Row 5 unlocks (ROLE · keeps the grazers in check); the Grimmaws re-appear, the meadow and forest heal, the island ripples on 'together'. |
| 0:51.4–0:54.7 | `lesson` | Don't design a monster. Design its place in the world. | The complete field card (BEFORE YOU DESIGN A MONSTER / GRIMMAW / 5 rows ticked) with 'Design its place in the world.' in serif italic. |
| 0:54.7–1:00.3 | `cta` | Share this with someone designing fantasy monsters. | End card: logo, EPISODE 26 / 50, title, SHARE THIS with someone designing fantasy monsters; it lifts to reveal the hook frame and title again. |

## 5. Generated assets

- **Figma** (file "Worldcraft Shorts EP26 art", `7wHdle0cigAS8MhVmZzZYJ`, plan `team::1384938462301182142`):
  - **1 generation** with `gpt-image-2.5-sunburst`: "Detailed 16-bit pixel art sprite of an original fantasy creature, full body, side view …" (full prompt in [`art/PROMPT.md`](art/PROMPT.md)). The result is an original hulking grey striped predator with rust spine plates, a bone skull-mask and an underslung jaw. It was right first time.
  - Saved at `episodes/ep26/art/grimmaw_sunburst.png` (1536×1024) and re-gridded by `pipeline/pixelate.py` to `episodes/ep26/assets/grimmaw_sprite.png` (168×108, 28 colours, transparent).
  - The same prompt on `gpt-image-2.5-flare` and `gemini-3.1-flash-image` was **blocked by the session's permission check before running** (no credits used), so the planned three-model comparison is incomplete.
- **Code-drawn:** everything else.
  - The island and its strata, every creature (the voxel Grimmaw was built to match the sprite's palette and silhouette), the herd and its births, territory rings, snow, overgrazing, the forest thinning.
  - The HUD, graphs, cards, stamps, sting, end card, all type.
- **No readable text in any generated image.** The creatures are original.

## 6. Final video and verification

**v2 (2 Nov 2026), the current files:**
- **QA:** `qa.py` **passed** on the master (49.1 MB), compat (42.2 MB), download (two-pass 1,600k, 14.1 MB) and player (two-pass 1,300k, 11.9 MB). All are 60.35 s, −14.0 LUFS, TP −1.4 dB.
- **Preview page:** the download copy published on the same page (version 3, https://claude.ai/artifact/CQMMgqMj4M6J1cjkLtCxRe) reads back byte-identical (sha256 `5d3b4d5d…`) and passes `qa.py`. The player is asset `/_blob/bd011c29ae5d5ce855c3ade80b3d42fa`; the v1 player asset was deleted after it was replaced.
- **Render:** 716 s.
- **Inspected:** the sheet and beat frames from the master, including the roar (1.3–1.9 s) and the "It ends it." handover. That's where v2's first render showed "YOUR WORLD." lingering under the title for about 0.2 s, now fixed in `CaptionsS2`.
- **Mix:** voice/music 14.0 LU.
- **Score checks:** all 16 instrument channels, 927 notes, no missing presets; stereo correlation 0.89 after panning.
- **Cover:** the hook at 1.5 s, mid-roar.
- **Sent in the chat:** `out/ep26_score_only.mp3`, the score by itself, so the music can be judged without the voice.

**v1 (1 Nov 2026), superseded:**
- **Sent with SendUserFile:**
  - `out/ep26.mp4` (master, 48.8 MB);
  - `out/ep26_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 41.9 MB).
- **Used on the preview page:**
  - `ep26_download.mp4`: two-pass **1,600k**, 14.2 MB. The 1,900k suggested in EP25's hand-off would come to about 16.3 MB, over the page-file limit, because the copied 256k AAC adds about 1.9 MB over 60 s.
  - `ep26_player.mp4`: two-pass 1,300k, 11.9 MB. A CRF-26 player came to 24.6 MB at 60 s, because pixel-art 3D is detail-heavy, which is over the asset upload cap.
  - All copies keep the master's audio (`-c:a copy`).
- **QA:** `qa.py` **passed** on all four local files: 1080×1920, 30 fps, **60.35 s** (window 55–62 s from `format.qa`), −14.1 LUFS, true peak −1.4 dB, no black gaps, no frozen video, no dropouts. The download copy published on the preview page (https://claude.ai/artifact/CQMMgqMj4M6J1cjkLtCxRe) was read back with Artifact `read`. It is byte-identical (sha256 `75c1b89e…`), and `qa.py` passes on it (60.35 s, −14.1 LUFS, TP −1.4 dB). The player is asset `/_blob/d117377151b3e95b4b8c742ae3a79494`.
- **Render:** **630 s (10.5 min)** for 1,810 frames with `--gl=swangle` on the 4-vCPU container, about 2.9 frames per second. The first full render took 715 s; trimming shadow casters and drawing only the live herd cut it to 648 s, then 630 s. The bottleneck is Chrome's single GPU process doing software rasterisation for every tab (about 2.7 cores), so more Remotion concurrency doesn't help. Three full renders in total; beat stills come from `pipeline/stills.mjs` at about 2 s each.
- **Inspected:** the contact sheet and 18 beat frames pulled from the master, including the sting, RUN press, delete, unlock, restore, end card and the loop seam, on every render. **Fixes made after looking:**
  1. **Mossbacks were green on a green meadow.** They're now cream wool with dark moss tufts and outlines, and read as a herd even from 190 units away.
  2. **The Grimmaw rendered almost black and read as a block head-on.** It now has a brighter hide, an inverted-hull outline matching the sprite's 1-px outline, and profile cameras.
  3. **Wide shots cropped the island in 9:16.** The maths says a whole-Isle shot needs a camera distance of at least about 180, so every wide shot now uses that.
  4. **The run-1 graph was scaled to 400**, so a herd of 120 sat on the floor. Each graph now has its own maximum.
  5. **The checklist card covered the territory rings.** It folds (`collapse` keys) for the rings and the runs, and land outside the rings dims.
  6. **Voxel clouds floated in front of medium shots as white boxes.** Removed; a pixel starfield and distance haze give the void its depth instead.
  7. **Captions overflowed** ("BIG HUNTS RARELY"). Now 13-character bursts at 78 px.
  8. **"RULE FIVE?" appeared twice** (caption and title). Fixed with `captionsOff` ranges.
  9. **The "+55 BORN" label sat under the caption.** The prey camera was re-aimed by projecting candidate anchors through the same camera maths.
  10. **"BREEDING" ran into its row text.** The label column is wider.
  11. **The Grimmaw counter lagged its reappearance by 0.15 s.** It now steps on the appear cue: the HUD must match the world.
  12. **The end card and the hook title cross-faded on top of each other.** The card now clears (0.3 s) before the title returns, and the last frame matches frame 0.
  13. **"EVERYTHING..." ran past the right safe edge (x ≈ 1075) and "IT ENDS IT." wrapped toward the bottom safe zone.** The ellipsis is gone and that title is now 100 px.
  14. **The hook was re-shot with a long lens** (fov 16.5 from 54 units, chosen over a 22° / 40-unit version), so the predator towers over its herd.
- **Season 1 regression:**
  - After every Season 2 change, EP24's and EP25's music, SFX and mix rebuilt **bit-identical**.
  - Their frame-300 stills render **byte-identical** (same MD5) to the post-merge stills.
- **Accepted compromises:**
  - In the fast-forward frames with hundreds of moving agents, the 1,600k and 1,300k web copies soften. The master and compat copies are crisp.
  - The starving Grimmaw lies down by rolling its voxel body. At that distance it reads as a dark shape settling more than as an animal lying down; the pin (FOOD IN RANGE: NONE) and the counter carry it.
  - The cub is small beside its sleeping parent in the snow; the 1 CUB pin points it out.
  - On the near-top-down territory shot, the north ring sits partly behind the folded card.
  - Lambs are drawn at 55 % size and grow over 4.5 s, so at the prey shot's distance they're only slightly smaller than adults.
- **Not verifiable by me:** how the narration, the new Season 2 score and its sound palette actually sound. I can't hear audio. They are measured (−14.1 LUFS; music about 15.3 LU under the voice, hotter than Season 1's ~19 LU). Please give it one listen, especially the score level under the voice and the `delete` and `stamp` hits.

## 7. Reusable components added

All are documented in `README.md` (Season 2 building blocks) and `docs/STYLE_S2.md`.

- **Composition:** `EpisodeS2` (selected by `"season": 2`).
- **World:** `Stage` (⅓-res pixel WebGL + camera rig + backdrop), the Isle (`island.ts`, `IslandMesh`), `Grimmaw` (walk, sleep, lie, dissolve, appear, spawn / despawn, outlines), `Herd` (instanced, simulation time, births grow, live-count culling), and the timeline (`resolveWorld`, `cameraAt`, `moodAt`, `predatorAt`, `simTime`, keyed sampling and integration).
- **Overlays:** `sting`, `simBar`, `simGraph`, `fieldCard` (intro / checklist / full, locked rows, `collapse`), `kinetic`, `stamp`, `pin`, `zzz`, `deleteFx`, `rewind`, `blockWipe`, `endCardS2`. Captions: `CaptionsS2` (with `captionsOff` ranges).
- **Music (v2):** `music_s2.py`, the composed-score engine (tempo map to picture, the series theme, 14 arrangement styles, accents, rests, fade).
- **Mix (v2):** `mix.voiceFx` narration polish.
- **World (v2):** the `roar` predator state and the `dust` layer.
- **Sound:** `score_s2.py` (beat-grid music with layered sections, drones and fade-out, plus the SFX palette: `sting`, `runPress`, `simTicks`, `births`, `losses`, `stamp`, `rewind`, `ringOn`, `snowAir`, `sleepZ`, `cubPop`, `delete`, `restore`, `cardSlide`, `check`, `unlock`, `worldRipple`, `stomp`, `crash`, `boomPop`).
- **Pipeline:**
  - `pixelate.py`;
  - `stills.mjs` (renders chosen frames in one browser session) and `tile.py`;
  - `encode.sh` (compat, two-pass download and player, all `-c:a copy`);
  - `build.sh` now copies `episodes/epNN/assets/`;
  - `qa.py` takes its window from `format.qa`;
  - `mix.py` takes the optional per-episode `mix`.
- **Backwards compatibility, verified:** after the `score.py` change, EP24's and EP25's `music.wav` and `sfx.wav` rebuilt **bit-identical**; after the `mix.py` change, EP25's `mix.wav` is bit-identical. My first S2 sound name, `ripple`, collided with EP22's, so it was renamed `worldRipple`. Stills of EP24 and EP25 render after the merge. EP01–EP25 have no `format.qa`, so `qa.py` keeps 27–33 s for them.

## 8. Cost (₱63.35 = $1)

**$0 cash.** One Figma AI generation (of the ~12 allowed for EP26). Everything else is free and open: Kokoro, fonts, three.js, the container. Details in `docs/COSTS.md`.

## 9. Platform metadata

In `episode.json → metadata`, and ready to paste in `docs/DISTRIBUTION.md` ("Episode 26 captions").
- YouTube title: *Don't Design a Monster. Design an Ecosystem. (Worldbuilding)*. Alternate: *Why your apex predator would starve*.
- TikTok caption: 244 characters.
- Instagram hook: "Your monster would starve."
- Pinned comments ask which of the five rules the viewer's monster breaks.
- AI label ON on all four platforms.

## 10. Experiments and metrics

- **The relaunch is the experiment.** For EP26–EP28, compare against the EP21–EP25 averages:
  - **average percentage viewed** (it drops naturally with length, so also compare **average view duration in seconds**);
  - **viewed vs swiped away** (the frame-0 hook);
  - **shares per 1,000 views** (the CTA and the field card);
  - **replays** (the loop).
- **Re-hook check:** in YouTube Studio's retention curve, look for a dip at about 20 s and a recovery after "The fifth is the twist". A cliff instead means the run-1 / drop section is too long.
- **Save signal:** the full card at 51–55 s is designed as the screenshot moment. If comments quote the five rules, keep the card format; if not, try a "save this" kicker on the card.
- **A/B idea for EP27:** the same format with the Isle seen at golden hour, to test whether warmer light lifts the first-second hold.

## 11. How to produce EP27 ("What Would Dragons Actually Change?", Arc 6)

1. **Branch:** `claude/worldcraft-ep27` from `claude/worldcraft-ep26`, which has EP01–EP26.

   **Read:**
   - `CLAUDE.md` and **`docs/STYLE_S2.md`** (Season 2 rules); `docs/SEASON2_RESEARCH.md` if you need the why;
   - this brief, especially §6 (what was fixed) and the render notes.

2. **Plan entry:**
   - Hook: "If dragons existed, your world's architecture would look very different."
   - Core: flying predators change roof design, livestock protection, military strategy, settlement placement and travel; ask what ordinary people must do differently.
   - CTA (a comment CTA): "What would your civilization invent to survive dragons?"

3. **Story on the Isle** (it grows: EP27 adds the first village):
   - **Hook:** a naive village on the meadow (thatched roofs, open pens, a hilltop hall) and a dragon's shadow sweeping the island.
   - **Run 1:** the dragon flies its route, roofs char (voxels turn black and smoke, nobody shown), the LIVESTOCK counter falls, and the trade road empties.
   - **Re-hook:** a field card for the DRAGON (one Figma pixel sprite, then `pixelate.py`), with four easy rows and one locked.
   - **The fixes, each one visible in the world:**
     - ROOFS: slate and turf replace thatch;
     - PENS: covered barns;
     - PLACE: the settlement moves into a valley or cliff, out of sight lines;
     - TRAVEL: night roads or a tunnel.
   - **Twist candidates** (pick one):
     - the sky becomes a border, so trade goes underground;
     - towers and bells change who holds power;
     - people *use* the dragon, with its burns clearing farmland.
   - Keep it about ordinary people's choices. No one is harmed on screen.

4. **New pieces this needs** (add to `src/s2/world/`; outline them like the Grimmaw):
   - voxel buildings with a roof material switch (thatch → slate) and a `char` amount;
   - a flying dragon (wing-flap gait, flight keys with altitude, a ground shadow);
   - livestock (re-skin `Herd`: white sheep with dark heads);
   - a `settlement` layer.
   - Reuse everything else: sim bar counters (e.g. ROOFS, LIVESTOCK, TRADE), graphs, field card, stamps, rewind, end card.
   - Use a comment CTA on `endCardS2` (`cta: "COMMENT"` with a speech-bubble sprite, which you'll need to add to `Pixel.tsx`).

5. **Music:** copy EP26's `MUSIC` plan (`"engine": "s2-score"`). Keep the series theme (it's the sonic logo), pick a style per beat (a `drive` for each run, `build` layers as the fixes switch on, `anthem` for the lesson), and put an accent (`hit` / `boom` / `stab`) on each punchline. Check the loudness envelope and the instrument list as in §v2, since you can't listen either.

6. **Art:** Figma credits need the user's go-ahead for each new episode (`CLAUDE.md`), and in EP26 this session's permission check blocked 2 of 3 generate calls. **Ask first** with AskUserQuestion: 1–2 generations for the dragon sprite. Fallback: local SDXL (`pipeline/local_stills.py`, prompt for a pixel-art sprite on a flat navy background), then `pixelate.py`.

7. **Narration:** 140–160 words, Kokoro `af_heart` at speed 1.05, measured before cueing. Check "dragon" names in the G2P if you invent one.

8. **Then:**
   - `python episodes/ep27/make_ep27.py` → `pipeline/build.sh ep27`;
   - beat stills with `node pipeline/stills.mjs` and `tile.py`;
   - render with `--gl=swangle` (EP26: 10.5 min), then `qa.py` (55–62 s), the sheet and beat frames including the loop tail;
   - `pipeline/encode.sh ep27` (1600k download), with `qa.py` on each;
   - `srt.py`, `storyboard.py`, the cover, the 11-section brief, docs (COSTS, DISTRIBUTION, README, STYLE_S2 if a rule changes);
   - a **new** preview page (same pattern as EP26's) with the Download button, then SendUserFile;
   - push to the episode branch.

9. **Scope after EP27:** EP28 intelligent species, EP29 immortality, EP30 a monster people worship. The Isle keeps what earlier episodes added (village, roads), so plan landmarks with `island.ts` `LANDMARKS`.
