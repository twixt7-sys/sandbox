# Cost per episode

Prices are published list prices checked on 2026-10-19 (see [RESEARCH.md](RESEARCH.md)). PHP uses **₱61.8 = $1**, the most recent rate I could find (ECB/Bank of Portugal cross rate, 19 Aug 2026). That rate is an assumption, so check today's rate before budgeting. "Estimate" means I applied published unit prices to this episode's measured usage. It is not a quote.

Episode 01 usage: 30.4 s, ~430 narration characters, 4 plate shots (the map is vector graphics), 2 hero clips (hook ≈ 7 s, lanterns ≈ 6 s).

## Primary architecture (Runway + ElevenLabs + Remotion on GitHub Actions)

| Item | Unit price (published) | Estimate per episode | With one retry per asset |
|---|---|---|---|
| Image drafts (`gen4_image_turbo`, 4) | $0.02 each | $0.08 | $0.08 |
| Final stills (`gen4_image` 1080p, 4) | $0.08 each | $0.32 | $0.64 |
| Hero clips (`gen4_turbo`, 13 s) | $0.05/s | $0.65 | $1.30 |
| Narration (ElevenLabs Multilingual v2, 3 takes) | $0.08 / 1K chars | $0.10 | $0.10 |
| Music + SFX | synthesized in code | $0.00 | $0.00 |
| Render (GitHub Actions, public repo) | free standard runners | $0.00 | $0.00 |
| Storage (≈15 MB; R2 free tier 10 GB) | $0.015/GB-mo past free tier | $0.00 | $0.00 |
| **Total** | | **≈ $1.15 (₱71)** | **≈ $2.12 (₱131)** |

Fixed monthly costs:

| Item | Monthly cost | Notes |
|---|---|---|
| ElevenLabs Starter | $6 (₱371) | Lowest tier with commercial rights. Alternatively, Runway resells `eleven_multilingual_v2` at $0.01 per 50 chars (≈$0.09/take) on the same Runway bill. Confirm the commercial terms in Runway's ToS before relying on that. |
| Runway API | prepaid credits | I could not verify a minimum top-up from the docs. Check the developer portal. |
| Remotion | $0 | Free for individuals and companies of 3 or fewer people. |
| GitHub | $0 | Public repo. A private repo uses the free-minute quota (estimate: 6–10 min per render). |
| Claude Pro | already paid | Writing, code and orchestration only. No third-party credits included. |

**50 episodes:** an estimated $58–106 in usage, plus $6/month for ElevenLabs.

## What Episode 01 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 background stills | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, upscaled to 1080×1920. 4 generations, no retries. | $0 (Figma AI credits on your Starter plan; Figma doesn't show per-call credit use through this connector, so check Settings → AI credits) |
| Narration | Kokoro-82M on CPU | $0 |
| Score + SFX | synthesized in code | $0 |
| Render + QA | Claude cloud container and GitHub Actions (public repo) | $0 |

## What Episode 02 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 background stills (hook landscape, cavern city, night market, sun ritual) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled to 1080×1920. 4 generations, no re-rolls (7 were approved). | $0 cash: Figma AI credits on your Starter plan. The connector doesn't report credits per call, so check Settings → AI credits. |
| 3 "extra" shots (clock, lesson diagram, method card) | Remotion code: night grade over the hook plate, plus a star/astrolabe scene | $0 |
| Sun vanish/return, gates opening, ring glow | Remotion code over the stills (no image-to-video available) | $0 |
| Narration | Kokoro-82M on CPU, 74 words, 29.9 s | $0 |
| Score + SFX (new: shimmer, tonal drop, clock, cave, market, stone doors, temple bell, sunrise) | synthesized in `pipeline/score.py` | $0 |
| Render + QA | Claude cloud container (and GitHub Actions on push, public repo) | $0 |
| **Total** | | **$0 cash (≈ ₱0)** plus 4 Figma AI credits' worth of image generation |

If you move EP03 to the paid primary stack, the estimate is the same as the table above: about **$1.15 (₱71)** per episode, or about **$2.12 (₱131)** with one retry per asset, plus $6 (₱371) a month for ElevenLabs Starter. The exchange rate is ₱61.8 = $1 (Aug 2026), so check today's rate.

