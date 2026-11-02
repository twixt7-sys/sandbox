# EP14 production brief: Give Every Nation a Different Definition of Honor

**Series:** Worldcraft Shorts, Episode 14 / 50. Fourth episode of **Arc 3: Civilization and Culture**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "What if two honorable people could consider each other evil?" Topic: conflicting moral systems. CTA: "Which matters more: personal freedom or collective responsibility?"
**Deliverable:** 29.8 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** a moral conflict feels real when both sides are right about something. One people prizes individual freedom, another collective duty. Each has a reason you can respect, and each calls the other heartless.
- **One example:** one person, one choice, two verdicts.
  - **Mira** (the only name) keeps watch on the river levee that protects her valley. She swore the oath at sixteen, and now she walks away from it, leaving the horn on the post.
  - **The free towns:** that's courage. *No one should own your life*, not even a promise made as a child.
  - **The valley league:** that's betrayal. *The levee she guarded keeps everyone alive*; it only holds because everyone holds it.
  - **The turn:** each side calls the other heartless, and both are right about something.
- **One shareable thought:** "Give both sides real reasons, and let neither be entirely right."
- **Neither side is a villain:** the free town is shown welcoming her, the league as a line of neighbours walking the levee together in the rain. Nobody is punished, and no one is hurt; the consequence is an object, the horn left hanging on an empty post.
- **Scope guard:**
  - EP13 was etiquette (what's polite, the gift). EP14 is morality (what's right): a sworn duty broken for a free life. No gift, no taboo, no insult.
  - Not EP11's funeral, EP12's festival or EP13's Adren and Vesk. Nothing about empire (EP17) or war memory (EP20).
- **Real-culture check:** freedom-vs-duty is a universal tension, and both peoples are invented: the levee league, the free towns, the horn oath. The dress is generic (a rust travelling cloak, slate hooded capes, patchwork tunics). The town plate reads as a generic sunny hill town, not a specific place.

### How EP14 varies the series rhythm

| | EP11 | EP13 | EP14 |
|---|---|---|---|
| Hook | The thing dismissed (an empty costume) | Split frame, both stamps | **One person, two verdicts:** a callout on Mira reads THE FREE TOWNS / *Hero.*, then the note is struck through and HER VALLEY / *Traitor.* rises in rust on "evil" |
| Spine | The same plate, re-graded | Mirrored plates | **A verdict scale** (FREEDOM / DUTY) carried across two plates: it drops to FREEDOM, "Courage.", in the free town, then tips to DUTY, "Betrayal.", on the levee |
| Turn | "Look again" wipe | The exchange replayed on each person | The scale over the empty post: both pans flash "Heartless.", then the beam comes **level** and both pans glow with their reasons ("No one owns you." / "Everyone needs you.") |
| Lesson | Peeled stack | Mirror ledger | `lessonStack`: "Give both sides real reasons." ↓ "Let neither be entirely right." |
| CTA | Follow | Share | **Comment:** the question, over the empty post at dusk (the rust cloth tied to it); loops to Mira at dawn |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The YouTube title is 68/100 characters, the TikTok caption 253, and Instagram's hook line is the first 32.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Five days old, so I didn't re-check it.
- **Figma:** I created the design file "Worldcraft Shorts EP14 plates" in your drafts (plan `team::1384938462301182142`; it's empty). `create_session` and the one `generate_image` attempt were both **blocked by this session's automatic permission check**, which treats a paid generation as a real-world transaction. The call never reached Figma, so I couldn't confirm whether credits were available (EP11 found the plan out until 1 Nov). No credits were used. Per your instruction ("do what we did in the ep 11 session if there arent any tokens for figma"), I used the free local route instead.
- Still no Runway, ElevenLabs or Creatomate keys. AWS credentials exist but weren't used.
- The idea itself: the pull between individual liberty and collective obligation is a long-standing theme in moral philosophy and cross-cultural psychology (individualism vs collectivism). The episode only uses it through an invented example and makes no claim about any real people.

## 2. Stack

Same stack as EP06–EP13:
- 4 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920);
- Remotion graphics (all code);
- Kokoro `af_heart` narration ("Mira" → /mˈIəɹə/, MEER-uh, checked in the G2P);
- synthesized score (E minor → E major) and SFX;
- `qa.py` plus a contact sheet and beat frames.

New in this episode:
- `verdictScale` and `watchPost` (`src/graphics/Morality.tsx`);
- `callout` `then: {label, note, color, at}` (a re-caption on a cue) and `noteSize`;
- `scaleTip` SFX;
- merge housekeeping: EP11 and EP13 had each added `src/graphics/Culture.tsx`. EP13's stays, and EP11's `shroud` moved to `src/graphics/Rites.tsx`.

