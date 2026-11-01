# Worldcraft Shorts, Season 2 style guide: "The World Engine" (EP26–EP50)

From EP26, every episode follows this guide. `docs/STYLE.md` still governs EP01–EP25, and those episodes must keep rendering exactly as they did. Why Season 2 looks like this is recorded in `docs/SEASON2_RESEARCH.md`; this file says *how*.

## The concept in one line
**One living pixel-voxel island (the Isle) where every episode tests a worldbuilding idea by pressing ▶ RUN:** the naive design visibly breaks, the fix visibly works, a twist shows what most people miss, and the viewer leaves with a field card checklist.

Three things recur in every episode. They are the series' signature, so don't drop them:
1. **The Isle:** the same seeded voxel island (`ISLE_SEED = 26` in `src/s2/world/island.ts`). Episodes add what lives and is built on it; they never regenerate the ground. Landmarks: the peak (NW), the forest (SW), the lake (centre), the meadows (E and N).
2. **▶ RUN:** the sim bar's button. Pressing it fast-forwards the world (clock, populations, seasons) with the world ripple and the `runPress` sound. Use at least two runs: the naive one and the fixed one.
3. **The field card:** a creature, institution or idea as a game-style card. It starts as an intro card, becomes a numbered checklist with a locked row (the visual open loop), and ends as the full card, which is the takeaway viewers save and share.

## Format
- 1080×1920, 30 fps, **55–62 s** (`episode.json → format.qa`; `pipeline/qa.py` reads it). H.264 yuv420p BT.709 + AAC, −14 LUFS, true peak ≤ −1 dB.
- `"season": 2` in `episode.json` selects `src/s2/EpisodeS2.tsx`. Without it, the Season 1 composition renders unchanged.
- **Render with `--gl=swangle`.** WebGL can't get a context under `angle` in the cloud container. Season 1 stays on `angle` (set in `remotion.config.ts`).
- The 3D stage renders at ⅓ size (360×640) and is upscaled ×3 with nearest-neighbour filtering. **One S2 pixel = 3 output px.** Sprites, HUD icons and borders snap to that grid.
- Narration: about 140–160 words, Kokoro `af_heart` at speed **1.05** (brisk host read). Measure with the real TTS before locking cues, and check invented names in the G2P (`KPipeline(...)(text).phonemes`).

## Story shape (60 s)
| Time | Beat | What's on screen |
|---|---|---|
| 0–4 s | **Hook:** the question over the world | Frame 0 is complete: subject plus big kinetic question (captions off). The **sting** (≤1.5 s) boots *over* the hook, never before it |
| 4–9 s | **Setup:** meet the subject, then "Press run." | Field card intro (sprite, name, one rust "danger" line), then sim bar in and ▶ RUN pressed |
| 9–17 s | **Run 1:** the naive design runs and fails | Wide shot, clock racing, counters and graph falling. Then a close-up of the consequence (an empty range, never a kill) |
| 17–21 s | **The drop** | Gloom mood, rust **stamp** (EXTINCT, COLLAPSED…), music cuts to a drone, kinetic one-liner |
| 21–25 s | **Re-hook:** rewind and an open loop | `rewind` + `blockWipe`, world restored. Checklist card with N−1 easy rows and **one locked row** ("the twist") |
| 25–38 s | **The fixes**, one rule per 2–4 s | Each rule switches on *in the world* (births, territory rings, sleep, winter). Its row ticks and its music layer joins |
| 38–42 s | **Run 2:** it works | Groove at full, graph oscillating, STABLE stamp |
| 42–51 s | **The twist:** the locked rule | A surprising experiment (e.g. DELETE the monster) and its consequence, then the row unlocks |
| 51–55 s | **Lesson** | The full card, complete: the screenshot moment. One serif italic line carries the principle |
| 55–60 s | **CTA, then loop** | `endCardS2` (full logo, episode N / 50, title, the share or comment ask). The last 0.7 s returns to frame 0 exactly: same camera, world state and hook title |

Re-hook around 20–25 s and twist around 43–47 s are deliberate; keep them near those marks.

