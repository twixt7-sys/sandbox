# EP07 production brief: Why Are Your Cities Built There?

**Series:** Worldcraft Shorts, Episode 07 / 50 (Arc 2: Geography and Nature).
**Plan entry** (`docs/SERIES_PLAN.md`): hook "Nobody builds a great city in the middle of nowhere without a reason." Topic: settlement placement. CTA: "Comment the most unusual place you'd build a city."
**Deliverable:** 29.7 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** a city exists where several reasons overlap on one spot. Give every settlement its reasons.
- **One example:** **Ostral** (the only name). It is a city on a lone limestone hill inside a river loop, and four reasons meet there:
  1. **water**: the river bends around the hill;
  2. **soil**: floodplain meadows that the spring floods renew;
  3. **defense**: a cliff-sided hill with a view of the whole valley;
  4. **trade**: two long-distance paths meeting right below it.
- **One shareable thought:** "Give every city a reason to exist, and your map tells its own history."
- **Scope guard:**
  - EP06 already covered range-scale geography, so EP07 has no mountains as a barrier.
  - EP10 is the single place everyone fights over, so the crossing here is only one reason of four, never the decisive chokepoint.
  - EP08 (water scarcity) is the water-power episode, so water here is a necessity, not power.

### How EP07 varies the series rhythm

| | EP05 | EP06 | EP07 |
|---|---|---|---|
| Hook | Title over ruins | Skyline trace and "empire?" | The finished city and "NO GREAT CITY / by accident." |
| Spine | Plate → plate → card | Map → plates → map | **Before/after on photographs.** The same valley, empty, is surveyed *on the plate itself*: water band, soil hatch, defense ring, roads. Two close-up plates break it up, then the layers overlap, glow, and dissolve into the city standing on that exact hill |
| Running device | Chips per clue | Map key at the end | **A reason tally** across the top (four empty slots fill one by one), which becomes the lesson: bracket → "GIVE EVERY CITY / a reason to exist." |
| CTA | Comment | Share | Comment (city at dusk, lights coming on) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 48/100 characters and the TikTok caption is 233 characters.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026), the same as EP06.
- Still no Runway, ElevenLabs or Creatomate keys. AWS credentials exist but weren't used.
- Figma: the user approved up to 6 generations for EP07, and 4 were used.
- Placement logic: water, fertile floodplain, defensible high ground and route crossings are the standard settlement factors in historical geography. The episode uses them through an invented example only.

## 2. Stack

Same stack as EP06:
- 4 Figma stills (`gemini-3.1-flash-lite-image`, lanczos to 1080×1920);
- Remotion graphics (all code);
- Kokoro `af_heart` narration ("Ostral" → /ˈɑstɹᵊl/, AH-strul, checked via the G2P);
- synthesized score and SFX;
- `qa.py` plus a contact sheet and beat frames.

New in this episode:
- `reasonTally` and `surveyPin` graphics (`src/graphics/Survey.tsx`);
- `tally` and `stake` SFX;
- `duskGrade` now takes a `lights` band so the windows sit on the city.

## 3. Narration (77 words, measured 29.71 s)

> Nobody builds a great city in the middle of nowhere without a reason. / Before Ostral, this valley was empty. Why here? / Fresh water at the river bend. / Soil the spring floods renew. / A hill no army can take by surprise. / And two trade roads meeting right below. / Every reason lands on the same spot. / Give every city a reason to exist, and your map tells its own history. / Comment the most unusual place you'd build a city.

The first draft ran to 83 words. Trimmed to 77, it measured 28.4 s, so I added beats after each surveyed reason, which brought it to 29.7 s.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.52 | "Nobody builds a great city in the middle of nowhere without a reason." | Ostral from the hillside: citadel on the rock, river bend, bridge where two roads meet; "NO GREAT CITY / by accident." | The answer first, as the strongest image |
| 2 | `empty` | 4.52–8.00 | "Before Ostral, this valley was empty. Why here?" | Same kind of valley, wild; survey stake drops on the hilltop with a "?"; four empty tally slots | The question |
| 3 | `survey` | 8.00–12.33 | "Fresh water at the river bend. Soil the spring floods renew." | Water-blue band traces the loop; ember-dashed floodplain; WATER and SOIL fill | Reasons 1 and 2 |
| 4 | `citadel` | 12.33–14.96 | "A hill no army can take by surprise." | Guards on the citadel wall over a sheer cliff; amber sightlines across the valley; DEFENSE fills | Reason 3 |
| 5 | `market` | 14.96–17.63 | "And two trade roads meeting right below." | Riverside market; carts and mules converge; ring on the square; TRADE fills | Reason 4 |
| 6 | `overlap` | 17.63–20.40 | "Every reason lands on the same spot." | Back to the empty valley: all layers, defense ring, both paths to the ford; rings converge and the hilltop glows | Payoff |
| 7 | `reveal` | 20.40–25.26 | "Give every city a reason to exist, and your map tells its own history." | Dissolve to Ostral, glow fading on the citadel; tally bracket and lesson line | Lesson |
| 8 | `cta` | 25.26–29.74 | "Comment the most unusual place you'd build a city." | Ostral at dusk, windows lit; CTA card | Comment CTA; loops to frame 1 |

