# Worldcraft Shorts, Season 2 style guide: "The World Engine" (EP26–EP50)

From EP26, every episode follows this guide. `docs/STYLE.md` still governs EP01–EP25, and those episodes must keep rendering exactly as they did. Why Season 2 looks like this is recorded in `docs/SEASON2_RESEARCH.md`; this file says *how*.

**The reference episode is EP31** (`episodes/ep31/`): its script, its brief and its scorecard (`pipeline/benchmark.py`, 25/25) are the worked example of everything below. Start a new episode from `episodes/ep31/make_ep31.py` and `episodes/ep31/BRIEF.md` §11.

## The concept in one line
**One living pixel-voxel island (the Isle) where every episode tests a worldbuilding idea by pressing ▶ RUN:** the naive design visibly breaks, the fix visibly works, a twist shows what most people miss, and the viewer leaves with a field card checklist.

Four things recur in every episode. They are the series' signature, so don't drop them:
1. **The Isle:** the same seeded voxel island (`ISLE_SEED = 26` in `src/s2/world/island.ts`). Episodes add what lives and is built on it; they never regenerate the ground. Landmarks: the peak (NW), the forest (SW), the lake (centre), the meadows (E and N).
2. **▶ RUN:** the sim bar's button. Pressing it fast-forwards the world (clock, populations, seasons) with the world ripple and the `runPress` sound. Use at least two runs: the naive one and the fixed one.
3. **The field card:** a creature, institution or idea as a game-style card. It starts as an intro card, becomes a numbered checklist with a locked row (the visual open loop), and ends as the full card, which is the takeaway viewers save and share.
4. **The World Engine chime and the ending formula** (from EP26 v3): the season's sound logo at the same three moments, and an ending that says the part number, asks for the follow with a reason, and opens the next run. See [The ending formula](#the-ending-formula-from-ep26-v3).

## Format
- 1080×1920, 30 fps, **55–62 s** (`episode.json → format.qa`; `pipeline/qa.py` reads it). H.264 yuv420p BT.709 + AAC, −14 LUFS, true peak ≤ −1 dB.
- `"season": 2` in `episode.json` selects `src/s2/EpisodeS2.tsx`. Without it, the Season 1 composition renders unchanged.
- **Render with `--gl=swangle`.** WebGL can't get a context under `angle` in the cloud container. Season 1 stays on `angle` (set in `remotion.config.ts`).
- The 3D stage renders at ⅓ size (360×640) and is upscaled ×3 with nearest-neighbour filtering. **One S2 pixel = 3 output px.** Sprites, HUD icons and borders snap to that grid.
- Narration: about 140–170 words, Kokoro `af_heart` at speed **1.05–1.07** (brisk host read; EP26 v3 runs 169 words at 1.07 in 60.97 s; EP31 runs 161 words at 1.05 in 59.47 s). Measure with the real TTS before locking cues, and check invented names in the G2P (`KPipeline(...)(text).phonemes`).
- **Writing rules (from EP31, checked by the scorecard):** one idea, one example, one sentence to keep. The hook is one question of 12 words or fewer that ends by 4 s, with its first word inside 0.5 s. Sentences average 6 words or fewer and none is longer than 12. No pause between lines longer than 0.45 s. The hook's question is answered by the twist, not before it.

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
| 48–50 s | **Light follow nudge** | `followChip` (+ FOLLOW · PART NN/50) top-right, only *after* the payoff line lands; no voice |
| 50–53 s | **Lesson** | The full card, complete: the screenshot moment, in golden light. One serif italic line carries the principle, on screen for at least 1.2 s (from EP31). The **chime** plays as it lands |
| 53–55 s | **Share ask** | `blockWipe` → `endCardS2` (full logo, PART NN / 50, title, the share ask) for about 2 s |
| 55–61 s | **The ending formula, then loop** | Part number, follow with a reason, next-run tease, then the hook title fades back in and the last frame matches frame 0 (camera, light, world, title). Details below |

