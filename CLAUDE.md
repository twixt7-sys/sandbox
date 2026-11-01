# Worldcraft Shorts: standing rules

These apply to every episode and every session working in this repo.

## Brand (default, always on)
- The series logo is `public/brand/logo.png` (source: `series/brand/logo-source.png`). Use it **unaltered**: white brackets around a grey "T", designed for dark backgrounds. Don't recolor, crop or redraw it.
- Every episode shows it two ways, configured in `series/series.json → brand`:
  - a corner logo, top-left inside the safe area (x 90, y 236, 66 px tall), drawn by `LogoBug` in `src/Episode.tsx`;
  - the full logo on the end card or CTA card (`useBrand()` + `<Logo>` in `src/brand/Logo.tsx`). Set `"hideLogoBug": true` on that shot so the logo isn't shown twice.
- Keep top-left editorial elements (tags, chips) at y ≥ 336 so they clear the corner logo.
- Series name: **Worldcraft Shorts**. Tagline: "Worldbuilding, from the ground up".

## Series style
- **Season 2 (EP26–EP50): read `docs/STYLE_S2.md` ("The World Engine") before designing any episode from EP26 on**, and follow its concept, 60-second story shape, look, layout, camera, motion vocabulary, sound, CTA card and delivery rules. Season 2 episodes set `"season": 2` in `episode.json` and render through `src/s2/EpisodeS2.tsx` (one persistent pixel-voxel island, the Isle; ▶ RUN; the field card). Why: `docs/SEASON2_RESEARCH.md`. Reuse `src/s2/*` and add new pieces only for genuinely new kinds of visuals.
- **Season 1 (EP01–EP25): `docs/STYLE.md` still governs them.** They must keep rendering exactly as before: anything global (composition, captions, QA, score, mix) changes only additively or behind the season / per-episode switches.

## Production conventions
- One episode = one folder `episodes/epNN/` with `episode.json` (script, shots, cues, prompts, metadata), `plates/` and `plates.json`. Generated audio and timing go to `public/epNN/` (gitignored; `pipeline/build.sh epNN` rebuilds them).
- Stills: Figma `generate_image` with the user's Figma AI credits (approved for Episode 01; confirm before using them for a new episode), saved as `episodes/epNN/plates/<shot>.jpg` at 1080×1920, then `python pipeline/plates.py epNN --register`. Never ask a model to render readable text; all typography is added in Remotion.
- Render with `--gl=angle` (set in `remotion.config.ts`); it's ~8× faster than swangle on CPU-only machines. **Exception, Season 2:** WebGL can't get a context under `angle` in the cloud container, so S2 renders pass `--gl=swangle` (about 12 min per 60 s episode).
- Every render must pass `python pipeline/qa.py out/epNN.mp4 --sheet out/epNN_sheet.jpg`, and the contact sheet must be visually inspected before delivery. The duration window comes from `episode.json → format.qa` (Season 2: 55–62 s; 27–33 s when unset).
- Don't spend money (Runway, ElevenLabs, AWS) without the user's approval. `plates.py` is a dry run unless `--yes`.
- Every episode's browser-preview Artifact has a **Download MP4 button** by default: declare `capabilities: {downloads: true}` and call `claude.use("downloads").save({filename, data})` on click (a plain `<a download>` is inert in artifacts). A page file can't exceed 15 MB, so publish a two-pass near-master copy (about `-b:v 3300k` for 30 s; about `-b:v 1600k` for a 60 s Season 2 episode (the copied 256k audio adds ~1.9 MB); under 15 MB) as `epNN_download.mp4`, keep the lighter CRF-26 copy for the player, and say that the untouched master goes through SendUserFile. Never overwrite another episode's page.
- Platform metadata lives in `episode.json → metadata`. Research notes and AI-disclosure guidance: `docs/DISTRIBUTION.md`. Turn the AI label on for all platforms.
