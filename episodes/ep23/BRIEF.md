# EP23 production brief: Make Magic Expensive Without Using Mana

**Series:** Worldcraft Shorts, Episode 23 / 50. Third episode of **Arc 5: Magic and Its Rules**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "What if every spell stole one of your memories?" Topic: creative costs of magic. Core message: magic can cost physical strength, time, lifespan, social standing, rare materials, emotional stability, or something the caster values. A meaningful cost creates difficult choices. CTA: "Comment the strangest price someone could pay for magic."
**Deliverable:** a 29.9 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. The AI disclosure is on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`. `episode.json` is written by [`make_ep23.py`](make_ep23.py).

## The brief

- **One idea:** a cost the caster truly values turns every spell into a decision. Mana is a fuel gauge; a memory is a choice.
- **One caster, one cost, two names:** **Wren**, spoken, and her mother's name **Maren**, on screen only (painted on a door, fading). Wren's G2P is clean (`ɹˈɛn`), and Maren is never spoken.
- **The device: a ledger of what she remembers**, drawn in code on a dark, gilt-edged card (`memoryLedger`). Four lines are written in as she names them: *My first snow*, *Mother's name*, *My sister's face*, *My own name*. Then each spell strikes one line in rust, the words fade to a ghost, and a small rose mote of light drifts off the page: the memory leaving.
  - **Spell I:** she stills a storm from a harbour wall. *My first snow* is struck.
  - **Spell II:** she breaks a fever behind a cottage door (rose light in the door's window). *Mother's name* is struck, and the name on the door's brass plate fades letter by letter (`fadingName`).
  - **Spell III:** her sister smiles at her from the garden gate, and the callout HER SISTER / *Smiling at her* is struck to A STRANGER / *Who is she?* in rust.
  - **The turn:** only *My own name* is left, breathing in rose light. "Is the next spell worth it?"
- **Brief variety on the lesson:** price pills YEARS · WARMTH · A SENSE · A MEMORY, then MAKE IT COST / *A real price makes every spell a choice.*
- **Platform-safe and gentle:** nobody is hurt, ill or frightened on screen. The fever happens behind a closed door, and loss of memory is shown through a fading name, a struck line and a sister's friendly smile that isn't recognised. There are no real-world religious or occult symbols; the header ring of four points is invented.
- **Scope guard within Arc 5:** EP21 (can / can't / costs) is assumed, not re-taught. Cheap magic (EP22) isn't revisited. Technology (EP24), weaknesses (EP25) and immortality (EP29) are untouched: "years" appears only as one price pill.

### How EP23 varies the series rhythm

| | EP21 | EP22 | EP23 |
|---|---|---|---|
| Hook | A blank spell page | The glowing touch, questioned | **The caster writing by candlelight**, a rose glow at her hand: "EVERY SPELL TAKES A MEMORY / Which one goes?" |
| Spine | Rows answered on a parchment page | Rings spreading from one plaza | **A ledger struck one line per spell**, riding in the corner over each spell's plate |
| Turn | The sigil ignites | The last ring finds a death | **One line left, her own name**: "Worth it?" |
| Lesson | The full page | All rings on the dimmed map | The ledger lifts; price pills; "A real price makes every spell a choice." |
| CTA | Save | Share | **Comment** (the attic again, the glow still at her hand) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules haven't changed since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The YouTube title is 55/100 characters, the TikTok caption 267, and Instagram's hook line is the first 27.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). It's nine days old and the peso has been steady, so I didn't re-check it.
- Figma: the Starter plan's AI credits reset on **1 Nov 2026**, and today is 31 Oct, so I used the free local route without asking, as the brief says.
- No Runway, ElevenLabs or Creatomate keys were used. AWS credentials exist in the environment but weren't used.
- The idea: costing magic in something other than an energy pool (memories, years, senses, relationships) is standard advice in fantasy craft writing (the "limitations and costs" test, and the idea that a cost should hurt the character in a way the story cares about). The episode makes no claim about real medicine or memory loss.
- **Branch consolidation:** `claude/worldcraft-ep23` was cut from `claude/worldcraft-ep22` (EP01–EP18, EP21, EP22), then `origin/claude/worldcraft-ep19` (6ce9c1b) and `origin/claude/worldcraft-ep20` (8a55f3f) were merged into it, in that order. Both merges conflicted only in additions: `README.md`, `docs/COSTS.md`, `docs/DISTRIBUTION.md`, `docs/STYLE.md`, and for EP20 also `pipeline/score.py` and `src/graphics/Graphics.tsx`. Every side is kept, in episode order: EP19's `crackTick`/`sealSplit` and EP20's `chisel`/`frameOpen` sit beside EP21's and EP22's SFX, and the `COLLAPSE`, `MEMORY`, `SPELLBOOK` and `RIPPLE` registrations are all present. Git had interleaved the DISTRIBUTION caption sections, so the EP19 and EP20 sections were reinserted whole before EP21's. After the merges, `tsc` passes, `pipeline/build.sh` rebuilt ep19, ep20, ep21 and ep22, and one still each of ep19, ep20, ep21 and ep22 rendered correctly. **This branch now holds EP01–EP23, and it's the single base for EP24.**

## 2. Stack

Same stack as EP11–EP22:
- 4 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++. Both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics, all code. Every spell is drawn in code over the plates and pinned with `"local": true`.
- Kokoro `af_heart` narration.
- Synthesized score (D minor → D major) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode (`src/graphics/Ledger.tsx`):
- `memoryLedger`: the ledger card. Lines are written on cues and struck on cues (a rust stroke, the words fade to a ghost, and a mote of light drifts off). A header ring has one point per line, which dims to rust as its line is struck. `active` marks the current line, `hoverAt` makes it breathe (the choice), `liftAt`/`lift` glide it, `prices` land as pills and `lessonKicker`/`lessonText` give the lesson. Cues are absolute, so the corner copies in later shots already show earlier strikes.
- `fadingName` (`local`): a name painted on a plate that fades letter by letter.
- `recall` and `forget` SFX (`pipeline/score.py`). `recall` is the memory spell's signature (a breath, then a soft rising music-box arpeggio), reused for every spell: the hook, the storm, the fever, the sister and the last line. `forget` is the price (a dry quill stroke, one music-box note sagging as it fades, and an airy whisper rising away) and plays on every strike.
- Reused: `mendGlow` (EP22) in the new motif colour, `callout` `then` (EP14), `titleLockup`, `oversizedWord` and `ctaCard` with the default comment icon.
- Motif colour: **memory `#f3b9c8`** (pale rose), used only for the spell's light, the ledger's live points and the price pills. Everything else stays on the series palette, with rust for what's been taken.

