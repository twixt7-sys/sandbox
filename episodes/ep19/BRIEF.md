# EP19 production brief: How Does a Kingdom Collapse?

**Series:** Worldcraft Shorts, Episode 19 / 50. Fourth episode of **Arc 4: Kingdoms and Power**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "Empires rarely fall because one person woke up and decided to be evil." Topic: political collapse. CTA: "Which would destroy your empire first: famine, civil war, or corruption?"
**Deliverable:** 29.5 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** collapse is a feedback loop. Economic strain, corruption, revolt and military overreach each make the next worse, and the loop speeds up until an ordinary event breaks a system that's already cracked. There's no villain and no single disaster.
- **One empire, one name:** **Tolmere** (on screen only, never spoken), first seen at its height.
- **The loop, one strain per plate, each line starting "So…":**
  - CRACK I · FAMINE: a bad harvest (cracked earth, a granary barn, a lone farmer seen from behind);
  - CRACK II · CORRUPTION: taxes rise and the collectors skim more (a collector over a table of coins);
  - CRACK III · REVOLT: the provinces refuse to pay (a town gate shut at dusk);
  - CRACK IV · OVERREACH: the army marches out, and feeding it empties the granaries, which closes the loop back to famine.
- **The small thing:** "Then the emperor dies with two heirs." A succession crisis that a healthy empire would survive splits the cracked seal in two (TWO HEIRS).
- **One shareable thought:** "No single crack brings down an empire. Cracks that feed each other do." On screen: NO SINGLE CRACK / *Cracks that feed each other do.*
- **Platform-safe and fictional:** unrest and war only by implication (an empty granary, a shut gate, an army seen from behind on a road, a seal breaking). No battle, weapon, body or harm. No real empire, flag or regime symbol; the seal's gate-tower device is invented.
- **Scope guard (no repeats):**
  - EP05 (ruins *after* a fall, built backward): EP19 is the *process* of falling, and no ruin appears. The CTA returns to the living capital, only dimmed.
  - EP17 (why people support an empire): legitimacy appears only implicitly, in the provinces refusing; nobody is asked why they obey, and there are no pillars.
  - EP16 (who really rules): no hidden holder of power. EP18 (law and fear): no law. Merged in before the final push; the two briefs don't overlap (EP18 keeps its old fall as unseen backstory).
  - EP37 (why the strongest army can still lose): the army is one strain among four. Its logistics only matter because feeding it feeds the famine; there's no battle and no morale.
  - EP10's `atlas` bridge was considered for the break (its brief suggested it could fall in EP19), but a falling bridge reads as one disaster, which is exactly the misconception this episode corrects. The loop needed a picture of *reinforcement*, so the break is the seal at the centre of the loop.

### How EP19 varies the series rhythm

| | EP16 | EP17 | EP18 | EP19 |
|---|---|---|---|---|
| Hook | The throne questioned | The cliché palace | An upside-down rule | **The empire at its height:** a golden capital, "TOLMERE · AT ITS HEIGHT / *No villain required.*" |
| Spine | Follow the grain on a map | A roof on five pillars | A law card, clause by clause | **A chain gathering speed:** four quick plates (2.0–2.8 s each), each a numbered crack, each line a "So…" |
| Turn | The crown moves | The pillars are people | The clauses light up | **The chain is a loop:** the plates become medallions round the seal, the last arrow closes in rust, a pulse runs round faster every lap, each pass cracks the seal, and "two heirs" splits it |
| Lesson | `titlePower` | Stack lifts | The card lifts | The loop lifts; *Cracks that feed each other do.* |
| CTA | Comment | Share | Comment | Comment (the same capital, drained to dusk) |

