# EP24 production brief: Why Teleportation Doesn't Replace the Road

**Series:** Worldcraft Shorts, Episode 24 / 50. Fourth episode of **Arc 5: Magic and Its Rules**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "If teleportation exists, why are merchants still using horses?" Topic: magic and technological development. Core message: consider range, reliability, cost, availability, safety and infrastructure; teleportation might need rare crystals while horses stay cheap and dependable. CTA: "What technology would magic replace first in your world?"
**Deliverable:** a 31.3 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. The AI disclosure is on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`. `make_ep24.py` writes `episode.json` (prompts in `prompts.json`, plate geometry in `geom.json`).

## The brief

- **One idea:** magic doesn't replace technology just by existing. It has to beat the ordinary tool on price, range, reliability and availability, and an ordinary tool that is cheap, dependable and everywhere wins most days. Magic takes the narrow jobs where its one advantage is worth its price.
- **One magic, one ordinary rival:** a crystal teleport gate against a muddy road of carts and horses. No realm name is spoken or shown; "a crystal gate links two cities" is the whole rule.
- **Why the cart still wins**, each shown on its own plate and scored on a counting board:
  - **Cost:** each jump burns a crystal (40 crowns) worth more than the cargo (a cart of cabbages, 12 crowns);
  - **Range:** it reaches one other city, and every village still needs the road;
  - **Reliability:** one jump in a hundred fails (the gate stutters and collapses on screen);
  - **Availability:** the guild rations the rest.
  
  **Then the turn, where the gate does win:** speed, but only for what can't wait (medicine, royal mail). The last bead flips to the gate as a courier walks into the light.
- **One shareable thought:** "Magic doesn't replace technology. Price, range and reliability decide who uses what." On screen: MAGIC DOESN'T REPLACE TECHNOLOGY / *Price, range and reliability decide who uses what.*
- **Safety and infrastructure** (from the plan's list) are carried by the failing gate (a failed jump is the safety problem, shown as a collapse and rust sparks, never harm) and by the road itself; the board keeps four rows plus speed so each one reads.
- **Platform-safe:** no harm to anyone. The failure is shown on the gate, not on a traveller. No real religious symbols: two small spire finials that could read as crosses were painted out of the gate and queue plates (using the plates' own sky), and a round-1 courier plate with a domed, church-like arch was rejected.
- **Scope guard within Arc 5:**
  - EP21 (the can / can't / costs framework) isn't re-taught.
  - EP22 (cheap magic changes society): this magic is expensive and rare, and the episode doesn't follow ripples.
  - EP23 (creative costs; produced in parallel, WIP at the final push): the crystal's price is a market price, noted once on one chip. No cost to the caster, no memory, no ledger strikes.
  - EP25 (weaknesses that make casters interesting): the 1-in-100 failure is a statistic of a machine, not a caster's weakness.
  - EP07 (why settlements are where they are) and EP10 (chokepoints) are only nodded to: the village at the end of the track.

### How EP24 varies the series rhythm

| | EP07 | EP14 | EP22 | EP24 |
|---|---|---|---|---|
| Hook | The empty valley | One person re-captioned | The cheap power at work | **The contradiction in one frame:** a wagon train on a muddy road, with the gate shimmering on the field beside it: "TELEPORTATION EXISTS / *So why horses?*" |
| Spine | `reasonTally` icons counting up | A verdict scale tipping | Ripples, one plate per ring | **A counting board scored live:** a walnut and brass board rides at the top of four plates; each question adds a row and its bead slides to the CART, the winner's note brightening |
| Turn | The city appears | The scale comes level | The last ring finds a death | **One bead flips:** SPEED slides to the GATE in lilac as a courier with the royal mail walks into the open gate |
| Lesson | Sum card | `lessonStack` | All rings on the map | The full board over the dimmed road, tally 1 · MOST DAYS, THE CART · 4, then it shrinks and the principle lands |
| CTA | Comment | Comment | Share | **Comment** (the road at dusk, the gate still shimmering) |

The board is deliberately unlike EP07's `reasonTally` (icons in a row), EP14's `verdictScale` (a balance), EP13's split frame and EP23's `memoryLedger` (a parchment card with lines struck in rust): it is a physical counting device, nothing is struck out, and the score is where the beads end up.

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules haven't changed since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 58/100 characters, the TikTok caption 241, and Instagram's hook line is the first 28.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Nine days old and stable, so I didn't re-check it.
- Figma: the Starter plan is out of AI credits until **1 Nov 2026** (today is 31 Oct), so I used the free local route without asking, as the brief says.
- No Runway, ElevenLabs or Creatomate keys were used. AWS credentials exist in the environment but weren't used.
- The idea: that magic must compete with ordinary technology on cost, range, reliability, availability, safety and infrastructure (and that a rare-fuel teleport would be a luxury service) is standard worldbuilding craft advice. The episode makes no claim about any real transport history.
- Parallel episodes: EP23 ("Make Magic Expensive Without Using Mana") had pushed only a WIP commit (`944d2e2`: script, `memoryLedger`, `fadingName`, `recall`/`forget`) when I started, so EP24 was written around it: its price is a market price, not a cost to a caster, and its board is a counting device, not a ledger with struck lines. **Before the final push EP23 had finished** (`ea4989c` "EP23: Make Magic Expensive Without Using Mana", then `50fbfa3`), so it is merged into this branch. The conflicts were in `README.md`, `docs/COSTS.md`, `docs/DISTRIBUTION.md`, `pipeline/score.py` and `src/graphics/Graphics.tsx`, all additions on both sides; every side is kept in episode order (EP23's `recall`/`forget` before EP24's `blink`/`gateFail`/`crystalBurn`/`bead`, `LEDGER` before `GATE`). Git interleaved the DISTRIBUTION caption sections, so that file was rebuilt as EP23's version plus the EP24 section. EP23 changes no shared component (it adds `Ledger.tsx`). After the merge, `tsc` passes, and one ep23 still (the storm, with its ledger) and one ep24 still (the queue, with the board) render correctly.

## 2. Stack

Same stack as EP11–EP22:
- 6 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++. Both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics, all code. The gate's light, its failure, the crystal and the stone ring on the hook's hill are drawn in code over the plates and pinned with `"local": true`.
- Kokoro `af_heart` narration.
- Synthesized score (D minor → D major) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode (`src/graphics/Gate.tsx`):
- `gateRing`: the gate's surface inside a stone ring on the plate. A faint lilac shimmer when idle, a turning swirl with a bright rim when it opens, a white flash and ring for each jump, and on `failAt` three stutters and a collapse to a point with rust sparks. `stone: true` draws the ring itself (the hook's distant gate, which SDXL wouldn't paint), and `occlude` masks a figure out of the light so the courier stays in front of it.
- `crystalPrice`: a floating crystal with a price chip that burns to lilac dust and turns the chip rust.
- `countingBoard`: the comparison device (above). It carries across shots with `enter: false`, `all` shows a recap, `score` adds the tally, and `moveAt` / `lessonText` make the lesson.
- `blink`, `gateFail`, `crystalBurn` and `bead` SFX (`pipeline/score.py`). `blink` is the gate's signature sound and is reused every time it opens or something goes through (the hook, the gate shot twice, the courier twice); `gateFail` is the same cluster stuttering and collapsing; `bead` plays on every row of the board.
- Motif colour: **crystal `#c4b5f7`** (pale lilac), used only for the gate, the crystal and the gate's side of the board. Everything else stays on the series palette, with amber for the cart and rust for the failure.