## 3. Narration (77 words, measured 29.83 s)

> What if every spell stole one of your memories? / Wren keeps a ledger of what she still remembers. / She stills a storm. Her first snow is gone. / She breaks a fever. Her mother's name fades. / One more spell, and her sister is a stranger. / Only her own name is left. Is the next spell worth it? / Years, warmth, a sense: a real price makes every spell a choice. / Comment the strangest price someone could pay for magic.

The first pass measured 27.28 s (Kokoro reads these short sentences quickly). Rather than pad the script, I lengthened the pauses after each price (0.45 → 0.65 s), after "a stranger" (0.8 s) and after "worth it?" (1.1 s), and gave the CTA card a 2.5 s tail. That brought it to 29.83 s and lets each strike land in silence.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–3.08 | "What if every spell stole one of your memories?" | Wren writing by candlelight, a rose glow at her pen hand; "EVERY SPELL TAKES A MEMORY / Which one goes?" | The premise |
| 2 | `ledger` | 3.08–6.30 | "Wren keeps a ledger of what she still remembers." | The attic dims; the ledger card, WHAT I REMEMBER / *Wren*, its four lines written in on the words | The price, as a list |
| 3 | `storm` | 6.30–9.44 | "She stills a storm. Her first snow is gone." | Wren on a harbour wall facing the storm, rose rings out over the sea; the corner ledger strikes I | Spell I and its price |
| 4 | `door` | 9.44–12.58 | "She breaks a fever. Her mother's name fades." | A blue cottage door; rose light in its window; MAREN on the brass plate fades; the ledger strikes II | Spell II and its price |
| 5 | `sister` | 12.58–15.86 | "One more spell, and her sister is a stranger." | Her sister smiling at the garden gate; HER SISTER / *Smiling at her* → A STRANGER / *Who is she?*; the ledger strikes III | The cost made personal |
| 6 | `choice` | 15.86–19.97 | "Only her own name is left. Is the next spell worth it?" | The ledger large over the dark attic, three lines struck, *My own name* breathing; "Worth it?" | The turn: a choice |
| 7 | `lesson` | 19.97–24.52 | "Years, warmth, a sense: a real price makes every spell a choice." | The ledger lifts; YEARS · WARMTH · A SENSE · A MEMORY; MAKE IT COST / *A real price makes every spell a choice.* | The lesson |
| 8 | `cta` | 24.52–29.83 | "Comment the strangest price someone could pay for magic." | The attic, dim, the glow at her hand; CTA card with the Comment below pill; cross-fades to the hook | Comment CTA; loops |

