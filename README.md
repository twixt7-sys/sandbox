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

## Producing the next episode (EP03 onward)

1. Ask Claude: *"Write ep04 for Worldcraft Shorts: topic X, hook Y. Copy episodes/ep03/episode.json's structure."* Claude asks before spending Figma credits (CLAUDE.md).
2. Claude creates `episodes/ep04/episode.json`:
   - **lines**: 8–10 short spoken lines, 60–75 words. Map each to a shot id and set `pauseAfter` and `emphasis`.
   - **shots**: 5–6 shots. Each needs a `scene` (an existing procedural scene, or any scene plus a plate), an `imagePrompt` and a `videoPrompt`. Graphics cues reference spoken words, e.g. `{"line":"L4","word":"bridge"}`, so timing stays in sync automatically.
   - **metadata** for the three platforms.
3. Optional AI plates. There are two routes:
   - **Figma (in-plan credits):** ask Claude to generate each shot's `imagePrompt` with Figma `generate_image`, save the files as `episodes/ep02/plates/<shot>.jpg`, then run `python pipeline/plates.py ep02 --register`.
   - **Runway (API key):** run `python pipeline/plates.py ep02` for a quote only, then `--yes --video hook,payoff`.
   Plates are committed with the episode. A shot without a plate falls back to its procedural scene.
4. Push. The workflow narrates, scores, mixes, renders and QA-checks the episode. Review the MP4 and contact sheet.
5. To fix something, edit the JSON and push again. To retime, adjust `pauseAfter`. To re-roll one plate, use `plates.py ep02 --yes --only lore`.

New *kinds* of visuals, such as a new diagram type, are added once as a component in `src/graphics` or `src/scenes` and reused in every later episode.

### Reusable building blocks (as of EP03)