## Look
- **Background:** deep midnight radial gradient per mood (`MOODS` in `src/s2/world/timeline.ts`): `day`, `dusk`, `gloom` (desaturated: failure), `winter`, `night`. The island floats in the void like a diorama on a dark desk.
- **World palette** (code, `BIOME_COLORS`): meadow `#86bb5c`, forest `#557f3c` with trees `#2f6a3c`/`#3a7a44`, water `#3f86b0`, sand `#dcc895`, rock `#8c9097`, snow `#eef3f5`, dirt (overgrazed) `#8f6c46`. Cut sides show soil, clay and rock strata ("from the ground up").
- **Creatures** are voxel models with a dark inverted-hull outline (`#12151c`), which matches the 1-px outline of their pixel sprites. Silhouette first: show predators **in profile** for close-ups (camera azimuth roughly perpendicular to the heading).
- **Series palette kept:** night, parchment `#efe6d2` (type), amber `#e9a94b` (kickers), ember `#f4c46e` (key words, the RUN button), rust `#d0603f` (failure: zero counters, stamps, struck lines). Season 2 adds **prey green** `#9bd16a` (populations, STABLE), **predator orange** `#f08a4b`, and **sky** `#8fc8ff` (rewind, sleep). Episodes may add one motif colour; name it in the brief.
- **Type:**
  - **Silkscreen:** HUD, labels, kinetic titles, stamps.
  - **Pixelify Sans:** card body text.
  - **Inter 900:** captions.
  - **Cormorant Garamond italic:** exactly two places, the lesson line on the full card and the title on the end card. That serif bridges back to the Season 1 brand.
  - All fonts are self-hosted (SIL OFL) in `public/fonts/`.
- **Brand:** unchanged. The corner logo is drawn automatically, top-left (x 90, y 236, 66 tall). The full logo appears only on `endCardS2`, and the CTA shot sets `hideLogoBug` with `hideLogoBugUntil` (a cue) so the corner logo is back for the loop frame. Name and tagline as in `CLAUDE.md`.