Local generation notes: this time about **50 s per image**, not EP11's 2.5 min. The first run asked for 4 shots × 2 seeds in one process and died silently at its first denoising step, probably from the memory limit. One shot per process (peak about 13 GB) worked every time. So run `local_stills.py epNN <one shot>` at a time, and don't wait on it with `pgrep -f local_stills`, which matches its own shell.

## 3. Narration (75 words, measured 29.81 s)

> What if two honorable people could consider each other evil? / Mira walks away from the oath she swore at sixteen. / In the free towns, that's courage. No one should own your life. / In the valley league, it's betrayal. The levee she guarded keeps everyone alive. / Each side calls the other heartless. Both are right about something. / Give both sides real reasons, and let neither be entirely right. / Which matters more: personal freedom, or collective responsibility?

The first measurement was 29.6 s. The hook's pause went from 0.55 to 0.8 s so "Traitor." holds on screen for about 1.3 s before the cut.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–3.90 | "What if two honorable people could consider each other evil?" | Dawn river path, Mira in a rust cloak walking away, the post and horn beside the path; callout THE FREE TOWNS / *Hero.* → struck through → HER VALLEY / *Traitor.* (rust) | One choice, two verdicts |
| 2 | `choice` | 3.90–7.13 | "Mira walks away from the oath she swore at sixteen." | Punch-in (1.3×) on Mira and the horn; tag MIRA / leaves her post.; callout THE OATH / sworn at sixteen | The dilemma, concretely |
| 3 | `free` | 7.13–10.80 | "In the free towns, that's courage. No one should own your life." | Mira walks into a sunlit town with townsfolk ahead; tag THE FREE TOWNS / Your life is yours.; the scale drops to FREEDOM: *Courage.* | Moral system 1 |
| 4 | `league` | 10.80–15.79 | "In the valley league, it's betrayal. The levee she guarded keeps everyone alive." | Rain; a line of hooded villagers along the levee; tag THE VALLEY LEAGUE / We hold it together.; the scale tips to DUTY: *Betrayal.* (rust) | Moral system 2, equally sympathetic |
| 5 | `both` | 15.79–19.90 | "Each side calls the other heartless. Both are right about something." | The empty post at dusk, dimmed; both pans "Heartless." (rust); the beam levels and glows: "No one owns you." / "Everyone needs you." | Neither is a villain |
| 6 | `lesson` | 19.90–24.32 | "Give both sides real reasons, and let neither be entirely right." | The levee line, dimmed; stack "Give both sides real reasons." ↓ "Let neither be *entirely right.*" | Lesson |
| 7 | `cta` | 24.32–29.81 | "Which matters more: personal freedom, or collective responsibility?" | The empty post at dusk with the horn and a rust cloth; CTA card, "Comment below" pill | Comment CTA; loops to the hook |

Motif: no new colour. Mira's rust cloak and the brass horn are the recurring objects.
- Amber marks the scale and the free-town verdict.
- Rust marks "Traitor.", "Betrayal." and "Heartless."
- Ember glows on the pans when both sides are right.

## 5. Generated assets

- `plates/hook.jpg` (seed 23): Mira on a misty dawn river path. Reused by `choice`.
- `plates/free.jpg` (seed 52, second prompt): the free town.
- `plates/league.jpg` (seed 11): the hooded line on the levee. Reused by `lesson`.
- `plates/cta.jpg` (seed 23): the empty stone-banked river at dusk. Reused by `both`.
- The prompts are in each shot's `sdxlPrompt`. Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, SDXL-Lightning under OpenRAIL++. Both allow commercial use with use-based restrictions, which this episode meets.
- 10 candidates in total, 4 kept. Rejected:
  - `hook_11`: fine, but sunset-warm; the misty dawn suits an oath at first light better.
  - `free_11`: modern wind turbines.
  - `free_23` and `free_37`: several red-cloaked figures, so Mira isn't singular.
  - `league_23`: a faint signature-like scribble.
  - `cta_11`: a cottage where the post should stand.
- **Drawn in code:** SDXL painted no watch post or horn in any seed, so the post, the brass horn and the rust cloth are `watchPost`, pinned to the hook and CTA plates.
- `ep14.srt` (15 cues) and `Worldcraft_Short_E14_cover.jpg` (the hook at 3.6 s: "HER VALLEY / Traitor.", the horn on the post).
- The Figma file "Worldcraft Shorts EP14 plates" exists but is empty.

## 6. Final video and verification

