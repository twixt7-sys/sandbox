# EP06 production brief: Mountains Can Change the Fate of Kingdoms

**Series:** Worldcraft Shorts, Episode 06 / 50. Opens **Arc 2: Geography and Nature**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "A mountain range can decide which kingdom becomes an empire." Topic: geography and political power. CTA: "Send this to someone drawing a fantasy map."
**Deliverable:** 30.7 s vertical Short (1080×1920, 30 fps), YouTube Shorts / TikTok / Facebook Reels (+ Instagram Reels captions), AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** a mountain range creates power before anyone fights. It decides who can move, who stays apart, and who gets paid.
- **One example:** the kingdom of **Veyra**, south of the **Ashspine** (only two names). North of the range, three cut-off vales. The range:
  1. **blocks invasion**: northern armies stall in the snow, so Veyra spends on farms instead of walls;
  2. **isolates cultures**: spurs split the north into vales that grow apart and never unite;
  3. **funnels trade**: the few roads through the range all end at Veyra's waystations.
  
  So Veyra becomes an empire "long before an army marched".
- **One shareable thought:** "Mountains decide who moves, who stays apart, and who gets paid." It's built for the "send to someone drawing a map" CTA.
- **Scope guard:** these are range-scale effects. EP10 (one chokepoint that matters more than a capital) and EP07 (why cities sit where they do) are kept for later. EP06 shows three gaps rather than one decisive pass, and places no city for a reason beyond "south of the wall".

### How EP06 varies the series rhythm (production rule: don't repeat EP05's shape)

| | EP05 | EP06 |
|---|---|---|
| Hook | Title lockup over ruins | No title. An amber line traces the range's skyline as it's named, then "empire?" lands in the sky |
| Spine | Plate → plate → plate → lesson stack → don't/do card | **Map → plates → map.** The animated map is the episode's spine: drawn once (Veyra), left for three plates, then returns *complete*, with the three effects stacking up in about a second |
| Lesson | Separate dark card | The lesson *is the map's key* ("Mountains decide: Who moves. Who stays apart. Who gets paid."), lit row by row as it's spoken |
| CTA | Comment | Share (paper-plane pill), "Pass it on" |

## 1. Research note (re-verified only what could have changed since 2026-10-19)

- Platform limits, hashtag guidance and AI-disclosure rules were researched on 2026-10-19 (`docs/DISTRIBUTION.md`, `docs/RESEARCH.md`). Four days later nothing material is likely to have changed, so I didn't re-research them. EP06 metadata follows the same limits: YouTube title 57/100, TikTok caption 255 chars, Instagram 5 hashtags.
- **Exchange rate changed:** the Bangko Sentral ng Pilipinas reference rate was **₱63.35 = $1 on 22 Oct 2026** (mid-market quotes ≈ 63.43–63.48). That's up from the ₱61.8 used in `docs/COSTS.md` (Aug 2026). EP06 costs below use ₱63.35.
- **Credentials:** no Runway, ElevenLabs or Creatomate keys are set. AWS credentials exist in the environment, but no AWS service was used (CLAUDE.md: no spending without approval).
- **Figma:** `generate_image` (`gemini-3.1-flash-lite-image`) works on the user's Starter plan. The user approved up to 6 generations for EP06, and 4 were used.
- **Geography sanity check:** the mechanism matches the real pattern writers cite (mountain barriers slowing armies, valley isolation producing distinct languages and customs, trade concentrating on a few passes). It's expressed through an original fictional example only, with no real-world claims on screen.

## 2. Stack and why

| Layer | Tool | Why |
|---|---|---|
| Stills (4) | Figma `generate_image`, lanczos-upscaled to 1080×1920 | Only approved image source. 4 generations, all kept on the first try |
| Map (2 shots) | **New `atlas` scene** (`src/scenes/Atlas.tsx`), pure SVG/React | The mechanism has to be legible, and a generated image can't animate cause and effect. Vector, $0, reusable |
| Motion graphics | Existing `ghostLines`, `oversizedWord`, `tag`, `evidenceRing`, `emberDusk`, `ctaCard`, plus new `snowfall` | Series look. Only genuinely new visuals got new components |
| Voice | Kokoro-82M `af_heart`, speed 1.0 | Series voice, free, no licensing risk. "Veyra" → /vˈAɹə/ (VAY-ruh), "Ashspine" → /ˈæʃspIn/, checked via the G2P |
| Music + SFX | `pipeline/score.py` (synthesized) | G minor → G major. New SFX: `blizzard`, `caravan` beds; `warHorn`, `mountainRise` hits |
| Render | Remotion 4, `--gl=angle`, cloud container | ≈3 min for the full render |
| QA | `pipeline/qa.py` + contact sheet + extra beat frames | Series rule |

