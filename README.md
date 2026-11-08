# Worldcraft Shorts

A config-driven production system for **Worldbuilding, from the ground up**, a series of vertical worldbuilding lessons (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels. **Season 1** (EP01–EP25) is 30-second fantasy-documentary episodes (`docs/STYLE.md`). **Season 2** (EP26 on) is "The World Engine": 60-second episodes in which one living pixel-voxel island tests a worldbuilding idea when you press ▶ RUN (`docs/STYLE_S2.md`, research in `docs/SEASON2_RESEARCH.md`).

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
| `src/s2/` | **Season 2 (World Engine):** `EpisodeS2.tsx` (selected by `"season": 2`), the 3D stage, the Isle, creatures, timeline, overlays, `CaptionsS2` |
| `pipeline/score_s2.py` | Season 2 World Engine SFX palette and the original beat-grid synth score (used only for season 2 episodes) |
| `pipeline/music_s2.py` | Season 2 **composed score**: the series theme arranged from story cues on a tempo map fitted to the narration, written as MIDI and played by FluidSynth on the MuseScore General SoundFont (`"music": {"engine": "s2-score"}`) |
| `pipeline/pixelate.py` | Re-grids generated "pixel art" onto a true pixel grid, with a small palette and a keyed background (field-card sprites) |
| `pipeline/stills.mjs`, `pipeline/tile.py` | Render chosen frames in one browser session (S2 needs `swangle` WebGL) and tile them into a review sheet |

Docs: [research and stack decision](docs/RESEARCH.md) · [costs](docs/COSTS.md) · [distribution and experiments](docs/DISTRIBUTION.md)

Instagram auto-posting for Worldcraft Shorts: see [posting/README.md](posting/README.md). TikTok: [posting/TIKTOK.md](posting/TIKTOK.md).

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
| graphic | `eraShift` | The matching plate from another century (`src`) laid over the shot's plate and dissolved on cues (`from`, `keys: [{at, to, dur}]`), softening and tinting mid-fade so it reads as time passing (`local`; EP12 festival ↔ punishment) |
| graphic | `originLedger` | Two-column NOW / THEN card: each `row` (`icon` `bell`/`fire`/`dawn`, `now`, `then`, `nowAt`, `thenAt`) writes its modern custom, then links it to its original purpose in ember; carries across shots (EP12) |
| graphic | `headCount` | Rows of small hooded figures lit one by one from `start` over `dur`; the last `missing` stay as dashed empty outlines (absence, never harm) (EP12) |
| sfx | `timeFold`, `headCount` (hits) | EP12: a reversed bell swelling out of a gust as centuries fold; a quick roll of soft wooden taps |
| graphic | `splitFrame` | Screen split along a drawn amber seam (a border), a plate in each half with its own `from`/`to` framing, `focus` dimming, and a label block per half: caps `kicker`, serif `text`, rust `stamp`, italic `heard` (EP13: the same gift on both sides of a border; one exchange as each side heard it). Use `local: true` on a `plateMotion: "still"` shot so the loop tail redraws it |
| graphic | `mirrorLedger` | Two culture columns under a dashed seam; rows (`label`, `cells`, `at`) light on cues, an arrow from each side meets in a rust spark at `clashAt`, then a two-line `sum` (EP13: rule / reason → "The conflict writes itself.") |
| graphic | `callout` `side: "up"`, `dx`, `backdrop` | Leader straight up from the point, then sideways; the label is centred above it, for notes too wide for either side. `backdrop: true` adds a soft dark glow behind the label on bright plates |
| captions | captions-off shots | A caption group no longer holds into a shot with `captions: false` |
| sfx | `giftSet`, `seam` (hits) | EP13: a glazed ceramic lid settling on its box (the gift's signature); a soft air sweep and tap as a split frame draws across |
| shot | `plateLook: {from, to?, at?, dur?}` | Grade a plate (`cold`, `warm` or any CSS filter) and wipe a second grade across it left to right on a cue, with an amber seam: the same scene re-read (EP11: a visitor's cold read → an insider's warm one) |
| graphic | `shroud` | Code-drawn linen-wrapped body on a bier (`at`, `length`, `height`, `head`, `sprigs`; `local`), for when the image model won't paint one (EP11) |
| sfx | `relook` (hit) | EP11: a swept breath blooming into a warm triad, on a perspective flip |
| tool | `pipeline/local_stills.py epNN shots --seeds …` / `--pick seed` | Free local stills (SDXL-Lightning, CPU, about 2.5 min each) from each shot's `sdxlPrompt`, when Figma credits run out |
| graphic | `verdictScale` | A drawn balance weighing two moral systems (`pans` labels, `tilts: [[cue, deg]]`, per-pan `words` replaced on cues, `glowAt` when it comes level); repeat it across shots with matching states so one scale tips one way, then the other (EP14: FREEDOM / DUTY) |
| graphic | `callout` `then: {label, note, color, at}` | Re-captions the same point on a cue: the first note is struck through and drops away, the leader turns the new colour (EP14: "Hero." → "Traitor.") |
| sfx | `scaleTip` (hit) | EP14: a wooden creak, two chain chinks and a soft knock as the verdict scale settles |
| graphic file | `src/graphics/Rites.tsx` | EP11's `shroud`, moved out of `Culture.tsx` when EP11 and EP13 (both had added a `Culture.tsx`) were merged |
| graphic | `inferChain` | An evidence chain inked onto the plate (`local`): a pen loop round the clue (`at`, `loop`), a leader to a text block (`box`, `align`), then `seen` (caps) → `means` (italic, `meansAt`) → ∴ `value` in an ember seal (`valueAt`); `backdrop`. Seal-only mode (just `value`) pins a value to a point on a wide plate (EP15: a habit read into values) |
| graphic | `bench` | Code-drawn plain timber bench (`at`, `length`, `tone: "day" \| "dusk"`, `cups`; `local`), for objects the image model won't put where the story needs them (EP15) |
| sfx | `benchSet`, `inferSeal` (hits) | EP15: a bench scraped and set down on cobbles; a pen tick and a warm rising fifth as a value is inferred |
| graphic | `titlePower` | Lesson card: one crown splits into a dashed TITLE crown and a gold POWER crown with a rust ≠ (`splitAt`), each column's kicker + italic `text` on `leftAt`/`rightAt`, then `items` chips lit on cues (EP16: formal authority vs actual power) |
| atlas | `crown` `{at, from?, ghost?, size?, lift?}`, `granary` `{at, size?}` | A crown on the map; with `from` it flies along an arc to `at` and glows on landing, `ghost` leaves a dashed outline (EP16: the crown leaves the palace for the guild); a storehouse-and-silos node that pulses |
| graphic | `keyRing`, `grainSack` | Code-drawn props SDXL won't place (`local`): an iron ring of keys swinging from a point; a tied burlap grain sack with spilled kernels (`tone`, `lean`) (EP16) |
| sfx | `grainPour`, `crownShift` (hits) | EP16: kernels hissing from a sack over a cloth thump; a gold ring lifted, carried on air and set down on a low chord (power changing hands) |
| graphic | `pillarStack` | An empire drawn as a roof on pillars (`label` on the entablature): the pillars rise as stone on `riseAt`, then `peopleAt[i]` turns each into a supporter, a portrait cut from their plate (`src`, plate point `x`/`y`, `zoom`) with its reason, or an `empty` dashed pillar for a missing alternative; `liftAt` shrinks the stack up and `lessonKicker` / `lessonText` land beneath it at `lessonAt` (EP17: BREAD / ORDER / THE WAGE / FEAR / NOTHING BETTER) |
| graphic | `pillarTag` | A `tag` with a pillar glyph and a numeral ("PILLAR I · BREAD" / *The farmer*), so each person we meet reads as one pillar of the stack (EP17) |
| sfx | `pillarSet`, `doorKnock` (hits) | EP17: grit and a dry stone thud as a pillar is set; three muffled knocks on a door down the street (fear by implication) |
| graphic | `lawText` | An invented law on a dark vellum card (EP18): `kicker` + `title`, `clauses: [{n, text, at, litAt, fear, fearKicker}]` write in left to right on `at`; on `litAt` a clause warms to ember and the fear behind it appears beneath (unlit clauses dim); rust wax seal; `liftAt` shrinks it up and `lessonKicker`/`lessonText` (optional per-line `lessonLineAt`) land beneath. Law text is always drawn in code, never generated |
| graphic | `glints` | Watchers behind shutters: warm slits with a halo lit one by one at plate `points` (`local`), `dur`, `size`, then dimmed together at `outAt` to `dimTo` (EP18: everyone noticed, nobody spoke) |
| sfx | `quill`, `clauseLight` (hits) | EP18: a clause written into the law; a clause lit by its fear (a breath of flame over a low open fifth) |
| graphic | `crackLoop` | A collapse drawn as a feedback loop (EP19): `nodes` (plate medallions: `src`, plate point `x`/`y`, `zoom`, `label`) on a ring round the empire's seal (`label`); medallions pop on `nodesAt`, arrows draw on `arrowsAt`, the closing rust arrow on `closeAt`; from `spinAt` a pulse runs round at `w0`·e^(`k`·τ) rad/s, lighting each node and adding a crack through the seal on every pass; `breakAt` splits the seal in two (`breakLabel`, default TWO HEIRS); `liftAt` shrinks it up, `kickerAt` / `lessonAt` land `lessonKicker` / `lessonText` beneath. Geometry: `center`, `radius`, `medallion`, `sealRadius`, `liftScale`, `lessonTop`, `lessonSize` |
| graphic | `crackTag` | A `tag` with a cracked-disc glyph and numeral ("CRACK I · FAMINE" / *A bad harvest*); `word` replaces "Crack" (EP19) |
| sfx | `crackTick`, `sealSplit` (hits) | EP19: a brittle glaze-crazing snap with a low knock (one per loop pass; the generator spaces them with the same `w0`/`k` as the pulse); a stone crack, a dropping boom and settling fragments as the seal breaks |
| graphic | `chronicleFrame` | The view a chronicle keeps (`local`): a gilt `frame: [x,y,w,h]` with corner brackets and a top `label` darkens everything outside it (`dim`), then `openAt` widens it past the plate edges so the plate shows what was cropped out (EP20: each nation's memorial frames out the other side's dead). `dim: 0` draws the border alone |
| graphic | `tablet` | A carved stone inscription, all text drawn in code: `kicker`, `lines` cut letter by letter from `start` over `dur`, an ember `seal` ("TRUE") stamped at `sealAt`, optional `leftOut: {text, at}` line; `align: "center"`, `size`, `width` (EP20) |
| graphic | `truthRows` | Short lesson rows landing on cues (`rows: [{text, at}]`, *word* amber), then a `sumKicker` + `sum` (*word* ember) at `sumAt` while the rows step back (EP20: Different losses / stories / values → ENEMIES / Neither is evil.) |
| graphic | `lanterns` | Small code-drawn memorial lanterns on posts at plate points, lit in turn with a warm flickering glow (`size`, `stagger`) (EP20: one at each nation's stone at dusk) |
| sfx | `chisel`, `frameOpen` (hits) | EP20: light chisel taps cutting an inscription; a breath of air widening over a low hollow fifth as a chronicle's frame opens |
| graphic | `spellPage` | A blank spell page drawn in code (parchment, ink, rust labels) at `at: {x, y, s}` (optionally gliding in `from`): rust `kicker`, a `title` written on `titleAt` (else on the first answer), and `rows: [{num, label, q, a, qAt, aAt}]` whose caps label and faded question appear on `qAt` and whose answer is inked left to right on `aAt`; cues are absolute, so a copy in a later shot already shows earlier rows. A three-point sigil lights one node per answer (`litAt` overrides) and ignites at `igniteAt` in the episode's `motif` colour; `active` marks the row being answered, `pulseAt` pulses the numerals, `dim` washes the plate, `lessonText` lands at `lessonAt` (EP21: CAN / CAN'T / COSTS) |
| graphic | `mendSeam` | A crack on the plate (`local`; `crack` polyline, `branches`, `width`) that opens at `crackAt` over `crackDur`, then light runs along it at `mendAt` and leaves a thin glowing seam; `fail: true` (`reach`, default 0.6) gutters to rust and dies, leaving the crack. Also the cost crack and a shattering, with no `mendAt` (EP21) |
| graphic | `storyQuestions` | Plot questions stacked from `top` (`items: [{num, text, at}]`, `gap`, `size`): a numeral badge naming the answer that raised each one, and an ember italic question (EP21: three answers → three story questions) |
| graphic | `ctaCard` `icon: "save"` | Bookmark pill for save CTAs (`button: "Save this"`) (EP21) |
| sfx | `mendKnit`, `mendFizzle`, `costCrack` (hits) | EP21: the mending magic's signature (fine crackle under a glassy cluster gliding up a fourth, settling on an open fifth; also the sigil igniting); a failed mend sagging and sputtering out; a brittle crack racing across glass or stone (the price) |
| graphic | `mendGlow` | Free healing drawn in code at a plate point (`at`, `r`, pin with `"local": true`): a breathing jade glow with rising sparks; each cue in `pulses` brightens it and sends a ring to `ringMax`; `core: false` draws only a ring sweeping across the frame from an off-frame origin; `failAt` makes it gutter twice and go out (EP22: the touch, healed soldiers, the menders' door, the one it couldn't save) |
| graphic | `rippleMap` | Rings of consequence spreading from `origin`: each of `rings: [{r, at, kicker, label, angle, side, lost}]` runs out as a wavefront on its cue and lights a pin with its label; a `lost` ring is dashed with a rust "?"; `idle` sends faint rings out; `liftAt` / `lift` shrink the map and `lessonKicker` / `lessonText` land beneath at `lessonAt` (EP22: MEDICINE / WAR / POWER / UNEXPLAINED) |
| graphic | `ringTag` | A `tag` with a concentric-ring glyph and numeral ("RING II · WAR" / *Nobody goes home*), the numbered ring lit; `lost: true` turns it rust and dashed (EP22) |
| sfx | `mend`, `ripple` (hits) | EP22: a soft breath blooming into glassy A-major partials (the healing touch, reused for every glow); a low round swell sinking in pitch as a consequence ring spreads |
| graphic | `memoryLedger` | A caster's ledger on a dark gilt card (EP23): `kicker`, `title`, `lines: [{num, text, at, strikeAt}]` written left to right on `at` and struck in rust on `strikeAt` (the words fade to a ghost and a mote of light drifts off); a header ring has one point per line, dimming as lines are struck; `active` marks the current line, `hoverAt` makes it breathe (the choice); `at`/`liftAt`/`lift` place and glide it (cues are absolute, so corner copies show earlier strikes); `prices: [{text, at}]` land as pills at `pricesTop`; `lessonKicker`/`lessonText` at `lessonAt`/`lessonTop` |
| graphic | `fadingName` | A name painted on a plate (`local`; `at`, `size`, `rotate`, `color`) that fades letter by letter from `fadeAt` over `fadeDur`, leaving a faint ghost (EP23: a mother's name on a door) |
| sfx | `recall`, `forget` (hits) | EP23: the memory spell's signature (a breath, then a soft rising music-box arpeggio, reused for every spell); a memory struck from the ledger (a quill stroke, one music-box note sagging as it fades, an airy whisper rising away) |
| graphic | `gazeBeam` | A caster's sight drawn in code on a plate (pin with `"local": true`): a soft beam along `points` (her eye first, then any mirror bounces, then the end), widening by `widths`; it draws out from `start`, `sway` swings the end like a searchlight, `flares` brighten it, motes drift along it (EP25: the Unmaker's sight on the courtyard, the gate, over the heroes, bent by a mirror) |
| graphic | `unmake` | Something erased by magic, never someone: the `poly` outline lights, then dissolves cell by cell from `from` into a dark void, shedding motes (EP25: the courtyard gate) |
| graphic | `sightPlan` | A tactical weakness as a top-down puzzle: a courtyard plan (`yard`, `eye`) where her sight cone sweeps and is ray-cast every frame against `blocks` (stone rects and circles, `smoke`, `fog`, `wall`, each growing in on a cue and optionally burning off with `until`), so cover casts true blind spots; `route` + `moves` walk three hero tokens through the shadows (`catch: true` turns a lit token rust); `labels`, `liftAt` / `lift`, `arcRow` and `lessonText` as in `rippleMap` (EP25) |
| sfx | `gaze`, `unmake` (hits) | EP25: a cold glassy open-fifth hum with a high whistle (her sight touching something, reused every time it lights); an inward rush, a falling tone and a spray of fine crackles with no impact (something unmade) |
| graphic | `gateRing` | A teleport gate's surface drawn in code inside a stone ring on the plate (`at`, `rx`, `ry`, pin with `"local": true`): a faint lilac shimmer when idle, a turning swirl with a bright rim on `openAt` (or `open: true`), a white flash and ring for each cue in `jumps`, three stutters and a collapse to rust sparks on `failAt`; `stone: true` draws the ring itself for plates without one, and `occlude: [[x, y, rx, ry]]` keeps a figure in front of the light (EP24) |
| graphic | `crystalPrice` | A floating crystal with a price chip (`kicker`, `price`, `side: left/right/below`); on `burnAt` it flares and crumbles into lilac dust and the chip turns rust (`burnedKicker`) (EP24: ONE JUMP / 40 crowns → BURNED) |
| graphic | `countingBoard` | A merchant's counting board, GATE vs CART, in walnut and brass: each of `rows: [{label, gate, cart, win, at}]` appears on its cue and its bead slides to the winning side, the winner's note brightening; `box`, `enter: false` to carry it across shots, `all` for a recap, `score` for the tally footer, `moveAt` / `move` and `lessonText` for the lesson (EP24: COST, RANGE, RELIABILITY, AVAILABILITY to the cart; SPEED to the gate) |
| sfx | `blink`, `gateFail`, `crystalBurn`, `bead` (hits) | EP24: a glassy E-major swell out of an inward rush, then a hollow pop (the gate opening or a jump, reused every time); the same cluster stuttering and collapsing on a thud; a glassy flare crackling into dust; a wooden bead brushed along a rod and clacking home |

### Season 2 building blocks (EP26–EP29, "The World Engine")

Selected by `"season": 2` in `episode.json`; the timeline lives in `episode.world` (generated by `episodes/epNN/make_epNN.py`). Full rules are in `docs/STYLE_S2.md`.

| Kind | Name | What it does |
|---|---|---|
| world | `Stage` (`src/s2/world/Stage.tsx`) | `@remotion/three` canvas rendered at ⅓ size and upscaled ×3 nearest-neighbour (the pixel diorama look); camera rig from az / el / dist / target / fov; warm key light whose direction follows the mood, with hard shadows over the whole island (±38-unit shadow box); backdrop slot (pixel starfield) |
| world | the Isle (`island.ts`, `IslandMesh.tsx`) | Seeded 46×46 voxel island (peak, forest, lake, meadows) with soil / clay / rock strata on the cut sides. Per-frame layers: `graze` (meadow to dirt), `forest` (trees thin), `snow`, territory `rings` (outside dimmed), world `ripple` |
| world | `Grimmaw`, `Herd` (`Creatures.tsx`) | Voxel predator (walk, sleep, lie / starve, dissolve, appear, spawn / despawn; inverted-hull outline) and an instanced mossback herd (up to 380) wandering in simulation time, born small and growing |
| world | timeline (`timeline.ts`, `keys.ts`) | `clock`, `speed` (integrated into sim time, negative = rewind), `camera` keys with eased moves, cuts and drift, `light` moods (day / dusk / gloom / winter / night / golden, each with a sun elevation and azimuth), `herd.count`, `pred`, `predators[].keys`, `layers`, `ambient`, `flyers`, `simLoop` (a hidden sim-time reset so the herd is back on its frame-0 spots at the loop) — all keyed to spoken words, or to the episode's end with `{"end": true, "offset": -0.5}` |
| world | `ambient` (default on) | Voxel birds circling in two flocks, pollen motes over the meadows (warm in golden light), glints on the water |
| world | `flyers` | A shadow-only creature crossing the Isle (invisible to the camera, it casts its shadow): the next episode's tease (EP26: a dragon) |
| world | `alert` state | The predator lifts its head to the sky (mouth shut) and settles back before its next key |
| overlay | `sting` | Series sting (≤1.5 s) over the hook: WORLD ENGINE typing in, `RUN NN · ARC` |
| overlay | `simBar` | ▶ RUN button (press and RUNNING states on `runAt` cues), clock, prey / predator counters read from the world |
| overlay | `simGraph` | Pixel population chart drawn up to "now" between `from` and `to` (`series` with colour / max / label) |
| overlay | `fieldCard` | `intro` (sprite ×3, name, kind, danger line), `checklist` (numbered rows that tick on cues, a locked row that blinks and unlocks, `collapse` keys to fold), `full` (the takeaway with a serif subtitle) |
| overlay | `kinetic` | Big titles that pop in per part on cues (pixel / caption / serif fonts); `preShow` for frame 0 and the loop |
| overlay | `stamp` | A slammed verdict (EXTINCT, STABLE) |
| overlay | `pin` | A label pinned to a world point or a predator, projected through the stage camera every frame |
| overlay | `zzz`, `deleteFx`, `rewind`, `blockWipe` | Sleeping Zs; selection brackets and a DEL key; scanline rewind; diagonal pixel-block transition |
| overlay | `endCardS2` | Full logo, `PART NN / 50`, serif title, a pixel panel with the ask (`SEND THIS`, `SHARE THIS`…), footer |
| overlay | `seasonBar`, `followButton`, `nextRun`, `followChip` | The ending formula: PART NN / 50 with a 50-segment bar filling to NN; a pixel "+ FOLLOW / FOR PART NN+1" button a pointer taps on its cue (flash, sparks, ✓ FOLLOWING); NEXT RUN · NN+1 with a locked silhouette and ??? decoding to the title; a light top-right follow chip for mid-video |
| captions | `CaptionsS2` | 1–3-word bursts popping per word; `captionsOff: [{line, from, to?}]` where a title says the words |
| sfx | `sting`, `runPress`, `simTicks`, `births`, `losses`, `stamp`, `rewind`, `ringOn`, `snowAir`, `sleepZ`, `cubPop`, `delete`, `restore`, `cardSlide`, `check`, `unlock`, `worldRipple`, `stomp`, `crash`, `boomPop` | The World Engine palette (`pipeline/score_s2.py`), one sound per event, reused every episode |
| sfx | `chime`, `engineWind`, `followPress`, `dragonPass` | **The World Engine chime**, Season 2's sound logo (D5 A5 D6 A6 on music box with 8-bit blips, ringing D7; rendered once from the score's SoundFont by `music_s2.render_chime()`, never ducked) at frame 0, the lesson card and the follow press; its clockwork wind-up; the follow button; a huge wingbeat pass panning with the dragon's shadow |
| lab | `S2Lab` composition (`src/s2/Lab.tsx`) | The bare Isle on a slow orbit, for testing the diorama look and render speed without an episode (`npx remotion still S2Lab out/lab.jpg --gl=swangle`) |
| music | `music.engine: "s2-score"` (default from EP26 v2) | Composed score on sampled instruments: sections on cues (`style`: hook, pulse, drive, drop, void, mystery, build 1–4, twist, rest, frenzy, crash, swell, anthem, outro, tease), the series theme, `accents` (hit, boom, stab, cymbal, riser, call, roll), `rests`, `fadeOut` (`{"fromEnd": 0.08}` plays to the loop point) |
| music | `music.engine: "s2"` | The first synth engine: beat-grid layers (pad, arp, bass, kick, hats, clap, bells), drones, ducks, `fadeOut` |
| sfx | `roar`, `stompHit` | A creature's display call (a rough growl through moving formants) and the thud of its stomp |
| world | `roar` state, `dust` layer | Head up, jaw open, body rocks back; a ring of voxel dust puffs at a point that expands and fades |
| mix | `mix.voiceFx` | Narration polish for phone speakers (high-pass, presence, air, gentle compression), opt-in per episode |
| world (EP27) | `dragons` (`Dragon.tsx`) | A flying voxel dragon matching the field-card sprite (rust hide, bone-fingered wings, outline). Keys `{at, x, z, y?, state, face?, dur?, ease?}`: `perch` (wings raised, half-spread, breathing), `roar`, `fly` (flapping), `glide`, `hidden`; `y` is altitude (none = on the ground); heading follows its motion, it banks into turns, and air/ground blend over 0.5 s. `make_ep27.py`'s `orbit()` writes dense circling keys |
| world (EP27) | `settlement` (`Settlement.tsx`) | The village layer: buildings (`house`, `hall`, `barn`) with a `roof` switch (thatch → slate / turf, one by one), `char` (roofs blacken and break) and `smoke`; `pens` (open fences) and `cover` (covered barns rising over them); `place` (each building unbuilds at site A and rises at site B, staggered; the herd follows via `herd.centersB`); `roads` A / B painted on the voxels with `route`; carts on the road (`tradeKey` series = the count) with `lanterns` for night travel; a `tower` with a bell that swings on its `rings` cues. Trees on building sites and roads are cleared |
| world (EP27) | `herd.skin: "sheep"`, `series`, `props` (cairn), `gaze` state | Livestock re-skin of the herd (white sheep, dark heads); extra keyed HUD numbers (`series.trade`); a cairn whose stones stack on their keys; the predator's `alert` pose held from its first frame (for frame 0 and the loop frame) |
| overlay (EP27) | `simBar.counters` + `compact`, `simGraph` series keys, `fieldCard.spriteW/H` + `dietLabel`, `pin.dragon`, `endCardS2.icon`, `nextRun.sprite` | Any three HUD counters (`herd`, `pred`, `roofs` = standing unburnt roofs read from the village, or a `series` key) in a compact bar with the clock; graphs of the same keys; a field-card sprite of any size; a pin that follows the dragon; the comment CTA's `bubble` icon; the next run's silhouette (EP27: `cairn`). New pixel sprites: `sheep`, `house`, `cart`, `bubble`, `cairn` |
| sfx (EP27) | `towerBell`, `burn` | A low cast bell (church-bell partials on G3; deliberately unlike the chime); a flame-and-crackle bed for roofs catching (own seeded RNG) |
| overlay (EP27) | `dragonEye` | **The dragon's-eye view.** `mode: "dragon"`: a red-vignetted, scanlined frame with a DRAGON'S-EYE VIEW chip; brackets lock (staggered from `lockAt`) onto every target the dragon can see, read from the world (`dragonTargets` in `Settlement.tsx`: thatch roofs still standing, flocks in open pens, the open village, carts on the open road by day), with a TARGETS readout. `mode: "light"`: brackets and readout only; a target that disappears flashes green, HIDDEN. `mode: "tower"`: the village looking back (sky-blue tint, one bracket on the dragon, DRAGON · SPOTTED). `minY` keeps brackets clear of cards |
| world (EP27) | camera `follow` | A camera key that rides with a dragon: `{dragon, look: [x, y, z], back, up}` sits `back` units behind it on the line from `look` and `up` above it, aimed at `look` (over the shoulder at the village); `az` offsets it sideways. Without `look`, it looks `ahead` along the heading |
| music (EP27) | `soar`, `raid`, `stealth` | Episode colours around the series theme: horns in open fifths with a taiko wingbeat (a dragon in the air); war drums with low horn stabs (a raid); a tiptoe pizzicato figure with `layer` 1–4 (hiding) |
| sfx (EP27) | `eyeOn`, `lockOn` | The view switching to the dragon's eye (a swell and a falling square sweep); a bed of 8-bit lock-on double beeps |
| world (EP28) | `folk` / `Fenn` (`Folk.tsx`) | A people walking the Isle: a crowd (`count`) around homes that move with `site` (`centers` → `centersB`), standing on decks over water, plus a keyed `hero` (`stack` lifts a stone overhead). One voxel body morphs trait by trait: `eyes` (big night eyes), `wet` (teal skin, fin frills instead of pointy ears, a reed sash; at 0 it's a human with pointy ears), `glow` (pulsing light spots) |
| world (EP28) | `settlements`, building `show` / `stiltsB` / `greathall`, `sink`, `stone`, `open`, `glow`, `clearTrees` | More than one village on the Isle; a building's own rise keys (houses giving way to one great hall); a hall on stilts at its site B (on the lake); houses sinking into turf mounds with glowing doors; walls turning to taller stone; walls opening into pillars; light patterns travelling along the walls; trees cleared along a shot's line of sight |
| overlay (EP28) | `editor`, `readout`, `fieldCard.sliders` | **The species editor**: a character-creator panel of trait sliders from HUMAN to the species' own value (the lazy version moves one, EARS); slider rows on the field-card checklist (each knob slides on its tick); a big readout with a 20-segment bar for any series (HUMAN-LIKE %, rust high and teal low). Sprites `fenn`, `hourglass` |
| music (EP28) | `folk`, `glow` (with section `programs`) | A people at home (kalimba ostinato, the theme on ocarina, hand drums, `layer` 1–4) and speaking in light (choir pad, vibraphone ripples, celesta theme); sections set GM programs and later ones set them back |
| sfx (EP28) | `morph`, `slide` | A body re-forming (rising square shimmer over air); an editor slider ticking |
| world (EP29) | `people` (`People.tsx`: `Person`, `Queen`, `Dais`) | Mortal people on the clock: each person in the crowd is born, grows up, greys and fades out over their own lifespan (`life`, in clock years), and the next generation takes the slot in new colours, so a time-lapse visibly turns the valley over. Plus an heir `queue` (waiting heirs who age in line), a `consort` who ages beside the ruler and is replaced, a `royal` share of the crowd (violet tunics and circlets), and a keyed `ruler` (the Undying Queen: `idle`, `alert` looks up) on her `dais` |
| world (EP29) | building kind `library`, props kind `offerings` | A tall stone library with lit windows and a stepped slate roof; a ring of candles that light one by one on `lights` keys (the EP30 tease) |
| overlay (EP29) | `lineage` | **The lineage strip**: a generations timeline under the world. The ruler's cell never changes (AGE 30, FOREVER) while one cell per generation is born, greys and is gone as the clock runs, scrolling left. A badge row shows the current rule on every generation (`badges`: `waited`, `land`, `council`, `titles`, `cap`, `memory`, `record`). Sprites `queen`, `mortal`, `elder`, `crown`, `seat`, `lamp`, `book`, `shrine` |
| music (EP29) | `clockwork`, `reign` | Centuries racing (harpsichord 16ths, woodblock tick-tock, pizzicato bass, the theme on celesta, tubular bells; `layer` 1–4) and the one who never changes (church organ chorale, cello pedal, timpani processional, the theme on horns) |
| sfx (EP29) | `crownPass`, `clockTicks` | A generation passes / the crown changes hands (glass shimmer up a fifth over a wooden knock); a pendulum clock tick-tock that speeds up through its bed |

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
