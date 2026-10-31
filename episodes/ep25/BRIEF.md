# EP25 production brief: The Strongest Magic System Has Weaknesses

**Series:** Worldcraft Shorts, Episode 25 / 50. Closes **Arc 5: Magic and Its Rules**, and marks the halfway point of the series.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "The secret to a terrifying wizard isn't making them unbeatable." Topic: strategic limitations. CTA: "Follow for more ways to make fictional powers interesting."
**Deliverable:** a 29.7 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. The AI disclosure is on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`. The script that writes `episode.json` is `make_ep25.py` (prompts in `prompts_ep25.py`).

## The brief

- **One idea:** a weakness forces characters to think. A caster nobody can stop is boring; a caster with one strategic gap is more frightening, because the heroes have to outwit her and she has to plan to cover the gap.
- **One caster, one name:** **the Unmaker**, an ordinary English compound. Kokoro's G2P reads it cleanly (`ʌnmˈAkəɹ`).
- **One power and one weakness:**
  - **Power:** she can erase anything she can see. It's shown once, on a thing: the courtyard gate dissolves into the dark.
  - **Weakness:** only what she can see. Line of sight is the whole rule.
- **Shown as a tactical puzzle:** a top-down courtyard plan in code. Her sight is a cone that sweeps the yard, and it is ray-cast against the cover every frame, so the pillars and the well throw real blind spots.
  - The heroes add smoke, fog and a wall, one per spoken word, and each cuts a new shadow out of the cone.
  - "Every shadow becomes a path": a dotted route draws from the gate through the shadows to her door, and three tokens walk it.
- **The puzzle cuts both ways:** she plans too. A mirror bends her sight, the lanterns burn and she stands higher.
- **One shareable thought:** "Unbeatable is boring. A weakness turns a fight into a puzzle."
- **Arc finale nod, in one line:** the lesson shows a small row, CAN · CAN'T · COSTS · CONSEQUENCES · WEAKNESS, with the last word in ember. It's on screen only and isn't spoken.
- **Platform-safe:** her power only ever touches a thing (a gate). The heroes are tokens on a plan, or hooded figures with their faces unseen. The threat is implied by the beam and what it would touch, with no harm shown. Clothing is plain invented cloaks, with no sigils or real-world symbols.
- **Scope guard within Arc 5:**
  - EP21 (the can / can't / costs framework): there, "can't" is a limit on what the magic can do. Here it's a tactical weakness of one caster, and the framework isn't re-taught.
  - EP22 (cheap magic and its ripples): no social consequences are explored.
  - EP23 (creative costs: Wren's memory ledger): her power has no price at all.
  - EP24 (magic vs technology; no branch yet): nothing about logistics or replacing tools.

### How EP25 varies the series rhythm

| | EP21 | EP22 | EP25 |
|---|---|---|---|
| Hook | A blank spell page | The cheap power itself | **The caster as a searchlight:** a cloaked figure on a balcony whose lilac sight sweeps a misty castle; "THE TERRIFYING WIZARD / isn't unbeatable." |
| Spine | The page fills in, one plate per question | Rings of consequence, one plate per ring | **Cut between the ground and the war table:** two plates (the gate erased; the heroes waiting by a column) alternate with a code-drawn top-down plan where the sight cone and its blind spots are live geometry |
| Turn | The answers write a plot | The last ring finds a death | **The puzzle cuts both ways:** her sight bends off a mirror and a lantern flares; "She plans too" |
| Lesson | The sigil ignites | All rings on the dimmed map | The solved plan lifts; the arc row; "UNBEATABLE IS BORING / A weakness turns a fight into a puzzle." |
| CTA | Save | Share | **Follow** ("HALFWAY THERE", 25/50), over the hook balcony by night |

## 1. Research note (only what could have changed)

- **Platforms:** limits, hashtags and AI-disclosure rules haven't changed since the 2026-10-19 research (`docs/DISTRIBUTION.md`).
  - The YouTube title is 57/100 characters and the TikTok caption 251.
  - Instagram's hook line is the first 21 characters.
- **Exchange rate:** ₱63.35 = $1 (BSP reference, 22 Oct 2026). It's nine days old, so I didn't re-check it.
- **Figma:** the Starter plan is out of AI credits until **1 Nov 2026**. Today is 31 Oct, so I used the free local route without asking, as the brief says.
- **Paid services:** no Runway, ElevenLabs or Creatomate keys were used. AWS credentials exist in the environment but weren't used.
- **The idea:** that limitations make powers more interesting than raw strength is widely cited fantasy craft advice. "Line of sight" is a standard tactical constraint in tabletop games. The episode makes the point in its own words, and the caster is invented.
- **Parallel episodes:**
  - EP23 had only a WIP commit (`944d2e2`) when I started, but had **finished by the final push** (`ea4989c` "EP23: Make Magic Expensive Without Using Mana", then `50fbfa3`). It is merged into this branch.
    - The conflicts were all side-by-side additions (README, COSTS, STYLE, `score.py`, `Graphics.tsx`), and both sides are kept, EP23's first: `LEDGER` and `SIGHTLINE` are both registered, and `recall`/`forget` sit beside `gaze`/`unmake`.
    - DISTRIBUTION is EP23's file with the EP25 section appended, to avoid git interleaving the caption sections.
    - After the merge, `tsc` passes, and one still each of ep23 (frame 330, the ledger at the door) and ep25 (frames 470 and 820, the plan and the CTA card) renders correctly.
  - EP24 was still WIP at the final push (`5ddc861`, "EP24 (WIP): …"), so it isn't merged.
  - No names collide. EP23 adds `memoryLedger`, `fadingName`, `recall` and `forget`; EP25 adds `gazeBeam`, `unmake`, `sightPlan`, `gaze` and `unmake` (SFX).

## 2. Stack

Same stack as EP11–EP22:
- **Stills:** 4 from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences:
  - SDXL base 1.0: CreativeML OpenRAIL++-M;
  - ByteDance SDXL-Lightning: OpenRAIL++.
  
  Both allow commercial use with use-based restrictions, which this series meets.
- **Graphics:** Remotion, all code. The plan replaces two plates, so this episode needs only 4 stills.
- **Voice:** Kokoro `af_heart` narration.
- **Sound:** synthesized score (C minor → C major) and SFX.
- **Checks:** `qa.py`, a contact sheet and beat frames.

New in this episode (`src/graphics/Sightline.tsx`, registered in `Graphics.tsx`):
- `gazeBeam`: her sight as a pale lilac beam along a list of points (her eye, any mirror bounces, the end). It widens with distance, draws out on its cue, sways like a searchlight, flares on cues and carries drifting motes. It is pinned to the plate with `"local": true`.
- `unmake`: an outline that lights up, then dissolves cell by cell from where the gaze lands into a dark void, shedding motes. It's only for things.
- `sightPlan`: the top-down puzzle board.
  - The yard, her eye on the wall, and a sweeping sight cone ray-cast every frame against the `blocks`. Blocks are stone rects or circles, `smoke`, `fog` or `wall`; each can grow in on a cue and burn off with `until`.
  - A `route` with three tokens that walk it by `moves`; `catch: true` turns a lit token rust.
  - Labels, `liftAt` / `lift`, an `arcRow` and the lesson text, as in `rippleMap`.
- **SFX `gaze`** (the signature of her sight, reused every time it lights: the hook, the gate, the plan, over the heroes, the mirror) and **SFX `unmake`** (the one erasure: an inward rush, a falling tone and fine crackles, with no impact).
- **Motif colour:** **gaze `#c7b8f5`** (pale lilac), used only for her sight. Everything else stays on the series palette: amber for the heroes' route and tokens, ember for the destination.

