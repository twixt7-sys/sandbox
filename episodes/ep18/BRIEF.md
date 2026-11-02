# EP18 production brief: Laws Reveal What a Society Fears

**Series:** Worldcraft Shorts, Episode 18 / 50. Third episode of **Arc 4: Kingdoms and Power**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "Imagine a kingdom where lying is legal, but silence is a crime." Topic: law as cultural worldbuilding. CTA: "Invent one law that would make outsiders fear your kingdom."
**Deliverable:** 29.8 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** a law tells you what the society that wrote it fears. A strange law becomes believable when it answers one specific disaster.
- **One kingdom, one law:** in **Velmarch** (on screen only, never spoken), *The Law of Answers*:
  - I. Answer every question asked aloud.
  - II. To keep silent is a crime.
  - III. A lie is no crime.
- **The wound:** two hundred years ago the city fell to a plot that everyone noticed and nobody mentioned. So Velmarch outlawed silence and left lying legal: "A lie can be argued with. Silence can't."
- **Absurd first, then explained:** the law is first shown at its most absurd (a magistrate fining a man for saying nothing), then written out, and only after the origin is each clause lit with the fear behind it:
  - I ← *the question nobody asked*;
  - II ← *the night nobody spoke*;
  - III ← *silence, more than lies*.
- **One shareable thought:** "Every strange law is a scar. Find the wound." It is spoken, and shown on screen under the kicker LAWS SHOW WHAT A PEOPLE FEAR.
- **Platform-safe and fictional:** the only penalty shown is a fine ("three silver"). The plot and the fall of the city are implied by a night street of watching shutters, with no violence, weapons or bodies. There is no real legal system, courtroom iconography (no gavel, wig, scales or bench), regime symbol or flag. The law text is drawn in code; no model was asked for text.
- **Scope guard (no repeats):**
  - EP12 (a tradition from a dark origin): no then/now dissolve and no matched plates. The spine is one code-drawn document lit clause by clause, and the origin is a separate place, not the same frame centuries apart.
  - EP13 (etiquette between two cultures) and EP14 (honour, morality): one people, one law, no second culture and no dilemma.
  - EP16 (who really holds power) and EP17 (why people support an empire): the king never appears, and nobody is asked who rules or why they obey; the question is what the law *reveals*.
  - EP19 (collapse): the fall two hundred years ago is the backstory, never shown or analysed.

### How EP18 varies the series rhythm

