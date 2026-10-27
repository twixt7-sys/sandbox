# EP15 production brief: The Best Cultural Detail Is Often Invisible

**Series:** Worldcraft Shorts, Episode 15 / 50. Closes **Arc 3: Civilization and Culture**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "You can reveal an entire civilization without showing a single palace." Topic: everyday cultural behaviour. CTA: "Follow for worldbuilding details that do more than decorate a setting."
**Deliverable:** 30.3 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** everyday behaviour is the cheapest, strongest exposition. Show one ordinary habit closely, and let the audience infer the values under it. Never state them first.
- **One people, one habit:** in **Tamsry**, when neighbours quarrel, they carry one bench into the street and sit on it together until they agree.
- **The evidence chain (behaviour → what it implies → value):**
  - No judge → no one sits higher → **∴ Equals**
  - One bench → nobody walks away → **∴ The street first**
  - In the open → every neighbour sees → **∴ Peace is public**
- **One shareable thought:** "Don't explain their values. Show one habit, and let us infer them." On screen: *Show one habit → A whole people.*
- **Never a palace or a ruler:** the camera stays at street level throughout. The hook's "Just a street." is the same plain street that, after the pull-back, carries all three values.
- **Sympathetic and platform-safe:** a quarrel with no shouting or villain. The two neighbours are just stubborn, and the custom is shown as wise.
- **Scope guard (no repeats):**
  - EP04: food, greetings, the rain bowl; "small details make settings feel inhabited". EP15 uses none of those; it is a dispute custom, read for values rather than texture.
  - EP11: a funeral misread by a visitor. EP15 has no outsider and no misreading; the viewer is the one inferring.
  - EP13: a gift, and two cultures colliding. EP15 has one culture and no collision.
  - EP14 (a moral dilemma, being made in parallel): not pushed when this was written, so I couldn't read its brief. EP15 stays on custom and values, not right and wrong.
- **Real-culture check:** many real societies have community mediation customs. The shared-bench rule, the name and the clothing are invented. The SDXL plates read as a generic old European town (plaster, shutters, terracotta), not a specific people. See section 6 for this as a compromise.

### How EP15 varies the series rhythm

| | EP04 | EP11 | EP13 | EP15 |
|---|---|---|---|---|
| Hook | The grand town, then one bowl | An empty costume | Split frame, two stamps | **The anti-establishing shot:** a plain street, "NO PALACE / Just a street." |
| Spine | `detailChain` card (detail → implication) | One plate read twice (`plateLook`) | Mirrored plates | **Inferences inked onto the plate:** `inferChain` loops each clue and seals its value, one per shot |
| Turn | — | "Look again" | The bridge replay | **Pull back:** the bench shrinks into its place in the street, and the values stay pinned to it as seals |
| Lesson | `lessonStack` | Lesson peeled off the costume | `mirrorLedger` | `reverseCard` over the street the values now sit in |
| CTA | Follow | Follow | Share | Follow (the same street at dusk, the bench empty: they agreed and went home) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 59/100 characters, the TikTok caption 272 characters, and Instagram's hook line is the first 32.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Five days old, so I didn't re-check it.
- Figma: the Starter plan is out of AI credits until **1 Nov 2026** (today is 27 Oct), so I used the free local route without asking, as the brief says.
- Still no Runway, ElevenLabs or Creatomate keys. AWS credentials exist but weren't used.
- The idea itself: that showing behaviour beats stating values ("show, don't tell") is standard craft advice. The episode applies it through an invented custom and makes no claim about any real people.

## 2. Stack

Same stack as EP11–EP13:
- 3 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++. Both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics (all code).
- Kokoro `af_heart` narration. "Tamsry" → /tˈæmsɹi/ (TAM-zree), checked in the G2P.
- Synthesized score (A minor → A major) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode:
- `inferChain` (`src/graphics/Everyday.tsx`): an evidence chain inked onto the plate. A pen loop round the clue, a leader, then *seen* → *means* → ∴ *value* in an ember seal, with an optional backdrop. Seal-only mode pins a value to a point on a wide plate.
- `bench` (same file): a code-drawn timber bench (day or dusk, optional cups). In 9 street and bench candidates over three prompts, SDXL never put a bench in the middle of the road.
- `benchSet` and `inferSeal` SFX.
- Merged in from EP11: `plateLook`, `shroud`, `relook` and `local_stills.py`. `shroud` now lives in `src/graphics/Culture.tsx` beside `splitFrame` and `mirrorLedger`.

## 3. Narration (77 words, measured 30.33 s)