- `out/ep14.mp4` (master, 35.0 MB) and `out/ep14_compat.mp4` (H.264 Main, CRF 20, 20.4 MB): sent with SendUserFile.
- `ep14_download.mp4` (two-pass 3300k, 13.3 MB) and `ep14_player.mp4` (CRF 26, 7.2 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four files: 1080×1920, 30 fps, 29.84 s, −14.0 LUFS, true peak −1.4 to −1.5 dB.
- Fixes made after inspecting the beat frames and the sheet:
  - the rust "Betrayal." was lost over the river, so the pan words got a dark backdrop and a lighter rust;
  - "Everyone needs you." ran past x 920, so the pan text column is narrower and both reasons break over two lines on purpose;
  - the hook's verdict was too small to stop a scroll, so the note is now 96 px (`noteSize`);
  - "Traitor." held for only 1 s, so the hook's pause is longer;
  - the CTA card said "collective duty" while the voice says "collective responsibility", so the card now matches the voice.
- **Accepted compromises:**
  - The generated league villagers walk along the levee rather than visibly passing stones. The tag ("We hold it together.") carries the meaning.
  - The cloaks and capes are generic, as EP11 found with SDXL.
  - In the hook, the caption band crosses the back of Mira's hood (no face is visible).
- **Not verifiable by me:** how the narration and mix sound, including the new `scaleTip`. Please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `verdictScale` | Any weighing of two values or factions: law vs mercy, the crown vs the guilds (EP16), trade-offs in magic systems; tip it across shots, level it for "both are right" |
| `callout` `then` / `noteSize` | One subject, two readings: hero/traitor, saint/heretic, liberator/conqueror (EP17), propaganda vs truth |
| `watchPost` | Oaths, posts, signal horns, abandoned duties; anywhere a single object stands for an absent person |
| SFX `scaleTip` | Every tip of the scale or a weighing |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 4 stills (10 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (the call was blocked before it reached Figma) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 4 stills: about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 14`. The AI label is ON for every platform. The pinned comments ask viewers to pick freedom or responsibility *and* to argue the other side, or to say what each of their peoples calls the other. That puts the "both are right" lesson into practice in the comments.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | One callout re-captioned "Hero." → "Traitor." | Both verdicts at once, left and right of Mira | Viewed vs swiped away; average % viewed |
| 2 | Spine | One scale tipping across two plates | No scale; the two verdict words alone on each plate | Retention 7–16 s; rewatch rate |
| 3 | CTA | Comment: "freedom or responsibility?" | Comment: "Is Mira a hero or a traitor?" | Comments per 1,000 views; share of comments that argue both sides |

Also track how many comments defend the side they *didn't* pick. That shows the lesson landed.

## 11. How to produce EP15 ("The Best Cultural Detail Is Often Invisible")

1. Branch `claude/worldcraft-ep15` from `claude/worldcraft-ep14`, which has EP01–EP14. Read:
   - `CLAUDE.md`, `docs/STYLE.md` and `docs/SERIES_PLAN.md`;
   - this brief and the EP11 and EP13 briefs.
2. **Stills:** Figma credits reset on 1 Nov 2026. Ask before spending them (about 4 images, up to 6). The `generate_image` call may be blocked by the session's permission check: if so, say so and ask the user to allow it, or use the local route. For the local route, run `python pipeline/local_stills.py ep15 <one shot> --seeds 11 23`, **one shot per process**, then `--pick`, then `plates.py --register`. Don't run Remotion while it runs.
3. Story (plan):
   - Hook: "You can reveal an entire civilization without showing a single palace."
   - Mechanism: everyday behaviour reveals values: how strangers share food, how children address elders, how neighbours settle disputes.
   - CTA: "Follow for worldbuilding details that do more than decorate a setting." This is a Follow CTA (`ctaCard`, `button: "Follow"`).
4. Scope:
   - Don't redo EP04's single detail (the rain bowl) or EP11's funeral.
   - Pick **one ordinary scene with three small behaviours**, each revealing a value.
   - The hook can pay off "without a palace" literally: show the palace, strike it, then a kitchen or a doorstep.
5. Vary the rhythm: not a scale, not a split, not the `plateLook` wipe again.
   - One option: a slow pull-back across a single wide plate, with three `callout`s landing one by one.
   - Then a `lessonStack` naming the values.
   - `watchPost`-style object graphics can draw whatever SDXL won't paint (a shared bowl, a gesture prop).
6. Narration about 70–78 words. Measure it with `cd pipeline && python tts.py ep15`. Check names in the G2P, and use `nth` for repeated words.
7. Then:
   - `pipeline/build.sh ep15` → render → `qa.py` → sheet and beat frames (including the loop tail);
   - compat, two-pass download and player encodes (`-c:a copy`);
   - `srt.py`, `storyboard.py`, the cover, and this brief's 11 sections;
   - docs;
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push.