Re-hook around 18–25 s and twist around 36–47 s are deliberate; keep them near those marks (the scorecard checks both). The table's times are EP26's; EP31's are in its brief.

## Look
- **Background:** deep midnight radial gradient per mood (`MOODS` in `src/s2/world/timeline.ts`): `day`, `dusk`, `gloom` (desaturated: failure), `winter`, `night`, `golden`. The island floats in the void like a diorama on a dark desk. Each mood also sets the sun's elevation and azimuth (`el`, `az`).
- **Golden-hour bookends** (from EP26 v3): frame 0 and the ending are `golden` (sun 16° high from az 58°, front-right of the hook camera: warm lit faces, long shadows, an amber glow behind the island), so the loop frame matches frame 0 and the first second is the warmest, most saturated image in the episode. Switch to `day` on the first setup line; return to `golden` for the lesson.
- **Hard pixel shadows everywhere:** every creature, tree and voxel casts and receives (BasicShadowMap 1024², a ±38-unit box). `Lights` rebuilds the shadow camera's projection after R3F sets the bounds; before EP26 v3 the box silently stayed at three.js's ±5 default, so only the island's centre had cast shadows.
- **Ambient life, on by default** (`world.ambient`): two loose flocks of voxel birds circling, pollen motes drifting over the meadows (warm in golden light), glints twinkling on the water. It keeps every wide shot alive between beats. Turn a part off with `{birds: 0}` etc.
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
| Device strip (EP30+) | 1352–1568 | x 96–900: the episode's device under the world (EP30's ledger, EP31's chronicles). Put what matters most at its top (EP31: the verdicts and the spine). Third-party safe-zone guides reserve the bottom 300–340 px for platform UI (`docs/SEASON2_RESEARCH.md` §7), so the strip ends 12 px above the most cautious of them; check it in each app's preview before posting |
| Free | > 1580 and x > 920 | Platform UI |

**Type sizes that survive a phone (from EP31):** nothing the viewer has to read is smaller than 18 px (caps, letter-spaced) or 20 px (Pixelify body); verdicts and numbers are 40 px or more. EP30's ledger labels (12 px) were too small to read on a phone; EP31's chronicles use 18 / 20 / 44.

The ending stack (55–61 s, captions off): `seasonBar` y 350–508, `followButton` 556–734, `nextRun` 772–958, all x 96–900, over the hook frame. `followChip` sits where the sting was (top-right, y 246–296), after the payoff.