> You can reveal an entire civilization without showing a single palace. / In Tamsry, when neighbours quarrel, they carry one bench into the street. / They sit on it together until they agree. / No judge. Nobody here stands above a neighbour. / One bench. The street matters more than winning. / In the open. Peace is everyone's business. / Don't explain their values. Show one habit, and let us infer them. / Follow for worldbuilding details that do more than decorate a setting.

It measured 30.33 s first time, so no cuts were needed. Each inference opens with a two-word clue and a full stop ("No judge.", "One bench.", "In the open."), so Kokoro leaves a beat before the conclusion while the ink loop draws.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.80 | "You can reveal an entire civilization without showing a single palace." | A plain cobbled street, the code bench small in the road; "NO PALACE / Just a street." | The anti-establishing shot |
| 2 | `bench` | 4.80–8.84 | "In Tamsry, when neighbours quarrel, they carry one bench into the street." | A man and a woman on one wooden bench, she turned away; tag "TAMSRY · A QUARREL / One bench. Two neighbours." | The habit, close |
| 3 | `agree` | 8.84–11.54 | "They sit on it together until they agree." | Punch-in; callout "THE HABIT / sit until it's settled" | The rule of the habit |
| 4 | `judge` | 11.54–14.63 | "No judge. Nobody here stands above a neighbour." | Ink loop round the empty cobbles where a judge would stand; NO JUDGE / no one sits higher / ∴ EQUALS | Inference 1 |
| 5 | `one` | 14.63–17.56 | "One bench. The street matters more than winning." | Ink loop round the bench; ONE BENCH / nobody walks away / ∴ THE STREET FIRST | Inference 2 |
| 6 | `public` | 17.56–20.67 | "In the open. Peace is everyone's business." | The bench frame shrinks into its place in the street (`pullBack`); loop round the overlooking windows; IN THE OPEN / every neighbour sees / ∴ PEACE IS PUBLIC; seals EQUALS and THE STREET FIRST settle onto the street | Inference 3 and the pull-back |
| 7 | `lesson` | 20.67–24.96 | "Don't explain their values. Show one habit, and let us infer them." | The street, dimmed, three seals pinned; "Don't explain their values." struck in rust → SHOW ONE HABIT / *A whole people.* | Lesson |
| 8 | `cta` | 24.96–30.33 | "Follow for worldbuilding details that do more than decorate a setting." | The same kind of street at dusk, lanterns lit, the bench empty with two cups; CTA card with a Follow pill; cross-fades to the morning street | Follow CTA; loops |

Motif: no new colour. Amber ink marks the evidence and ember seals mark the inferred values. Rust appears once, on the struck "explain".

## 5. Generated assets