## 3. Narration (77 words, measured 31.26 s)

> If teleportation exists, why are merchants still using horses? / Here, a crystal gate links two cities. / Each jump burns a crystal worth more than the cargo. / It reaches one city. Every village needs the road. / One jump in a hundred fails. The guild rations the rest. / So it carries only what can't wait: medicine, royal mail. / Magic doesn't replace technology. Price, range and reliability decide who uses what. / What technology would magic replace first in your world?

The first pass (78 words) measured 32.07 s, with the lesson line alone 5.4 s. I kept the shareable line whole, dropped "still" from "every village still needs the road" and shortened four pauses, which brought it to 31.26 s (QA window 27–33 s). No invented name is spoken.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.22 | "If teleportation exists, why are merchants still using horses?" | A wagon train on a muddy road in the rain; on the field by the bend a stone ring gate (code) shimmers and flashes on "teleportation"; "TELEPORTATION EXISTS / So why horses?" | The contradiction |
| 2 | `gate` | 4.22–6.82 | "Here, a crystal gate links two cities." | A stone ring in a town square, a merchant in a blue coat beside it; its opening fills with a lilac swirl and flashes; THE GATE / *Two cities, one blink* | The one magic |
| 3 | `cargo` | 6.82–9.72 | "Each jump burns a crystal worth more than the cargo." | A cart heaped with cabbages; a crystal (ONE JUMP / 40 crowns) burns to dust; CARGO / 12 crowns; the counting board arrives: COST → cart | Cost |
| 4 | `village` | 9.72–12.90 | "It reaches one city. Every village needs the road." | A thatched hill village at the end of a muddy track, a cart arriving; RANGE → cart | Range |
| 5 | `queue` | 12.90–16.75 | "One jump in a hundred fails. The guild rations the rest." | Two travellers wait at a framed ring gate; the open gate stutters and collapses; RELIABILITY and AVAILABILITY → cart | Reliability, availability |
| 6 | `courier` | 16.75–20.82 | "So it carries only what can't wait: medicine, royal mail." | Night; a hooded courier walks into a stone arch as the gate opens in it (courier occluded in front of the light); SPEED → **gate**; a jump flash on "mail" | The turn: where magic wins |
| 7 | `lesson` | 20.82–26.75 | "Magic doesn't replace technology. Price, range and reliability decide who uses what." | The dimmed road; the full board, tally 1 · MOST DAYS, THE CART · 4; it shrinks and the principle lands beneath | The lesson |
| 8 | `cta` | 26.75–31.26 | "What technology would magic replace first in your world?" | The hook road at dusk, the gate still shimmering; CTA card with the "Comment below" pill; cross-fades to the hook | Comment CTA; loops |

