# EP31 production brief: Your World Needs a History Nobody Agrees On

**Series:** Worldcraft Shorts, Episode 31 / 50. Season 2, "The World Engine", **Arc 7: History and Mythology** (the arc's first episode). **The Season 2 reference episode**: start EP32 and every later episode from this brief and `make_ep31.py`.

**Plan entry** (`docs/SERIES_PLAN.md`):
- Hook: "What if the greatest hero in history was actually the worst person who ever lived?"
- Topic: conflicting historical accounts.
- Core: history is interpreted through incomplete records, political interests, cultural values and personal memories. Conflicting accounts create mysteries that can drive entire stories.
- CTA: "Follow for more ways to turn history into plot." This is a follow ask, and the ending formula already asks for the follow, so the end card asks for a comment instead: a one-word verdict.

**Deliverable:** a 59.5 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. The AI disclosure is on everywhere.

**Shot list and timings:** [`STORYBOARD.md`](STORYBOARD.md). The script that writes `episode.json`, including the whole world timeline, is `make_ep31.py`.

## The brief

The request: make EP31, improve everything, write the script to the highest standard, benchmark it against top-performing short-form content from start to finish, and polish it so that EP31 can be the reference for the episodes that follow. For the art, the user asked to try free tools first and use Figma only if none was good enough. The standing direction holds: close EP30's loop ("hero, or monster?"), follow EP30's §11 hand-off, make the episode **its own** (`docs/STYLE_S2.md` → "Make every episode its own"), and end on the ending formula with a tease for EP32 ("Create an Ancient War That Still Matters").

### Why EP31 is the reference
What EP31 adds to *how* an episode is made, for every episode after it:
1. **A measured script.** The benchmark research (`docs/SEASON2_RESEARCH.md` §7) became a 25-row retention scorecard, `pipeline/benchmark.py`: hook timing, pace, how often the picture changes, where the story beats land, how long the lesson can be read, the ending, the loop. **EP31 passes 25 of 25; EP30 passes 21 and EP29 23** (§6). Run it before every render.
2. **Writing rules**, in `docs/STYLE_S2.md` (Format): one idea, one example, one line to keep; a hook of 12 words or fewer that ends by 4 s; sentences of 6 words on average and never more than 12; the hook's question answered by the twist and not before.
3. **Picture rules learned by looking:** the episode's device changes on the spoken word; nothing on screen holds still for more than 2.5 s; the line to keep stays readable for at least 1.2 s.
4. **Tools in the repo:** the scorecard and the camera probe (`pipeline/camprobe.ts`), which EP30 and EP31 needed and which until now lived only in a scratchpad.
5. **Lessons written down** in `docs/STYLE_S2.md` → "Making the next episode", in the order they cost time.
6. **A free art route:** local SDXL for the plain subject, the composition done in code (`art/PROMPT.md`).

### EP31's own idea: the two chronicles
**Two open pages under the world**, one for each people that remembers Maren: THE VALLEY SAYS on the left in gold, THE COURT SAYS on the right in rust. Each fact is written, never written, lost or (at the twist) true on each page, a one-word verdict heads each page, and the spine between them counts how far the pages agree. The episode's argument is in the device: *a history is the set of facts each teller kept, and a dispute is a number you can watch fall.*

The chronicles, beat by beat:
- **The lazy version:** both pages HERO, MONSTER GONE, FLOCK SAVED: **AGREE 100%**. Run 1 stamps the same verdict every century, then CASE CLOSED.
- **The rewind** to the night itself: both pages are blank and the spine waits (· · ·).
- **Rule 1, witnesses:** as the valley is named, its page is written (HERO, MONSTER GONE, FLOCK SAVED); as the court is named, its page is written (MONSTER, FIELDS BURNED, HARVEST LOST), and the spine pops to **AGREE 0%**.
- **Rule 2, motive:** a coin stamps each page (each telling pays its teller).
- **Rule 3, loss:** a row is struck from each page: PAGE LOST.
- **Rule 4, retelling:** HERO becomes SAINT, MONSTER becomes DEMON.
- **The twist:** every row on both pages turns ember, **BOTH TRUE**. Then "Now hide that": the pages fall back to their halves and the spine locks, **THE TRUTH · HIDDEN**.

The four rules are the plan's four sources of disagreement, in an order that builds: **witnesses** (personal memories), **motive** (political interests), **loss** (incomplete records), **retelling** (cultural values, inflating with each generation).

**What else is EP31's own:**
- **The camera language: the split frame.** Every pose but the two wides and the lesson is frontal on the statue's centre line (az 0), so the valley's side is always the left of the frame and the court's the right, and the frame itself is graded in two halves at the hook, during rule 2 and in the loop. EP26 orbited, EP27 rode a dragon, EP28 sat at eye height, EP29 was a locked-off tripod, EP30 looked up.
- **The witness veil:** the half of the frame a witness never saw is hatched out, UNSEEN, so the viewer literally sees each side's half of the night.
- **The monument:** a hooded stone woman with a torch in each hand on a two-step plinth. Each telling paints its half: gilded, torch lit, flowers and candles on the valley's side; tarred and scratched, torch dead, on the court's. Each retelling makes her taller.
- **Motif colour:** chronicle ink `#7f95ff` (the chronicles' frame, HAS WITNESSES, THE TRUTH, the DISPUTED stamp, the TELLINGS counter).
- **Music band** around the series theme, at 96 BPM:
  - `chronicle`: a lute ostinato (nylon guitar on the marimba channel), tambourine, pizzicato bass, the theme on recorder, then harp and glockenspiel, one family per rule;
  - `dispute`: the theme's bars alternate between a recorder and a bassoon that never quite agree (the hook, and the night unveiled).
- **Sound:** `quill` (an entry written) and `pageTear` (a page lost).
- **Fresh wording for the recurring beats:**
  - the drop: "Case closed. Nothing left to solve.", stamped CASE CLOSED · 0 QUESTIONS · NOTHING TO SOLVE;
  - the thesis: REAL HISTORY / HAS WITNESSES;
  - the checklist: MAREN · THE RECORD / CRACK IT OPEN;
  - run 2's verdict: DISPUTED · 1 NIGHT · 2 HISTORIES;
  - the twist: RULE 5? THE TRUTH, then SHE DID / BOTH, ONE TORCH · BOTH STORIES, and ONLY YOU KNOW · HIDDEN.

| Time | Beat |
|---|---|
| 0–6.8 s | **Hook (closes EP30's loop):** golden hour, frontal on a long lens: the split statue, gilded left and tarred right, the valley's people in gold and the court's in rust, the frame graded in two halves. HERO / OR MONSTER? is on screen from frame 0; the gold half flares on "hero", the rust half on "monster?". Field card: MAREN · DISPUTED FIGURE · DID: one thing, 300 years ago |
| 6.8–11.3 s | **"The lazy version":** an ink wipe to year 0, the plain stone statue: ONE HISTORY / EVERYBODY AGREES. The chronicles slide in, AGREE 100%; RUN |
| 11.3–15.4 s | **Run 1:** the whole Isle; YEAR 0→300 as the crowds turn over; YEAR 100 · HERO, YEAR 200 · HERO, YEAR 300 · HERO; TELLINGS 01, QUESTIONS 00 |
| 15.4–18.0 s | **The drop:** the plain statue in gloom: **CASE CLOSED · 0 QUESTIONS · NOTHING TO SOLVE** |
| 18.0–23.0 s | **Re-hook:** rewind to the night itself (dusk, year 0, no statue): Maren with her torch on the spot, the Grimmaw to her left, the court's ripe field to her right, three witnesses from each side. REAL HISTORY / HAS WITNESSES; the checklist CRACK IT OPEN, row 5 locked ("the twist") |
| 23.0–28.1 s | **Rule 1, witnesses:** THE VALLEY SAW (the right half UNSEEN) as the Grimmaw roars and is driven off; THE COURT SAW (the left half UNSEEN) as the field burns. Each page is written as its witness is named: AGREE 0% |
| 28.1–31.4 s | **Rule 2, motive:** day; the statue rises on the spot between the two archives; a coin on each page; the valley gilds its half, the court tars its half, and the frame splits |
| 31.4–34.0 s | **Rule 3, loss:** dusk; BOTH ARCHIVES · PAGES BURN; PAGE LOST on each chronicle; seventy years pass and the crowds thin |
| 34.0–37.3 s | **Rule 4, retelling:** the years race to 300 and the statue grows a third taller: SAINT / DEMON |
| 37.3–39.8 s | **Run 2:** the whole Isle; QUESTIONS climbs to 40: **DISPUTED · 1 NIGHT · 2 HISTORIES** |
| 39.8–46.1 s | **The twist: "Rule five? The truth. She did both."** The night again, unveiled: her torch lights the field and the Grimmaw flees from the fire, in one frame. SHE DID / BOTH, every entry ember: BOTH TRUE; ONE TORCH · BOTH STORIES. "Now hide that from your world": ONLY YOU KNOW · HIDDEN |
| 46.1–48.4 s | **"Let your characters fight over the pieces."** Today, the split statue; row 5 unlocks: THE TRUTH · know it. hide it. 5/5; the follow chip |
| 48.4–51.2 s | **Lesson:** the full card over the Isle in golden light, *History is who's telling it.* (on screen 1.7 s) |
| 51.2–53.8 s | **Comment CTA:** "Hero or monster? Give us your verdict." HERO and MONSTER pop as vote chips on their words |
| 53.8–59.5 s | **The ending formula:** PART 31 / 50, FOLLOW FOR PART 32, NEXT RUN · 32 UNFINISHED · A WAR THAT NEVER ENDED; in the hook frame each crowd raises a war standard in its own colour, the valley's bell tolls, the Queen and the Grimmaw look up; the standards sink and the hook title returns on frame 0 |

**Why Maren and why a burned field.** One act with two true consequences: she drove off the Grimmaw (the Isle's own predator since EP26), which saved the valley's flocks, and she did it by burning the court's harvest. Nobody lies. Each side keeps the half that happened to it, and the gap between them is the plot. The plan's hook makes hero and monster two readings of one person; EP31's "What if history's greatest hero was also its worst monster?" says it in 10 words, and "also" sets up the twist, *she was both*, which the episode pays off at 41.7 s.

**The Isle remembers:**
- the valley is EP27's humans (the watchtower's bell rings the tease);
- the court is EP29's, and the Undying Queen looks up from her dais at the end;
- EP28's Fenn hall on the lake and the cairn;
- EP30's worshipped Grimmaw, garlanded on the north-west meadow today.

Maren's statue stands on the south-east meadow, on the spot where she stood that night. Every frontal frame keeps the older landmarks out (checked with the camera probe).

**Nothing graphic, nothing real:** the Grimmaw is driven off by fire and walks away; the field burns with nobody in it; "witnesses die" is a crowd thinning as seventy years pass. Maren, the valley and the court are invented, and the statue is an original design (a first sprite that resembled a real monument was rejected).

## 1. Research note

`docs/SEASON2_RESEARCH.md` §7 (12–14 Nov 2026), in short:
- **What benchmarking could mean here.** I have no access to anyone's analytics and can't watch other channels, so I collected what is published about how high-retention Shorts are written and cut, recorded how strong each source is, turned the patterns several sources agree on into measurable targets, and scored EP31, EP30 and EP29 with one script.
- **The one primary source:** YouTube's blog (19 Aug 2026): from 24 Aug 2026 a view counts from the first frame, and an engaged view means "watching past the initial seconds". So raw views say nothing about the hook; the number to watch is "viewed vs swiped away".
- **The patterns** (all vendor and creator guidance, numbers unverified): the first word within half a second on the most striking frame, with text on screen from the first word; one idea, one example, one takeaway; short sentences written for the ear; the problem by about 15 s; a teased secret in the middle; the hook's promise paid off late, as the climax; something to do at the end; the ask after the value.
- **Comments:** Socialinsider's 2026 dataset (79.8 million posts from brand accounts) puts average comments per video at TikTok 50, Reels 20, Shorts 10. A binary prompt "where both options have vocal defenders" lowers the effort to reply, but no source measures it against an open question, and "the goal is friction, not offense".
- **Safe zones:** third-party guides reserve the bottom 300–340 px for platform UI; the device strip under the world (y 1352–1568) ends 12 px above the most cautious figure. No platform publishes one.
- **Free tools for the art:** the local SDXL-Lightning pipeline already in the repo did the job (§5). Apache-2.0 alternatives (Z-Image-Turbo, FLUX.1 [schnell]) were considered; I found no CPU timings I could verify and both are larger, so they weren't tried in this container.

## 2. Stack

Unchanged (Remotion 4 + `@remotion/three` + three.js in software WebGL, `swangle`). New this episode, all additive (EP01–EP30 render as before; see §6):
- **World:**
  - `src/s2/world/People.tsx`: `Statue` (`rise`, `gild`, `tar`, `grow`), `Standard` (a war banner that rises in a `color`), `Figure` (a keyed person with an optional torch); `PeopleLayer` takes `figures`, `watch` (the crowd stands still facing a point) and `tints` (a tunic colour per crowd centre);
  - `WorldScene.tsx`: the `statue` and `standard` props; `fields.burn` (the crop chars from one edge, with `FieldFire` flames and smoke);
  - `timeline.ts`: the new prop kinds and keys, all optional.
- **Overlays** (`src/s2/overlays/Overlays.tsx`): `chronicles`, `veil`, `splitTone`; `kinetic` parts take `pulseAt`; `endCardS2` takes `choices` and `withAt`; `nextRun` takes `titleSize`. Sprites `flame`, `coin`, `standard`.
- **Sound:** music styles `chronicle` and `dispute` (`pipeline/music_s2.py`); SFX `quill` and `pageTear` (`pipeline/score_s2.py`), each with its own seeded noise, so nothing older changes.
- **Tools:** `pipeline/benchmark.py` (the scorecard) and `pipeline/camprobe.ts` (the camera probe).
- **Environment:** as EP30's (`npm ci`, FluidSynth and the MuseScore General SoundFont, espeak-ng, a Python 3.12 venv for Kokoro and SDXL).

## 3. Narration (161 words, 59.47 s total)

> What if history's greatest hero was also its worst monster? Meet Maren. Three hundred years ago, she did one thing. The lazy version: one history, and everybody agrees. Press run. Three hundred years. One statue. One story. Zero questions. Case closed. Nothing left to solve. Real history has witnesses. Four rules crack it open. The fifth is the twist. One: witnesses. The valley saw her drive the monster off. The court saw their fields burn. Two: motive. Each side keeps the half that flatters it. Three: loss. Pages burn. Witnesses die. Four: retelling. Every generation makes her bigger. Run it again. One night. Two histories. Rule five? The truth. She did both. She burned the fields to drive it off. Now hide that from your world. Let your characters fight over the pieces. History isn't what happened. It's who's telling it. Hero or monster? Give us your verdict. Part 31 of 50. Follow for part 32: a war that never ended.

**How it is written** (the rules in `docs/STYLE_S2.md`, measured in §6):
- **The hook** is a 10-word question built on a contradiction, spoken from 0.20 s over a frame that already shows both answers.
- **"Meet Maren. Three hundred years ago, she did one thing."** A name and a withheld fact in 9 words. The field card repeats it, DID: one thing, and the episode doesn't say what for 35 seconds.
- **The lazy version is the reader's own default** ("one history, and everybody agrees"), and it fails for a story reason, not a realism reason: "Case closed. Nothing left to solve." That is the plan's core point: conflicting accounts are what drive a story.
- **The re-hook** states the thesis in four words ("Real history has witnesses.") and makes the series' promise ("Four rules crack it open. The fifth is the twist.").
- **Every rule has the same shape**, "N: word." then one sentence of ten words or fewer, and each one changes something on screen.
- **The twist answers the hook** ("She did both.") and then gives the writer two jobs: "Now hide that from your world." and "Let your characters fight over the pieces."
- **The lesson** is eight words in a contrast that can be quoted: "History isn't what happened. It's who's telling it."
- **The ask loops back to the hook:** "Hero or monster? Give us your verdict." Both answers are defensible because both are true, and Maren is fictional, so it invites a side without inviting anger.

**Measured with the real TTS** (Kokoro `af_heart`) before any cue was set: the first draft (157 words) ran 58.4 s, so two lines were sharpened ("Now hide that." became "Now hide that from your world."; "Let your characters fight over it." became "...over the pieces.") for **161 words at speed 1.05: 59.47 s**.

**G2P checked:** "Maren" → mˈæɹən; "flatters" is fine; "31", "50" and "32:" read as numbers.

**Landmarks:** "lazy" 7.0 s · "run" 10.7 · "Case" 15.6 · "Real" 18.1 · "the twist" 22.3 · "valley" 24.5 · "court" 26.6 · "Two" 28.2 · "Three" 31.5 · "Four" 34.2 · "Run" 37.4 · "Rule" 40.0 · "both" 41.7 · "hide" 44.8 · "Let" 46.2 · "fight" 47.1 · "History" 48.5 · "Hero" (wipe −0.3) 51.3 · "Part" 53.9 · "Follow" 55.5 · "war" 57.2 · "ended" 57.9.

## 4. Timed storyboard

See [`STORYBOARD.md`](STORYBOARD.md).

## 5. Generated assets

- **Free local SDXL-Lightning** (`pipeline/local_stills.py`, CPU): 4 candidates in two rounds; seed 62 used. **0 Figma generations.** The first round came back crowned and gold all over (one reads as a famous real monument) and ignored the "half gilded, half tarred" instruction. The second asked for the plain subject: a grey stone statue of a hooded shepherd woman. Seed 62 holds a torch in each hand on a two-step plinth, and the voxel statue is built to it. The gilded and tarred halves were added in code (`art/split_statue.py`) and the result re-gridded to `assets/statue_sprite.png` (62×127, `--colors 24`). Prompts and steps: [`art/PROMPT.md`](art/PROMPT.md).
- **Tested for the next episodes: a pixel-art LoRA.** The same local pipeline with the nerijs/pixel-art-xl LoRA (CreativeML OpenRAIL-M) fused into the UNet draws real pixel art (a true pixel grid, cleaner shading, a brick plinth) at the same speed, 85 s an image. Seed 62 gave the same hooded statue with two torches; seed 5 came back with a halo, which reads as a religious icon. Split and re-gridded, seed 62 shaded more cleanly than the shipped sprite, but the split script greyed out its right torch and it came out taller (62×145), so EP31 keeps its sprite rather than render a fourth time for a marginal gain. It is now `python pipeline/local_stills.py <ep> <name> --sprite --prompt "…"` (needs `peft`): use it for EP32's sprites.
- **Code-drawn:** everything else (the statue in the world, Maren, the crowds, the Grimmaw, the fire, the archives, the standards, the chronicles, the veil, the split tone).
- **Cover:** `Worldcraft_Short_E31_cover.jpg`, the hook frame at 3.5 s (the split statue under HERO / OR MONSTER?, no bird over the corner logo).
- **No readable text in any generated image.**

## 6. Final video and verification

- **QA:** `qa.py` **passed** on all four copies, each 59.48 s, −14.0 LUFS, TP −1.4 dB:
  - master: 17.3 MB;
  - compat: 15.7 MB;
  - download (two-pass 1,600k): 13.9 MB;
  - player (two-pass 1,300k): 11.7 MB.
- **The loop:** the last frame against frame 0 differs by **0.87/255**, about two ordinary frame steps (0.45 at the start, 0.34 at the end).
- **The scorecard** (`python pipeline/benchmark.py ep31 ep30 ep29`; targets and sources in `docs/SEASON2_RESEARCH.md` §7):

| Group | Metric | Target | EP31 | EP30 | EP29 |
|---|---|---|---|---|---|
| Hook | First spoken word starts | ≤ 0.5 s | ✓ 0.20 s | ✓ 0.20 s | ✓ 0.20 s |
| Hook | Spoken hook ends | ≤ 4.0 s | ✓ 3.48 s | ✓ 3.84 s | ✓ 3.19 s |
| Hook | Hook length | ≤ 12 words | ✓ 10 words | ✗ 13 words | ✓ 11 words |
| Hook | Words heard in the first 3 s | ≥ 7 | ✓ 9 | ✓ 9 | ✓ 10 |
| Hook | Title on screen at frame 0 | yes | ✓ yes | ✓ yes | ✓ yes |
| Hook | First change of picture after the hook | ≤ 4.5 s | ✓ 2.93 s | ✓ 4.09 s | ✓ 3.44 s |
| Pace | Narration | 140–170 | ✓ 161 words | ✓ 170 words | ✓ 161 words |
| Pace | Speaking rate | 150–175 wpm | ✓ 162 wpm | ✓ 169 wpm | ✓ 158 wpm |
| Pace | Average sentence | ≤ 6.0 | ✓ 4.1 words | ✓ 4.5 words | ✓ 4.5 words |
| Pace | Longest sentence | ≤ 12 | ✓ 10 words | ✗ 13 words | ✓ 11 words |
| Pace | Longest pause between lines | ≤ 0.45 s | ✓ 0.40 s | ✓ 0.40 s | ✓ 0.40 s |
| Picture | Changes of picture | ≥ 40 a minute | ✓ 63 (64 a minute) | ✓ 48 (48 a minute) | ✓ 47 (46 a minute) |
| Picture | Longest stretch without a change | ≤ 2.5 s | ✓ 2.08 s | ✗ 4.09 s | ✗ 4.38 s |
| Picture | Median stretch | ≤ 1.0 s | ✓ 0.88 s | ✓ 0.81 s | ✓ 0.84 s |
| Story | Run 1 starts | ≤ 12 s | ✓ 11.4 s | ✓ 10.6 s | ✓ 10.6 s |
| Story | The drop (naive design fails) | 13–19 s | ✓ 15.6 s | ✓ 14.4 s | ✓ 14.1 s |
| Story | Re-hook ('the twist' promised) | 18–25 s | ✓ 22.3 s | ✓ 20.2 s | ✓ 21.0 s |
| Story | The twist | 36–47 s | ✓ 40.0 s | ✓ 38.5 s | ✓ 41.5 s |
| Story | Payoff line (the lesson) | after the twist, ≥ 45 s | ✓ 48.5 s | ✓ 48.3 s | ✓ 50.1 s |
| Story | Lesson line stays on screen | ≥ 1.2 s | ✓ 1.72 s | ✗ 0.37 s | ✗ 0.54 s |
| Ending | CTA | ≤ 10 words, one ask | ✓ 7 words | ✓ 9 words | ✓ 8 words |
| Ending | Ending formula (part, follow, tease) | yes | ✓ yes | ✓ yes | ✓ yes |
| Ending | Follow ask in the last | final 3–7 s | ✓ 5.6 s | ✓ 5.3 s | ✓ 5.2 s |
| Ending | Hook title returns for the loop | yes | ✓ yes | ✓ yes | ✓ yes |
| Format | Duration | 55–62 s | ✓ 59.47 s | ✓ 60.22 s | ✓ 61.26 s |
| | **Score** | | **25/25** | **21/25** | **23/25** |

- **Renders:** three full renders with `--gl=swangle` (1,784 frames, 9–11 min each). The first two were set aside after looking at them (fixes 12–14 below). The final one: 9 min.
- **Preview page:** https://claude.ai/artifact/P5QLyR41JpWiRdt4FWdcsK (new; EP26–EP30's pages are untouched).
  - It declares `downloads` and `assets` and has a Download MP4 button.
  - The download reads back byte-identical (sha256 `c92a50be…`) and passes `qa.py`.
  - The player is asset `/_blob/586d6b554a75867dca676cb0747dd987` (sha256 matches `out/ep31_player.mp4`).
  - It also steps through the two chronicles' nine states (LAZY to HIDDEN) and shows the scorecard.
- **Inspected:**
  - beat stills on many rounds, including an overhead scout of the layout and probe checks of every frontal pose;
  - the QA contact sheet of each master;
  - 40 frames from the first master and 44 from the later ones;
  - frame 0 against the last frame;
  - the cover candidates.
- **Fixes made after looking:**
  1. **The first layout failed.** The statue, framed too close, read as a slab; the present-day Grimmaw photobombed; the dais, the cairn and the Fenn hall crept into frames; the night's actors were tiny. The scene moved to the south-east meadow with every frontal pose on one centre line (az 0), and each pose was checked with the projection probe. The night, loss, twist and role poses were tightened to keep the Queen's dais out.
  2. **The statue was redesigned twice** (a hood, a face and a cloak; a palette per part; less gleam).
  3. **The night was hard to read:** Maren was scaled ×2 with a THAT NIGHT · MAREN pin; the Grimmaw's flight was retimed to "monster" and "drive" so it is seen to go; the witnesses moved to the foreground corners; the veils stop short of the centre so Maren stays visible to both sides.
  4. **States jumped 0.25 s after the rewind wipe.** A block wipe is centred on its cue, so every jump moved to the wipe's own cue (the `jump()` helper).
  5. **The chronicles read AGREE 2/4 with one page empty;** the spine became a percentage of written facts.
  6. **Pins overlapped the HUD** or were hidden by the card: anchors and end cues changed, and one pin (THE GAP IS THE PLOT) was cut.
  7. **UNFINISHED overflowed the next-run card:** `nextRun.titleSize` (66).
  8. **The war standards covered the statue:** lowered and moved over the crowds.
  9. **The split tone was missing from the last frame** (a graphic ends where the next shot starts): it moved into the last shot's list, and frame 0 against the last frame went from a visible mismatch to 0.34/255 on that still. The motive split tone showed a top edge; it moved to the head of the setup list, at full height, under the HUD.
  10. **The scorecard found static stretches** (hook 3.73 s, run 1 2.84 s, CTA 2.72 s): the hook's halves now pulse on "hero" and "monster?", run 1 stamps YEAR n · HERO each century, and the CTA's vote chips pop on their words.
  11. **The first sprites resembled a real monument and had no split** (§5); the sprite's keying left holes in the statue's mid-greys, fixed with a border-connected background mask.
  12. **After the first render: the chronicles got ahead of the voice.** The valley's page kept HERO from the lazy version through the rewind, the spine said 0% while the court's page was still blank, and the HUD said TELLINGS 01 at year 0. Now both pages are blank after the rewind, each is written as its witness is named (with the quill), the spine waits (· · ·) until both exist and pops when its reading changes, and TELLINGS counts 0, 1, 2.
  13. **After the second render: the lesson line was on screen for under half a second.** It arrived on the last spoken word and the card left 0.5 s later (EP29 and EP30 had the same problem: 0.54 s and 0.37 s). It now arrives as the first sentence ends and stays until the wipe covers the card: 1.72 s. A scorecard row checks it now.
  14. **SHE DID / BOTH** left after 0.2 s; it now holds through "She burned the", and the ONE TORCH pin follows on "fields".
- **Sound (measured):**
  - −14.04 LUFS, peak −1.48 dBFS, voice/music 14.0 LU;
  - the chime windows on the SFX track are −23.4 / −22.3 / −23.2 LUFS (EP30: −23.4 / −22.4 / −23.9);
  - the score follows the story: dispute hook −20.2, the lazy chronicle −26.1, run 1 −21.4, drop −18.7 (the boom on "closed"), mystery −26.7, chronicle 1–4 −26.8 / −25.6 / −25.3 / −20.4 as the rules switch on, run 2 −17.5, twist −23.5, dispute (the night unveiled) −20.3, anthem −17.5, outro −29.8, tease −23.9;
  - fixes 12–14 moved two SFX cues; the score (`music.wav`) is bit-identical across all three renders.
- **Regression, all with the final EP31 code:**
  - EP25's, EP29's and EP30's `music.wav`, `sfx.wav` and `mix.wav` are **bit-identical** to the baselines (narration and timing fixed);
  - EP30 stills at 0, 8.8, 26.8, 42.5 and 60.2 s and EP25 stills at 2.0, 14.0 and 27.0 s are **byte-identical** to stills rendered from a worktree of `claude/worldcraft-ep30`;
  - `src/Episode.tsx` (Season 1) is untouched.
  - One caveat: in an earlier run, EP25's still at 2.0 s (the first frame rendered in that session) differed slightly from the old tree's (0.57/255 on average). Rendering the same frame again in the same tree gave a different result from the first run, and the second runs matched byte for byte, so it is run-to-run noise in the first still of a session, not a code change.
- **Not verifiable by me:** how anything sounds. In particular, listen to the recorder and bassoon trading the theme under the hook, the lute chronicle as it builds, the quill on each entry, the page tear, the fire bed, and the bell and frame drum under "a war that never ended".
- **Accepted compromises:**
  - the field-card sprite is small (62×127: the statue is tall and thin);
  - the night is dusk-dark and the veils cover half of it by design;
  - the war standards at the end are small in the hook frame (they're a tease, read with the NEXT RUN card);
  - the chronicles' bottom row sits close to the bottom 340 px that some guides reserve for platform UI; the verdicts and the spine are at its top.

## 7. Reusable components added

All are documented in `README.md` (Season 2 building blocks) and `docs/STYLE_S2.md` (motion vocabulary).
- **`chronicles`:** any dispute between two accounts: two peoples' myths (Arc 7), two sides' war records (Arc 8), two merchants' books (Arc 9). The spine makes the disagreement a number.
- **`veil`:** any point of view: what one side can't see (a border, a fog of war, a secret).
- **`splitTone`:** two readings of one picture.
- **`statue`:** a monument that changes with its tellers (`rise`, `gild`, `tar`, `grow`).
- **`standard`:** war banners that rise in a side's colour (EP32's opener).
- **`fields.burn`:** scorched earth, a cursed or salted field.
- **`people.figures`, `watch`, `tints`:** one named person in a crowd; a crowd attending to something; two peoples told apart by colour.
- **`kinetic.pulseAt`, `endCardS2.choices`, `nextRun.titleSize`:** a title that answers the voice; a vote on the comment card; a long next-run title.
- **Music:** `chronicle` (a record being written) and `dispute` (two tellings). **SFX:** `quill`, `pageTear`.
- **Tools:** `pipeline/benchmark.py`, `pipeline/camprobe.ts`.

## 8. Cost (₱63.35 = $1)

**$0 cash, 0 Figma generations.** The sprite came from the free local SDXL pipeline; everything else is free and open. Details in `docs/COSTS.md`.

## 9. Platform metadata

In `episode.json → metadata`, and ready to paste in `docs/DISTRIBUTION.md` ("Episode 31 captions").
- YouTube title: *Your World Needs a History Nobody Agrees On (Worldbuilding)* (59 characters). Alternate: *Their greatest hero. Their worst monster. Same person.*
- Instagram hook: "Hero to one village. Monster to the next." TikTok opens with "Same night. Two histories."
- Pinned comments ask for the verdict in one word, then the reason. Post the pin straight away and answer early comments in the first hour.
- Every description ends with "Part 31 of 50. Follow for part 32: a war that never ended."
- AI label ON on all four platforms.

## 10. Experiments and metrics

- **The scorecard against reality.** EP31 scores 25/25, EP29 23 and EP30 21. Compare viewed vs swiped away, average percentage viewed and the retention curve at 15.6 s (the drop), 22.3 s (the re-hook) and 40–42 s (the twist). If EP31 isn't better, the targets need revisiting, not just the episode.
- **A vote against an invention prompt.** EP31's "Hero or monster?" against EP30's "What creature would your civilization worship?": comment count, length, and replies to comments.
- **The readable lesson.** The lesson line now stays on screen 1.7 s (EP30: 0.4 s). Compare saves per 1,000 views.
- **The device in the middle:** retention at 23–37 s (the four rules) against EP30's ledger in the same slot.
- **Arc 7's opener:** follows per 1,000 views against EP30.

## 11. How to produce EP32 ("Create an Ancient War That Still Matters")

1. **Branch:** `claude/worldcraft-ep32` from `main` once EP27–EP31 are merged (or from `claude/worldcraft-ep31`; merge `origin/main` first, keeping both sides). Read `CLAUDE.md`, `docs/STYLE_S2.md` (the reference-episode note, the writing rules, "Make every episode its own", "Making the next episode"), `docs/SEASON2_RESEARCH.md` §7 and this brief.
2. **Plan entry:**
   - Hook: "The war ended a thousand years ago. So why are people still dying because of it?"
   - Core: ancient wars leave disputed borders, inherited prejudices, cursed territories, religious divisions, stolen artifacts and unresolved claims. The past stays relevant while its consequences persist.
   - CTA: "What unresolved conflict would your ancestors leave behind?" (an invention prompt, like EP30's; a good contrast with EP31's vote).
3. **Close EP31's loop.** EP31 ends with two war standards, wheat gold on the valley's side and rust on the court's, rising over the two crowds before Maren's split statue; the valley's bell tolls and the Queen and the Grimmaw look up; NEXT RUN · 32 UNFINISHED · A WAR THAT NEVER ENDED. EP32's frame 0 should show that war's consequence *today*. One reading that keeps the Isle's continuity: the war the valley and the court fought over Maren, whose border now runs down the statue's seam, with the two standards still planted on either side and the burned field never farmed again.
4. **Give EP32 its own device** (not an editor, a point of view, a timeline, a balance or a pair of chronicles). One idea, unused so far and true to the tagline "from the ground up": **the strata.** The war is in the ground: a cut-away of the island's side where the battle is one layer and every century since is laid on top, and each consequence (a border stone, a buried relic, salted earth, bones) runs up through the layers to the surface. Camera language: a vertical crane down through the cut. Pick a motif colour that isn't rust, which already means failure (bronze, slate or lichen green), and a music band (e.g. a march slowed to a dirge, war drums heard through earth).
5. **Reuse:** `standard` (the tease), `fields.burn` (cursed ground), `people.tints` and `watch` (two peoples facing each other), the `statue` (the border runs through it), `veil` (what each side can't see across the border), `splitTone`; `ledger` to weigh grievances if needed. Keep `chronicles` for a brief callback only, so EP32 doesn't become a re-skin of EP31.
6. **Writing:** start from `make_ep31.py`'s structure, not its words. Measure with the real TTS, then run `python pipeline/benchmark.py ep32 ep31` and fix every ✗ before rendering a single still.
7. **Pipeline notes:**
   - Kokoro needs Python ≤ 3.12, and `tts.py` needs `VIRTUAL_ENV` set to the venv. SDXL needs the same venv, about 10 GB of RAM, and nothing else running.
   - **Plan every camera pose with `pipeline/camprobe.ts`** before rendering stills (usage at the top of the file).
   - **Regressions:** before changing shared code, save `public/ep31/{narration.wav,timing.json,music.wav,sfx.wav,mix.wav}` (and EP25's, EP30's); afterwards, fix the narration and timing, re-run `score.py` + `mix.py` and `cmp` the outputs. Render stills from a `git worktree` of this branch (symlink `node_modules` and `public`) and byte-compare. Render a throwaway still first: the first still of a session can differ from run to run.
   - A block wipe is centred on its cue; a graphic ends where the next shot starts unless it has an `end`; overlays draw in shot order, then list order; `captionsOff`'s `to` word is exclusive and has no `nth`.
   - Remotion bundles `public/` when a render starts. If the audio changes during a render, re-mux the master's audio from the new `mix.wav`.
8. **Then** the same delivery: stills, a `--gl=swangle` render (about 10 min), `qa.py`, encodes, SRT, storyboard, cover, this 11-section brief with the scorecard, docs, a new preview page with the Download button, push.
