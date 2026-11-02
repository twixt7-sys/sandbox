# EP21 production brief: The Three Questions Every Magic System Needs

**Series:** Worldcraft Shorts, Episode 21 / 50. Opens **Arc 5: Magic and Its Rules**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "Before inventing a spell, answer these three questions." Topic: magic-system design. CTA: "Save this before designing your next magic system."
**Deliverable:** 29.95 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** before writing a spell, answer three questions. What can it do (capabilities)? What stops it from doing everything (limitations)? What does using it cost (consequences)? Together, the answers start generating story on their own.
- **One invented magic, answered through all three:** mending.
  - **Can:** menders fix anything broken.
  - **Can't:** only what they touched before it broke.
  - **Costs:** each mend cracks something they own.
  - **The story writes itself:** the queen's crown shatters, and the only mender who ever held it is a thief. Three plot questions follow, one from each answer: *Why did a thief hold it?* (can't), *Will she mend it?* (can), *What cracks at home?* (costs).
- **One shareable thought:** "Can. Can't. Costs. Answer all three before your first spell."
- **Magic is drawn in code, never painted:** the plates show the world and the caster (the workshop, a jar, a wheel, a window, a crown, a thief). The crack, the light that knits it, the failed mend and the price are all `mendSeam` over the plate, pinned with `"local": true`. One signature sound for the magic, `mendKnit`, is reused every time it works, including when the sigil ignites.
- **Scope guard: this is the framework episode.** Each question is touched once and lightly:
  - EP22 (cheap magic breaks society): no talk of what mending would do to a whole economy;
  - EP23 (creative costs, "every spell steals a memory"): the cost is deliberately *not* a memory. It's a physical, plot-making price (a crack moves into your own home), shown once;
  - EP24 (magic vs technology): nothing about carts or replacing craftsmen;
  - EP25 (weaknesses that make casters interesting): the limit is stated once, as a rule, without exploring tactics.
- **Platform-safe:** no violence. The "thief" is a hooded silhouette with her face hidden. No real-world religious symbols: the sigil is a plain ring with an inscribed triangle and three nodes, standing for the three questions.

### How EP21 varies the series rhythm

| | EP15 | EP16 | EP17 | EP21 |
|---|---|---|---|---|
| Hook | A plain street | The throne, questioned | The cliché palace | **A blank form:** an empty spell page with three numbered lines over a workshop full of broken things |
| Spine | Ink chains on one plate | Follow the crown on a map | A roof on pillars, one portrait each | **The form fills in:** the page rides top-left while each question gets a plate and an inked answer (mend works / mend fails / the price cracks her window) |
| Turn | Pull back | The crown flies | The pillars are people | **The answers write a plot:** the crown shatters; the only mender who held it is a thief; one story-question chip per answer |
| Lesson | `reverseCard` | `titlePower` | Lifted stack | The full page returns and its sigil ignites only when all three rows are lit: "Can. Can't. Costs." |
| CTA | Follow | Share | Share | **Save** (first in the series: a bookmark pill), over the workshop in morning light |

EP18–EP20 were made in parallel. EP18 ("Laws Reveal What a Society Fears", a law card drawn in code) finished and is merged into this branch; its dark vellum `lawText` and EP21's light parchment `spellPage` are deliberately different looks. EP19 and EP20 were still WIP at the final push (EP19 has `crackLoop`/`crackTag`; EP21's cracks are a separate component, `mendSeam`, and are mended or moved, never a collapse).

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 56/100 characters, the TikTok caption 217, and Instagram's hook line is the first 18. `#MagicSystem` replaces the arc-specific tag.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Seven days old, so I didn't re-check it.
- Figma: the Starter plan is out of AI credits until **1 Nov 2026** (today is 29 Oct), so I used the free local route without asking, as the brief says.
- No Runway, ElevenLabs or Creatomate keys were used. AWS credentials exist but weren't used.
- The idea: the "what it can do / what it can't / what it costs" frame is common craft advice for fantasy magic systems (for example the widely cited "limitations are more interesting than powers" principle). The episode states it in its own words and example; the mending magic is invented.

## 2. Stack