## Camera (keys in `episode.world.camera`, eased over `dur`, optional `cut`, slow `drift` in deg/s)
- **Hero close:** dist 34–40, el 10–14, fov 22, profile azimuth. Introductions. For the **hook**, use a long lens (EP26: fov 16.5 from dist 54, el 8): less perspective, so the creature towers over everything around it.
- **Medium:** dist 80–100, el 28–36, fov 24.
- **Wide (whole Isle):** dist ≥ 180, el 42–66, fov 26. Anything closer crops the island in 9:16.
- **Frontal on one centre line (EP31):** when an episode sets two sides against each other, fix the azimuth so one side is always screen-left and the other screen-right, and *cut* between poses on that line instead of orbiting (EP31: az 0 on the statue's centre line, valley left, court right; hook el 9, dist 76, fov 15). Check every pose with a projection probe so older landmarks fall outside the frame.
- Every key may drift 1–3°/s. Pushes and orbits only: no shakes, whip-pans or spins (Season 1 rule, kept). The stamp's 0.3 s shake is the single exception.

## Motion vocabulary (reuse; don't invent new ones per episode)
| Event | Visual | Sound (`pipeline/score_s2.py`) |
|---|---|---|
| Series sting (t = 0) | `sting` label typing in + world ripple | the **chime** + `worldRipple`, over the score's opening theme (EP26 v2 used the `sting` square arpeggio here) |
| **Sound logo** (3 fixed moments) | frame 0 · the full lesson card lands · the follow button is pressed | `chime`; `engineWind` 0.5 s before it when there's room (and at end −0.54 s, so the loop's wind-up lands on frame 0's chime) |
| RUN | Button press, `RUNNING` blink, world ripple, clock racing | `runPress` + `worldRipple` + `simTicks` bed |
| Births | Small agents pop in and grow over 4.5 s | `births` bed |
| Losses | Agents shrink out | `losses` bed |
| Failure | Mood → gloom, rust `stamp` | `stamp`, music drop to near-silence + a `boom` accent on the punchline |
| A creature's display (hook) | `roar` state (head up, jaw open, body rocks back) + `dust` ring at its feet | `roar` + `stompHit` |
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
| Looking up | `alert` state (head up to the sky, mouth shut, settles back before its next key) | — |
| Part number | `seasonBar`: PART NN / 50 counts up as a 50-segment bar fills to NN; the current segment blinks | `simTicks` bed for the fill |
| Follow | `followButton`: a pixel pointer glides in and taps "+ FOLLOW / FOR PART NN+1" on the word "Follow"; flash, sparks, flips to ✓ FOLLOWING | `followPress` + `chime` |
| Next run | `nextRun`: NEXT RUN · NN+1 with a locked silhouette and ???, decoding to the title on its cue | `cardSlide` in, `unlock` on the reveal |
| A dragon (EP27+) | `dragons`: perched in the sprite's pose (wings raised), `roar` on the hook, takes off and circles in `fly`, `glide` for passes; it hunts *things in the open*, never people | `roar` + `stompHit` on its display, `dragonPass` on each takeoff / pass |
| A creature's point of view (EP27+) | `dragonEye`: the frame tinted in the episode's motif colour, brackets locking onto what it can see, a TARGETS count read from the world; `light` to keep counting through the fixes; `tower` for the other side looking back | `eyeOn` as it switches on, `lockOn` bed while targets lock, `unlock` as a target hides |
| Riding with a creature (EP27+) | camera `follow` with `look`: over its shoulder at what it's looking at; loop-safe when the creature's path is a closed orbit timed to the loop | — |
| A trait slider moves (EP28+) | `editor` / `fieldCard.sliders`: a knob slides from HUMAN to the species' value; the body (`folk` eyes / wet / glow) and the village (`sink`, `stone`, `show`, `stiltsB`, `open`, `glow`) change with it, and a `readout` (HUMAN-LIKE %) falls | `slide` + `morph` (body) or `restore` (buildings) |
| Generations turn over (EP29+) | `people` on the clock (born, grey, gone, replaced in new colours) beside a ruler who never changes; the `lineage` strip scrolls one cell per generation with a badge for the current rule; the camera stays **locked off** (drift 0) while the clock races | `clockTicks` bed, `crownPass` as a generation or crown passes |
| Roofs burn (EP27+) | `settlement.char`: thatch blackens and breaks one roof at a time, smoke rises; no people anywhere | `burn` bed |
| A change switches on in the village (EP27+) | `roof` (thatch → slate / turf), `cover` (barns rise), `place` (unbuild at A, rise at B), `route` + `lanterns` (night road), `tower` (rises, bell swings) | `restore`, `check`; `towerBell` for the bell |
| A deal is weighed (EP30+) | `ledger`: GIFTS and COSTS hang on a balance beam; items join, grow or lift off on their keys (or follow a world series), and the beam tips: TIPPED, LEVEL, WORTH IT, EMPTY | `beamTip` each time the balance changes |
| A ritual switches on (EP30+) | `shrine` props: the shrine rises (`rise`), candles light (`lights`), a tithe sheep, sheaves and plates are laid before it; the crowd walks to it and rings it (`people.gather`); keepers in robes (`people.robe`) | `frameDrum`, `restore`, `check` |
| Two tellings of one event (EP31+) | `chronicles`: two open pages under the world, one per teller. Each fact is written, never written, lost (PAGE LOST) or the truth on each page; a one-word verdict heads each page; the spine shows how much the pages agree (· · · until both are written, then a percentage, BOTH TRUE, or THE TRUTH · HIDDEN). Write each page on the word that names its witness | `quill` for each entry, `pageTear` when a page is lost, `unlock` on the truth, `stamp` when it is hidden |
| What a witness never saw (EP31+) | `veil`: the unseen half of the frame is hatched out (UNSEEN) and the seen half is labelled with the witness (`side` left / right); `middle` hides a centre band (the author hiding the truth) | `eyeOn` |
| Two readings of one picture (EP31+) | `splitTone`: the frame graded in two halves along a seam, warm on one side, drained and rust on the other; `pulses` make a half answer a spoken word. List it in an early shot so it draws under the HUD | `crownPass` / `stompHit` on the hook's two words |
| A monument changes with its tellers (EP31+) | `statue` prop: `rise` (built), `gild` (one half gilded, its torch lit, flowers), `tar` (the other half tarred and scratched), `grow` (taller with each retelling) | `restore` as it rises, `unlock` on the gilding, `stamp` on the tar, `morph` as it grows |
| A field burns (EP31+) | `fields.burn`: the crop chars from one edge, flames and smoke above it; no people in it | `burn` bed |
| One named person in the crowd (EP31+) | `people.figures`: a keyed figure with her own tunic, scale and a torch; `people.watch` turns the crowd to face a point; `people.tints` dresses each crowd centre in its own colour | — |
| A word answers the voice (EP31+) | `kinetic` parts with `pulseAt`: a title word already on screen flares on its spoken cue (the hook's HERO, then MONSTER?) | the hook's two sounds |
| A vote (EP31+) | `endCardS2.choices`: answer chips pop on their spoken words (HERO, MONSTER), then the ask (`with`, on `withAt`) | `check` per chip |
| A war in the ground (EP32+) | `world.strata`: the war is a dark layer in the Isle's cut side flecked with bronze-green, centuries pile on it as thin bands, it sinks and fades when forgotten, veins rise from it to the grass for each consequence, and its colour floods up to the surface when the war is still on; the `strata` overlay pins a depth ruler and vein tags to it | `rumble` bed while the centuries pile on, `dig` as each vein is seeded |
| A border drawn (EP32+) | `border` prop: boundary stones rise along a line from the middle outward | `stones` |
| A fear and its answer (EP33+) | `world.fears`: a fear is an indigo shadow on the map (`dark`), a belief a lamplit pool with a bright rim that opens inside it (`lit`), with a lamp post and its rite (`offerings`, `lanterns`, `sheaves`, robed keepers); an `umbra` (an eclipse's shadow) crosses the map and lamps burn inside it; `fearTags` name each fear, then its answer | `creep` bed as shadows spread, `lampOn` as each light opens |
| A people looks up (EP33+) | `people.look` tilts every head back to the sky (faces to an overhead camera); `people.lamps` puts a lamp in their hands | — |
| A crack of light (EP33+) | a `rift` fear: glowing voxels open along a line in the turf from its middle out (something buried under the myth) | `rift` |
| The next creature, teased in-world | `flyers`: a shadow-only creature crosses the Isle (EP26: a dragon's shadow sweeps the meadow and the Grimmaw looks up). EP31 teases a war: two `standard` props rise over the two crowds | `dragonPass` (whoosh + wingbeats, panning with it); EP31: `towerBell` + `frameDrum` |

- **Settlements (EP27+):** the Isle now has a village (`settlement` in `episode.world`). Frame 0 and the loop frame show the *naive* village (thatch, open pens, the road over the open meadow); everything the episode changes resets under the share card's wipe. Later episodes can start from either site; plan landmarks with the constants at the top of `make_ep27.py`.
- **Deaths are never shown as violence.** A starving creature lies down, greys and dissolves out of the simulation. Prey loss is a falling counter and agents shrinking away, never a kill.
- **Numbers on screen must match the world.** The HUD, graphs and visible agents all read the same keys (`herd.count`, `pred`, `clock`).

## Sound
- **Music, default from EP26 v2 (`music.engine: "s2-score"`, `pipeline/music_s2.py`):** a composed score played on sampled instruments (FluidSynth + the MuseScore General SoundFont, MIT).
  - **The series theme:** a 4-bar melody (D A D F E | D E F A, then B A F E D | E F E D in D major). It recurs every episode, in minor for the problem and in major for the payoff. It's the season's musical identity, so keep it.
  - **Tempo map to picture:** each section starts on a spoken cue, and the beat stretches slightly (±5 BPM around 100) so every change lands exactly on its story beat.
  - **Styles:** `hook`, `pulse`, `drive` (16th marimba + chip arps + pizzicato + bass + drums; `theme: true` adds the melody), `drop`, `void`, `mystery`, `build` with `layer` 1–4 (one instrument family joins per rule), `twist`, `rest`, `frenzy`, `crash`, `swell`, `anthem`, `outro`, `chronicle` with `layer` 1–4 (EP31: a lute ostinato, tambourine, pizzicato bass, the theme on recorder, then harp and glockenspiel), `dispute` (EP31: the theme's bars alternate between a recorder and a bassoon), `tease` (the last line: the dominant held as open fifths, chord `A5`, under the theme's first bar asked as a question).
  - **Accents on exact cues:** `hit`, `boom`, `stab`, `cymbal`, `riser`, `call` (a horn call in open fifths: the next creature), `roll` (a timpani roll swelling into the cue, e.g. the loop point).
  - **Rests:** `rests` silences windows such as the beat after "Delete".
  - **Fade:** `fadeOut: {"fromEnd": 0.08}` plays to the loop point with only a click-free fade (from EP26 v3); `{"at", "dur"}` fades earlier.
  - **The arc:** curious hook → driving run → drop to near-silence → layered build as the fixes switch on → full groove on run 2 → dark twist with a hard stop → big hit on the resolution → anthem lesson → soft outro under the share ask → the tease holds the dominant to the end, and the loop resolves it into frame 0's D minor.
  - **Setup:** `apt-get install fluidsynth musescore-general-soundfont-small` and `pip install mido`.
  - **Fallback:** the original synth engine (`"engine": "s2"`, `score_s2.py`) still works.
- **Mix:** `episode.mix` sets `musicLufs` −25, `duckDb` −8, `sfxLufs` −29 and `voiceFx: true`.
  - The music sits about 14 LU under the voice, ducks 8 dB while she speaks and swells in the gaps.
  - `voiceFx` is phone clarity: high-pass 85 Hz, +2.5 dB at 3.2 kHz, a touch of air, gentle 2.5:1 compression.
  - Season 1 episodes set no `mix`, so their audio is bit-identical (verified for EP24 and EP25).
- **The World Engine chime, the season's sound logo** (Season 1 had its sine bells): a rising open fifth D5 A5 D6 A6 on music box with 8-bit square blips, ringing D7 on music box and glockenspiel, about 2.9 s with its tail. `render_chime()` (`pipeline/music_s2.py`) renders it once from the score's SoundFont, and it plays as the SFX `chime`: the same clip every time, always on D, never ducked. It sits about 6–7 LU under the voice. Use it only at its three moments (frame 0, the lesson card, the follow press) so it stays a signal, and keep `engineWind` (a clockwork ratchet that winds up into it) for the moments with room before them.
- **SFX:** synthesised, from the palette table above, one sound per event, reused every episode. The chime is the one SoundFont-rendered clip. New sounds get their own seeded random generator (EP31's `quill` and `pageTear` use seeds 311 and 312), so adding one never changes an older episode's audio.

## Captions
- `CaptionsS2`: 1–3-word bursts, ≤13 characters. Each word pops on its own timestamp; emphasis words in ember.
- Turn captions off where a kinetic title says the same words (`captions: false` on the shot, or `captionsOff: [{line, from, to?}]`).

## CTA card (`endCardS2`)
Full logo (y 268) → `PART NN / 50` (Silkscreen, amber) → title in Cormorant italic → a pixel panel with the ask (pixel icon + `SEND THIS` / `SHARE THIS` / `COMMENT` …, then Inter 800 detail) → footer `WORLDCRAFT SHORTS · WORLDBUILDING, FROM THE GROUND UP`. For a comment ask with two answers, `choices` shows them as chips that pop on their spoken words, and `with` (on `withAt`) carries the ask (EP31: HERO / MONSTER, "Give us your verdict."). It comes in on a `blockWipe` (anything that has to jump for the loop, like the camera cut to the hook pose, jumps on the wipe's midpoint) and lifts on the word "Part" for the ending formula.

## The ending formula (from EP26 v3)
Why: `docs/SEASON2_RESEARCH.md` → "Follow ask, part numbers and the sound logo". The formula is the same every episode so it becomes familiar.

1. **Spoken, as the last line:** "Part NN of 50. Follow for part NN+1: <a concrete tease>." The tease names the next run in a few words (EP26: "a dragon lands here."). Specific beats generic: never "follow for more".
2. **Shown at the same time** (captions off; the overlays carry the words): `seasonBar` on "Part", `followButton` pressed on "Follow" with `followPress` + the chime, `nextRun` in on "NN+1" with a locked silhouette, decoding to the title on the tease word.
3. **Teased in the world:** the next episode's subject appears *indirectly* on the Isle (a shadow, a sound, a footprint), and the current creature reacts (`alert`). The tease is the open loop; the next episode closes it.
4. **Loop, seamless:** the overlays clear at the tease line's end + 0.6 s (gone 0.3 s later), *then* the hook title fades back in. Everything else lands on frame 0:
   - **Camera:** cut on the share card's wipe, drifting so it lands exactly on frame 0's pose (`loop_span()` in `make_ep26.py`).
   - **Light:** `golden`.
   - **The herd:** `world.simLoop` (a cue under the wipe) resets sim time so it reaches 0 at the end.
   - **Ambient motion:** birds, pollen, star twinkle, water shimmer and grazing heads run whole cycles per episode (`loopFreq` in `src/s2/keys.ts`).
   - **Sound:** the music holds the dominant to the end, and `engineWind` winds up into frame 0's chime.
   - **Result (EP26 v3):** the last frame differs from frame 0 by under 0.5/255 on average, against about 19/255 before the reset.
5. **A light mid-video nudge**, once: `followChip` for about 2 s right after the payoff line, never before it.
6. **Metadata** repeats it: descriptions end "Part NN of 50. Follow for part NN+1: …".

## Art
- **The world and creatures are code** (voxels). Generated art is used for **field card sprites only**:
  - Figma `generate_image` (`gpt-image-2.5-sunburst` gave the best EP26 sprite);
  - prompt for "detailed 16-bit pixel art sprite … side view … crisp dark one-pixel outline … plain flat dark navy background … no text";
  - then `python pipeline/pixelate.py src.png episodes/epNN/assets/<name>.png --width 168 --colors 28`.
  - Shown at ×3, the sprite sits on the same pixel grid as the world.
  - Build the voxel model to match the sprite's palette and silhouette.
- **Free alternative (EP31):** the local SDXL-Lightning pipeline (`pipeline/local_stills.py`, about 2 minutes an image on 4 CPU cores, no credits). It can't follow a compositional instruction such as "left half gilded, right half tarred", so ask it for the plain subject on a flat background and make the change in code (`episodes/ep31/art/split_statue.py`), then `pixelate.py`. For sprites, `--sprite --prompt "…"` fuses a pixel-art LoRA into the model and draws a real pixel grid at the same speed (tested on EP31; use it from EP32). Run it alone: it needs about 10 GB of RAM, and a render or a TTS build beside it gets killed.
- Creatures, dress and architecture are original. No readable text in generated art (all type is code). Look at each candidate before using it: a statue with a crown and a raised torch came back looking like a real monument and was rejected.
- Runtime assets go in `episodes/epNN/assets/`; `pipeline/build.sh` copies them to `public/epNN/`.

## Delivery (every S2 episode)
1. `python episodes/epNN/make_epNN.py` → `pipeline/build.sh epNN`.
   - Then **the scorecard:** `python pipeline/benchmark.py epNN ep31` (25 rows: hook, pace, how often the picture changes, where the beats land, how long the lesson line can be read, the ending, the loop; why in `docs/SEASON2_RESEARCH.md` §7). Fix every ✗ before rendering, or say in the brief why it stays.
2. Beat stills: `node pipeline/stills.mjs epNN out/epNN_beats <seconds…>` and `python3 pipeline/tile.py out/epNN_beats out/epNN_beats.jpg`.
3. Render: `npx remotion render Episode out/epNN.mp4 --props='{"episodeId":"epNN"}' --gl=swangle --browser-executable <headless shell>` (10–20 min for 60 s with full shadows and ambient life, depending on the crowd: EP29 18 min, EP30 9, EP31 9).
4. `python pipeline/qa.py out/epNN.mp4 --sheet out/epNN_sheet.jpg`, then inspect the sheet and the beat frames, including the loop tail.
5. Encodes, all `-c:a copy` and each through `qa.py`:
   - compat: H.264 Main, CRF 20, `+faststart`;
   - download: two-pass at **1,600k** so it stays under 15 MB at 60 s (the copied 256k audio adds about 1.9 MB, and 1,900k would come to about 16.3 MB);
   - player: two-pass 1,300k (≈12 MB). A CRF-26 copy of a 60 s pixel-art render is about 25 MB, over the asset upload cap.
6. SRT, storyboard, cover, the 11-section brief, docs, preview page with a Download button, then SendUserFile.

## Make every episode its own (from EP27 v2)
The recurring signature (the Isle, ▶ RUN, the field card with a locked row, the chime, the ending formula, golden bookends) is what makes an episode *Season 2*. Inside it, each episode needs **its own idea that the viewer could describe in one line**, so episodes never feel like re-skins of each other:
- **One episode device:** a new way of *seeing* the run, built on the episode's subject (EP27: the dragon's-eye view: what a predator sees is a target, and every fix removes targets). It should carry the hook, the failure, the fixes and the payoff, not just appear once.
- **One camera language:** EP26 is grounded profile shots and orbits; EP27 rides on the dragon's back. Don't re-use the previous episode's hook pose.
- **One motif colour** (named in the brief; EP27: dragon-sight red `#ff5a4e`) and **one band of music colour** around the series theme (EP27: `soar`, `raid`, `stealth`).
- **EP28's answer:** the device is the *species editor* (a character creator whose sliders rebuild the world), the camera stays at the species' eye height, the motif colour is bioluminescent teal `#5fe0c0`, and the music band is `folk` / `glow`.
- **EP29's answer:** the device is the *lineage strip* (generations born, greying and gone beneath a ruler whose cell never changes), the camera is a *locked-off tripod* (each tableau holds one frame while centuries pass through it), the motif colour is ageless violet `#b48cff`, and the music band is `clockwork` / `reign`.
- **EP30's answer:** the device is the *ledger* (a balance beam under the world: what the monster gives on one pan, what it costs on the other, and every ritual is a weight that levels it), the camera takes the *worshipper's angle* (low and long-lensed, the monster against the sky over its people), the motif colour is shrine madder `#ef6f9c`, and the music band is `hymn` / `rite`.
- **EP31's answer:** the device is the *two chronicles* (two open pages under the world, one per teller, and a spine that counts how much they agree) with the *witness veil* in the world; the camera language is the *split frame* (everything frontal on one centre line, one side's telling on the left, the other's on the right, the picture itself graded in two halves); the motif colour is chronicle ink `#7f95ff`; and the music band is `chronicle` / `dispute`.
- **EP32's answer:** the device is *the strata* (the war is a layer in the Isle's cut side with every century since laid on top of it; a war that only ended sinks and fades, a war that matters sends verdigris veins up through every layer to the grass, and at the twist the war's own colour floods up to the surface), the camera language is *the cutaway crane* (one azimuth facing the cut, moving only up and down between the war below and today above; the only orbit is the lesson wide), the motif colour is verdigris `#46c2a0` (the war's bronze, turned green in the ground), and the music band is `dirge` / `earth`.
- **EP33's answer:** the device is *the fear map* (what a people fears is drawn on the Isle as indigo shadows, and each belief is a lamplit pool that opens inside one, with its rite growing in the light; gods invented first are lamps on sunny ground that answer nothing and go out; the twist is the deepest fear, that nobody is listening, and the god is the last light), the camera language is *the map table* (every pose looks almost straight down with north up and only slides and zooms across the Isle like a hand over a map; the only turn is the lesson, when the map rotates), the motif colour is lamplight `#ffe45c`, and the music band is `vigil` / `lantern`.
- **Fresh wording for the recurring beats:** the drop line, the stamp, the run-2 verdict and the checklist title belong to the episode's own idea (EP27: "They just lived in plain sight"; TARGETS 00, NOTHING TO HUNT; HIDE FROM THE SKY).

## Making the next episode
- **Start from EP31.** Copy `episodes/ep31/make_ep31.py` (not EP26's): it has the helpers the later episodes needed (`jump` for hard changes on a cut, `shift`, `loop_span`, frontal poses as named dicts), and `episodes/ep31/BRIEF.md` §11 is the hand-off checklist.
- **Lessons from EP31, in the order they cost time:**
  - *A block wipe is centred on its cue.* The frame is fully covered at `at`, so every state that has to jump under a wipe (camera cut, clock, props, light) is keyed at the wipe's own cue, not after it.
  - *A graphic ends where the next shot starts* unless it has an `end`. Anything that must still be on screen in the last frame (the split tone, the returning hook title) belongs in the last shot's list.
  - *Overlays draw in shot order, then list order.* A full-frame grade goes in an early shot's list so the HUD draws over it.
  - *The device changes on the spoken word.* EP31's first render wrote the valley's page before anyone had named the valley; the final version writes each page as its witness is named. If a sound (`quill`) plays, something has to be written.
  - *A line the viewer should keep needs time to be read.* The lesson line used to arrive on the last spoken word and leave with the card half a second later (EP29, EP30, and EP31's first render). Bring it in as the first sentence ends (`subtitleAt`) and hold the card until the wipe covers it. The same goes for the reveal word: EP31's BOTH now holds through the next three words.
  - *Nothing static for more than 2.5 s.* The scorecard found a 3.7 s hold in the hook and 2.8 s in run 1; the fixes were small (two title pulses, a verdict stamped each century).
  - *Look at a model's output before building on it.* The first statue silhouette read as a slab at phone size, and the first sprite looked like a real landmark.
- **Low angles on the Isle (learned on EP30):** a camera at eye height (1–2 units above the grass, negative elevation) almost never works here. The meadows are terraced voxels, trees and buildings sit everywhere, and anything within ten units fills the frame. The worshipper's angle that works is a *low elevation from medium distance on a long lens* (el 5–12°, dist 30–44, fov 15–22), which puts the subject against the sky with its people small below it. Check each pose before rendering with `pipeline/camprobe.ts` (from EP31; usage at the top of the file): it prints the line of sight's tightest clearance over the terrain and trees, and where each landmark you name (the Fenn's great hall, the cairn, the Queen's dais, your subject) lands in the 1080×1920 frame, or that it falls outside it.
- Copy `episodes/ep26/make_ep26.py`. Keep the Isle; add new species or props in `src/s2/world/` (voxel parts with outlines) and new overlay types in `src/s2/overlays/` only for genuinely new kinds of visuals.
- The world timeline is keyed to spoken words (`cue(line, word, offset)`), so re-measuring the TTS moves every beat with the voice. `{"end": true, "offset": -0.5}` is a cue relative to the episode's end (the loop point), in both the Python pipeline and Remotion.
- Order on a narration change: `tts.py` → `make_epNN.py` (the loop camera reads the measured timing) → `build.sh`.
- Plan the camera first: hero close for introductions, wide for every run, and no wide shot closer than dist 180.
