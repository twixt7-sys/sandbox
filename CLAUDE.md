# Worldcraft Shorts: standing rules

These apply to every episode and every session working in this repo.

## Brand (default, always on)
- The series logo is `public/brand/logo.png` (source: `series/brand/logo-source.png`). Use it **unaltered**: white brackets around a grey "T", designed for dark backgrounds. Don't recolor, crop or redraw it.
- Every episode shows it two ways, configured in `series/series.json → brand`:
  - a corner logo, top-left inside the safe area (x 90, y 236, 66 px tall), drawn by `LogoBug` in `src/Episode.tsx`;
  - the full logo on the end card or CTA card (`useBrand()` + `<Logo>` in `src/brand/Logo.tsx`). Set `"hideLogoBug": true` on that shot so the logo isn't shown twice.
- Keep top-left editorial elements (tags, chips) at y ≥ 336 so they clear the corner logo.
- Series name: **Worldcraft Shorts**. Tagline: "Worldbuilding, from the ground up".

## Series style (keep consistent from episode 01 to 50)
- Read `docs/STYLE.md` before designing any episode, and follow its palette, type, layout, story shape, motion, sound, CTA card and delivery rules. Reuse the existing components (`src/graphics/*`, `src/scenes/*`) and add new ones only for genuinely new kinds of visuals.

## Production conventions
- One episode = one folder `episodes/epNN/` with `episode.json` (script, shots, cues, prompts, metadata), `plates/` and `plates.json`. Generated audio and timing go to `public/epNN/` (gitignored; `pipeline/build.sh epNN` rebuilds them).
- Stills: Figma `generate_image` with the user's Figma AI credits (approved for Episode 01; confirm before using them for a new episode), saved as `episodes/epNN/plates/<shot>.jpg` at 1080×1920, then `python pipeline/plates.py epNN --register`. Never ask a model to render readable text; all typography is added in Remotion.
- Render with `--gl=angle` (set in `remotion.config.ts`); it's ~8× faster than swangle on CPU-only machines.
- Every render must pass `python pipeline/qa.py out/epNN.mp4 --sheet out/epNN_sheet.jpg`, and the contact sheet must be visually inspected before delivery.
- Don't spend money (Runway, ElevenLabs, AWS) without the user's approval. `plates.py` is a dry run unless `--yes`.
- Platform metadata lives in `episode.json → metadata`. Research notes and AI-disclosure guidance: `docs/DISTRIBUTION.md`. Turn the AI label on for all platforms.