The new beat is acceleration: shots shorten through the example (5.0 → 2.4 → 2.8 → 2.2 → 2.0 s), the music pulse climbs 72 → 92 bpm, and the crack ticks bunch together as the loop spins.

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`); nothing in the last ten days suggested otherwise, so not re-researched. Title 44/100 characters; TikTok caption 296 (under 300); Instagram's hook line is the first 28 characters.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Seven days old, so not re-checked.
- Figma: the Starter plan is out of AI credits until **1 Nov 2026** (today is 29 Oct), so the free local route was used without asking, as the hand-off says.
- No Runway, ElevenLabs or Creatomate keys were used. AWS credentials exist in the environment but weren't used.
- The idea: that state collapse usually comes from several mutually reinforcing stresses (fiscal crisis, elite corruption, provincial revolt, military overextension, succession disputes, environmental shocks, lost legitimacy) rather than one cause or one bad ruler is a standard point in historical scholarship on collapse and a staple of worldbuilding advice. The episode applies it to an invented empire and makes no claim about any real one.

## 2. Stack

Same stack as EP11–EP18:
- 5 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++; both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics (all code).
- Kokoro `af_heart` narration. No invented name is spoken; "heirs" checked in the G2P (/ˈɛɹz/).
- Synthesized score (C minor → C major, pulse climbing 72 → 92 bpm) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode:
- `crackLoop` (`src/graphics/Collapse.tsx`): strain medallions cut from their plates on a ring round the empire's seal; arrows draw on cues and a rust closing arrow makes it a loop; a pulse runs round at w0·e^(k·τ) rad/s, lighting each node as it passes and adding a crack through the seal per pass; `breakAt` splits the seal in two; `liftAt` / `kickerAt` / `lessonAt` lift it and land the lesson.
- `crackTag` (same file): a `tag` with a cracked-disc glyph and numeral.
- `crackTick` and `sealSplit` SFX. The episode generator computes each tick's time from the same `w0` and `k` as the pulse, so every tick lands on a node pass.
- Merged in from EP18 (`be11236`) before the final push. The only conflicts were adjacent additions in `src/graphics/Graphics.tsx` (`COLLAPSE` and `LAW`) and `pipeline/score.py` (`crackTick`/`sealSplit` and `quill`/`clauseLight`); both sides are kept, the docs merged cleanly, and EP19's sections follow EP18's. After the merge `tsc` passes and an ep18 still (its origin shot) renders correctly.
- Environment note: the headless shell is now `/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell` (the `-1194` path in earlier notes is gone).

## 3. Narration (75 words, measured 29.52 s)

> Empires rarely fall because one person woke up and decided to be evil. / Usually, it starts with a bad harvest. / So taxes rise, and collectors skim more. / So the provinces refuse to pay. / So the army marches out, and feeding it empties the granaries. / Then the emperor dies with two heirs. / No single crack brings down an empire. Cracks that feed each other do. / Which would destroy your empire first: famine, civil war, or corruption?

The first measure was 29.33 s. The pause after "granaries" was then lengthened from 0.7 to 0.9 s so the loop has about 2 s to speed up before the split, which brought it to 29.52 s. The three "So…" lines carry the chain; "Then" marks the small thing that isn't a strain at all.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–5.05 | "Empires rarely fall because one person woke up and decided to be evil." | A golden domed capital over a river at sunset; TOLMERE · AT ITS HEIGHT / *No villain required.* | Deny the cliché |
| 2 | `harvest` | 5.05–7.49 | "Usually, it starts with a bad harvest." | Cracked path through withered wheat to a granary barn, a farmer from behind; CRACK I · FAMINE / *A bad harvest* | Strain 1 |
| 3 | `taxes` | 7.49–10.30 | "So taxes rise, and collectors skim more." | A collector over a candlelit table of coins; CRACK II · CORRUPTION / *Taxes rise*; a coin | Strain 2, fed by 1 |
| 4 | `provinces` | 10.30–12.46 | "So the provinces refuse to pay." | A town gate shut at dusk; CRACK III · REVOLT / *The provinces refuse*; a gate slam | Strain 3, fed by 2 |
| 5 | `army` | 12.46–14.49 | "So the army marches out…" | A long column winding away over bare hills; CRACK IV · OVERREACH / *The army marches* | Strain 4, fed by 3 |
| 6 | `loop` | 14.49–23.84 | "…and feeding it empties the granaries. Then the emperor dies with two heirs. No single crack brings down an empire. Cracks that feed each other do." | Four medallions round the seal of TOLMERE; the rust arrow closes OVERREACH → FAMINE; the pulse speeds up, the seal cracks on every pass; on "two" the seal splits (TWO HEIRS); the loop lifts; NO SINGLE CRACK / *Cracks that feed each other do.* | Mechanism, break, lesson |
| 7 | `cta` | 23.84–29.52 | "Which would destroy your empire first: famine, civil war, or corruption?" | The same capital drained to dusk; CTA card, *Comment below* pill; cross-fades to the golden hook | Comment CTA; loops |

Motif: no new colour. Amber arrows for the chain, rust for the arrow that closes the loop and for the split, ember for the pulse and the cracks.

## 5. Generated assets

- The plates, from local SDXL-Lightning (prompts in each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: the capital at sunset, seed 11 (also used, dimmed, under the loop and the CTA);
  - `plates/harvest.jpg`: the failed harvest, seed 23;
  - `plates/taxes.jpg`: the tax table, seed 11;
  - `plates/provinces.jpg`: the shut gate, seed 23 (round 2);
  - `plates/army.jpg`: the column on the road, seed 11.
- **13 candidates in two rounds:**
  - round 1, 10 images: hook, harvest, taxes and army kept. Neither provinces candidate showed a shut gate (one a sunset road, one an open lane).
  - round 2, 3 images (provinces only, a front-on prompt): seed 23 is a closed, centred gate with the town beyond. Seed 11 had a modern pylon in the sky, and seed 7's gate stood half open.
- **Code-drawn:** the loop, the medallion crops, the seal and its gate-tower device, the cracks and the split, all type.
- `ep19.srt` (17 cues) and `Worldcraft_Short_E19_cover.jpg` (the loop mid-spin at 17.0 s, with HOW DOES A KINGDOM / *collapse?* set in the series fonts under it).

## 6. Final video and verification

- `out/ep19.mp4` (master, 35.7 MB) and `out/ep19_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 20.8 MB): sent with SendUserFile.
- `ep19_download.mp4` (two-pass 3300k, 13.2 MB) and `ep19_player.mp4` (CRF 26, 6.4 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 29.55 s, −14.0 LUFS, true peak −1.4 dB (the download copy −1.5 dB). The download copy published on the preview page was read back and QA'd as well (see the page's Checks).
- Fixes made after inspecting the beat frames and the contact sheet:
  - the loop first rendered too small for a phone (medallions 86 px radius on a 262 px ring); it's now 106 on 282, with a 148 px seal, thicker cracks (4.5 px) and a bigger pulse head;
  - two medallion crops landed on dark corners of their plates (corruption, revolt); they're re-aimed at the collector's face and hands and at the gate, using a grid of the plate;
  - the TWO HEIRS label collided with the REVOLT medallion; it now sits inside the split seal on a dark chip;
  - after the lift, the lesson lines crowded the caption and there was a dead gap before they landed; the loop now lifts to 62 %, the kicker NO SINGLE CRACK lands on "single" and the two lines on "Cracks";
  - process note: Remotion reads the copy of `episode.json` in `public/ep19/`, which only `build.sh` refreshes, so my second and third rounds of beat stills showed stale geometry. The episode generator now writes both copies.
