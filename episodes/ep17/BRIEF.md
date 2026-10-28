# EP17 production brief: Why Would Anyone Support an Evil Empire?

**Series:** Worldcraft Shorts, Episode 17 / 50. Second episode of **Arc 4: Kingdoms and Power**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "If your empire is so evil, why hasn't everyone rebelled?" Topic: political legitimacy. CTA: "Share this with someone writing a one-dimensional villainous empire."
**Deliverable:** 30.0 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** a regime lasts because many ordinary people hold it up, each for an understandable reason: prosperity, stability, self-interest, fear, and the lack of any better alternative.
- **One empire, one name:** **Valdren** (on screen only, never spoken). It stays clearly cruel: the hook calls it so, the lesson says "Still cruel · still standing".
- **Seen from the ground, one supporter per reason:**
  - the farmer: safe roads and bread every winter (**Bread**, prosperity);
  - the clerk: remembers the chaos before the throne (**Order**, stability);
  - the soldier's mother: needs his wage (**The wage**, self-interest and loyalty);
  - the neighbour: keeps quiet, because complainers get a knock at night (**Fear**);
  - everyone: nobody can picture anything better (**Nothing better**, an empty pillar).
- **One shareable thought:** "A villainous empire is believable when its supporters aren't villains." On screen: *Its supporters aren't villains.*
- **Explain, never endorse; platform-safe:** fear and force are implied (a lone figure in a dark doorway, a knock on a door), never shown. No violence, no real regime's flags, salutes, uniforms or symbols, no parallel to any real state or living politics. The palace and costume are invented.
- **Scope guard (no repeats):**
  - EP16 (made in parallel, merged into this branch before the final push): formal vs actual power, the crown moving from the throne to the Granary Guild in Orvane. EP17 never asks who secretly rules; it asks why the many go along, and the throne is never entered. The one shared motif is grain: EP16 follows it to its holder, EP17's farmer only carries it as his reason (bread).
  - EP19 (collapse): the pillars all hold; nothing cracks or falls.
  - EP20 (two nations, one war) and EP14 (honour, freedom vs duty): no second nation, no dilemma.
  - EP10 (the chokepoint): no geography as the answer.

### How EP17 varies the series rhythm

| | EP13 | EP14 | EP15 | EP17 |
|---|---|---|---|---|
| Hook | Split frame, two stamps | One person re-captioned | A plain street | **The cliché:** a black palace over a stair, "VALDREN · A CRUEL EMPIRE / Still standing." |
| Spine | Mirrored plates | Verdict scale tipping | Ink chains on one plate | **A roof on pillars:** "THE EMPIRE" rises on five blank stone pillars, then four quick portraits, each tagged as a pillar (`pillarTag`) |
| Turn | The bridge replay | The scale comes level | Pull back | **The pillars are people:** each stone pillar turns into the supporter we met, and the fifth becomes an empty dashed pillar, NOTHING BETTER |
| Lesson | `mirrorLedger` | `lessonStack` | `reverseCard` | The stack lifts; *Its supporters aren't villains.* lands under it |
| CTA | Share | Comment | Follow | Share (the same palace in morning light over a busy market: ordinary life keeps it standing) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 56/100 characters, the TikTok caption 248, and Instagram's hook line is the first 26.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Six days old, so I didn't re-check it.
- Figma: the Starter plan is out of AI credits until **1 Nov 2026** (today is 28 Oct), so I used the free local route without asking, as the brief says.
- No Runway, ElevenLabs or Creatomate keys were used. AWS credentials exist but weren't used.
- The idea: that regimes rest on a mix of coercion, material benefits, habit, ideology and the lack of alternatives is a standard point in political science (legitimacy and "pillars of support" analyses). The episode applies it to an invented empire and makes no claim about any real one.

## 2. Stack

Same stack as EP11–EP15:
- 6 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++. Both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics (all code).
- Kokoro `af_heart` narration. No invented name is spoken, so there's nothing for the G2P to mispronounce.
- Synthesized score (D minor → D major) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode:
- `pillarStack` (`src/graphics/Pillars.tsx`): an entablature with a rust label on stone pillars that rise on a cue. `peopleAt[i]` turns pillar i into a portrait cut from a plate (`src`, plate point, `zoom`) with its reason, or an `empty` dashed pillar. `liftAt` shrinks the stack up and a two-line lesson lands beneath.
- `pillarTag` (same file): a `tag` with a pillar glyph and numeral.
- `pillarSet` and `doorKnock` SFX.
- Merged in from EP16 (`0713436`) before the final push. Both branches had added a `src/graphics/Power.tsx`, so EP16's keeps that name and EP17's pillar graphics live in `src/graphics/Pillars.tsx`; docs, README rows and SFX keep both sides.
- Merged in from EP14 (finished, `b874755`): its plates, brief, srt, cover and docs. The only conflict was `docs/DISTRIBUTION.md`, where git interleaved the EP14 and EP15 caption sections; both are kept whole, in episode order. After the merge `tsc` passes and one still each of ep14 and ep15 renders correctly.

