# Worldcraft Shorts

A config-driven production system for **Worldbuilding, from the ground up**, a series of 30-second vertical fantasy-documentary lessons (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels.

Rendering and generation all run in the cloud (GitHub Actions or a Claude Code cloud session). Your computer only needs a browser.

```
episodes/<ep>/episode.json  ──►  pipeline/build.sh  ──►  remotion render  ──►  pipeline/qa.py  ──►  MP4 artifact
   script · shots · prompts       TTS + word timings       scenes, maps,          duration, size,
   cues · sfx · metadata          score + SFX + mix        captions, grade        loudness, black/
                                  (-14 LUFS, ducked)       (1080×1920@30)         freeze, contact sheet
          └── optional: pipeline/plates.py → AI stills / image-to-video clips per shot (dry-run by default)
```

## Layout

| Path | What it is |
|---|---|
| `series/series.json` | Brand constants: palette, type, safe areas, image-style suffix, loudness target |
| `episodes/<ep>/episode.json` | **The only file you edit per episode:** narration lines, shots, prompts, graphics cues, SFX cues, music, metadata |
| `episodes/<ep>/STORYBOARD.md` | Generated production doc (timed shots, prompts, captions, metadata) |
| `pipeline/tts.py` | Narration: Kokoro (free, default) or ElevenLabs (`--provider elevenlabs`), with word timings and scripted pauses |
| `pipeline/score.py` | Original score and sound design synthesized from cues (no licensing) |
| `pipeline/mix.py` | Loudness gain-staging, music ducking under the voice, two-pass EBU R128 to −14 LUFS / −1.5 dBTP |
| `pipeline/plates.py` | Runway stills and image-to-video clips per shot, with a cost quote and spend guard |
| `pipeline/qa.py` | Automated checks and contact sheet; exits non-zero on failure |
| `src/scenes/` | Procedural scenes (valley, river-level, bridge, map, lantern river, end card) and `PlateScene` for AI plates |
| `src/graphics/` | Reusable editorial graphics: year counter, oversized word, statement, tag, dated label, ledger, end card |
| `src/captions/` | Phrase-chunked, word-timed captions with selective emphasis, inside the safe area |
| `.github/workflows/render.yml` | Cloud render on push or manual dispatch; uploads MP4, QA report and contact sheet |

Docs: [research and stack decision](docs/RESEARCH.md) · [costs](docs/COSTS.md) · [distribution and experiments](docs/DISTRIBUTION.md)

## Render in the cloud (no local install)

1. GitHub → **Actions → Render episode → Run workflow**, then pick the episode (e.g. `ep02`) and the voice provider. Pushing changes to `episodes/**` also triggers a render.
2. When the run finishes, open it and download the **`<ep>-render`** artifact. It contains `out/<ep>.mp4`, the QA JSON and a contact sheet.
3. Optional secrets (Settings → Secrets and variables → Actions): `ELEVENLABS_API_KEY`, `RUNWAYML_API_SECRET`.

## Producing Episode 02

1. Ask Claude: *"Write ep02 for Worldcraft Shorts: topic X, hook Y. Copy episodes/ep01/episode.json's structure."*
2. Claude creates `episodes/ep02/episode.json`:
   - **lines**: 8–10 short spoken lines, 60–75 words. Map each to a shot id and set `pauseAfter` and `emphasis`.
   - **shots**: 5–6 shots. Each needs a `scene` (an existing procedural scene, or any scene plus a plate), an `imagePrompt` and a `videoPrompt`. Graphics cues reference spoken words, e.g. `{"line":"L4","word":"bridge"}`, so timing stays in sync automatically.
   - **metadata** for the three platforms.
3. Optional AI plates: `python pipeline/plates.py ep02` (quote only), then `--yes --video hook,payoff`.
4. Push. The workflow narrates, scores, mixes, renders and QA-checks the episode. Review the MP4 and contact sheet.
5. To fix something, edit the JSON and push again. To retime, adjust `pauseAfter`. To re-roll one plate, use `plates.py ep02 --yes --only lore`.

New *kinds* of visuals, such as a new diagram type, are added once as a component in `src/graphics` or `src/scenes` and reused in every later episode.

## Local / Claude-session commands

```bash
npm ci
pip install -r pipeline/requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu   # + ffmpeg, espeak-ng
pipeline/build.sh ep01                   # narration, timings, score, mix -> public/ep01
npx remotion render Episode out/ep01.mp4 --props='{"episodeId":"ep01"}'
python pipeline/qa.py out/ep01.mp4 --sheet out/ep01_sheet.jpg
python pipeline/storyboard.py ep01
```

## Licensing notes

- Voice: Kokoro-82M is Apache-2.0. ElevenLabs output needs a paid plan for commercial use. Don't clone a real person's voice without authorization.
- Music and SFX are synthesized in code from scratch, with no samples, so you own them.
- Fonts: Cormorant Garamond and Inter, SIL Open Font License (`public/fonts/LICENSE-*`).
- Remotion is free for individuals and companies of 3 or fewer people. Above that, you need a company license.
