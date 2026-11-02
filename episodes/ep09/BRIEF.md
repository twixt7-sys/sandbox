# EP09 production brief: Your Climate Should Affect Your Culture

**Series:** Worldcraft Shorts, Episode 09 / 50 (Arc 2: Geography and Nature).
**Plan entry** (`docs/SERIES_PLAN.md`): hook "Why would people living in a frozen wasteland dress like desert nomads?" Topic: climate-driven culture. CTA: "Share this with a friend creating a fantasy civilization."
**Deliverable:** 30.3 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** climate is the cause and culture is the answer. Every layer of ordinary life should respond to the weather.
- **One example:** the **Haskari** (the only name), a people of a frozen coast. Four layers, each stated as cause → effect:
  1. **clothing**: wind bites, so they layer hooded furs (fur over felt, a wind-proof hood, sealed mitts);
  2. **housing**: heat leaks, so their homes sink half underground, below the wind;
  3. **food**: summer is short, so every catch is smoked over the fire or frozen in ice pits;
  4. **festival / migration**: when the sun returns, they migrate, and the journey itself is the festival.
- **One shareable thought:** "Let the weather shape your people, and they'll feel like they belong."
- **Scope guard:**
  - EP08 (parallel) is the desert where water is power, so EP09 is cold and seasonal, with no scarcity or control angle.
  - EP04 covered one ordinary detail (the rain bowl); EP09 is a whole set of adaptations with one shared cause.
  - EP11 is culture as values beyond clothing, so EP09 stays on material adaptation (clothes, homes, food, calendar).

### How EP09 varies the series rhythm

| | EP06 | EP07 | EP09 |
|---|---|---|---|
| Hook | Skyline trace and "empire?" | The finished city and "NO GREAT CITY / by accident." | **The wrong image itself:** a traveller in desert robes and sandals in a polar blizzard, "FROZEN WASTELAND / desert robes?" |
| Spine | Map → plates → map | Before/after survey on a photograph | **Strike and rebuild.** The robes are struck out in rust ("Don't / Dress for the wrong world" → "Let the cold / design them."), then the same framing dissolves to the same stance in Haskari furs, and the culture is rebuilt one layer per line, each line a cause → effect |
| Running device | Map key at the end | Reason tally | `callout`s (new): field-guide labels on the costume, the house, the racks and the procession, with the EP07 tally counting CLOTHING, HOUSING, FOOD, FESTIVAL and summing to the lesson |
| CTA | Share | Comment | Share, over the hook's framing with the fur-clad Haskari; the loop cross-fades back to the robed traveller, so the question re-asks itself |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 55/100 characters and the TikTok caption is 247 characters. `#FantasyCulture` replaces `#FantasyMap` for this episode.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026), the same as EP06 and EP07. It's one day old, so I didn't re-check it.
- Still no Runway, ElevenLabs or Creatomate keys. AWS credentials exist but weren't used.
- Figma: the user approved up to 6 generations for EP09, and 5 were used.
- Adaptation logic: layered insulating clothing, semi-subterranean houses, smoking and cold storage of food, and seasonal migration timed to the sun are standard cold-climate adaptations in human geography. The episode uses them only through an invented people, and the costume, animals and objects were prompted as invented, not as any real culture's dress.

## 2. Stack

Same stack as EP06 and EP07:
- 4 Figma stills (`gemini-3.1-flash-lite-image`, lanczos to 1080×1920);
- Remotion graphics (all code);
- Kokoro `af_heart` narration ("Haskari" → /hæskˈɑɹi/, hass-KAR-ee, checked with the G2P);
- synthesized score and SFX;
- `qa.py`, plus a contact sheet and beat frames.

New in this episode:
- the `callout` graphic (`src/graphics/Climate.tsx`);
- `reasonTally` icons `clothing`, `housing`, `food` and `festival`, and a `gap` option;
- the `hearth` and `procession` beds and the `strike` hit.

## 3. Narration (76 words, measured 30.28 s)

> Why would people living in a frozen wasteland dress like desert nomads? / They wouldn't. Let the cold design them. / Wind bites, so the Haskari layer hooded furs. / Heat leaks, so homes sink underground. / Summer is short, so every catch is smoked and frozen. / When the sun returns, they migrate, and the journey is a festival. / Let the weather shape your people, and they'll feel like they belong. / Share this with a friend creating a fantasy civilization.

The first measured draft landed at 30.28 s (QA window 27–33 s), so it shipped unchanged.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–5.00 | "Why would people living in a frozen wasteland dress like desert nomads?" | A traveller in thin desert robes and sandals in a blizzard; "FROZEN WASTELAND / desert robes?" | The wrong image, as the hook |
| 2 | `strike` | 5.00–7.57 | "They wouldn't. Let the cold design them." | "Don't / Dress for the wrong world" struck in rust, a rust X over the robes, then "LET THE COLD / design them." | Strike it; state the method |
| 3 | `furs` | 7.57–10.85 | "Wind bites, so the Haskari layer hooded furs." | Dissolve to the same framing, now in furs; callouts LAYERS / HOOD / MITTS; tally appears, CLOTHING fills | Layer 1 |
| 4 | `camp` | 10.85–13.50 | "Heat leaks, so homes sink underground." | Sunken stone-and-turf domes with fire-lit tunnels and smoking vents; ground line; HALF SUNK / below the wind; HOUSING fills | Layer 2 |
| 5 | `food` | 13.50–17.18 | "Summer is short, so every catch is smoked and frozen." | Punch-in on the fish racks and the ice pit; SMOKED / FROZEN callouts; FOOD fills | Layer 3 |
| 6 | `migrate` | 17.18–21.52 | "When the sun returns, they migrate, and the journey is a festival." | First sunrise: a ribboned procession with sledges and shaggy horned beasts; amber route; FESTIVAL / the move itself; FESTIVAL fills | Layer 4, the warm turn |
| 7 | `lesson` | 21.52–25.36 | "Let the weather shape your people, and they'll feel like they belong." | Dissolve back to the Haskari in the storm; tally bracket → "LET THE WEATHER / shape your people." | Lesson |
| 8 | `cta` | 25.36–30.28 | "Share this with a friend creating a fantasy civilization." | Same framing; CTA card with the paper-plane pill; cross-fade to the robed traveller for the loop | Share CTA, loops to frame 1 |