Same stack as EP11–EP17:
- 6 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++. Both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics (all code).
- Kokoro `af_heart` narration. No invented names are spoken ("menders" is an ordinary word).
- Synthesized score (F minor → F major) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode (`src/graphics/Spellbook.tsx`, a file for Arc 5):
- `spellPage`: the blank spell page, its three rows, the three-point sigil and the lesson line;
- `mendSeam`: a crack that opens, is mended by light, fails to mend (`fail`), or just appears as a price;
- `storyQuestions`: plot questions, each badged with the answer that raised it;
- `ctaCard` `icon: "save"`: a bookmark pill for save CTAs;
- SFX `mendKnit` (signature), `mendFizzle`, `costCrack`.
- Merged in from EP18 (finished, `be11236`) before the final push. Conflicts were all side-by-side additions, and both sides are kept: `LAW` and `SPELLBOOK` in `Graphics.tsx`, EP18's `quill`/`clauseLight` and EP21's SFX in `score.py`, and both sections in README, STYLE, COSTS and DISTRIBUTION (DISTRIBUTION is EP18's file with the EP21 section appended). After the merge `tsc` passes, and one still each of ep18 (frame 300, the law card) and ep21 (frame 700, the lesson page) renders correctly. EP19 and EP20 had only WIP commits, so they weren't merged.

## 3. Narration (78 words, measured 29.93 s)

> Before inventing a spell, answer these three questions. / One: what can it do? Menders fix anything broken. / Two: what stops it? Only what they touched before it broke. / Three: what does it cost? Each mend cracks something they own. / Then the queen's crown shatters. / The only mender who ever held it? A thief. / Three answers, and the story writes itself. / Can. Can't. Costs. Answer all three before your first spell. / Save this before designing your next magic system.

The first measured pass came in at 29.93 s, so nothing needed cutting. The "One / Two / Three" openings give the three example shots the same beat as the page's numerals.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–3.50 | "Before inventing a spell, answer these three questions." | The mender's workshop, dimmed; a blank spell page (A NEW SPELL, an empty title line, I · II · III empty lines, an unlit sigil); the numerals pulse on "three" | The promise |
| 2 | `can` | 3.50–6.79 | "One: what can it do? Menders fix anything broken." | The page glides to the top-left; a cracked fish jar; light runs up the crack and leaves a lilac seam; row I writes CAN · *Mend anything broken.* and the title *Mending* | Capabilities |
| 3 | `cant` | 6.79–10.33 | "Two: what stops it? Only what they touched before it broke." | A stranger's broken cart wheel in a dusk lane; the mend light starts, gutters to rust and dies; row II CAN'T · *Only what you touched before it broke.* | Limitations |
| 4 | `cost` | 10.33–14.04 | "Three: what does it cost? Each mend cracks something they own." | Her cottage window at night; a crack races across the panes on "cracks"; row III COSTS · *Each mend cracks something you own.* | Consequences |
| 5 | `crown` | 14.04–15.86 | "Then the queen's crown shatters." | A jeweled crown on a velvet cushion; fractures burst across it; tag THEN / *The queen's crown.* | The answers make a plot |
| 6 | `thief` | 15.86–21.64 | "The only mender who ever held it? A thief. Three answers, and the story writes itself." | A hooded thief on a moonlit rooftop; tag WHO EVER HELD IT / *A thief.*; three ember chips: II *Why did a thief hold it?* I *Will she mend it?* III *What cracks at home?* | The twist, and the story questions |
| 7 | `lesson` | 21.64–25.63 | "Can. Can't. Costs. Answer all three before your first spell." | The full page over the dimmed workshop; rows flash and the sigil's nodes light on "Can.", "Can't.", "Costs."; the sigil ignites; *Answer all three / before your first spell.* | The lesson |
| 8 | `cta` | 25.63–29.95 | "Save this before designing your next magic system." | The workshop in a warm morning grade, reframed so the mender sits clear of the type; CTA card, *Save this* bookmark pill; cross-fades to the hook | Save CTA; loops |

Motif colour: **mend light, lilac-white `#d6c2ff`** (deeper `#5b47a0` for the lit sigil strokes on parchment). The page is parchment with ink and rust labels; everything else stays on the series palette.

## 5. Generated assets

- The plates, from local SDXL-Lightning (prompts in each shot's `sdxlPrompt`), all from round 1:
  - `plates/hook.jpg`: the mender at her bench among broken pottery, seed 23 (also used for the lesson and the CTA);
  - `plates/can.jpg`: the fish jar, seed 11;
  - `plates/cant.jpg`: the wheel in the lane, seed 11;
  - `plates/cost.jpg`: the cottage window and table, seed 11;
  - `plates/crown.jpg`: the crown on its cushion, seed 23;
  - `plates/thief.jpg`: the hooded thief on the rooftop, seed 11.
- **12 candidates in one round**, so the budgeted second round wasn't needed. Rejected: hook 11 (the mender's face sat by the corner logo), can 23 (smaller jar), cant 23 (a better broken cart, but the wheel was too small to carry the crack), cost 23, crown 11 (the crown filled the frame edge to edge), thief 23 (crouching, with her face visible).
- **Code-drawn:** the spell page and sigil, every crack and mend, the story chips, and all type.
- `ep21.srt` (21 cues) and `Worldcraft_Short_E21_cover.jpg` (the hook at 3.1 s: the blank page, "questions").

## 6. Final video and verification

- `out/ep21.mp4` (master, 35.3 MB) and `out/ep21_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 20.4 MB): sent with SendUserFile.
- `ep21_download.mp4` (two-pass 3300k, 13.4 MB) and `ep21_player.mp4` (CRF 26, 6.1 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 29.95 s, −14.1 LUFS, true peak −1.4 dB (the compat copy, whose AAC is re-encoded, measures −1.3 dB). The download copy published on the preview page was read back and QA'd as well (see the page's Checks).
- Fixes made after inspecting the beat frames and the contact sheet:
  - the corner page was unreadable at 0.56 scale; it's now 0.7;
  - the cracks on the wheel and the crown were too thin to see; they're wider, and the jar and window cracks moved right, clear of the bigger page;
  - the failed mend was a barely visible dot; the light now travels 60 % of the crack (was 40 %) before it gutters to rust;
  - the ignited sigil was lilac on parchment and hard to see; lit strokes are now a deeper violet with a lilac glow;
  - the lesson line arrived only about 1.5 s before the CTA dissolve; it now lands just after "Costs.";
  - the CTA title ran over the mender's head; the CTA plate is reframed (1.25×, shifted right and down, margins wider than the shift).
- **Accepted compromises:**
  - The broken-wheel plate has no traveller (SDXL dropped him in both seeds); the narration carries "a stranger's".
  - The wheel isn't visibly broken in the plate; the code-drawn crack is the break.
  - The lesson's on-screen line repeats the caption under it, as in earlier lessons.
  - The SDXL dress is generic (an indigo apron, a hooded cloak); the magic, the rules and the story are original. No plate shows a real place, people or symbol.
- **Not verifiable by me:** how the narration and mix sound, including the new `mendKnit`, `mendFizzle` and `costCrack`. I can't hear the audio; please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `spellPage` | Any rule set filled in line by line: EP22's consequences, EP23's costs, EP25's weaknesses, EP47's rule audit; a law page, a contract, a recipe |
| `mendSeam` | Magic drawn on a plate (mend, fail, a price that appears); also plain cracks and shattering |
| `storyQuestions` | Turning a rule set into plot questions on screen |
| `ctaCard` `icon: "save"` | Every save CTA (EP47 is another) |
| SFX `mendKnit`, `mendFizzle`, `costCrack` | A magic working, failing, and its price |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 6 stills (12 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 6 stills: about **$1.10 (₱70)**, or **$2.48 (₱157)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 21`. The AI label is ON for every platform. The pinned comments ask viewers to write their own magic in three lines (can / can't / costs), which turns the lesson into the comment game.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The blank page and the line | Open on the thief: "Only one mender ever held the queen's crown." then rewind to the page | Viewed vs swiped away; average % viewed |
| 2 | CTA | Save (from the plan) | Comment: "Write your magic in three lines: can, can't, costs." | Saves per 1,000 views vs comments per 1,000 |
| 3 | Example density | One magic, three plates | The page alone (no example plates), filled in faster | Retention 4–15 s; rewatch rate |

Saves are new for this series: record saves per 1,000 views on every platform as the baseline for later save CTAs (EP47). Also count comments that give all three lines, which shows the framework landed.

## 11. How to produce EP22 ("The Most Dangerous Magic Is Cheap Magic")

1. Branch `claude/worldcraft-ep22` from `claude/worldcraft-ep21`. Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief, the EP17 brief, and the EP02 storyboard (one impossible rule followed through its consequences is EP22's closest ancestor).
2. **Stills:** Figma credits reset on **1 Nov 2026**. If it's on or after that date and Figma would be clearly better, ask with AskUserQuestion first (about 4 images, up to 6). Otherwise use `python pipeline/local_stills.py ep22 <shots> --seeds 11 23`, then `--pick`, then `plates.py --register`, with nothing else heavy running. Budget a second round.
3. Story (plan): hook "If healing is free, why does anyone ever die from an injury?" Powerful magic changes society: cheap healing changes medicine; easy resurrection changes inheritance, warfare and religion. CTA: "Share this with a fantasy writer who loves overpowered magic." That's a share CTA (`icon: "share"`).
   - Pick up one row of EP21's page: take a magic whose *cost* line is empty ("Costs: nothing") and show what that does to a whole society, institution by institution (the physician's guild empties, the inheritance court is crowded…). `spellPage` can open with the COSTS row struck through or blank.
   - Draw the healing in code (a `mendSeam`-like light on skin is too close to gore: use objects and institutions, not wounds). Keep it platform-safe: no injuries shown, no real religion.
   - Don't spend EP23 (creative costs) or EP24 (technology).
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep22`. Check names in the G2P, and use `nth` for repeated words in cues.
5. Then:
   - `pipeline/build.sh ep22` → render (the headless shell is now at `/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`) → `qa.py` → sheet and beat frames, including the loop tail;
   - compat, two-pass download and player encodes, all `-c:a copy` except compat, with `qa.py` on each;
   - `srt.py`, `storyboard.py`, the cover, and an 11-section brief;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
