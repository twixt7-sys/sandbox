# EP20 production brief: Make Two Nations Enemies Without Making One Evil

**Series:** Worldcraft Shorts, Episode 20 / 50. Closes **Arc 4: Kingdoms and Power**. The series reaches 20/50.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "What if both kingdoms are telling the truth about the same war?" Topic: competing historical narratives. CTA: "Tag someone who loves morally complicated fantasy."
**Deliverable:** 30.0 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`. `episode.json` is written by [`make_ep20.py`](make_ep20.py) from the plate geometry in [`geom.json`](geom.json).

## The brief

- **One idea:** two nations can remember the same war truthfully and still be enemies, because each lost something different, inherited a different story and holds a different value sacred. Each memorial is true, and each leaves out the other side's dead.
- **One war, two invented kingdoms** (names on screen only, never spoken, so the G2P has nothing to mispronounce):
  - **Arvel**, upstream. Its stone says "They crossed the river and burned our town." True: the village by the stone is razed.
  - **Dunmere**, downstream. Its cairns say "They dammed the river and we starved." Also true.
  - Each account is factual, and each crops out the other's loss. Neither side is shown fighting, and the war isn't pinned on either.
- **One shareable thought:** "Give each side a true story and a real loss, and you'll never need a villain."
- **Platform-safe:** loss is shown only through a memorial stone, a razed village, a field of cairns, an empty valley and two lanterns. There's no battle, no bodies, no weapons, and no real nation, flag, war or symbol. The clothing question doesn't arise because no people appear, and the architecture is generic ruin.
- **Scope guard (no repeats):**
  - EP13 (one gesture, two etiquettes): no split frame; the two sides come one after the other, then share one frame.
  - EP14 (freedom vs duty): no verdict scale and no dilemma; both accounts are stamped TRUE rather than weighed.
  - EP17 (why people support an empire): no regime, and no supporters.
  - EP18 (laws and fear) and EP19 (collapse): see "Parallel episodes" below. EP20 has no law text, and nothing cracks.
  - Later topics: no single hero judged two ways (EP31), no ancient war that still kills (EP32), no causes of war (EP36: the dam is a grievance, not an analysis), no single sympathetic villain (EP39). The episode is specifically two nations' memories of one war.
- **Parallel episodes:** at the start of this session neither `claude/worldcraft-ep18` nor `claude/worldcraft-ep19` existed on the remote, so there were no briefs to read; EP20 was kept clear of their planned shapes (law text drawn in code; `crackLoop` / `crackTag`). See §6 for the state at the final push.

### How EP20 varies the series rhythm

| | EP13 | EP14 | EP17 | EP20 |
|---|---|---|---|---|
| Hook | Split frame, two stamps | One person re-captioned | The cliché palace | **The paradox:** a dawn valley with a memorial stone on each bank, "ONE RIVER · ONE WAR / Two truths." |
| Spine | Mirrored plates | Verdict scale tipping | Pillars that are people | **Two chronicles, two frames:** each side's carved tablet sits inside a gilt `chronicleFrame` that darkens the rest of the plate; TRUE is stamped on it |
| Turn | The bridge replay | The scale comes level | The empty pillar | **The frame opens:** on "Look what it leaves out", the crop widens and the camera pulls back, and a rust callout names what it cut out (downstream: *Their dead.*; upstream: *Their burned town.*) |
| Lesson | `mirrorLedger` | `lessonStack` | Stack lifts | **Both truths in one frame:** both tablets, both TRUE, over the opening valley; `truthRows` give the reasons (losses, stories, values), then ENEMIES / *Neither is evil.*; then the shareable thought, word by word |
| CTA | Share | Comment | Share | **Tag** (the same valley at dusk, a lantern lit at each nation's stone: both sides mourn) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 61/100 characters, the TikTok caption 230, and Instagram's hook line is the first 24.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Seven days old, so I didn't re-check it.
- Figma: the Starter plan is out of AI credits until **1 Nov 2026** (today is 29 Oct), so I used the free local route without asking, as the brief says.
- No Runway, ElevenLabs or Creatomate keys were used. AWS credentials exist in the environment but weren't used.
- The idea: that rival nations keep incompatible but individually accurate memories of shared wars (each commemorating its own dead and losses) is a commonplace of memory studies and historiography (contested commemoration, "competing victimhoods"). The episode applies it to two invented kingdoms and makes no claim about any real conflict.

## 2. Stack

Same stack as EP11–EP17:
- 3 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++. Both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics (all code), including every word of the inscriptions.
- Kokoro `af_heart` narration.
- Synthesized score (A minor → A major) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode (`src/graphics/Memory.tsx`):
- `chronicleFrame`: a gilt crop on the plate (`local`) that darkens everything outside it, then opens on a cue.
- `tablet`: a carved inscription cut letter by letter, with a TRUE seal and an optional "left out" line.
- `truthRows`: lesson rows plus a sum line.
- `lanterns`: small memorial lanterns with a flickering glow.
- `chisel` and `frameOpen` SFX in `pipeline/score.py`.

## 3. Narration (78 words, measured 29.99 s)

> What if both kingdoms are telling the truth about the same war? / Upstream, the stone says: they crossed the river and burned our town. / True. Look what it leaves out. / Downstream: they dammed the river, and we starved. / True too. It leaves out the fire. / Different losses, stories and values. Enemies, but neither is evil. / Give each side a true story and a real loss, and you'll never need a villain. / Tag someone who loves morally complicated fantasy.

The first measurement came in at 28.5 s, so I lengthened the beats after the hook, after each reveal and after the lesson lines (the pauses only, not the words). The second measurement was 29.99 s. "Upstream" / "Downstream" and "True." / "True too." give the two accounts the same shape, so the second plays as a mirror of the first without a split frame.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–3.68 | "What if both kingdoms are telling the truth about the same war?" | A misty dawn valley with a memorial stone on each bank; "ONE RIVER · ONE WAR / Two truths." | The paradox |
| 2 | `arvel` | 3.68–10.08 | "Upstream, the stone says: they crossed the river and burned our town. True. Look what it leaves out." | A gilt frame, WHAT ARVEL KEEPS, holds the stone and the razed village while the rest goes dark. The tablet is cut (ARVEL'S STONE · UPSTREAM) and stamped TRUE. On "Look" the frame opens and the camera pulls back down the river: LEFT OUT · DOWNSTREAM / *Their dead.* | One true account and its crop |
| 3 | `dunmere` | 10.08–15.78 | "Downstream: they dammed the river, and we starved. True too. It leaves out the fire." | WHAT DUNMERE KEEPS: the cairn field, framed. The tablet is cut and stamped TRUE. The frame opens on the river winding upstream: LEFT OUT · UPSTREAM / *Their burned town.* | The mirror account |
| 4 | `both` | 15.78–20.62 | "Different losses, stories and values. Enemies, but neither is evil." | The dawn valley dimmed, both stones in shot; ARVEL REMEMBERS and DUNMERE REMEMBERS tablets side by side, both TRUE. Different *losses.* / *stories.* / *values.*, then ENEMIES / *Neither* is evil. | Both truths in one frame; the reasons |
| 5 | `lesson` | 20.62–25.11 | "Give each side a true story and a real loss, and you'll never need a villain." | The valley almost dark; the line lands word by word (true, real, villain in amber) | The shareable thought |
| 6 | `cta` | 25.11–30.02 | "Tag someone who loves morally complicated fantasy." | The same valley at dusk, a lantern lit at each stone; CTA card with a "Tag a friend" pill; cross-fades to the dawn hook | Tag CTA; loops |

Motif: no new colour. Amber is the chronicle's frame, rust is what it leaves out, and ember is TRUE.

## 5. Generated assets

- **Plates** (local SDXL-Lightning; prompts in each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: the dawn valley, seed 11 (round 1). SDXL painted only one stone in all four hook candidates (round 2's two stood in the river), so the second stone is **composited from the plate itself**: the first stone is cut with a luminance mask, flipped, scaled to 0.42, hazed toward the far-bank tone and set on the far bank, with a faint reflection in the water. No outside imagery was used.
  - `plates/arvel.jpg`: the stone and the razed village, seed 11 (round 1). The intact cottage behind the stone was darkened (luminance-masked) into a burned shell, since "burned our town" needs one.
  - `plates/dunmere.jpg`: the cairn field by the shrunken river, seed 23 (round 1).
- **12 candidates in three rounds:**
  - round 1, 6 images: dunmere 23 was kept. The hooks had one stone each. The Arvel plates had a stone but no burned village.
  - round 2, 4 images: the hook's stones stood in the river, and the Arvel plate gave a ruined tower and no stone.
  - round 3, 2 images: Arvel again, but one plate had a church and the other an intact village, so the round-1 plate and the darkening described above won out.
- **Code-drawn:** both frames, both tablets and all inscription text, the TRUE seals, the callouts, the lesson rows, the lanterns and all other type.
- `ep20.srt` (18 cues) and `Worldcraft_Short_E20_cover.jpg` (the hook at 2.6 s, with the title).

## 6. Final video and verification

- `out/ep20.mp4` (master, 34.1 MB) and `out/ep20_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 20.7 MB): sent with SendUserFile.
- `ep20_download.mp4` (two-pass 3300k, 13.4 MB) and `ep20_player.mp4` (CRF 26, 7.4 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 30.02 s, −14.1 LUFS, true peak −1.4 dB. The download copy was read back from the preview page and QA'd as well (see the page's Checks).
- Fixes made after inspecting the beat frames and the contact sheet:
  - `build.sh` copies `episode.json` into `public/ep20/`, so a regenerated JSON wasn't being rendered until it was copied again (this is now in STYLE.md);
  - the Dunmere "left out" label collided with the tablet's seal, so it now hangs below its point;
  - the TRUE seal covered the tablet kickers in the two-tablet frame, so it moved to the lower-right corner;
  - the tablets were enlarged (52 px carved type; 35 px in the two-tablet frame);
  - the left CTA lantern sat behind the pill, so it moved to the left of the stone; the lantern glow is now a blurred disc (the first radial-gradient glow didn't show in the render).
- **Accepted compromises:**
  - The CTA lanterns are subtle under the card's dark band. They read on a phone but don't dominate.
  - Each reveal shows the *river leading to* the other side's loss, not the loss itself: SDXL wouldn't put cairns or ruins on the far bank, and the callout names them.
  - In the two-tablet frame, the rows sit over the dimmed left stone.
- **EP18 / EP19 merge:** neither branch existed at the start of the session. At the final fetch:
  - EP18 was finished (`be11236`), so it is merged in. The conflicts were all "both sides added" (README rows, the COSTS and STYLE sections, SFX in `score.py`, the `...LAW` / `...MEMORY` registrations), and every one keeps both sides. `DISTRIBUTION.md`'s caption sections, which git had interleaved, were rebuilt whole in episode order: 17, 18, 20. After the merge `tsc` passes, and one still each of ep18 and ep20 renders correctly.
  - EP19 had only WIP commits, so it was not merged.
- **Not verifiable by me:** how the narration and mix sound, including the new `chisel` and `frameOpen`. I can't hear the audio; please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `chronicleFrame` | Any "what the record leaves out" reveal: propaganda, a hero's statue that hides the conquered (EP31), a map that omits a people |
| `tablet` | Carved or written text that has to be legible and invented: laws, oaths, epitaphs, treaty clauses |
| `truthRows` | Short lesson rows with a sum line |
| `lanterns` | Mourning, vigils, festivals at night; warm points on a dusk plate |
| SFX `chisel`, `frameOpen` | Inscriptions being cut; a reveal that widens the view |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 3 stills (12 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 20`. The AI label is ON for every platform. The pinned comments ask viewers for their own two memorials of one event (what each carves and what it leaves out), which turns the lesson into the comment game alongside the tag CTA.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The valley and the question | Open inside Arvel's frame with the tablet already cut: "This is true. So is the opposite." | Viewed vs swiped away; average % viewed |
| 2 | Reveal | The frame opens on each account | Both frames open at the same time in the final shot only | Retention 4–16 s; rewatch rate |
| 3 | CTA | Tag (from the plan) | Comment: "Write the other side's memorial for a war in your world." | Shares and tags per 1,000 views vs comments per 1,000 |

Also track the share of comments that give both sides' losses (not just one), which shows the lesson landed.

## 11. How to produce EP21 ("The Three Questions Every Magic System Needs", opens Arc 5: Magic and Its Rules)

1. Branch `claude/worldcraft-ep21` from `claude/worldcraft-ep20`, which has EP01–EP18 and EP20. Merge EP19 once it is finished. Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief, and the EP01–EP03 briefs: the earliest episodes' sun and water magic are the nearest earlier "magic" visuals, with a signature sound per effect.
2. **Stills:** Figma credits reset on **1 Nov 2026**. If it's on or after that date and Figma would be clearly better (magic glows, a practitioner), ask with AskUserQuestion first (about 4 images, up to 6). Otherwise use `python pipeline/local_stills.py ep21 <shots> --seeds 11 23`, then `--pick`, then `plates.py --register`, with nothing else heavy running.
   - When waiting on it, don't `pgrep -f local_stills` from a shell whose own command line contains that string, because it matches itself and never ends. Wait for "wrote …" in the log instead.
   - Budget a second round. If SDXL won't paint a second copy of something, composite it from the plate's own pixels (see STYLE.md).
3. Story (plan): open Arc 5 with a three-question frame (where the power comes from, what it costs, who can use it, or the plan's exact wording). Show one invented magic answering each question on screen. Draw the magic itself in code, pinned to the plate, with one signature SFX. Don't reuse this episode's frame/tablet shape as the spine.
4. Narration of about 70–78 words, measured with `cd pipeline && python tts.py ep21`. Check names in the G2P, and use `nth` for repeated words in cues.
5. Then:
   - `pipeline/build.sh ep21` → render → `qa.py` → sheet and beat frames, including the loop tail. After any JSON change without a rebuild, copy `episode.json` to `public/ep21/`.
   - Compat, two-pass download and player encodes, all `-c:a copy`, with `qa.py` on each.
   - `srt.py`, `storyboard.py`, the cover, and an 11-section brief.
   - Docs: COSTS, DISTRIBUTION, README, STYLE.
   - A new preview page with a Download MP4 button, then SendUserFile.
   - Commit and push to the episode branch.