## 3. Narration (76 words, measured 30.72 s with real TTS)

> A mountain range can decide which kingdom becomes an empire. / Take Veyra, sheltered behind the Ashspine. / Invaders stall in the snow, so Veyra builds farms, not walls. / North of the peaks, cut-off valleys grow apart and never unite. / And every caravan must cross the few roads Veyra guards. / It became an empire long before an army marched. / Mountains decide who moves, who stays apart, and who gets paid. / Send this to someone drawing a fantasy map.

The first draft was measured at 30.37 s. A 0.3 s pause after the hook was then added so "empire?" holds before the dissolve, giving 30.72 s (QA window 27–33 s).

## 4. Timed storyboard

Seven shots. The full per-shot table (start/end, exact narration, image prompt, camera, foreground/midground/background, lighting, on-screen text, motion graphics, SFX/music, transition, purpose) is in [`STORYBOARD.md`](STORYBOARD.md). In brief:

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.40 | "A mountain range can decide which kingdom becomes an empire." | Golden kingdom under the Ashspine; amber skyline trace; "empire?" | Claim plus proof image; plate reads as a map |
| 2 | `veyra` | 4.40–7.08 | "Take Veyra, sheltered behind the Ashspine." | Map draws: range with 3 gaps, 2 spurs, 3 northern vales, Veyra, river, farms | Name the example and place it |
| 3 | `snow` | 7.08–11.15 | "Invaders stall in the snow, so Veyra builds farms, not walls." | Army stalled in a blizzard; drawn snow; PROTECTION, "No walls needed." | Effect 1: blocks invasion |
| 4 | `valleys` | 11.15–15.28 | "North of the peaks, cut-off valleys grow apart and never unite." | Knife-edge ridge between terraced white-dome vale and black-timber vale; amber crest line, rust ✕ | Effect 2: isolates cultures |
| 5 | `caravan` | 15.28–19.11 | "And every caravan must cross the few roads Veyra guards." | Caravan on switchbacks to a toll waystation; dashed road line, ring on gate | Effect 3: funnels trade |
| 6 | `empire` | 19.11–26.68 | "It became an empire long before an army marched. Mountains decide who moves, who stays apart, and who gets paid." | Map returns: arrows halt, vales tint and their links are cut, roads flow to Veyra with tolls, amber reach spreads, "The Empire of Veyra"; key lights row by row | Payoff and lesson |
| 7 | `cta` | 26.68–30.72 | "Send this to someone drawing a fantasy map." | Opening view at ember dusk, trace still glowing; CTA card, "Share this" | Share CTA; loops to frame 1 |

Motif colours (STYLE.md allows one per episode): snow/ice white `#e6eef0` on the range glyphs. The three vale tints (`#7fb2cf`, `#9cc68a`, `#c79ac0`, at 20 % opacity) are map-only, there so the separate cultures read as separate. Everything else stays on the series palette.

## 5. Generated assets