- **Accepted compromises:**
  - The harvest barn is a plain timber barn rather than a stone granary, and its doors don't visibly open on emptiness; the tag and the narration carry "bad harvest".
  - The army plate reads as a mounted column with round helmets, not wagons of grain; the "feeding it" link is carried by the narration and the rust arrow.
  - The collector looks more like an elderly merchant than an official; on a coin table, with "skim", it reads as corruption.
  - The gate is ornate ironwork rather than timber. Costumes and architecture are generic old-European, not strongly invented; the empire, its seal and the story are original, and no plate shows a real place, people or regime.
- **Not verifiable by me:** how the narration and mix sound, including the new `crackTick` (spaced to the pulse) and `sealSplit`. I can't hear the audio; please give it one listen, especially the tick run before the split.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `crackLoop` | Any vicious (or virtuous) circle: collapse (EP19), a feud that feeds itself (EP20's two nations), a magic system's escalating cost, an economy's boom and bust; with `breakAt` off it's a plain cycle diagram with plate medallions |
| `crackTag` | Numbering strains, causes or stages as we meet them; `word` swaps "Crack" for another noun |
| SFX `crackTick`, `sealSplit` | Strain building; a seal, pact or alliance breaking |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 5 stills (13 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 5 stills: about **$1.25 (₱79)**, or **$2.27 (₱144)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 19`. The AI label is ON for every platform. The pinned comments ask viewers to name the first crack in their empire *and the one it widens next*, which turns the lesson (reinforcement) into the comment game rather than a one-word vote.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The golden capital, "No villain required." | Open on the seal already cracked and the loop spinning: "Here's how empires actually fall." | Viewed vs swiped away; average % viewed |
| 2 | Loop reveal | Plates first, joined into the loop at the end | The loop drawn from the start, each plate popping in as its node is named | Retention 14–24 s; rewatch rate |
| 3 | CTA | The plan's three-way vote (famine, civil war, corruption) | "Name the first crack in your empire, and what it breaks next." | Comments per 1,000 views; share of comments that name a *second* strain |

Also track how many comments name a chain (two or more linked causes) rather than a single one, which shows the lesson landed.

## 11. How to produce EP20 ("Make Two Nations Enemies Without Making One Evil", closes Arc 4)

1. Branch `claude/worldcraft-ep20` from `claude/worldcraft-ep19`, which has EP01–EP19 (EP18 merged). Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief, the EP18 brief, the EP13 brief (the split frame, two cultures) and the EP14 brief (both sides sympathetic, the verdict scale).
2. **Stills:** Figma credits reset on **1 Nov 2026**. If it's on or after that date and Figma would be clearly better, ask with AskUserQuestion first (about 4 images, up to 6). Otherwise use `python pipeline/local_stills.py ep20 <shots> --seeds 11 23`, then `--pick`, then `plates.py --register`, with nothing else heavy running. Budget a second round (EP19 needed one for a shut gate). Avoid "stacked terraces" or "tiered" for buildings. Note that `pgrep -f local_stills.py` in a wait loop matches the loop's own command line; wait on the log's last "wrote" line instead.
3. Story (plan): hook "What if both kingdoms are telling the truth about the same war?" Nations remember the same events differently because of different losses, inherited stories and values. CTA: "Tag someone who loves morally complicated fantasy." That's a share-style CTA (`ctaCard` `icon: "share"`, or a tag pill).
   - One war, two memorials or two history lessons, the same event told twice, each true to what that side lost. EP13's `splitFrame` is the obvious tool, so vary it: for example one battlefield plate re-captioned twice (`callout` `then`), or two `crackLoop`-style cycles of grievance feeding each other (each side's loss becomes the other's story).
   - Don't repeat EP13 (etiquette between cultures) or EP14 (one person's verdict re-read). As Arc 4's closer, it can glance back at power, legitimacy and collapse, but the subject is memory.
   - Keep it fictional and platform-safe: no real conflict, flags or atrocity parallels; war shown through memorials, empty places and objects, never violence.
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep20`. Check names in the G2P and use `nth` for repeated words in cues. If you edit `episode.json` after `build.sh`, copy it into `public/ep20/` too (Remotion reads that copy).
5. Then:
   - `pipeline/build.sh ep20` → render → `qa.py` → sheet and beat frames, including the loop tail;
   - compat, two-pass download and player encodes, all `-c:a copy`, with `qa.py` on each;
   - `srt.py`, `storyboard.py`, the cover, and an 11-section brief;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