## 3. Narration (74 words, measured 29.69 s)

> The secret to a terrifying wizard isn't making them unbeatable. / Meet the Unmaker. Anything she can see, she can erase. / But only what she can see. / So the heroes stop fighting, and start thinking. / Smoke. Fog. A wall. Every shadow becomes a path. / And she has to plan too: mirrors, lanterns, a higher tower. / Unbeatable is boring. A weakness turns a fight into a puzzle. / Follow for more ways to make fictional powers interesting.

- The first pass measured 28.79 s, with only 1.75 s on the plan.
- I lengthened five pauses: after the hook (+0.1 s), "erase" (+0.1 s), "can see" (+0.35 s, so the blind spots read), "thinking" (+0.1 s) and "path" (+0.25 s). That brought it to 29.69 s.
- The second "she" in L2 is addressed with `nth: 2`.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.32 | "The secret to a terrifying wizard isn't making them unbeatable." | The cloaked Unmaker on an arched balcony over a misty castle; her lilac sight sweeps the mist; THE TERRIFYING WIZARD / *isn't unbeatable.* | The caster as a threat |
| 2 | `erase` | 4.32–8.10 | "Meet the Unmaker. Anything she can see, she can erase." | The courtyard gate at dusk; her beam slants in, the gate's edge lights, and on "erase" it dissolves into the dark; THE UNMAKER / *Sees it. Erases it.* | The power, shown once on a thing |
| 3 | `plan` | 8.10–10.20 | "But only what she can see." | The top-down courtyard: her eye on the wall, the sight cone opening and sweeping, blind spots behind the pillars and the well; BLIND SPOT chips; THE WEAKNESS / *Line of sight* | The weakness, made visible |
| 4 | `heroes` | 10.20–12.99 | "So the heroes stop fighting, and start thinking." | Three hooded adventurers by a great column; a lilac sweep passes above; THE HEROES / *Think, don't fight* | What the weakness does to the other side |
| 5 | `path` | 12.99–16.81 | "Smoke. Fog. A wall. Every shadow becomes a path." | The plan: SMOKE, FOG and WALL drop in on their words and each cuts a new shadow; a dotted route draws through the shadows to her door and three tokens walk it; THE PUZZLE / *Make your own shadows* | The puzzle, solved |
| 6 | `mirror` | 16.81–21.10 | "And she has to plan too: mirrors, lanterns, a higher tower." | The Unmaker beside a huge oval iron mirror frame; her sight strikes it and bends away across the castle; the lantern flares; HER MOVE / *She plans too* | The turn: the puzzle cuts both ways |
| 7 | `lesson` | 21.10–25.23 | "Unbeatable is boring. A weakness turns a fight into a puzzle." | The solved plan lifts; CAN · CAN'T · COSTS · CONSEQUENCES · WEAKNESS; UNBEATABLE IS BORING / *A weakness turns a fight into a puzzle.* | The lesson and the arc nod |
| 8 | `cta` | 25.23–29.68 | "Follow for more ways to make fictional powers interesting." | The hook balcony by night, her sight still sweeping; CTA card (Episode 25 / 50, HALFWAY THERE, Follow pill); cross-fades to the hook | Follow CTA; loops |