There's no separate motif colour: the cold is carried by the plates and the snowfall, rust marks the struck idea, and the callouts and route are amber.

## 5. Generated assets

- From the Figma file "Worldcraft Shorts EP09 plates" in the user's drafts:
  - `plates/hook.jpg` (robes in a blizzard);
  - `furs.jpg` (the same framing in furs);
  - `camp.jpg` (the sunken winter camp with fish racks and an ice pit);
  - `migrate.jpg` (the sunrise procession).
- Reuse:
  - the strike reuses the hook plate;
  - the food shot reuses the camp plate;
  - the lesson and CTA reuse the furs plate.
- The first migration plate was rejected. It had reindeer, conical tents and beaded trim that read as a real herding people, and faces in the caption band. The re-roll has invented beasts and saffron sashes, with everyone seen from behind.
- `ep09.srt` (16 cues) and `Worldcraft_Short_E09_cover.jpg` (the hook frame at 3.4 s).

## 6. Final video and verification

- `out/ep09.mp4` (master, 37.4 MB) and `out/ep09_compat.mp4` (22.7 MB): sent to the user with SendUserFile.
- `ep09_download.mp4` (two-pass 3300k, 13.5 MB) and `ep09_player.mp4` (CRF 26, 7.5 MB): used on the preview page. Both copy the master's audio.
- `qa.py` **passed** on all four files: 1080×1920, 30 fps, 30.32 s, −14.0 LUFS, true peak −1.4 dB.
- Fixes from inspecting the frames:
  - the tally labels CLOTHING and HOUSING collided, so I added `gap` and set it to 196;
  - I enlarged the callout type;
  - the camp callout first sat on a bright roof and then collided with the tally, so I moved it into the band below;
  - the frost-blue ground line vanished on snow, so I made it amber;
  - the sun glow on the migration plate sat behind the tally icons, so I removed it, since the sun is already the brightest thing in the frame.
- **Not verifiable by me:** how the narration and mix sound. Please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `callout` (`at`, `label`, `note`, `side`, `reach`, `rise`, `start`/`end`) | Annotating any plate: EP11 cultural markers, EP15 trade goods, EP23 a magic item's parts, EP46 the hidden forest |
| `reasonTally` icons `clothing`, `housing`, `food`, `festival`; `gap` | Any "layers of daily life" count; longer labels |
| SFX `hearth`, `procession` (beds), `strike` (hit) | Interiors and camps; parades, migrations, rituals; every `reverseCard` |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 5 stills, Figma AI credits (4 kept plus 1 re-roll, of the approved 6) | $0 / ₱0 cash |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)** + 5 Figma generations |

On the paid primary stack: about **$2.12 (₱134)** including the one retry, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata` (pasted in `docs/DISTRIBUTION.md → Episode 09`).
- The AI label is ON for every platform.
- The pinned comments ask viewers for a climate and the one strange custom it forced, and Instagram's asks them to tag a world-building friend, which fits the share CTA.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook image | The wrong costume (robes in a blizzard) | The right costume first, with "Why does this work?" | Viewed vs swiped away; average % viewed |
| 2 | Spine | Strike-and-rebuild with callouts | Same plates, tally only, no callouts | Retention between 7 and 17 s |
| 3 | CTA | "Share this with a friend creating a fantasy civilization" | "Comment your world's climate and we'll guess one custom" | Shares per 1,000 views (A) vs comments per 1,000 (B); follows from shares |

Also track how many comments describe a cause → effect ("monsoon, so…") rather than only naming a climate. That shows the lesson landed.

## 11. How to produce EP10 ("The Most Important Place on Your Map")

1. Branch `claude/worldcraft-ep10` from the latest episode branch that contains EP08 and EP09. Read `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`, and the EP07 and EP09 briefs.
2. **Ask before spending Figma credits** (about 4 stills). The default is no public release.
3. Story: hook "The most important location in your world might not be a capital." This is the single-chokepoint payoff that EP06 and EP07 deliberately held back: one narrow pass, sacred spring, bridge or harbour that everyone depends on, so it matters more than any palace.
   - Good fits: the `atlas` scene to show every route funnelling through one point (`route` with `flow`, `gate`, `wash`); `surveyPin` with `glowAt` on the chokepoint; `callout` for what passes through it; `reasonTally` for who depends on it.
   - Avoid re-doing EP07's "reasons a city is here". EP10 is about dependence and contest, not settlement.
4. Vary the rhythm again: for example, open on the palace, pull back to the map, and let every line converge on a place that isn't the palace.
5. Narration of about 70–78 words. Measure it with `cd pipeline && python tts.py ep10` before locking cues.
6. CTA is a question ("What location would every kingdom fight to control?"), so use `ctaCard` with the default comment icon.
7. Then:
   - `pipeline/build.sh ep10` → stills → render → `qa.py` → sheet and beat frames;
   - encodes (compat, download, and a player copy with `-c:a copy`);
   - `srt.py`, `storyboard.py`, cover;
   - preview page with a Download MP4 button, SendUserFile;
   - commit and push to the episode branch.