## What Episode 03 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 stills (reservoir, farms, machine district, council) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled. 4 generations, no re-rolls (7 approved). | $0 cash (Figma AI credits; check Settings → AI credits) |
| Gauge, brown-out, allocation map, lesson stack, dusk grade | Remotion code | $0 |
| Narration | Kokoro-82M, 78 words, 29.1 s | $0 |
| Score + SFX (new: machine hum, room tone, power-down) | `pipeline/score.py` | $0 |
| Render + QA | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)** plus 4 Figma image generations |

The paid primary stack (Runway stills and clips + ElevenLabs) would still cost about **$1.15 (₱71)** per episode, or **$2.12 (₱131)** with one retry per asset, plus $6 (₱371) a month for ElevenLabs Starter, at ₱61.8 = $1 (Aug 2026 rate).

## What Episode 04 actually used

| Item | Used | Cash cost |
|---|---|---|
| 5 stills (Bellweather wide, doorstep bowl, child at the doorstep, broth stall, rainy street) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled to 1080×1920. 5 generations, no re-rolls (8 approved). | $0 cash (Figma AI credits; check Settings → AI credits) |
| 4 extra shots (cut-in on the bowl, greeting reframe, lesson chain, CTA) | Reframes of the same plates plus Remotion code: rain, steam, bowl-flip diagram, detail chain | $0 |
| Narration | Kokoro-82M, 76 words, 29.8 s | $0 |
| Score + SFX (new: rain bed, wet-stone footsteps, wooden bowl knock, ladle pour) | `pipeline/score.py` | $0 |
| Render + QA | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)** plus 5 Figma image generations |

On the paid primary stack (Runway stills and clips + ElevenLabs), EP04 would cost about **$1.25 (₱77)**, or **$2.30 (₱142)** with one retry per asset, because it has one more still than EP01. ElevenLabs Starter adds $6 (₱371) a month. Rate: ₱61.8 = $1 (Aug 2026).

## What Episode 05 actually used