## Layout (px, 1080×1920)
| Zone | y | Notes |
|---|---|---|
| Corner logo | 236–302 (left) | Never covered |
| Sting | 246–300 (right, ends x ≤ 920) | First 1.5 s only |
| Sim bar | 340–432 | x 96–900 |
| Card / graph / kinetic | 448–~900 | Fold the checklist (`collapse` keys) whenever the world needs the space (wide rings, a run's graph) |
| World focus | ~800–1300 | Frame subjects here with the camera target's y (raise target y to push the world down) |
| Captions | centred on 1238 | 1–3 words, ≤13 chars, Inter 900 caps, 7-px outline |
| Free | > 1360 and x > 920 | Platform UI |

## Camera (keys in `episode.world.camera`, eased over `dur`, optional `cut`, slow `drift` in deg/s)
- **Hero close:** dist 34–40, el 10–14, fov 22, profile azimuth. Introductions. For the **hook**, use a long lens (EP26: fov 16.5 from dist 54, el 8): less perspective, so the creature towers over everything around it.
- **Medium:** dist 80–100, el 28–36, fov 24.
- **Wide (whole Isle):** dist ≥ 180, el 42–66, fov 26. Anything closer crops the island in 9:16.
- Every key may drift 1–3°/s. Pushes and orbits only: no shakes, whip-pans or spins (Season 1 rule, kept). The stamp's 0.3 s shake is the single exception.

## Motion vocabulary (reuse; don't invent new ones per episode)
| Event | Visual | Sound (`pipeline/score_s2.py`) |
|---|---|---|
| Series sting (t = 0) | `sting` label typing in + world ripple | `sting` + `worldRipple` |
| RUN | Button press, `RUNNING` blink, world ripple, clock racing | `runPress` + `worldRipple` + `simTicks` bed |
| Births | Small agents pop in and grow over 4.5 s | `births` bed |
| Losses | Agents shrink out | `losses` bed |
| Failure | Mood → gloom, rust `stamp` | `stamp`, music drop + drone |
| Rewind | `rewind` overlay + `blockWipe`, clock and populations run back | `rewind` |
| Card in / out | Slide 0.35 s | `cardSlide` |
| Row ticks | Checkbox fills, text slides in | `check` |
| Locked row opens | Ember fill | `unlock` |
| Territory | Rings painted on the voxels, outside dimmed | `ringOn` |
| Winter | Snow layer on columns and trees | `snowAir` |
| Sleep | `zzz` pinned to the creature | `sleepZ` |
| Delete (an experiment, never a death) | `deleteFx` brackets + DEL key, voxels fly apart | `delete` |
| Restore | `appear` (reverse fly-apart), layers heal | `restore` |
| Population boom | Dense pops | `boomPop` |
| Crash | Graph falls | `crash` |

- **Deaths are never shown as violence.** A starving creature lies down, greys and dissolves out of the simulation. Prey loss is a falling counter and agents shrinking away, never a kill.
- **Numbers on screen must match the world.** The HUD, graphs and visible agents all read the same keys (`herd.count`, `pred`, `clock`).

## Sound
- **Music** (`music.engine: "s2"`): a beat grid (default 100 BPM) with sections from cues. Each section names chords and layers (`pad`, `arp` 8/16, `bass`, `kick` four/half/heart/one, `hats` 8/16, `clap`, `bells`). The arc: sparse hook → driving run → drop to drone → rebuild layer by layer as fixes switch on → full groove on run 2 → dark twist → major resolution → soft outro, faded out (`fadeOut`) before the loop point.
- **Mix:** `episode.mix` (`musicLufs` −28, `duckDb` −6, `sfxLufs` −29) puts the music about 15 LU under the voice, hotter than Season 1's ~19 LU. Season 1 episodes don't set `mix`, so their mix is unchanged (verified bit-identical for EP25).
- **SFX:** synthesised only, from the palette table above, one sound per event, reused every episode.

## Captions
- `CaptionsS2`: 1–3-word bursts, ≤13 characters. Each word pops on its own timestamp; emphasis words in ember.
- Turn captions off where a kinetic title says the same words (`captions: false` on the shot, or `captionsOff: [{line, from, to?}]`).

## CTA card (`endCardS2`)
Full logo (y 268) → `EPISODE NN / 50` (Silkscreen, amber) → title in Cormorant italic → a pixel panel with the ask (pixel icon + `SHARE THIS` / `COMMENT` …, then Inter 800 detail) → footer `WORLDCRAFT SHORTS · WORLDBUILDING, FROM THE GROUND UP`. It fades out over the last ~0.6 s into the loop frame.

## Art
- **The world and creatures are code** (voxels). Generated art is used for **field card sprites only**:
  - Figma `generate_image` (`gpt-image-2.5-sunburst` gave the best EP26 sprite);
  - prompt for "detailed 16-bit pixel art sprite … side view … crisp dark one-pixel outline … plain flat dark navy background … no text";
  - then `python pipeline/pixelate.py src.png episodes/epNN/assets/<name>.png --width 168 --colors 28`.
  - Shown at ×3, the sprite sits on the same pixel grid as the world.
  - Build the voxel model to match the sprite's palette and silhouette.
- Creatures, dress and architecture are original. No readable text in generated art (all type is code).
- Runtime assets go in `episodes/epNN/assets/`; `pipeline/build.sh` copies them to `public/epNN/`.

## Delivery (every S2 episode)
1. `python episodes/epNN/make_epNN.py` → `pipeline/build.sh epNN`.
2. Beat stills: `node pipeline/stills.mjs epNN out/epNN_beats <seconds…>` and `python3 pipeline/tile.py out/epNN_beats out/epNN_beats.jpg`.
3. Render: `npx remotion render Episode out/epNN.mp4 --props='{"episodeId":"epNN"}' --gl=swangle --browser-executable <headless shell>` (about 12 min for 60 s).
4. `python pipeline/qa.py out/epNN.mp4 --sheet out/epNN_sheet.jpg`, then inspect the sheet and the beat frames, including the loop tail.
5. Encodes, all `-c:a copy` and each through `qa.py`:
   - compat: H.264 Main, CRF 20, `+faststart`;
   - download: two-pass at **1,600k** so it stays under 15 MB at 60 s (the copied 256k audio adds about 1.9 MB, and 1,900k would come to about 16.3 MB);
   - player: two-pass 1,300k (≈12 MB). A CRF-26 copy of a 60 s pixel-art render is about 25 MB, over the asset upload cap.
6. SRT, storyboard, cover, the 11-section brief, docs, preview page with a Download button, then SendUserFile.

## Making the next episode
- Copy `episodes/ep26/make_ep26.py`. Keep the Isle; add new species or props in `src/s2/world/` (voxel parts with outlines) and new overlay types in `src/s2/overlays/` only for genuinely new kinds of visuals.
- The world timeline is keyed to spoken words (`cue(line, word, offset)`), so re-measuring the TTS moves every beat with the voice.
- Plan the camera first: hero close for introductions, wide for every run, and no wide shot closer than dist 180.