## 5. Generated assets

- **Plates**, from local SDXL-Lightning (the prompts are in each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: the Unmaker on the balcony, seed 23 (round 1);
  - `plates/erase.jpg`: the wooden courtyard gate, seed 11 (round 1, daylight graded to dusk with `plateLook`);
  - `plates/heroes.jpg`: three hooded figures by a great column, seed 11 (round 2);
  - `plates/mirror.jpg`: the Unmaker beside the oval mirror frame, seed 7 (round 2).
- **14 candidates in two rounds:**
  - Round 1 (8 images, seeds 11 and 23): both hooks look out over a misty city rather than down into a courtyard, so the beam reaches into the mist instead. Both heroes plates show people loitering, not hiding. Both mirror plates left the mirror out entirely.
  - Round 2 (6 images, seeds 7, 11 and 23): heroes and mirror re-prompted. The mirror now leads the prompt and is described as "taller than a person", which gave a huge oval frame.
- **Code-drawn:** her sight and every bounce, the erasure, the whole courtyard plan (cover, smoke, fog, wall, the sight cone and its shadows, the route and tokens), the lantern glow, and all type. The plates show the world and people, never magic.
- **Subtitles and cover:** `ep25.srt` (18 cues) and `Worldcraft_Short_E25_cover.jpg` (the hook at 2.3 s, with the title and the beam).

## 6. Final video and verification

- **Sent with SendUserFile:**
  - `out/ep25.mp4` (master, 37.1 MB);
  - `out/ep25_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 21.6 MB).
- **Used on the preview page:** `ep25_download.mp4` (two-pass 3300k, 13.3 MB) and `ep25_player.mp4` (CRF 26, 7.2 MB), both with the master's audio copied.
- **QA:** `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 29.72 s, −14.1 LUFS, true peak −1.5 dB. The compat copy, with its AAC re-encoded, measures −14.2 LUFS and −1.3 dB. The download copy published on the preview page (https://claude.ai/artifact/MNrHBuYpjMPnwaeEhoc4VL) was read back with Artifact `read`: it is byte-identical (sha256 `a3b37372…`) and `qa.py` passes (29.72 s, −14.1 LUFS, TP −1.5 dB).
- **Fixes made after inspecting the beat frames and the contact sheet:**
  - The sight cone didn't draw at all on the first beat stills: the sweep's phase was taken from a cue object without resolving it to a time, which gave NaN. It now resolves the cue, and the cone sweeps continuously across all three plan shots.
  - The hook's kicker wrapped to two lines. It's now THE TERRIFYING WIZARD / *isn't unbeatable.*, and the hook beam is wider and brighter.
  - The heroes' hoods sat in the caption band. The plate is now ×1.20 and lowered 185 px (margin 192 px, so no edge shows).
  - The arc row landed while the plan was still lifting. The lift now starts 0.1 s before the lesson shot, and the row waits for "is".
- **Accepted compromises:**
  - The hook looks out over a misty castle rather than down into the courtyard of the plan; the plan is a separate "war table", not a literal map of the plate.
  - The mirror is an ornate oval iron frame you can see through, not a silvered glass. The bending beam carries the idea.
  - Her hair is uncovered on the mirror plate but hooded on the hook plate.
  - Only one lantern is visible, although the line says "lanterns".
  - On "a path" the tokens are still passing the wall label; they reach the door just before the cut.
- **Not verifiable by me:** how the narration and mix sound, including the new `gaze` and `unmake`. I can't hear audio; please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `gazeBeam` | Any sight, scrying, searchlight, lighthouse or line-of-fire on a plate, with mirror bounces (EP27 dragons scanning a valley; EP40-style surveillance) |
| `unmake` | Anything that vanishes: a spell erasing a thing, a ruin fading from memory, a border wiped from a map |
| `sightPlan` | Any tactical or stealth puzzle seen from above: a siege, a guarded vault, a predator's hunting cone (EP26's ecosystem could reuse the cone for a predator's range) |
| SFX `gaze`, `unmake` | Watching or scrying magic; something ceasing to exist |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 4 stills (14 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 4 stills: about **$1.05 (₱67)**, or about $2.20 (₱139) with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

The source of truth is `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 25`. The AI label is ON for every platform.

The pinned comments ask viewers to give their strongest caster one weakness and say what a clever hero would do with it, which turns the lesson into the comment game. The description carries the arc nod: "Can, can't, costs, consequences, and now weakness."

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The searchlight caster and "isn't unbeatable" | Open on the plan: her cone sweeping, one token frozen in a blind spot, "She can erase anything she sees. Where do you hide?" | Viewed vs swiped away; average % viewed |
| 2 | Spine | Alternating plates and plan | Plan only, with small inset plates on each move | Retention 8–17 s; rewatch rate |
| 3 | CTA | Follow (from the plan, at the halfway mark) | Comment: "Give your strongest caster one weakness." | Follows per 1,000 views vs comments per 1,000 |

Also track how many comments propose a weakness *and* a tactic that exploits it; that shows the "puzzle" idea landed.

## 11. How to produce EP26 ("Don't Design a Monster. Design an Ecosystem.", opening Arc 6: Creatures and Species)

1. **Branch:** `claude/worldcraft-ep26` from `claude/worldcraft-ep25`, which has EP01–EP23 and EP25. EP24 wasn't finished when EP25 was pushed: merge it if it has since landed, keeping both sides of every doc, SFX and graphics registration.
   
   **Read:**
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief, EP22's (ripples) and EP08's (the pull-back).
2. **Stills:** Figma credits reset on **1 Nov 2026**. On or after that date, if Figma would be clearly better (creatures are hard for SDXL), ask with AskUserQuestion first: about 4 images, up to 6.
   
   Otherwise:
   - run `python pipeline/local_stills.py ep26 <shots> --seeds 11 23`, adding seed 7 for creatures or hands;
   - `--pick`;
   - `plates.py --register` **and `pipeline/build.sh`**.
   
   Name each prompt after its shot id. Run nothing heavy alongside.
   
   When waiting on it, `pgrep -f "[l]ocal_stills.py"`: a plain `pgrep -f local_stills.py` inside a shell loop matches the loop itself and never ends.
3. **Story (plan):** a giant predator that "eats everything" raises the question of why everything isn't extinct.
   - Show one invented predator's place in a food web: prey, territory, energy, breeding season, and what limits its numbers.
   - Keep it biology, not fights: no kills on screen; show hunger through an empty range or a migration.
   - **Don't repeat** EP22's ripple map or EP25's sight plan.
   - **One idea:** a food-web pyramid drawn in code, each tier lit as a plate is shown, with the predator's tier deliberately small; or `sightPlan` re-skinned as a territory map with the predator's hunting range as the cone, and prey moving through the gaps.
   - **Scope:** EP27 is what dragons change for people, EP28 is intelligent species, and EP29 is immortality.
4. **Narration:** about 70–78 words, measured with `cd pipeline && python tts.py ep26`. Check invented names in the G2P, and use `nth` for repeated words in cues.
5. **Then:**
   - `pipeline/build.sh ep26` → render with `--browser-executable` (the headless shell is at `/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`) → `qa.py` → sheet and beat frames, including the loop tail;
   - the compat, two-pass download and player encodes, all `-c:a copy`, with `qa.py` on each;
   - `srt.py`, `storyboard.py`, the cover, and an 11-section brief;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
