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

## What Episode 11 actually used

| Item | Used | Cash cost |
|---|---|---|
| 3 stills (an empty costume on a dress form, the Varenni funeral courtyard, the costume worn by an elder) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 11 candidates, 3 kept. Figma was tried first: the plan is out of AI credits until 1 Nov 2026, so the call was refused and nothing was charged | $0 |
| Grade wipe (outsider → insider), code-drawn shroud, callouts, ring, lesson stack | Remotion code (new `plateLook`, `shroud`; `callout`, `ghostLines`, `lessonStack`, `dustBeam`, `tag`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 76 words, 31.16 s | $0 |
| Score + SFX (new: relook) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

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

## What Episode 13 actually used

| Item | Used | Cash cost |
|---|---|---|
| 3 stills (the Adren hill doorway, the Vesk magistrate's hall, the border bridge) | Figma `generate_image` (`gemini-3.1-flash-lite-image`), 768×1376, lanczos-upscaled. 4 generations of the 6 approved: the first Vesk plate was re-rolled because its window showed a recognisably real city and its host read as a stereotype. The hook, the two-sided replay and the CTA reuse these plates | $0 cash (Figma AI credits) |
| Split frames, labels and stamps, callouts, mirror ledger, dusk grade | Remotion code (new `splitFrame` and `mirrorLedger`; `callout` `side: "up"` and `backdrop`; `tag`, `emberDusk`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 77 words, 30.9 s | $0 |
| Score + SFX (new: giftSet, seam) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)** plus 4 Figma image generations |

On the paid primary stack, with 3 stills plus one re-roll (4 images): about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 14 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 stills (Mira on the dawn river path, the free town, the valley league's hooded line, the empty bank at dusk) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 10 candidates, 4 kept. Figma was tried first: the `generate_image` call was blocked by the session's permission check before reaching Figma, so no Figma credits were used | $0 |
| Verdict scale, re-captioned callout, watch post and horn, tags, rain, lesson stack, CTA card | Remotion code (new `verdictScale`, `watchPost`, `callout` `then` and `noteSize`; `tag`, `rain`, `lessonStack`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 75 words, 29.8 s | $0 |
| Score + SFX (new: scaleTip) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 4 stills: about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 15 actually used

| Item | Used | Cash cost |
|---|---|---|
| 3 stills (the morning street, the two neighbours on the bench, the same street at dusk) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 12 candidates in three rounds, 3 kept: street seed 23, bench seed 8 (third prompt), dusk seed 11. A gibberish shop sign on the bench plate was painted out with PIL. Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| Ink evidence chains, value seals, code-drawn street bench, pull-back, lesson card, CTA card | Remotion code (new `inferChain` and `bench`; `pullBack`, `callout`, `tag`, `titleLockup`, `reverseCard`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 77 words, 30.33 s | $0 |
| Score + SFX (new: benchSet, inferSeal) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 16 actually used

| Item | Used | Cash cost |
|---|---|---|
| 3 stills (the king in the throne hall, the guild keeper among the sacks, the empty throne) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 12 candidates in two rounds, 3 kept (seeds 5, 11, 8). Figma not used: out of AI credits until 1 Nov 2026 | $0 |
| Map, moving crown, granary, key ring, grain sack, lesson card, CTA card | Remotion code (new `titlePower`, `keyRing`, `grainSack`, atlas `crown` and `granary`; `atlas`, `inferChain`, `callout`, `tag`, `titleLockup`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 74 words, 29.7 s | $0 |
| Score + SFX (new: grainPour, crownShift) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 17 actually used

| Item | Used | Cash cost |
|---|---|---|
| 6 stills (the black palace over the stair, the farmer and his ox, the clerk in the records hall, the soldier's mother in her doorway, the neighbour in the night street, the palace over the morning market) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 18 candidates in two rounds, 6 kept: hook 11, farmer 11, cta 11 (round 2), clerk 23, mother 11, neighbour 11 (round 1). Round 1's palaces read as real tiered temples and were re-rolled. Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| Pillar stack (pillars that turn into the supporters), pillar tags, title, CTA card | Remotion code (new `pillarStack` and `pillarTag`; `titleLockup`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 74 words, 30.02 s | $0 |
| Score + SFX (new: pillarSet, doorKnock) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 6 stills: about **$1.35 (₱86)** (scaling EP15's 3-still and EP14's 4-still figures at about $0.10 a still), or **$2.48 (₱157)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 18 actually used

| Item | Used | Cash cost |
|---|---|---|
| 3 stills (the silent man before the official in the square, the shuttered night street, the square at dusk) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 13 candidates in three rounds, 3 kept: hook 11 (round 1), origin 11 (round 2), cta 23 (round 1). Rounds 2 and 3 couldn't paint a seated magistrate before a silent man, and no round painted an open gate, so the gate was dropped from the story. Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| The law card (written clause by clause, then lit with the fear behind each clause), window glints, tags, title, CTA card | Remotion code (new `lawText` and `glints`; `titleLockup`, `tag`, `callout`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 78 words, 29.76 s | $0 |
| Score + SFX (new: quill, clauseLight) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.15 (₱73)** with one retry per still, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 19 actually used

| Item | Used | Cash cost |
|---|---|---|
| 5 stills (the capital at its height, the failed harvest, the tax table, the shut provincial gate, the army marching out) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 13 candidates in two rounds, 5 kept: hook 11, harvest 23, taxes 11, army 11 (round 1), provinces 23 (round 2; round 1 never painted a shut gate). Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| The crack loop (four medallions, arrows closing into a loop, an accelerating pulse, cracks spreading through the seal, the seal splitting), crack tags, title, CTA card | Remotion code (new `crackLoop` and `crackTag`; `titleLockup`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 75 words, 29.52 s | $0 |
| Score + SFX (new: crackTick, sealSplit) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 5 stills: about **$1.25 (₱79)**, or **$2.27 (₱144)** with one retry per asset (scaled from EP16–EP17), plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).
## What Episode 20 actually used

| Item | Used | Cash cost |
|---|---|---|
| 3 stills (the dawn valley with a stone on each bank, Arvel's stone by the razed village, Dunmere's cairn field) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 12 candidates in three rounds, 3 kept, all from round 1: hook 11, arvel 11, dunmere 23. The second stone on the hook plate is the first stone, flipped, scaled, hazed and composited onto the far bank (SDXL wouldn't paint two); the cottage behind Arvel's stone was darkened into a burned shell. Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| Chronicle frames, carved tablets, lesson rows, lanterns, title, statement, CTA card | Remotion code (new `chronicleFrame`, `tablet`, `truthRows`, `lanterns`; `callout`, `titleLockup`, `statement`, `emberDusk`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 78 words, 29.99 s | $0 |
| Score + SFX (new: chisel, frameOpen) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).
## What Episode 21 actually used

| Item | Used | Cash cost |
|---|---|---|
| 6 stills (the mender's workshop, the fish jar, the broken wheel in a lane, the cottage window, the crown on its cushion, the hooded thief on a rooftop) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 12 candidates in one round, 6 kept: hook 23, can 11, cant 11, cost 11, crown 23, thief 11. The lesson and CTA reuse the hook plate. Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| Spell page, mend seams and cracks, story questions, tags, CTA card (new save icon) | Remotion code (new `spellPage`, `mendSeam`, `storyQuestions`; `tag`, `ctaCard` `icon: "save"`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 78 words, 29.93 s | $0 |
| Score + SFX (new: mendKnit, mendFizzle, costCrack) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 6 stills: about **$1.10 (₱70)** (EP17's estimate less its retries, at about $0.10 a still plus the fixed per-episode items), or about $2.48 (₱157) with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).
## What Episode 22 actually used

| Item | Used | Cash cost |
|---|---|---|
| 6 stills (the mender and the young man in the market street, the walled city from above, the abandoned workshop, the soldiers in the dawn field, the queue up the hall steps, the mender alone by the empty bed) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 18 candidates in two rounds, 6 kept: touch (city) 23, surgeon 23, war 11, lost 11 (round 1); hook 7, menders 23 (round 2). Round 1's hook had no patient and both menders plates read as monks (one in saffron robes), so they were re-rolled. Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| Healing glow, rings of consequence, ring tags, title, CTA card | Remotion code (new `mendGlow`, `rippleMap` and `ringTag`; `titleLockup`, `tag`, `oversizedWord`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 78 words, 30.05 s | $0 |
| Score + SFX (new: mend, ripple) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 6 stills: about **$1.35 (₱86)**, or **$2.48 (₱157)** with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 23 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 stills (Wren writing by candlelight, the harbour wall in a storm, the blue cottage door with a brass plate, her sister smiling at the garden gate) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 15 candidates in two rounds, 4 kept: hook 7, storm 7, door 7 (round 1); sister 11 (round 2). Round 1's sister plates all walked away down a lane, so it was re-prompted from Wren's point of view. Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| Memory ledger, fading name on the door, spell glows, sister callout, price pills, title, CTA card | Remotion code (new `memoryLedger` and `fadingName`; `mendGlow`, `callout` `then`, `titleLockup`, `oversizedWord`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 77 words, 29.83 s | $0 |
| Score + SFX (new: recall, forget) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 4 stills: about **$1.05 (₱67)**, or **$1.15 (₱73)** with one retry per still, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).
## What Episode 24 actually used

| Item | Used | Cash cost |
|---|---|---|
| 6 stills (the wagon train on the muddy road, the stone ring gate in a town square, the cabbage cart, the hill village, two travellers at a framed ring gate, the hooded courier at a night arch) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 21 candidates in two rounds, 6 kept: hook 11, cargo 23, village 23 (round 1); gate 23, queue (gate prompt, seed 7), courier 7 (round 2). Round 1 painted no stone ring in any gate shot, so the gate, queue and courier prompts were rewritten as "a giant circular stone ring portal standing upright on its edge". Two spire finials that could read as crosses were painted out of the gate and queue plates with the plates' own sky. Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| Gate light, stone ring on the hook's hill, crystal, counting board, tags, title, CTA card | Remotion code (new `gateRing`, `crystalPrice` and `countingBoard`; `titleLockup`, `tag`, `callout`, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 77 words, 31.26 s | $0 |
| Score + SFX (new: blink, gateFail, crystalBurn, bead) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 6 stills: about **$1.10 (₱70)**, or about $2.48 (₱157) with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 25 actually used

| Item | Used | Cash cost |
|---|---|---|
| 4 stills (the Unmaker on her balcony over the misty castle, the courtyard gate, the three hooded heroes by the great column, the Unmaker beside the oval mirror frame) | **Local SDXL-Lightning** (`pipeline/local_stills.py`, 4-step, CPU, 768×1344, lanczos to 1080×1920). 14 candidates in two rounds, 4 kept: hook 23, erase 11 (round 1); heroes 11, mirror 7 (round 2). Round 1's heroes weren't hiding and both mirror plates left the mirror out, so those two were re-rolled with seeds 7, 11 and 23. Figma credits are out until 1 Nov 2026, so it wasn't tried | $0 |
| Her sight, the erased gate, the courtyard plan with its ray-cast sight cone, tags, title, CTA card | Remotion code (new `gazeBeam`, `unmake` and `sightPlan`; `titleLockup`, `tag`, `mendGlow` for the lantern, `ctaCard`) | $0 |
| Narration | Kokoro-82M (`af_heart`), 74 words, 29.69 s | $0 |
| Score + SFX (new: gaze, unmake) | `pipeline/score.py` | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, no Figma credits |

On the paid primary stack, with 4 stills: about **$1.05 (₱67)**, or about $2.20 (₱139) with one retry per asset, plus $6 (₱380) a month for ElevenLabs Starter, at ₱63.35 = $1 (BSP, 22 Oct 2026).

## What Episode 26 actually used (Season 2 relaunch)

| Item | Used | Cash cost |
|---|---|---|
| Field card sprite (the Grimmaw) | **Figma AI, 1 generation**: `generate_image` with `gpt-image-2.5-sunburst`, 1536×1024, in the new file "Worldcraft Shorts EP26 art", on the user's Starter plan (`team::1384938462301182142`), approved for EP26. I attempted two more calls (the same prompt on `gpt-image-2.5-flare` and `gemini-3.1-flash-image`, to compare models), but the session's permission check **blocked both before they ran**, so they used no credits. Re-gridded to a 168 px sprite with `pipeline/pixelate.py` | $0 cash (1 of the ~12 generations allowed) |
| The Isle, the Grimmaw and mossback models, the herd simulation, HUD, graphs, field cards, stamps, end card, all type | Remotion + three.js (`@remotion/three`) code, software WebGL (`swangle`) | $0 |
| Narration | Kokoro-82M (`af_heart`, speed 1.05), 159 words, 51.6 s of speech, 60.3 s total | $0 |
| Score + SFX (new Season 2 palette) | `pipeline/score_s2.py` | $0 |
| Fonts (Silkscreen, Pixelify Sans, Inter 900) | Fontsource packages, SIL OFL, self-hosted | $0 |
| Render, QA, encodes | Claude cloud container | $0 |
| **Total** | | **$0 cash (₱0)**, 1 Figma generation |

**EP26 v2 (2 Nov 2026):** the music is now a composed score played by FluidSynth on the MuseScore General SoundFont (MIT, free from the Ubuntu archive). Still **$0** and no further Figma generations.

On the paid primary stack: no stills are needed any more (the world is code), so the only paid item would be ElevenLabs narration (about 900 characters, inside the $6 (₱380) a month Starter allowance), at ₱63.35 = $1 (BSP, 22 Oct 2026).

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
