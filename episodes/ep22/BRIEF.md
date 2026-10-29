# EP22 production brief: The Most Dangerous Magic Is Cheap Magic

**Series:** Worldcraft Shorts, Episode 22 / 50. Second episode of **Arc 5: Magic and Its Rules**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "If healing is free, why does anyone ever die from an injury?" Topic: magic and consequences. CTA: "Share this with a fantasy writer who loves overpowered magic."
**Deliverable:** a 30.1 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. The AI disclosure is on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** a cheap power changes society more than a rare one, because everybody uses it. So follow every major ability outward, and make the world explain the cases the power should have prevented.
- **One realm, one name:** **Veyra**, shown on screen only and never spoken. Its healers are *menders*, an ordinary English word, so there's nothing for the text-to-speech to mispronounce.
- **One cheap ability, followed into society:** one touch from a mender closes any wound. The episode shows three knock-on changes that a lazy story would forget:
  - **Medicine:** surgeons vanished, and nobody remembers how to set a bone (an abandoned workshop);
  - **War:** wars got longer, because no wound sends a soldier home (a line of unhurt soldiers, with small glows healing them back into the line);
  - **Power:** menders became the most powerful class (a queue up the steps of their hall).
  
  Then the turn: **if anyone in your story dies of a wound, explain why.** A mender sits beside an empty bed, and her glow gutters out.