| Item | Used | Cash cost |
|---|---|---|
| 5 stills (city and gateway, tower, machine chamber, symbol passage, broken aqueduct) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled. 5 generations, no re-rolls (8 approved). The reconstruction and CTA shots reuse the city plate. | $0 cash (Figma AI credits; check Settings → AI credits) |
| Title, survey rings, dust in the sunbeam, aqueduct clue line, amber reconstruction lines, "Don't → Build backward" card, ember dusk | Remotion code (`src/graphics/Ruins.tsx`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 73 words, 29.9 s | $0 |
| Score + SFX (new: stone shift, mechanism resonance, rebuild) | `pipeline/score.py` | $0 |
| Subtitles | `pipeline/srt.py` from the word timings | $0 |
| Render, QA, delivery encode | Claude cloud container (render ≈ 4 min) | $0 |
| **Total** | | **$0 cash (₱0)** plus 5 Figma image generations |

No Runway, ElevenLabs or Creatomate key was configured, and no AWS service was used. The paid primary stack would still cost about **$1.15 (₱71)** per episode, or **$2.12 (₱131)** with one retry per asset, plus $6 (₱371) a month for ElevenLabs Starter, at ₱61.8 = $1 (Aug 2026 rate).

## What Episode 06 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 stills (golden kingdom under the range, army stalled in a blizzard, ridge between two valleys, caravan at a toll waystation) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled. 4 generations, no re-rolls (6 approved). The CTA reuses the hook plate | $0 cash (Figma AI credits) |
| Two animated map shots, skyline trace, snowfall, ridge line, road line, map key | Remotion code (new `atlas` scene, `src/graphics/Terrain.tsx`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 76 words, 30.7 s | $0 |
| Score + SFX (new: blizzard, caravan, war horn, mountain rise) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container (render ≈ 3 min) | $0 |
| **Total** | | **$0 cash (₱0)** plus 4 Figma image generations |

Rate update: the BSP reference rate was **₱63.35 = $1 on 22 Oct 2026** (used for EP06 onward). At that rate the paid primary stack is about **$1.15 (₱73)** per episode, or **$2.12 (₱134)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter.

## What Episode 07 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 stills (Ostral in its river bend, the empty valley, the citadel wall, the riverside market) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled. 4 generations, no re-rolls (6 approved). The survey, overlap, reveal and CTA shots reuse plates | $0 cash (Figma AI credits) |
| Survey overlay, reason tally, survey pin and overlap glow, sightlines, road lines, dusk lights | Remotion code (`src/graphics/Survey.tsx`, `ghostLines`, `duskGrade`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 77 words, 29.7 s | $0 |
| Score + SFX (new: tally, stake) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)** plus 4 Figma image generations |

On the paid primary stack: about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 08 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 stills (the cup beside gold coins, the courtyard house, the locked water stand, the caravan in the dunes) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled. 4 generations, no re-rolls (6 approved). The cup shot, lesson and CTA reuse the cup plate; the map is all code | $0 cash (Figma AI credits) |
| Pull-back insets, desert map (dunes, wells, padlocks, key threads, control wash), spout lines, rings, dusk lights | Remotion code (new `pullBack` in `src/graphics/Scale.tsx`; new atlas kinds `dunes`, `well`, `lock`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 77 words, 30.7 s | $0 |
| Score + SFX (new: drop, lock) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container (render ≈ 4.5 min) | $0 |
| **Total** | | **$0 cash (₱0)** plus 4 Figma image generations |
## What Episode 09 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 stills (traveller in desert robes in a blizzard, the same framing in Haskari furs, the sunken winter camp with fish racks, the sunrise migration) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled. **5 generations** (6 approved): the first migration plate read too close to a real reindeer-herding people's dress and tents and had faces in the caption band, so it was re-rolled once. The strike, food, lesson and CTA shots reuse plates | $0 cash (Figma AI credits) |
| Callouts, reason tally (new climate icons), reverse card, rust strike, route line, smoke, snowfall | Remotion code (new `src/graphics/Climate.tsx`; `reasonTally`, `reverseCard`, `ghostLines`, `steam`, `snowfall`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 76 words, 30.3 s | $0 |
| Score + SFX (new: hearth, procession, strike) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container (render ≈ 3.5 min) | $0 |
| **Total** | | **$0 cash (₱0)** plus 5 Figma image generations |

On the paid primary stack: about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 10 actually used

| Item | Used | Cash cost |
|---|---|---|
| 3 stills (the palace city of Solenne, the Kestrel bridge over its gorge, the bridge gate shut at night) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled. 3 generations, no re-rolls (6 approved). The CTA reuses the palace plate; the three map shots are code | $0 cash (Figma AI credits) |
| Realm map, zoom and pull-back, gorge and bridge, closing ✕ and darkening, flow lines, lesson stack, dusk lights | Remotion code (`atlas` scene with new `gorge`, `bridge`, `palace` glyph and cue-timed zoom; `ghostLines`, `lessonStack`, `duskGrade`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 75 words, 30.0 s | $0 |
| Score + SFX (new: gateSlam) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)** plus 3 Figma image generations |

On the paid primary stack, with 3 stills instead of 4: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 12 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 stills: two matched then/now pairs (Bellnight outside the walls of Dunmere and the same gate barred in a blizzard; the bonfire ring and the same ring huddled at a dying fire) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled. 4 generations, no re-rolls (6 approved). The festival, count, lesson and CTA shots reuse them | $0 cash (Figma AI credits) |
| Era dissolves, origin ledger, head count, title, tag, lesson stack, snow, CTA card | Remotion code (new `eraShift`, `originLedger`, `headCount`; existing `titleLockup`, `tag`, `lessonStack`, `snowfall`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 78 words, 30.6 s | $0 |
| Score + SFX (new: timeFold, headCount) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)** plus 4 Figma image generations |

On the paid primary stack: about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## Alternatives

| Option | Per-episode | Monthly | Comment |
|---|---|---|---|
| **Zero-cost fallback** (Kokoro + procedural scenes + synth score + GH Actions) | $0 | $0 | Episode 01 first render; still the fallback for any shot without a plate. |
| Figma `generate_image` for stills | Figma AI credits (cost per image unpublished) | inside your Starter plan (500 credits/mo, 150/day) | No new bill; good for drafts and stills. |
| Creatomate instead of Remotion | 19 credits per 30 s 1080×1920@30 render | Essential plan (docs mention $54; third-party lists conflict) | Adds a fixed fee; less custom motion design. |
| Remotion Lambda instead of GH Actions | ≈ $0.01 AWS compute (scaled from Remotion's $0.017 / 1-min example) | $0 | Worth it only if you need parallel renders at scale. |
| Veo 3.1 Fast (no audio) instead of gen4_turbo | $0.10/s → $1.30 for 13 s | — | Try on one hero shot if gen4_turbo motion is weak. |

## Cost controls built in

- `pipeline/plates.py` is a dry run by default and prints an estimate. It spends money only with `--yes`.
- The map is vector graphics, so it never needs generation.
- Clips are only for the hook and payoff; every other shot uses a still with a restrained camera move.
- `--only <shot>` regenerates a single failed shot instead of the whole set.