- The plates, from local SDXL-Lightning (prompts in each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: the morning street, seed 23;
  - `plates/bench.jpg`: the two neighbours on the bench, seed 8 (third prompt);
  - `plates/cta.jpg`: the street at dusk, seed 11.
- **12 candidates in three rounds:**
  - round 1, 6 images: no bench in any street, and the bench prompt gave three elders on a ledge or people standing;
  - round 2, 3 images: neighbours on steps and ledges, never two on one bench;
  - round 3, 3 images: seed 8 has the two on a real bench.
- **Edits:** SDXL painted a gibberish shop sign ("TNAVYNNAS") over the door in the bench plate. I painted it out with PIL, using a vertical blend of the board's own colour plus grain, so the plate carries no lettering.
- **Code-drawn:** the bench in the street and at dusk, the ink loops, the seals and all type.
- `ep15.srt` (19 cues) and `Worldcraft_Short_E15_cover.jpg` (the hook at 3.9 s, the title down).

## 6. Final video and verification

- `out/ep15.mp4` (master, 34.5 MB) and `out/ep15_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 19.9 MB): sent with SendUserFile.
- `ep15_download.mp4` (two-pass 3300k, 13.5 MB) and `ep15_player.mp4` (CRF 26, 6.6 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 30.34 s, −14.0 LUFS, true peak −1.5 dB (the compat copy, whose AAC is re-encoded, measures −14.1 LUFS and −1.3 dB). The download copy published on the preview page was read back and QA'd as well (see the page's Checks).
- Fixes made after inspecting the beat frames and the contact sheet:
  - none of the wide street shots had the bench (it was in the story, not in the plate), so I added the code `bench` to the hook, the pull-back, the lesson and the CTA;
  - the agree callout ran off the left edge, so it's shorter ("sit until it's settled") and centred above the pair;
  - the second chain ran off the right edge, so all three chains now hang top-centre over a soft backdrop, with only the loops on the plate;
  - the first "no judge" loop circled a window. It now circles the empty cobbles beside the bench, where a judge would stand;
  - the CTA's first line wrapped, so the card is now three lines at size 72;
  - the "PEACE IS PUBLIC" seal collided with the lesson card, so it moved below its pin;
  - the amber kickers were faint over bright plaster, so they're bolder (34 px, 800) with a stronger backdrop;
  - the street bench read as a pale plank, so it's larger and darker.
- **Accepted compromises:**
  - The plates look like a generic old European town (plaster, shutters, terracotta) rather than a strongly invented one; SDXL's clothing is generic too. The custom, name and story are original, and no plate shows a recognisable real place or people.
  - In the bench shots the woman's face is lifted to about y 1100, above the caption band; her chest sits behind the captions.
  - During the pull-back's first ~0.3 s, the full-frame bench picture covers the corner logo before it shrinks. This is how `pullBack` worked in EP08.
  - The street bench sits at y ≈ 1480, in the bottom zone that platforms overlay. It's decorative, and the seal and leader that name it sit higher.
- **Not verifiable by me:** how the narration and mix sound, including the new `benchSet` and `inferSeal`. Please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `inferChain` | Any "read the world from a clue": a ruin's purpose, a map detail, a costume, a law; Arc 4's "who really rules" (follow the grain cart, ∴ the merchant guild) |
| `inferChain` seal-only mode | Pinning conclusions onto a wide plate or map after a pull-back |
| `bench` | Street furniture the image model won't place, at day or dusk |
| SFX `benchSet`, `inferSeal` | Wooden objects set down; every "therefore" moment |
| PIL paint-out of generated lettering | Any SDXL plate that sneaks in text |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 3 stills (12 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 15`. The AI label is ON for every platform. The pinned comments ask viewers for one everyday habit from their world and promise to read the culture from it, turning the lesson into the comment game.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The plain street, "NO PALACE / Just a street." | Open on the two sulking neighbours with the same line | Viewed vs swiped away; average % viewed |
| 2 | Chain reveal | Clue and conclusion on screen together (seen → means → seal) | Seal only, with the loop; let the narration carry the "means" | Retention 11–20 s; rewatch rate |
| 3 | CTA | Follow (from the plan) | Comment: "Give us one habit from your world; we'll read the culture." | Follows per 1,000 views vs comments per 1,000 |

Also track how many comments give a habit *and* a value it implies. That shows the inference idea landed, not just the image.

## 11. How to produce EP16 ("Who Really Rules Your Kingdom?", opens Arc 4: Kingdoms and Power)

1. Branch `claude/worldcraft-ep16` from `claude/worldcraft-ep15` (which has EP11–EP13 and EP15, and EP14 if it was pushed in time; check `git log` for the EP14 merge and merge `claude/worldcraft-ep14` first if it's missing). Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief and the EP10 brief (EP10's map zoom and palace are the nearest earlier power story).
2. **Stills:** Figma credits reset on **1 Nov 2026**. If it's on or after that date and you want Figma's better invented costumes, ask with AskUserQuestion first (about 4 images, up to 6). Otherwise use `python pipeline/local_stills.py ep16 <shots> --seeds 11 23`, then `--pick`, then `plates.py --register`, with no Remotion running while it does. Expect SDXL to ignore key objects; budget a third prompt round and draw small props in code.
3. Story (plan): hook "The king wears the crown. But who controls the food supply?" Separate formal authority from actual power: merchants, priests, generals, landowners, or whoever controls an essential resource. CTA: "Who would secretly control your fictional kingdom?" This is a comment CTA (`ctaCard` default icon, `button: "Comment below"`).
   - Arc 4 finally shows a palace. Invert EP15: open on the throne, then follow one essential thing (a grain cart, a water key, a ledger) out of the palace to whoever really holds it.
   - `inferChain` fits "follow the evidence" (∴ THE GRANARY GUILD), but don't repeat EP15's three identical chains. Use one, or put the chain on a map (`atlas`) along the grain route.
   - Don't repeat EP10's bridge chokepoint as the answer. Power here is a person or institution, not a geography.
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep16`. Check names in the G2P, and use `nth` for repeated words in cues.
5. Then:
   - `pipeline/build.sh ep16` → render → `qa.py` → sheet and beat frames, including the loop tail;
   - compat, two-pass download and player encodes, all `-c:a copy`, with `qa.py` on each;
   - `srt.py`, `storyboard.py`, the cover, and an 11-section brief;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