| Where | Name | Use |
|---|---|---|
| shot | `plateFrom: "<shot>"` | Reuse another shot's plate (e.g. the same landscape by night) |
| shot | `plateMotion` | `push`, `pull`, `driftL`, `driftR`, `descend`, `still` |
| shot | `plateFrame: {from:{s,x,y}, to:{s,x,y}}` | Custom camera move, e.g. to keep faces below the caption band |
| graphic | `"local": true` | Pin a graphic to the plate so it moves with the camera |
| graphic | `sunCycle` | Code-drawn sun: `vanish` / `night` / `return`, with darkness spreading from it and an optional warm `glow` point |
| graphic | `celestialClock` | 24-hour dial with a one-hour dark sector, orbiting sun, night counter |
| graphic | `gates` | Carved doors swinging open on a cue (reveal transition) |
| graphic | `ringGlow` | Traces and lights a ring in the plate |
| graphic | `consequenceTree` | Premise → 3 consequences (plate medallions) → sum |
| graphic | `method` | "Don't" cloud struck out → "Start with …" word-synced |
| graphic | `levelGauge` | Draining gauge with dated marks (resource running out) |
| graphic | `flicker` | Brown-out stutter that settles dimmer |
| graphic | `allocation` | One supply split between two needs; channel width, percentages and medallion brightness follow the share |
| graphic | `plateBands` + `lessonStack` | Three dimmed plate strips behind a stacked, arrowed lesson |
| graphic | `duskGrade` | Turns a daytime plate into dusk with city lights and a glowing pool |
| graphic | `ctaCard` | Full logo + episode + large CTA + pill (spoken CTA shown verbatim) |
| shot | `startAt: cue` | Cut to a shot mid-line (EP04: town wide → bowl on "to make it believable") |
| graphic | `rain` | Drawn rain streaks (`density`, `opacity`) + optional ripple `splashes: [x0,y0,x1,y1]` |
| graphic | `steam` | Soft rising steam at a plate point (use `local: true`) |
| graphic | `bowlFlip` | Line-art badge: object flips on a cue, rain glances off (makes a custom readable) |
| graphic | `detailChain` | Rows of medallion + detail → arrow → implication, word-synced (FOOD → climate …) |
| graphic | `ctaCard` options | `size` (CTA line size), `icon: "follow"` |
| sfx | `rain`, `footsteps` (beds); `bowlKnock`, `ladle` (hits) | EP04; `market` doubles as quiet market ambience |
| graphic | `endcard`, `tag`, `oversizedWord`, `statement`, `yearCounter`, `dateLabel`, `ledger` | From EP01 |
| scene | `nightSky` | Midnight backdrop for diagrams |
| sfx | `shimmer`, `tonalDrop`, `doors`, `ritualBell`, `sunrise`, `powerDown` (hits); `clock`, `cave`, `market`, `hum`, `room` (beds) | Plus EP01's `wind`, `water`, `ticks`, `swell`, `impact`, `rumble`, `whoosh`, `paper`, `ink`, `coin`, `drum`, `chimes` |
| cue | `nth` | Pick a repeated word: `{"line":"L8","word":"start","nth":2}` |
| music | `drone`, `events: [{"type":"duck","at":cue,…}]` | Root drone and cue-timed music ducks (no more per-episode hacks in `score.py`) |
| graphic | `titleLockup` | Hook title: amber caps kicker + one large serif italic word (EP05) |
| graphic | `evidenceRing` | Thin survey ring with ticks marking a clue on the plate (`local`) |
| graphic | `dustBeam` | Dust motes drifting inside a light beam polygon (`local`) |
| graphic | `ghostLines` | SVG line drawing over a plate, drawn path by path between two cues: reconstruction of ruins, a missing span (`local`; `dash`, `color`, `width`, `instant`) |
| graphic | `reverseCard` | "Don't …" struck in rust → method kicker → large serif payoff line |
| graphic | `emberDusk` | Dusk grade without city lights (for ruins) |
| sfx | `stoneShift`, `resonance`, `rebuild` (hits) | EP05: stone settling, dormant bronze mechanism, reconstruction lines drawing in |
| scene | `atlas` | Data-driven fantasy map (EP06): define `episode.atlas.features` once (`range`, `river`, `region`, `fields`, `town`, `route` with `flow`, `arrow` with `stop`, `cut`, `pattern`, `gate`, `coin`, `wash`, `label`, `key`), then each shot lists `atlas.show` entries with `at`/`dur`/`until`/`pulse` cues so the map builds up across shots |
| graphic | `snowfall` | Wind-driven snow in three depth layers (`density`, `wind`, `opacity`) |
| graphic | `ctaCard` `icon: "share"` | Paper-plane pill for share CTAs (EP06) |
| sfx | `blizzard`, `caravan` (beds); `warHorn`, `mountainRise` (hits) | EP06 |
| graphic | `reasonTally` | Row of icon slots across the top (`items: [{icon, label, at}]`; icons `water`, `soil`, `defence`, `trade`) that fill on cues and carry across shots; `sumAt` + `sumKicker` + `sum` closes a bracket into the lesson line (EP07) |
| graphic | `surveyPin` | Survey stake dropped on a plate point (`local`): `ask` "?" badge, `glowAt` converging rings + glow, `fadeAt`, `stake: false` for glow only |
| graphic | `duskGrade` `lights` | `[x0,y0,x1,y1]` band for the city windows |
| sfx | `tally`, `stake` (hits) | EP07: a reason checked off; a survey stake driven into turf |
| graphic | `pullBack` | The previous shot's picture (`src`) starts full-frame at its last framing (`from: {s,x,y}`) and shrinks into a framed inset at `to: [cx,cy,w]` on the new shot, holds, fades: a "zoom out to the system" cut (EP08: cup → cistern, caravan photo → its map route) |
| scene | `atlas` kinds `dunes`, `well`, `lock` | Desert crescents (`box`, `avoid`), oasis wells (water-blue, pulse), padlocks that snap shut beside a feature (EP08); key threads are thin `route`s |
| sfx | `drop`, `lock` (hits) | EP08: a drop of water into a full cup; an iron padlock snapping shut |
| graphic | `callout` | Field-guide label pinned to a plate point (`local`): ring, elbow leader, caps `label` + italic `note`; `side`, `reach`, `rise`, `start`/`end` (EP09: annotating how a costume, house or store answers the weather) |
| graphic | `reasonTally` icons `clothing`, `housing`, `food`, `festival`; `gap` | EP09 climate layers; `gap: 196` fits long labels |
| sfx | `hearth`, `procession` (beds); `strike` (hit) | EP09: fire crackle in a winter camp; hide drums, steps on snow and bells; a wrong idea struck out (`reverseCard`) |
| tool | `pipeline/srt.py epNN` | SRT from the word timings, same grouping as the burned-in captions, paired into 2-line cues |
| atlas | `gorge` `{pts, width?}`, `bridge` `{at, len?, angle?}` | A chasm with cliff hachures that draws west→east, and a single stone span across it that pulses (EP10's chokepoint) |
| atlas | `town` `palace: true`, `cut` `size` | Domed palace glyph for a capital; a larger ✕ for a crossing being shut |
| atlas | shot `zoom: {from, to, origin, at, dur}` | Cue-timed camera move on the map: EP10 holds 2.5× on the capital, then pulls back to 1× on "Pull back" |
| graphic | `lessonStack` `size`, `restSize` | Smaller type for longer lesson lines |
| sfx | `gateSlam` (hit) | EP10: a chain run down, then a deep timber-and-iron boom as a gate shuts |

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