| | EP15 | EP16 | EP17 | EP18 |
|---|---|---|---|---|
| Hook | A plain street | The throne questioned | The cliché palace | **An upside-down rule:** a silent man before an official in a crowded square, "LYING IS LEGAL / *Silence is a crime.*" |
| Spine | Ink chains on one plate | Follow the grain on a map | A roof on five pillars | **A document:** the law written on a vellum card, clause by clause with a quill sound (`lawText`) |
| Turn | Pull back | The crown moves | The pillars are people | **The clauses light up:** after the origin night (shutters lighting one by one, `glints`; "Everyone saw." re-captioned in rust "Nobody spoke."), each clause warms to ember with the fear behind it |
| Lesson | `reverseCard` | `titlePower` | Stack lifts | The card lifts; *Every strange law is a scar. Find the wound.* |
| CTA | Follow | Comment | Share | Comment (a square like the hook's, at dusk, loud and talking) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`); nothing in the last ten days suggested otherwise, so not re-researched. Title 48/100 characters; TikTok caption 237; Instagram's hook line is the first 24 characters.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Seven days old, so not re-checked.
- Figma: the Starter plan is out of AI credits until **1 Nov 2026** (today is 29 Oct), so the free local route was used without asking, as the hand-off says.
- No Runway, ElevenLabs or Creatomate keys were used. AWS credentials exist in the environment but weren't used.
- The idea: that legal codes encode a society's fears, taboos and remembered crises (laws written after a specific catastrophe, sumptuary and speech laws, oaths of disclosure) is a standard point in legal history and anthropology, and a staple of fantasy worldbuilding advice. The episode applies it to an invented kingdom and makes no claim about any real law or state.

## 2. Stack

Same stack as EP11–EP17:
- 3 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++. Both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics (all code).
- Kokoro `af_heart` narration. No invented name is spoken ("Velmarch" is on screen only), so there was nothing for the G2P to mispronounce.
- Synthesized score (C minor → C major) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode (`src/graphics/Law.tsx`):
- `lawText`: an invented law on a dark vellum card. It has a kicker and title; `clauses` write in left to right on their cues; `litAt` warms a clause to ember with a glow and shows the fear behind it (`← FEAR · …`) while unlit clauses dim. It carries a rust wax seal; `liftAt` and `lessonKicker`/`lessonText` (with optional per-line `lessonLineAt`) handle the lesson. Any law, oath, charter or treaty can reuse it.
- `glints`: watchers behind shutters, warm slits that light one by one at plate points (`local`) and dim together on a cue.
- SFX `quill` (a clause written: three nib strokes and a dot) and `clauseLight` (a clause lit: a breath of flame over a low open fifth).

## 3. Narration (78 words, measured 29.76 s)

> Imagine a kingdom where lying is legal, but silence is a crime. / Here, a magistrate fines a man for saying nothing. / Absurd? Read the law. / Two hundred years ago, the city fell to a plot that everyone noticed, and nobody mentioned. / So they outlawed silence. A lie can be argued with. Silence can't. / Laws show what a people fear. Every strange law is a scar. Find the wound. / Invent one law that would make outsiders fear your kingdom.

The first measurement was 28.86 s. Rather than add words (78 is the top of the range), I lengthened five pauses. Most of the extra time (0.45 → 0.8 s) went after "Read the law.", which gives viewers time to read the clauses.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.20 | "Imagine a kingdom where lying is legal, but silence is a crime." | A hooded man stands before a robed official in a crowded square; LYING IS LEGAL / *Silence is a crime.* | The upside-down rule |
| 2 | `fine` | 4.20–7.47 | "Here, a magistrate fines a man for saying nothing." | Punch-in (1.30→1.34) on the pair; tag FINED · THREE SILVER / *for saying nothing.*; coin | The law, absurd |
| 3 | `law` | 7.47–11.08 | "Absurd? Read the law. Two hundred years ago," | Dimmed square; vellum card VELMARCH · BY ROYAL DECREE / *The Law of Answers*; three clauses written in with quill strokes; wax seal | Read the text |
| 4 | `origin` | 11.08–15.56 | "…the city fell to a plot that everyone noticed, and nobody mentioned." | Night street; TWO HUNDRED YEARS AGO / *The quiet night*; shutters light one by one; callout THE PLOT / *Everyone saw.* → rust *Nobody spoke.* | The wound |
| 5 | `lesson` | 15.56–25.17 | "So they outlawed silence. A lie can be argued with. Silence can't. Laws show what a people fear. Every strange law is a scar. Find the wound." | The card returns over the dimmed street; II, I and III light in ember with their fears; the card lifts; LAWS SHOW WHAT A PEOPLE FEAR / *Every strange law is a scar. Find the wound.* | Turn and lesson |
| 6 | `cta` | 25.17–29.76 | "Invent one law that would make outsiders fear your kingdom." | A busy square at dusk, full of talk; CTA card, "Comment below" pill; cross-fades to the hook | Comment CTA; loops |

Motif: no new colour. Ember marks a lit clause (the fear made visible), rust marks the law's numerals and seal and "Nobody spoke."

## 5. Generated assets

- Plates, from local SDXL-Lightning (prompts in each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: the hooded man before the robed official in the square, seed 11 (round 1);
  - `plates/origin.jpg`: the shuttered night street, seed 11 (round 2);
  - `plates/cta.jpg`: the square at dusk, seed 23 (round 1).
- **13 candidates in three rounds:**
  - Round 1, 6 images: hook 11 had the confrontation, but its robes lean saffron and red; both night streets were lamp-lit alleys with no shutters, watchers or gate; cta 23 was kept, while cta 11 had a cathedral-like spire.
  - Round 2, 4 images: an invented teal-and-silver magistrate came out as women in witch hats with no silent man, and SDXL again painted lamps and no gate. The colder, shuttered street (origin 11) was kept.
  - Round 3, 3 images: a wide framing with the man's back to us; there was no tribunal at all. Round-1 hook 11 stays.
- **Script change from the stills:** no round painted an open city gate, so the gate was dropped from the story. The callout now sits at the dark far end of the street (THE PLOT), and the watchers are drawn in code (`glints`).
- **Code-drawn:** the whole law card (text, numerals, fears, seal), the window glints, all type.
- `ep18.srt` (17 cues) and `Worldcraft_Short_E18_cover.jpg` (the hook at 3.6 s with the title, rendered with captions off).

## 6. Final video and verification

- `out/ep18.mp4` (master, 34.9 MB) and `out/ep18_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 20.1 MB): sent with SendUserFile.
- `ep18_download.mp4` (two-pass 3300k, 13.3 MB) and `ep18_player.mp4` (CRF 26, 6.3 MB), both with the master's audio copied, are used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 29.78 s, −14.1 LUFS, true peak −1.5 dB. The download copy published on the preview page was read back and QA'd as well (see the page's Checks).
- Fixes made after inspecting beat frames and the contact sheet:
  - The fine shot's rust callout ran its leader straight through the silent man's face and crowded the corner logo. It is now a plain top-left tag (FINED · THREE SILVER / *for saying nothing.*).
  - The window glints were too small to read, so they're now 1.8× with a stronger halo.
  - `lawText` first crashed on frames with no `litAt` yet (Remotion's `interpolate` rejects `Infinity`). Absent cues now use `1e9`, as `pillarStack` does.
  - The hook kicker "Velmarch · lying is legal" was too wide at 40 px caps; it's now "Lying is legal", and the kingdom's name moved to the law card.
- **Accepted compromises:**
  - **The hook plate's costumes:** the official wears a mustard robe with a red sash, and some of the crowd behind are in red, with close-cropped grey heads. The architecture and dress read as generic old-Mediterranean market rather than any one real people, but the warm robes are the closest any EP18 plate comes to resembling real monastic dress. Two re-rolls toward invented teal-and-silver dress lost the scene entirely. Re-roll this plate with Figma after 1 Nov if you'd rather not ship it.
  - The official stands rather than sits at a table, so "magistrate" is carried by the narration and the tag.
  - The night street has wall lamps, which SDXL insisted on. It reads as night in an old city; the glints carry "everyone saw".
  - The CTA square is a different square from the hook's (dusk, lanterns, crowded), not the same frame; it is the "same kind of square, now loud".
- **Not verifiable by me:** how the narration and mix sound, including the new `quill` and `clauseLight`. I can't hear the audio; please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `lawText` | Any written rule lit by its reason: a law, an oath, a guild charter, a treaty's clauses (EP20 could light the same treaty clause from both sides), a prophecy's lines |
| `glints` | Watchers, a town's lit windows coming on, signal fires along a ridge, eyes in a forest |
| SFX `quill`, `clauseLight` | Writing a document; a hidden reason revealed |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 3 stills (13 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.15 (₱73)** with one retry per still, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 18`. The AI label is ON for every platform. The pinned comments ask for one law *and the disaster it answers*, which turns the lesson ("find the wound") into the comment game.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The silent man in the square, "Silence is a crime." | Open on the law card itself, clause II already lit in rust: "This law is real in one kingdom." | Viewed vs swiped away; average % viewed |
| 2 | Order | Law written first, fears revealed after the origin | Each clause lit by its fear as soon as it's written (no separate origin shot) | Retention 7–20 s; rewatch rate |
| 3 | CTA | Comment: "Invent one law that would make outsiders fear your kingdom." | Comment: "Write a strange law. Someone else guesses the wound." | Comments per 1,000 views; share of comments that name a disaster |

Also track how many comments include a *reason* (a disaster or fear) and not just a law, which shows the lesson landed.

## 11. How to produce EP19 ("How Does a Kingdom Collapse?")

1. Branch `claude/worldcraft-ep19` from `claude/worldcraft-ep18`, which has EP01–EP18. Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief and the EP17 brief (its `pillarStack` was explicitly left for EP19: pillars cracking one by one).
2. **Stills:** Figma credits reset on **1 Nov 2026**. On or after that date, if Figma would be clearly better (EP18's hook needed a scene SDXL couldn't compose), ask with AskUserQuestion first (about 4 images, up to 6; plan key `team::1384938462301182142`). Otherwise use `python pipeline/local_stills.py ep19 <shots> --seeds 11 23`, then `--pick`, then `plates.py --register`.
   - Run nothing heavy alongside it, and budget two rounds.
   - SDXL won't compose a specific two-person interaction (an official *fining* someone) or paint a gate on request, so plan scenes it can paint (a place, a crowd, one figure) and draw the key object in code.
   - Watch out for tooling: `pgrep -f local_stills.py` also matches your own wait loop; wait on the log line `wrote …/<last>.png` instead.
3. Story (plan): hook "Empires rarely fall because one person woke up and decided to be evil." Economic strain, succession crises, military overextension, corruption, environmental disasters and declining legitimacy reinforce one another until the system breaks. CTA: "Which would destroy your empire first: famine, civil war, or corruption?" That's a comment CTA (`ctaCard` default icon, `button: "Comment below"`).
   - The one idea is **feedback**: each strain makes the next worse. A loop or chain where one crack spreads beats a list of five causes.
   - `pillarStack` with pillars cracking in turn is the obvious reuse, but EP17 already used the pillars as a spine. If you reuse them, make the *cracks connecting* the new part (a crack running from one pillar into the next), not the pillars.
   - Show decline through objects and absence (an empty granary, unpaid soldiers' boots, a cracked seal), never violence. No real empire's collapse is named or mirrored.
   - Don't repeat EP18's lit document, EP16's map follow or EP17's stack-and-portraits as the spine.
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep19`. Check any spoken name in the G2P, and use `nth` for repeated words in cues.
5. Then:
   - `pipeline/build.sh ep19` → render → `qa.py` → sheet and beat frames, including the loop tail;
   - compat, two-pass download and player encodes, all `-c:a copy`, with `qa.py` on each;
   - `srt.py`, `storyboard.py`, a caption-free cover (render a still with the hook shot's `captions` off in `public/`), and an 11-section brief;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