## 5. Generated assets

- The plates, from local SDXL-Lightning (prompts in `prompts.json` and each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: the wagon train on the muddy road, seed 11 (round 1);
  - `plates/cargo.jpg`: the cabbage cart, seed 23 (round 1);
  - `plates/village.jpg`: the hill village, seed 23 (round 1);
  - `plates/gate.jpg`: the stone ring in the town square, seed 23 (round 2);
  - `plates/queue.jpg`: two travellers at a framed ring gate, the round-2 **gate** prompt at seed 7 (used for the queue shot);
  - `plates/courier.jpg`: the courier at the night arch, seed 7 (round 2).
- **21 candidates in two rounds:**
  - round 1, 12 images (seeds 11, 23): no gate plate had a stone ring at all (one painted a giant boulder on a cart); one courier plate had a domed, church-like arch. Hook, cargo and village were kept.
  - round 2, 9 images (seeds 11, 23, 7) for gate, queue and courier, re-prompted as "a giant circular stone ring portal standing upright on its edge … a round hole through its middle". Two of three gate seeds painted the ring. All three queue seeds were rejected (one with a cross on a gable, one with the arch too high for the board, one with monastic robes), so the queue shot uses the gate prompt's seed 7.
- **Retouched:** two small spire finials (one on the gate plate, two on the queue plate) that could read as crosses were painted out with each plate's own neighbouring sky.
- **Code-drawn:** the gate's light, swirl, flashes and failure; the stone ring on the hook's field; the crystal and its price; the counting board; all type. Plates show the world and people, never magic.
- `ep24.srt` and `Worldcraft_Short_E24_cover.jpg` (the hook at 2.6 s with the title).

## 6. Final video and verification

- `out/ep24.mp4` (master, 37.7 MB) and `out/ep24_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 21.6 MB): sent with SendUserFile.
- `ep24_download.mp4` (two-pass 3300k, 14.0 MB) and `ep24_player.mp4` (CRF 26, 6.7 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 31.27 s, −14.0 LUFS, true peak −1.4 dB (the compat copy, with its AAC re-encoded, measures −14.1 LUFS / −1.4 dB). Preview page (private): https://claude.ai/artifact/9WySrA5jw73nG3P6QZiMDm, with the player copy in the asset store and a Download MP4 button (`downloads` capability) serving `ep24_download.mp4`. That published file was read back: byte-identical to the local copy (sha256 `0ae9e14c…`) and `qa.py` **passed** on it (31.27 s, −14.0 LUFS, TP −1.4 dB).
- Fixes made after inspecting the beat frames and the contact sheet (two full renders):
  - the code-drawn stone ring on the hook first sat on the far ridge beside the title, where it read as a dark letter "O"; it now stands on the field at the road's bend, lighter and larger;
  - the courier's gate light overran the arch and covered the courier; it is smaller and lower, and the courier is masked out of it (`occlude`), so he walks into the light;
  - the crystal burned 0.3 s after appearing; it now shows from the start of the shot and burns on "worth";
  - the hook's gate also shimmered behind the CTA text; it was removed from the CTA (the loop still lands on it);
  - the losing side's notes on the board were too dim (38 %); they're now 50 %;
  - spire finials that could read as crosses were painted out of the gate and queue plates (section 5);
  - the plates were reframed to keep faces and key points out of the caption band and under the board: gate ×1.12 raised 100 px, cargo ×1.2 lowered 180 px, queue ×1.3 raised 280 px, courier ×1.1 lowered 80 px.
- **Accepted compromises:**
  - The gate looks different in each plate (a free-standing ring, a ring in a stone frame, an arch at night, and a small code-drawn ring on the hook's field). SDXL wouldn't paint one consistent gate; the lilac light, the `blink` sound and the board tie them together.
  - The queue shot shows two travellers waiting, not a long queue (all three queue seeds were rejected); the board's AVAILABILITY row and "the guild rations the rest" carry the rationing.
  - The board is empty for about a second at the start of the cargo shot before COST lands; the header (GATE / WHO WINS? / CART) introduces it.
  - Runtime is 31.3 s, a little over the 30 s target (inside the 27–33 s window), to keep the shareable line whole.
  - The SDXL costumes and towns are generic old-European. The gate, the guild, the crystal and the story are original; no plate shows a real place, people, flag or religious symbol.
- **Not verifiable by me:** how the narration and mix sound, including the new `blink`, `gateFail`, `crystalBurn` and `bead`. I can't hear the audio; please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `gateRing` | Any portal, scrying pool or warded doorway on a plate; `failAt` for a spell that breaks down (EP25's weaknesses), `occlude` whenever a figure stands in the light |
| `crystalPrice` | Any priced resource that is consumed: a spell's reagent, a toll, a ration |
| `countingBoard` | Any two-way comparison scored row by row (magic vs mundane, two kingdoms, two careers); rows can go either way and the tally falls out |
| SFX `blink`, `gateFail`, `crystalBurn`, `bead` | Portals and translocation; a spell failing; a consumed resource; counting or scoring anything |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 6 stills (21 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 6 stills: about **$1.10 (₱70)**, or **$2.48 (₱157)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 24`. The AI label is ON for every platform. The pinned comments turn the board into the comment game: score your own magic against one ordinary tool, or name a job magic should have killed and say why it survives.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The wagon train with a small gate shimmering by the road | Open on the gate failing mid-jump: "One in a hundred of these fails. Would you send your cargo?" | Viewed vs swiped away; average % viewed |
| 2 | Spine | The board rides over four plates | A literal race: the cart and a crystal-powered jump scored on a split timeline, each problem a delay on the gate's side | Retention 6–17 s; rewatch rate |
| 3 | CTA | Comment: what would magic replace first? | Comment: "Score your magic vs one ordinary tool: who wins?" | Comments per 1,000 views; share of comments naming a *reason* (cost, range…) |

Also track how many comments name a *limit* on the magic rather than just a technology, which shows the lesson landed.

## 11. How to produce EP25 ("The Strongest Magic System Has Weaknesses"), closing Arc 5

1. Branch `claude/worldcraft-ep25` from `claude/worldcraft-ep24`, which has EP01–EP24 (EP23 merged). Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief and the EP21, EP22 and EP23 briefs, so the arc's closer doesn't repeat any of them.
2. **Stills:** Figma credits reset on **1 Nov 2026**. If it's on or after that date and Figma would be clearly better (it would likely paint key props like the ring that SDXL ignored), ask with AskUserQuestion first (about 4 images, up to 6; plan key `team::1384938462301182142`). Otherwise use `python pipeline/local_stills.py ep25 <shots> --seeds 11 23` (add 7 for hands), `--pick`, `plates.py --register` **and `pipeline/build.sh ep25`**. Run nothing heavy alongside it, and budget a second round. SDXL won't paint unusual key objects even when they're the subject: describe them as plain physical shapes ("a giant circular stone ring standing upright on its edge"), and draw anything smaller in code. Check every spire and gable for crosses.
3. Story (plan): weaknesses make casters interesting. One caster, one strong power, one weakness that creates choices (not a cost, which was EP23). Show the weakness through a situation the caster must plan around, never injury.
   - `gateRing` `failAt` and `mendGlow` `failAt` both suit a power that cuts out; `countingBoard` could score a powerful and a weak caster, but don't reuse it as the spine.
   - As the arc's closer, the lesson can briefly gather Arc 5's four answers (can/can't/costs, cheap ripples, a real price, magic vs tools) before the weakness lands, without re-teaching them.
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep25`; target 30 s and trim pauses before words.
5. Then the usual: build → render (the Chromium headless shell is under `/opt/pw-browsers/chromium_headless_shell-1243/*/chrome-headless-shell`) → `qa.py` → sheet and beat frames, including the loop tail; compat, two-pass download and player encodes (`-c:a copy`, `-passlogfile` before the output), `qa.py` on each; `srt.py`, `storyboard.py`, cover, 11-section brief; docs; a new preview page with a Download MP4 button; SendUserFile; commit and push to the episode branch.