- **One shareable thought:** "Every cheap power rewrites a hundred ordinary lives. Follow it." On screen: FOLLOW THE RIPPLE / *Every cheap power rewrites a hundred lives.*
- **Platform-safe:** no wound, blood or body is shown anywhere. Injury and death are implied: unhurt soldiers, an empty bed, a light that goes out. The healing glow is jade light drawn in code. There are no real-world medical or religious symbols: no cross, no snake staff, and no saffron robes (a round-1 plate with them was rejected).
- **Scope guard within Arc 5:**
  - EP21 (the can / can't / costs framework) isn't re-taught. EP22 assumes it, and "one touch" is the whole rule.
  - EP23 (creative costs): this magic is simply free. The episode never explores what a cost could be.
  - EP24 (magic vs technology): medicine appears only as one ring, not as a technology comparison.
  - EP25 (weaknesses): the failure on the lost plate stays an open question ("explain why"), not a weakness taught.
  - EP29 (immortality): no resurrection at all. The magic heals wounds; death remains.

### How EP22 varies the series rhythm

| | EP02 | EP16 | EP17 | EP22 |
|---|---|---|---|---|
| Hook | Premise over the sky | The throne, questioned | The cruel palace | **The cheap power itself:** a mender's hand glowing on a young man's arm in a sunny street, "IN VEYRA, HEALING IS FREE / So who dies?" |
| Spine | `consequenceTree`: medallions on branches | A map traces the grain roads | A roof on pillars | **Ripples from one point:** the city from straight above, the glow in its plaza sending rings out; each consequence plate arrives on a ring sweeping across the frame and is numbered as a ring (`ringTag`) |
| Turn | The sum | The crown flies to the guild | The pillars are people | **The last ring finds a death:** a rust, dashed RING IV · UNEXPLAINED; the glow fails over the mender's hands; "Why?" |
| Lesson | Sum card | `titlePower` | Stack lifts | All four rings on the dimmed map (three jade, one dashed "?"), which lifts as the lesson lands |
| CTA | — | Follow | Share | Share (the opening street at dusk, the glow still under the mender's hand) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules haven't changed since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 55/100 characters, the TikTok caption 238, and Instagram's hook line is the first 27.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). It's a week old, so I didn't re-check it.
- Figma: the Starter plan is out of AI credits until **1 Nov 2026** (today is 29 Oct), so I used the free local route without asking, as the brief says.
- No Runway, ElevenLabs or Creatomate keys were used. AWS credentials exist in the environment but weren't used.
- The idea: treating a magic system's social and economic side-effects as part of its design is standard craft advice in fantasy writing (the "if it's cheap, everyone uses it" test). The episode makes no claim about any real medicine, army or faith.
- Parallel episodes: when I started, only EP19 and EP20 had pushed, and both were WIP (`ec27b63`, `476bd6a`). EP18 and EP21 had no branch, so there was no EP21 brief to build on. EP22 therefore assumes only the plan's framing of EP21 (can / can't / costs) and avoids it.

## 2. Stack

Same stack as EP11–EP17:
- 6 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++. Both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics, all code. The healing magic is drawn in code over the plates and pinned with `"local": true`.
- Kokoro `af_heart` narration.
- Synthesized score (A minor → A major) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode (`src/graphics/Ripple.tsx`):
- `mendGlow`: a breathing jade glow with rising sparks at a plate point. `pulses` brighten it and send a ring out. `core: false` draws only a ring sweeping across the frame. `failAt` makes it gutter twice and go out, leaving a faint rust ember.
- `rippleMap`: rings of consequence spreading from one origin. Each ring has a wavefront, a pin and a label; a `lost` ring is dashed with a rust "?". `idle` sends faint rings out. `liftAt` / `lift` and `lessonText` lay out the lesson, as `pillarStack` does.
- `ringTag`: a `tag` with a concentric-ring glyph and a numeral; `lost` turns it rust and dashed.
- `mend` and `ripple` SFX (`pipeline/score.py`). `mend` is the signature sound of the healing and is reused every time a glow lights: the hook, the touch, the three soldiers, the menders' door, the bed. `ripple` plays on every ring.
- Motif colour: **mend `#a6e3c4`** (pale jade), used only for the healing and its rings. Everything else stays on the series palette, with rust for the unexplained death.

## 3. Narration (78 words, measured 30.05 s)

> If healing is free, why does anyone ever die from an injury? / Here, one touch from a mender closes any wound. / Surgeons vanished. Nobody remembers how to set a bone. / Wars got longer, because no wound sends a soldier home. / And menders became the most powerful class. / If anyone in your story dies of a wound, explain why. / Every cheap power rewrites a hundred ordinary lives. Follow it. / Share this with a fantasy writer who loves overpowered magic.

The first pass measured 29.70 s. I then lengthened the pause after "explain why" (0.55 → 0.9 s) so "Why?" holds on screen before the dissolve, which brought it to 30.05 s. No invented name is spoken.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–3.99 | "If healing is free, why does anyone ever die from an injury?" | A mender in a moss-green hood holds a young man's hand in a sunny market street, with a jade glow under her palm; "IN VEYRA, HEALING IS FREE / So who dies?" | The premise and its contradiction |
| 2 | `touch` | 3.99–6.98 | "Here, one touch from a mender closes any wound." | The walled city from straight above; the glow in the small plaza pulses and faint rings spread; ONE CHEAP POWER / *A mender's touch* | The one cheap ability; the origin of every ring |
| 3 | `surgeon` | 6.98–10.43 | "Surgeons vanished. Nobody remembers how to set a bone." | An abandoned workshop, dusty and empty; a ring sweeps across; RING I · MEDICINE / *Surgeons, forgotten* | Medicine |
| 4 | `war` | 10.43–13.92 | "Wars got longer, because no wound sends a soldier home." | A line of unhurt soldiers in a dawn field, with three small glows lighting on them in turn; RING II · WAR / *Nobody goes home*; distant horn | War |
| 5 | `menders` | 13.92–16.70 | "And menders became the most powerful class." | A crowd queuing up the steps of a grand hall, with a glow at its door; RING III · POWER / *Menders rule*; a coin | Power |
| 6 | `lost` | 16.70–20.53 | "If anyone in your story dies of a wound, explain why." | Candlelit room: the mender alone by an empty bed; the glow over her hands gutters out; rust RING IV · UNEXPLAINED / *Couldn't save*; "Why?" | The turn |
| 7 | `lesson` | 20.53–24.83 | "Every cheap power rewrites a hundred ordinary lives. Follow it." | The dimmed city: rings I–III in jade (MEDICINE, WAR, POWER) and a dashed IV "?" (UNEXPLAINED / Why?); the map lifts; FOLLOW THE RIPPLE / *Every cheap power rewrites a hundred lives.* | The lesson |
| 8 | `cta` | 24.83–30.05 | "Share this with a fantasy writer who loves overpowered magic." | The hook street at dusk, the glow still lit; CTA card with the Share pill; cross-fades to the hook | Share CTA; loops |

## 5. Generated assets

- The plates, from local SDXL-Lightning (the prompts are in each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: the mender and the young man, seed 7 (round 2);
  - `plates/touch.jpg`: the walled city from above, seed 23 (rendered as the `city` prompt and renamed for the shot id);
  - `plates/surgeon.jpg`: the abandoned workshop, seed 23;
  - `plates/war.jpg`: the soldiers at dawn, seed 11;
  - `plates/menders.jpg`: the queue up the hall steps, seed 23 (round 2);
  - `plates/lost.jpg`: the mender by the empty bed, seed 11.
- **18 candidates in two rounds:**
  - round 1, 12 images: both hooks lacked a patient (a lone hooded girl). One menders plate put the crowd in saffron robes, which reads as real monks, so it was rejected; the other looked monastic too. The city, workshop, soldiers and empty-bed plates were kept.
  - round 2, 6 images (3 seeds each): hook seed 7 shows the touch, and menders seed 23 is a mixed crowd climbing to the door.
- **Code-drawn:** every glow and ring, the failing light, the ring tags and map, and all type. Plates show the world and people, never spells.
- `ep22.srt` (17 cues) and `Worldcraft_Short_E22_cover.jpg` (the hook at 2.3 s with the title).

## 6. Final video and verification

- `out/ep22.mp4` (master, 36.0 MB) and `out/ep22_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 20.4 MB): sent with SendUserFile.
- `ep22_download.mp4` (two-pass 3300k, 13.5 MB) and `ep22_player.mp4` (CRF 26, 6.5 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 30.08 s, −14.1 LUFS, true peak −1.5 dB (the compat copy, with its AAC re-encoded, measures −1.4 dB). The download copy published on the preview page was read back and QA'd as well (see the page's Checks).
- Fixes made after inspecting the beat frames and the contact sheet:
  - the city plate didn't show on the touch and lesson shots (it was registered as `city`, but the shot id is `touch`), so it was renamed and the build re-run;
  - the lifted map shrank to 60 %, which made the ring labels unreadable; it now lifts to 78 %, the labels are larger (27 px kicker, 50 px serif), and the lift waits for "rewrites";
  - the rings recap ran after the lift had started, so they now begin 0.3 s before the lesson shot and stagger by 0.22 s;
  - "Why?" appeared only during the dissolve, so it now lands on "explain", with a longer pause after the line;
  - three plates were reframed to keep faces and key points out of the caption band and the tag area: war ×1.16 raised 150 px, menders ×1.13 lowered 120 px, and lost ×1.22 shifted right and up, with the tag shortened to *Couldn't save* so it clears her face.
- **Accepted compromises:**
  - The menders plate has no clearly distinct healers at the top of the steps; the glow at the hall door and the tag carry "menders rule". Many in the queue also wear green, like the menders' coats.
  - The bed in the lost plate is a low cot at the left edge rather than a clear empty bed; the gutting glow over the mender's hands carries the loss.
  - The city's "plaza" is a small square in front of a gate, not a round central plaza.
  - The SDXL costumes are generic old-European (hooded coats, tunics). The realm, the menders and the story are original; no plate shows a real place, people, faith or medical symbol.
- **Not verifiable by me:** how the narration and mix sound, including the new `mend` and `ripple`. I can't hear the audio; please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `mendGlow` | Any magic drawn on a plate: healing, wards, a spell that fails (`failAt`); EP23–EP25 can reuse it for costs and weaknesses, with a different `color` |
| `rippleMap` | Following any one cause outward: a spell, an invention (EP24), a law, a plague; `lost` rings for the gap the story must explain |
| `ringTag` | Numbering consequences as we meet them |
| SFX `mend`, `ripple` | Healing or benign magic; consequences spreading |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 6 stills (18 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 6 stills: about **$1.35 (₱86)**, or **$2.48 (₱157)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 22`. The AI label is ON for every platform. The pinned comments ask viewers to name the cheapest power in their world and one ordinary job it destroyed, which turns the lesson into the comment game. The TikTok caption uses ✨ rather than a bandage emoji, keeping medical symbols out.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The glowing touch and the question | Open on the empty bed and the failing glow: "Healing is free here. So why is this bed empty?" | Viewed vs swiped away; average % viewed |
| 2 | Spine | One plate per ring, the map only at the start and the lesson | Stay on the map; each ring lights its institution as a small inset of its plate | Retention 4–17 s; rewatch rate |
| 3 | CTA | Share (from the plan) | Comment: "Name your world's cheapest power and the job it destroyed." | Shares per 1,000 views vs comments per 1,000 |

Also track how many comments name a *consequence* (not just a power), which shows the lesson landed.

## 11. How to produce EP23 ("Make Magic Expensive Without Using Mana")

1. Branch `claude/worldcraft-ep23` from `claude/worldcraft-ep22`. Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief, the EP21 brief (once it's pushed: the can / can't / costs framework) and EP17's.
2. **Stills:** Figma credits reset on **1 Nov 2026**. If it's on or after that date and Figma would be clearly better, ask with AskUserQuestion first (about 4 images, up to 6). Otherwise use `python pipeline/local_stills.py ep23 <shots> --seeds 11 23` (add a third seed, such as 7, for people doing something specific with their hands), then `--pick`, then `plates.py --register` **and `pipeline/build.sh`**, since the plates reach `public/` only through the build. Name each prompt after its shot id. Run nothing heavy alongside, and budget a second round.
3. Story (plan): costs that aren't mana. "Every spell steals a memory" is the plan's example; others are years of life, warmth, a name, a sense. The cost should create drama and choices.
   - One caster and one cost, shown through what it takes from them (a family that she can't recognise, a fading name on a door), never through injury.
   - `mendGlow` can draw the spell in a new motif colour; `failAt` and a rust ember suit a price being paid.
   - Don't repeat EP22's ripple map or EP02's tree. One idea: a ledger of the caster's life drawn in code, with one line struck out per spell (`callout` `then` can strike and re-caption).
   - Scope: EP21 is the framework, EP24 is magic vs technology, EP25 is weaknesses, and EP29 is immortality.
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep23`. Check invented names in the G2P, and use `nth` for repeated words in cues.
5. Then:
   - `pipeline/build.sh ep23` → render (the Chromium headless shell is now under `/opt/pw-browsers/chromium_headless_shell-1243/*/chrome-headless-shell`) → `qa.py` → sheet and beat frames, including the loop tail;
   - the compat, two-pass download and player encodes, all `-c:a copy`, with `qa.py` on each;
   - `srt.py`, `storyboard.py`, the cover, and an 11-section brief;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