Motif colour: water `#7fd3ec` (the river band). The soil hatch uses ember and the defense ring parchment, so everything else stays on the series palette.

## 5. Generated assets

- `plates/hook.jpg` (the city), `empty.jpg`, `citadel.jpg`, `market.jpg`, from the Figma file "Worldcraft Shorts EP07 plates" in the user's drafts. The reveal and CTA reuse the city plate, and the survey and overlap shots reuse the empty plate.
- `ep07.srt` (14 cues), `Worldcraft_Short_E07_cover.jpg` (hook frame at 3.4 s).

## 6. Final video and verification

- `out/ep07.mp4` (master, 37.5 MB) and `out/ep07_compat.mp4` (23.4 MB): sent to the user with SendUserFile.
- `ep07_download.mp4` (two-pass 3300k, 13.0 MB) and `ep07_player.mp4` (CRF 26, audio copied from the master, 8.5 MB): used on the preview page.
- `qa.py` **passed** on all four files: 1080×1920, 30 fps, 29.74 s, −14.1 LUFS, true peak −1.5 dB.
  - The first player encode re-encoded the audio at AAC 128k and **failed** true peak (0.0 dB). Copying the master's audio stream fixed it, and STYLE.md now says to do this.
- Fixes from inspecting the frames:
  - the citadel guards' heads sat in the caption band, so I reframed;
  - the sightlines were too faint;
  - the defense-ring fill fogged the hill;
  - the overlap glow was too weak.
- **Not verifiable by me:** how the narration and mix sound. Please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `reasonTally` (`items: [{icon, label, at}]`, `sumAt`, `sumKicker`, `sum`), with icons `water`, `soil`, `defence`, `trade` | Any "N factors" episode: EP09 climate (clothing, housing, food…), EP19 collapse causes, EP21 the three magic questions |
| `surveyPin` (`ask` "?", `glowAt` overlap glow, `fadeAt`, `stake: false`) | Marking the subject of a question on a plate (EP10's key location, EP46's hidden forest) |
| `duskGrade` `lights: [x0,y0,x1,y1]` | Any city-at-dusk CTA |
| SFX `tally`, `stake` | Checklists, survey moments |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 4 stills, Figma AI credits (4 of the approved 6) | $0 / ₱0 cash |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)** + 4 Figma generations |

On the paid primary stack: about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata` (pasted in `docs/DISTRIBUTION.md → Episode 07`). The AI label is ON for every platform. The pinned comments ask for the most unusual city location and the reason people would still live there.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook image | Finished city first, empty valley second | Empty valley first ("Why here?"), city only at the reveal | Viewed vs swiped away; average % viewed |
| 2 | Running tally | Four icons visible from 0:05 | No tally; tags per reason (EP05 style) | Retention between 8 and 17 s |
| 3 | CTA prompt | "Most unusual place you'd build a city" | "Where's the capital on your map, and why there?" | Comments per 1,000 views; replies to the pinned comment |

Also track how many comments name a real reason (water, defense…) rather than only a place. That signals the lesson landed.

## 11. How to produce EP08 ("What If a Desert Had No Water?")

1. Branch `claude/worldcraft-ep08` from `claude/worldcraft-ep07`. Read `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`, and the EP06 and EP07 briefs.
2. **Ask before spending Figma credits** (about 4 stills). The default is no public release.
3. Story: hook "How does a civilization survive where water is worth more than gold?" One invented desert society, and one mechanism: scarcity reshapes architecture, law, transport and power, so whoever holds the water holds the region.
   - Good fits: the `atlas` scene (wells as `town`/`coin`, control as `wash`) or `allocation` (EP03's split-supply graphic). The latter is already water-coloured.
   - Avoid re-showing EP07's "water is a reason to settle". EP08 is about control and rules.
4. Vary the rhythm again: for example, open on a single cup of water and pull back to the system it sits in.
5. Narration about 70–78 words. Measure it with `cd pipeline && python tts.py ep08` before you lock the cues.
6. Then:
   - `pipeline/build.sh ep08` → stills → render → `qa.py` → sheet and beat frames;
   - encodes (compat, download, and a player copy with `-c:a copy`);
   - `srt.py`, `storyboard.py`, cover;
   - preview page with a Download MP4 button, SendUserFile;
   - commit and push to the episode branch.