## 3. Narration (74 words, measured 30.02 s)

> If your empire is so evil, why hasn't everyone rebelled? / Ask the people holding it up. / The farmer gets safe roads, and bread every winter. / The clerk remembers the chaos before the throne. / The soldier's mother needs his wage. / The neighbour keeps quiet. Complainers get a knock at night. / And nobody can picture anything better. / A villainous empire is believable when its supporters aren't villains. / Share this with someone writing a one-dimensional villainous empire.

It measured 30.02 s on the first pass, so nothing needed cutting. Every supporter line starts with "The…", which gives the four portraits the same beat as the pillars.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.02 | "If your empire is so evil, why hasn't everyone rebelled?" | Black spired palace above a long stair; "VALDREN · A CRUEL EMPIRE / Still standing." | The cliché, and the question |
| 2 | `ask` | 4.02–5.96 | "Ask the people holding it up." | Palace dimmed; "THE EMPIRE" roof; five stone pillars rise under it | The structure |
| 3 | `farmer` | 5.96–9.18 | "The farmer gets safe roads, and bread every winter." | Farmer walking with an ox carrying grain sacks; PILLAR I · BREAD / *The farmer* | Prosperity |
| 4 | `clerk` | 9.18–11.86 | "The clerk remembers the chaos before the throne." | Old clerk reading in a records hall; PILLAR II · ORDER / *The clerk* | Stability |
| 5 | `mother` | 11.86–14.06 | "The soldier's mother needs his wage." | A mother in a lit doorway with a small purse; PILLAR III · THE WAGE / *The soldier's mother*; coin | Self-interest |
| 6 | `neighbour` | 14.06–17.56 | "The neighbour keeps quiet. Complainers get a knock at night." | An old man half hidden in a dark doorway; PILLAR IV · FEAR / *The neighbour*; three muffled knocks | Fear, implied |
| 7 | `lesson` | 17.56–24.66 | "And nobody can picture anything better. A villainous empire is believable when its supporters aren't villains." | The pillars turn into the four supporters (BREAD, ORDER, THE WAGE, FEAR); the fifth becomes an empty dashed pillar (NOTHING BETTER); the stack lifts; STILL CRUEL · STILL STANDING / *Its supporters aren't villains.* | Reveal and lesson |
| 8 | `cta` | 24.66–30.02 | "Share this with someone writing a one-dimensional villainous empire." | The palace in morning light over a busy market; CTA card, Share pill; cross-fades to the grey hook | Share CTA; loops |

Motif: no new colour. Rust is the empire's name on the entablature; ember marks the reasons; the empty pillar is mist.

## 5. Generated assets