## 5. Generated assets

- The plates, from local SDXL-Lightning (the prompts are in each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: Wren writing by candlelight, seed 7 (round 1);
  - `plates/storm.jpg`: the harbour wall and the breaking storm, seed 7 (round 1);
  - `plates/door.jpg`: the blue door with the glass panes and the blank brass plate, seed 7 (round 1);
  - `plates/sister.jpg`: her sister smiling at the garden gate, seed 11 (round 2).
- **15 candidates in two rounds:**
  - round 1, 12 images (seeds 11, 23 and 7 for each of the 4 shots). In none of the sister candidates was the sister facing Wren: they were all walking away down a lane.
  - round 2, 3 images: the sister plate was re-prompted as Wren's point of view (the sister at her gate, facing the viewer). Seed 11 smiles warmly at the camera; nobody waves, so the callout reads *Smiling at her* rather than "waving".
- **Code-drawn:** every glow and ring, the ledger and all its writing, the name on the door, the callouts, the price pills and all type. The plates show the world and the people, never a spell.
- `ep23.srt` (17 cues) and `Worldcraft_Short_E23_cover.jpg` (the hook at 1.6 s with the title).

## 6. Final video and verification

- `out/ep23.mp4` (master, 35.0 MB) and `out/ep23_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 20.2 MB): sent with SendUserFile.
- `ep23_download.mp4` (two-pass 3300k, 13.4 MB) and `ep23_player.mp4` (CRF 26, 5.9 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 29.87 s, −14.1 LUFS, true peak −1.5 dB. The download copy published on the preview page (https://claude.ai/artifact/RpqcfdbeD2QvzPicNF5oWU) was read back: byte-identical to the local file, and QA passed.
- Fixes made after inspecting the beat frames and the contact sheet:
  - "Worth it?" sat on the caption band and doubled the caption. The choice ledger now sits higher at 0.85 scale, with "Worth it?" beneath it, above the captions;
  - the lesson text ran into the caption band, so the ledger now lifts smaller (0.45), the pills sit at y 660 and the lesson at y 880;
  - the hook glow was too small to read, so its radius went from 44 to 58;
  - the corner ledger was shrunk to 0.55 so the door's window glow and the sister's face clear it. The sister plate is pushed in ×1.35 and shifted right and down so her face sits beside the ledger, not under it;
  - the writing hand on the hook plate was low (y 1420), so the attic plate is framed ×1.12 and raised 100 px (the CTA pulls back to the same framing, for the loop);
  - the door plate is pushed in ×1.4 so the 120-px brass plate, and the name on it, are readable on a phone.
- A build error came from a new SFX shadowing the score's `env` helper; it was renamed before the final build.
- **Accepted compromises:**
  - On the storm plate Wren's raised hand isn't visible (she's seen from behind, hands in front of her), so the glow sits at her chest and rings out over the sea.
  - In the sister shot the corner ledger touches the edge of her hair, and the rust A STRANGER kicker is lower in contrast over the dark gate post, though the serif line *Who is she?* reads clearly.
  - The SDXL costumes are generic (a plum wool coat, a green dress) and the cottage is generic old-European stone; the people, names and story are original.
- **Not verifiable by me:** how the narration and mix sound, including the new `recall` and `forget`. I can't hear the audio; please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `memoryLedger` | Any list being spent or lost: a caster's memories, a kingdom's treaties, a family's heirlooms; `hoverAt` for the last item at stake; `prices` for a lesson in pills |
| `fadingName` | Any name or inscription that should vanish on a plate: a forgotten god on a lintel, a disowned heir on a door |
| SFX `recall`, `forget` | Gentle magic; something taken or forgotten |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 4 stills (15 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 4 stills: about **$1.05 (₱67)**, or **$1.15 (₱73)** with one retry per still, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 23`. The AI label is ON for every platform. This is a **comment** CTA, so the pinned comments seed the game with examples (years, warmth, your shadow, your sense of taste) and ask for a price that forces a hard choice. The TikTok caption uses 🕯️ (the attic candle); no brain, skull or medical emoji.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | Wren writing, "Which one goes?" | Open on the struck ledger with one line left: "She has one memory left. Would you cast?" | Viewed vs swiped away; average % viewed |
| 2 | The sister beat | The sister smiling, re-captioned to "A stranger" | Hold on the sister for 1 s longer, with no callout, before the strike | Retention 12–16 s; rewatch rate |
| 3 | CTA | "Comment the strangest price" (plan) | "Would Wren cast again? Yes or no below." (a binary choice) | Comments per 1,000 views; share of comments that name a price vs just answer yes or no |

Also track how many comments name a price that forces a choice (not just "blood" or "mana"), which shows the lesson landed.

## 11. How to produce EP24 ("Why Doesn't Magic Replace Technology?")

1. **Base:** branch `claude/worldcraft-ep24` from `claude/worldcraft-ep23`, which now holds **all of EP01–EP23**, so no merges are needed. Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief and EP22's (`rippleMap`, which suits following an invention outward).
2. **Stills:** Figma credits reset on **1 Nov 2026**. If Figma would be clearly better, ask with AskUserQuestion before spending them (about 4 images, up to 6; plan key `team::1384938462301182142`). Otherwise use `python pipeline/local_stills.py ep24 <shots> --seeds 11 23` (add 7 for hands), `--pick`, then `plates.py --register` **and `pipeline/build.sh ep24`**. Run nothing heavy alongside, and budget a second round: this time the sister plate needed one, because SDXL painted figures walking away when a face toward the camera was wanted. Ask for "facing the viewer".
3. **Story (plan):** "If teleportation exists, why are merchants still using horses?" Consider range, reliability, cost, availability, safety and infrastructure: teleportation needs rare crystals, while horses stay cheap and dependable.
   - One idea: a side-by-side **ledger of trade-offs** (a teleport circle vs a horse caravan) could reuse `memoryLedger` rows as costs, with `prices` pills for range, reliability, cost, availability, safety and infrastructure. Or a `rippleMap` from a single teleport circle that reaches only three cities.
   - Draw the teleport effect in code (`mendGlow` with `core: false` rings, in a new motif colour), with one signature sound.
   - Scope: EP25 is weaknesses, so keep the limits economic and practical rather than tactical.
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep24`. Kokoro reads short sentences fast: expect about 27–28 s for 77 words, and plan pauses (0.6–1.1 s) where a beat should land. Check invented names in the G2P, and use `nth` for repeated words in cues.
5. Then:
   - `pipeline/build.sh ep24` → render (`--browser-executable /opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`) → `qa.py` → sheet and beat frames, including the loop tail;
   - the compat, two-pass download and player encodes, all `-c:a copy` except the compat copy, with `qa.py` on each;
   - `srt.py`, `storyboard.py`, the cover, and an 11-section brief;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