- `plates/hook.jpg`, `snow.jpg`, `valleys.jpg`, `caravan.jpg`: Figma file "Worldcraft Shorts EP06 plates" (in the user's drafts), 768×1376 → 1080×1920.
- `ep06.srt` (17 cues); cover `Worldcraft_Short_E06_cover.jpg` (hook frame at 3.6 s).
- `public/ep06/` (gitignored, rebuilt by `pipeline/build.sh ep06`): narration, music, sfx, mix, timing.

## 6. Final video and verification

- `out/ep06.mp4` (master, 40.2 MB), `out/ep06_compat.mp4` (H.264 Main CRF 20 +faststart, 24.2 MB): sent to the user with SendUserFile.
- `ep06_download.mp4` (two-pass 3300k, 13.4 MB) on the preview page's Download button; `ep06_player.mp4` (CRF 26, 7.7 MB) in its player.
- `qa.py` **passed** on the master, compat, download and player copies: 1080×1920, 30 fps, 30.72 s, H.264 yuv420p, audio present, decodes cleanly, no black gaps, no frozen video, −14.1 LUFS, true peak −1.4 dB (player copy −1.2 dB), no dropouts.
- I viewed the contact sheet and beat frames at the hook word, the dissolve, every map beat and the CTA. Fixes made from that inspection: black edges on two reframed plates, a cluttered spur glyph, the map key colliding with captions, a coin over the range label, and "empire?" not holding long enough before the dissolve.
- **Not verifiable by me:** how the narration *sounds* (pronunciation, pacing, warmth) and the mix balance by ear. I checked phonemes and loudness numerically but couldn't listen. Please give it one listen before posting.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `atlas` scene (`src/scenes/Atlas.tsx`), with the map defined once in `episode.json → atlas.features` and built up per shot via `shot.atlas.show` (cues, `until`, `pulse`) | EP07 city placement (towns, rivers, resources), EP08 water control, EP10 chokepoints, any war or trade map. Feature kinds: `range`, `river`, `region`, `fields`, `town`, `route` (with flowing caravans), `arrow` (with `stop` halt), `cut`, `pattern`, `gate`, `coin`, `wash`, `label`, `key` (legend lit on cues) |
| `snowfall` graphic (`src/graphics/Terrain.tsx`) | Any winter or high-altitude plate (EP09 climate) |
| `ctaCard` `icon: "share"` | Every "send this / share this" CTA (EP09, EP13, EP17, …) |
| SFX `blizzard`, `caravan` (beds), `warHorn`, `mountainRise` (hits) | Arc 2 and Arc 8 (war) |

## 8. Cost (₱63.35 = $1, BSP 22 Oct 2026)

| Item | Cash |
|---|---|
| 4 stills, Figma AI credits (4 of the approved 6 generations) | $0 / ₱0 cash; credits come from the Starter plan's monthly allowance |
| Map, graphics, narration, score, SFX, render, QA, encodes | $0 / ₱0 |
| **Total** | **$0 (₱0)** + 4 Figma generations |

On the paid primary stack (Runway stills + ElevenLabs), EP06 (4 stills, no clips needed) would cost about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata` (also pasted in `docs/DISTRIBUTION.md → Episode 06`). The AI label is ON for every platform. The pinned comments ask viewers about a mountain or barrier on their own map.

## 10. Experiments and metrics

| # | Variable | A (EP06 as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Map vs plate in the first 2 s | Cinematic plate with an amber skyline trace | Cold-open on the *finished* empire map, then rewind to "Take Veyra" | YouTube viewed-vs-swiped-away; TikTok 2-s retention |
| 2 | Share CTA wording | "Send this to someone drawing a fantasy map." | "Tag the friend whose map has no mountains." | Shares per 1,000 views; TikTok sends |
| 3 | Lesson as map key vs card | Key lit row by row on the map | Full-screen 3-line card (EP05 style) | Average % viewed at 22–26 s; rewatch rate |

Also track: comments answering the pinned prompt (barriers named), saves, and follows from the Short. Compare against EP04/EP05 baselines once each has 48 h of data.

## 11. How to produce EP07 ("Why Are Your Cities Built There?")

1. New session, branch `claude/worldcraft-ep07` off this branch. Read `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`, this brief.
2. **Ask before spending Figma credits** (about 4 stills). Ask about a public release only if wanted (default: no).
3. Story: hook "Nobody builds a great city in the middle of nowhere without a reason." One invented city whose site has three reasons: water, a ford or harbour on a trade route, defensible high ground. Reuse the **`atlas` scene**: copy `episodes/ep06/episode.json → atlas` as a template, swap in a coastline or river `region`, add `town` sites that appear only where the conditions overlap, and use `key` for "Water. Trade. Defence." Don't reuse the Ashspine payoff (EP06) or a single decisive chokepoint (EP10).
4. Vary the rhythm again (e.g. open on an *empty* map, then let the city "find" its spot).
5. Narration about 70–78 words. Measure with `cd pipeline && python tts.py ep07` before locking the cues.
6. Run `pipeline/build.sh ep07`, render stills, then render, `qa.py`, inspect the sheet and beat frames, then encodes (compat, download, player), `srt.py`, `storyboard.py`, cover, preview page with a Download MP4 button, SendUserFile, and commit and push to the episode branch.
