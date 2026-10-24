# Worldcraft Shorts: series style guide

Every episode, from 01 to 50, follows this guide so the series reads as one show. It records what EP01–EP03 actually use. Change it only on purpose, and then update earlier episodes or note the break here.

## Format
- 1080×1920, 30 fps, about 30 s (27–33 s passes QA). H.264 yuv420p BT.709 + AAC, −14 LUFS, true peak ≤ −1 dB.
- 6–8 shots. Every shot carries new information; no motion for its own sake.

## Story shape (every episode)
1. **Hook, 0–4 s:** the strongest line over the most striking image. No intro, greeting or logo animation; the corner logo is already there.
2. **Example:** one original fantasy scenario, shown as cause and effect over 2–4 shots, each with a tag naming what it demonstrates.
3. **Lesson:** a clean diagram or stack on a dark background (`nightSky` scene or dimmed `plateBands`). Spell the principle out in on-screen words.
   EP09 varied it again: the hook's wrong image (desert robes in a blizzard) was struck out with `reverseCard`, then the culture was rebuilt layer by layer in cause → effect lines ("Wind bites, so…"), annotated with `callout`s and counted by `reasonTally`; the lesson and CTA return to the hook's framing with the person the climate designed, and the loop lands back on the wrong image.
   EP07 varied it again: the example was surveyed on the plate itself (the empty valley), a running `reasonTally` counted the reasons, and the overlap dissolved into the finished city.
   EP08 varied it again as a pull-back: one object (a cup of water) first, then each shot steps out a scale (house → street → road → region map), with `pullBack` shrinking the previous picture into its place in the next one. The lesson returned to the opening object.
   EP10 varied it again: the hook shows the obvious answer (the palace), the map zooms in on it and then pulls back until the real key (one bridge) appears, and the lesson sits over the consequence (the gate shut at night).
   EP12 varied it again as a then/now mirror: two pairs of matched plates (same frame, same objects, three centuries apart). The festival dissolves into the punishment it grew from (`eraShift`), an `originLedger` pairs each custom with its forgotten purpose, and on the lesson the festival grows back over the origin. Darkness is shown only through absence (`headCount`'s empty outlines), never harm.
   EP06 varied this: the lesson was the map's own key (`atlas` scene), lit row by row on the same map the example built. Maps are the default way to explain any geography mechanism in Arc 2.
4. **CTA:** return to the opening image in a changed state (EP02: the sun returns; EP03: the same reservoir at dusk), show `ctaCard`, and cross-fade the last 0.6 s into the first frame so the video loops.

## Look
- **Palette** (`series/series.json`): night `#0b1216`, slate `#16222a`, fog `#9fb1b8`, mist `#d6dfe0`, parchment `#efe6d2` (type), amber `#e9a94b` (accents, emphasis), ember `#f4c46e` (payoff words), rust `#b9543a` ("don't" or struck-out). Diagram backgrounds use deep midnight blue (`#070e1e`–`#0d1a33`). An episode may add one motif colour for its magic or resource (EP02: sun gold; EP03: water `#7fd3ec`). Name it in the episode's storyboard and keep everything else on the series palette.
- **Type:** Cormorant Garamond (display; amber or ember italic for the key words) and Inter (captions 800 weight, and uppercase kickers with 0.22–0.24em letter-spacing). Self-hosted, so never load fonts from a CDN.
- **Stills:** Figma `generate_image` (`gemini-3.1-flash-lite-image`, 1080×1920 requested), lanczos-upscaled. Every prompt starts "Vertical 9:16 cinematic fantasy documentary still" and ends "Painterly realism, atmospheric perspective, 35mm anamorphic look, soft film grain, original architecture/clothing. No text, no letters, no signage, no logos, no watermark." Figures at a modest distance with natural hands; faces partly shaded. Invented peoples wear invented dress: if a plate reads as a specific real culture (EP09's first migration plate looked like a real reindeer-herding people, down to the tents and trim), re-roll it with more invented specifics (colours, animals, objects) rather than ship it.
- **Grade:** the series `Grade`, `Vignette` and `Grain` on every frame (automatic in `src/Episode.tsx`). Use `plateScrim` (0.3–0.75) where type sits over a bright sky.

## Layout (px, 1080×1920 frame)
- Corner logo: x 90, y 236, 66 tall (`LogoBug`, automatic). Never cover it, and don't put the full logo anywhere except the CTA card (`hideLogoBug: true` on that shot).
- Top-left tags (`tag`): y ≥ 336. Kicker in amber caps, then one serif italic line.
- Captions: centred on y 1250, max 20 characters per line, amber on emphasis words only. Keep faces out of y 1200–1300 (use `plateFrame` to reframe).
- Keep the right edge (x > 920) and the bottom (y > 1360) free of anything important; platform buttons and captions sit there.
- Diagram block: y 340–1150.

## Motion
- Camera: slow `push`/`pull`/`drift`/`descend` only (≤ 12 % scale over a shot). No spins, shakes, whip-pans or glitch effects.
  Exception (EP10): a map may pull back from a close-up (up to 2.5×) to the whole map once, on a spoken cue like "Pull back", when the reveal *is* the story. Use `atlas` `zoom.at` so the move lands on the word and takes about 2 s.
- Magic and effects are drawn in code over the plate and pinned to it (`"local": true`), so they move with the camera.
- Text enters with a soft rise and fade or a mask reveal (≤ 0.6 s) and leaves with a short fade. One idea on screen at a time.
- Transitions: hard cut on a spoken word by default. Use dissolves (0.35–0.6 s) into diagrams and the CTA, and `fog`/`flash` only when the story motivates them.

## Sound
- Voice: Kokoro `af_heart` at speed 1.0 (or ElevenLabs when a key exists). About 70–78 words. Warm and measured, never trailer-style.
- Music: synthesized pads in `pipeline/score.py`, one key per episode, building through the example and resolving (minor → major) on the lesson and CTA. Fades out before the last frame.
- SFX: synthesized only, never sampled or downloaded. One signature sound per magic or effect, reused every time it appears.
- Mix: `pipeline/mix.py` (voice −18, music ducked about 19 LU under it). Use `music.events` ducks to let a key line land.

## CTA card
`ctaCard`: full logo (y 300) → "Episode NN / 50" kicker → episode title in italic → "YOUR TURN" (or a fitting kicker) → CTA in 3 short lines of large serif (one line in ember italic) → amber pill (y 1180).

## Delivery (every episode)
- Run `python pipeline/qa.py out/epNN.mp4 --sheet out/epNN_sheet.jpg`, inspect the sheet plus extra frames at every graphic beat, and fix and re-render before delivering.
- Hand the user both `epNN.mp4` (master) and `epNN_compat.mp4` (H.264 Main, CRF 20, `+faststart`) with `SendUserFile`, plus a private preview Artifact page. The video goes in the asset store (`capabilities: {assets: {}}`, upload with `asset: true`, then `src="/_blob/<id>"`), never as a plain page file.
- `duskGrade` always draws a reflecting pool. When the plate has no water there (EP10's plaza), move it off-frame (`pool: [540, 2400, 10, 5]`).
- Encode the player and download copies with the master's audio copied (`-c:a copy`). Re-encoding AAC at 128k pushed EP07's true peak to 0.0 dB and failed QA.
- For a then/now pair, write both prompts with the same layout sentence for sentence (EP12: wall across the middle, one arched gate centred, two round towers, open snow in the lower half); the gates landed within about 60 px, close enough for a dissolve.
- No public GitHub Release unless the user says yes for that episode (they said no for EP03).
