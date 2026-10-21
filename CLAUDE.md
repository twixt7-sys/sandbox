# Worldcraft Shorts: standing rules

These apply to every episode and every session working in this repo.

## Brand (default, always on)
- The series logo is `public/brand/logo.png` (source: `series/brand/logo-source.png`). Use it **unaltered**: white brackets around a grey "T", designed for dark backgrounds. Don't recolor, crop or redraw it.
- Every episode shows it two ways, configured in `series/series.json → brand`:
  - a corner logo, top-left inside the safe area (x 90, y 236, 66 px tall), drawn by `LogoBug` in `src/Episode.tsx`;
  - the full logo on the end card or CTA card (`useBrand()` + `<Logo>` in `src/brand/Logo.tsx`). Set `"hideLogoBug": true` on that shot so the logo isn't shown twice.
- Keep top-left editorial elements (tags, chips) at y ≥ 336 so they clear the corner logo.
- Series name: **Worldcraft Shorts**. Tagline: "Worldbuilding, from the ground up".

## Production conventions
- One episode = one folder `episodes/epNN/` with `episode.json` (script, shots, cues, prompts, metadata), `plates/` and `plates.json`. Generated audio and timing go to `public/epNN/` (gitignored; `pipeline/build.sh epNN` rebuilds them).
- Stills: Figma `generate_image` with the user's Figma AI credits (approved for Episode 01; confirm before using them for a new episode), saved as `episodes/epNN/plates/<shot>.jpg` at 1080×1920, then `python pipeline/plates.py epNN --register`. Never ask a model to render readable text; all typography is added in Remotion.
- Render with `--gl=angle` (set in `remotion.config.ts`); it's ~8× faster than swangle on CPU-only machines.
- Every render must pass `python pipeline/qa.py out/epNN.mp4 --sheet out/epNN_sheet.jpg`, and the contact sheet must be visually inspected before delivery.
- Don't spend money (Runway, ElevenLabs, AWS) without the user's approval. `plates.py` is a dry run unless `--yes`.
- Every episode's browser-preview Artifact has a **Download MP4 button** by default: declare `capabilities: {downloads: true}` and call `claude.use("downloads").save({filename, data})` on click (a plain `<a download>` is inert in artifacts). A page file can't exceed 15 MB, so publish a two-pass near-master copy (about `-b:v 3300k`, under 15 MB) as `epNN_download.mp4`, keep the lighter CRF-26 copy for the player, and say that the untouched master goes through SendUserFile. Never overwrite another episode's page.
- Platform metadata lives in `episode.json → metadata`. Research notes and AI-disclosure guidance: `docs/DISTRIBUTION.md`. Turn the AI label on for all platforms.