- The plates, from local SDXL-Lightning (prompts in each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: the palace over the stair, seed 11 (round 2);
  - `plates/farmer.jpg`: the farmer and his ox, seed 11 (round 2);
  - `plates/clerk.jpg`: the clerk, seed 23;
  - `plates/mother.jpg`: the mother in her doorway, seed 11;
  - `plates/neighbour.jpg`: the night street, seed 11;
  - `plates/cta.jpg`: the palace over the morning market, seed 11 (round 2).
- **18 candidates in two rounds:**
  - round 1, 12 images: both hook palaces and one market palace read as real tiered temples (the prompt's "stacked terraces"), the farmer was tiny or missing, and the road was dirt. The clerk, mother and neighbour were kept.
  - round 2, 6 images: an invented gothic basalt palace with thin spires (hook and CTA match), and a farmer at mid-frame.
- **Code-drawn:** the pediment, the pillars and their portraits, the empty pillar, all type.
- `ep17.srt` (16 cues) and `Worldcraft_Short_E17_cover.jpg` (the hook at 3.6 s with the title).

## 6. Final video and verification

- `out/ep17.mp4` (master, 35.7 MB) and `out/ep17_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 20.7 MB): sent with SendUserFile.
- `ep17_download.mp4` (two-pass 3300k, 13.4 MB) and `ep17_player.mp4` (CRF 26, 6.7 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 30.04 s, −14.1 LUFS, true peak −1.5 dB (the compat copy, whose AAC is re-encoded, measures −1.4 dB). The download copy published on the preview page was read back and QA'd as well (see the page's Checks).
- Fixes made after inspecting the beat frames and the contact sheet:
  - the pillars' rise used a back-ease overshoot, so a rising pillar briefly covered "THE EMPIRE"; it now eases out with no overshoot;
  - the lifted stack was too small to read the reasons, so it now lifts to 70 % (was 62 %) and the lesson sits lower;
  - the lesson line arrived only about 2 s before the CTA dissolve; it now lands on "empire" in L8;
  - the empty pillar's dashed outline was faint; it's now mist, 3 px, fully opaque;
  - the mother's tag grazed her hair; the plate is lowered 60 px (at 1.08–1.11 scale, so no edge shows).
- **Accepted compromises:**
  - The farmer's road is a dirt track, not paved; the "safe roads" are carried by the narration.
  - The neighbour plate shows him in a doorway rather than behind a shutter, and has no lantern down the street; dark and watchful is enough for "keeps quiet".
  - The SDXL costumes are generic old-European (coats, shawls, straw hat), not strongly invented. The palace, the empire and the story are original; no plate shows a real place, people or regime.
  - The clerk's ledgers carry SDXL's lettering-like squiggles on the pages; none of it is readable.
- **Not verifiable by me:** how the narration and mix sound, including the new `pillarSet` and `doorKnock`. I can't hear the audio; please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `pillarStack` | Anything held up by several supports: a regime's pillars (EP17), what keeps a guild, a religion or a trade route alive; empty pillars for missing pieces; EP19 could reuse it with pillars cracking one by one |
| `pillarTag` | Numbering parts of a system as we meet them |
| SFX `pillarSet`, `doorKnock` | Stone set in place; menace by implication |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 6 stills (18 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 6 stills: about **$1.35 (₱86)**, or **$2.48 (₱157)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 17`. The AI label is ON for every platform. The pinned comments ask viewers to name one ordinary supporter of their own empire and the reason they'd give, which turns the lesson into the comment game.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The palace and the question | Open on the empty dashed pillar: "What's holding your empire up?" | Viewed vs swiped away; average % viewed |
| 2 | Reveal order | Portraits first, pillars become them at the end | Pillars turn into people one by one as each is named | Retention 6–20 s; rewatch rate |
| 3 | CTA | Share (from the plan) | Comment: "Name one ordinary supporter of your empire and their reason." | Shares per 1,000 views vs comments per 1,000 |

Also track how many comments give a *reason* (not just a villain), which shows the lesson landed.

## 11. How to produce EP18 ("Laws Reveal What a Society Fears")

1. Branch `claude/worldcraft-ep18` from `claude/worldcraft-ep17`, which has EP01–EP17 (EP14 finished, EP16 merged). Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief, the EP16 brief and the EP12 brief (EP12's "tradition with a dark history" is the nearest earlier story: a rule from a remembered disaster).
2. **Stills:** Figma credits reset on **1 Nov 2026**. If it's on or after that date and Figma would be clearly better, ask with AskUserQuestion first (about 4 images, up to 6). Otherwise use `python pipeline/local_stills.py ep18 <shots> --seeds 11 23`, then `--pick`, then `plates.py --register`, with nothing else heavy running (a TTS run alongside it got the first EP17 batch OOM-killed). Budget a second round; avoid words like "stacked terraces" or "tiered" for buildings, which pull SDXL towards real temples.
3. Story (plan): hook "Imagine a kingdom where lying is legal, but silence is a crime." Laws reveal what a society considers dangerous, sacred or intolerable; strange laws are believable when they come from a specific historical problem. CTA: "Invent one law that would make outsiders fear your kingdom." That's a comment CTA (`ctaCard` default icon, `button: "Comment below"`).
   - Show the law first as absurd (a magistrate fining a silent man), then trace it back to the disaster it answers (a conspiracy hatched in silence, a plague of hidden symptoms).
   - Don't repeat EP12's then/now dissolve as the spine. One idea: a law text drawn in code (never generated), with each clause lit by the fear behind it.
   - Keep it fictional and platform-safe, with no real legal system or regime iconography.
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep18`. Check names in the G2P, and use `nth` for repeated words in cues.
5. Then:
   - `pipeline/build.sh ep18` → render → `qa.py` → sheet and beat frames, including the loop tail;
   - compat, two-pass download and player encodes, all `-c:a copy`, with `qa.py` on each;
   - `srt.py`, `storyboard.py`, the cover, and an 11-section brief;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
