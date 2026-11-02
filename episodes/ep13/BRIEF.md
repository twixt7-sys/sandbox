# EP13 production brief: Every Culture Has Something It Considers Shameful

**Series:** Worldcraft Shorts, Episode 13 / 50. Third episode of **Arc 3: Civilization and Culture**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "In one kingdom, refusing a gift is an insult. In another, accepting it is." Topic: cultural taboos. CTA: "Share this with a writer who wants believable cultural differences."
**Deliverable:** 30.9 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** a taboo feels real when it has a reason inside its own culture. Give two neighbours opposite rules about the same act, and polite people on both sides insult each other without meaning to.
- **One example:** two names, one gesture.
  - **Adren**, the hill country: a gift binds two families. Refusing one says you'll never need them. The reason, shown on screen: *hill winters are shared.*
  - **Vesk**, the river city across the water: a gift is a debt. Accepting one says you can be bought. The reason: *debts get called in.*
  - **The collision:** on the border bridge, an Adren envoy offers the same blue box and a Vesk magistrate courteously refuses. Both are polite. Both are insulted: "You scorn us." / "You think I'm for sale."
- **One shareable thought:** "Write the rule and the reason, and the conflict writes itself."
- **Neither side is silly or villainous:** each rule is shown from the inside as a sensible answer to how that people lives (hard winters; a trading city), and both hosts are calm and courteous.
- **Scope guard:**
  - EP11 (one people's whole value system, read by an outsider) wasn't pushed when this was made, so I couldn't check its example. EP13 is specifically **two** rule-sets colliding over one act. Nobody is an outsider, both sides misread.
  - EP12 (pushed; merged into this branch): a festival with a forgotten origin. EP13 has no festival, ritual or history; it's a living etiquette rule. Its `originLedger` is a two-column card too, but it carries EP12's example over plates (now / then); EP13's `mirrorLedger` is only the lesson, on the night sky, with the clash arrows as its point.
  - EP14 (honour, freedom vs duty) comes next, so EP13 stays on etiquette and taboo. Nothing about right and wrong, only what counts as polite.
- **Real-culture check:** gift refusal and reciprocity customs exist in many real societies. Both cultures here are invented (dress, architecture, the gift object), and the first Vesk plate was rejected because its window showed a recognisably real city (Venice) and its bearded, skull-capped host in a money-and-debt scene read as an antisemitic stereotype.

### How EP13 varies the series rhythm

| | EP10 | EP12 | EP13 |
|---|---|---|---|
| Hook | The obvious answer, targeted | Pure joy, undercut | **Split frame:** the same gift on both sides of a border at once, each half lit as it's named, a rust INSULT stamp on each |
| Spine | Zoom in, then pull back (map) | Era shift: now ↔ then on matching plates | **Mirrored plates:** two matching compositions (giver left, host right, gift centred), then the border where they meet |
| Consequence | The realm goes dark | A head count with gaps | **One exchange, played twice:** the bridge plate split and framed on each person, with what each one heard |
| Lesson | `lessonStack` over the consequence | `lessonStack` over the punishment | `mirrorLedger`: rule and reason for each side, arrows meeting in a spark, "The conflict *writes itself.*" |
| CTA | Comment | Comment | Share (the bridge at dusk) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 62/100 characters, the TikTok caption 268 characters, and Instagram's hook line is the first 27.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Three days old, so I didn't re-check it.
- Still no Runway, ElevenLabs or Creatomate keys. AWS credentials exist but weren't used.
- Figma: you approved up to 6 generations, and 4 were used (one Vesk re-roll). The re-roll had to wait about 4 hours: the Starter plan's daily allowance ran out after the first 3, probably because other episode sessions generated the same day.
- The idea itself: different rules about gifts, hospitality and reciprocity are a well-documented source of cross-cultural misunderstanding. The episode only uses it through an invented example and makes no claim about any real people.

## 2. Stack

Same stack as EP06–EP12:
- 3 Figma stills (`gemini-3.1-flash-lite-image`, lanczos to 1080×1920);
- Remotion graphics (all code);
- Kokoro `af_heart` narration, with both names checked in Kokoro's G2P:
  - "Adren" → /ədɹˈɛn/ (uh-DREN);
  - "Vesk" → /vˈɛsk/;
- synthesized score (G minor → G major) and SFX;
- `qa.py` plus a contact sheet and beat frames.

New in this episode:
- `splitFrame` and `mirrorLedger` (`src/graphics/Culture.tsx`);
- `callout` `side: "up"` with `dx`, and `backdrop`;
- `giftSet` and `seam` SFX;
- captions no longer hold into a captions-off shot (`Captions.tsx`, and `srt.py --burned-only`);
- the loop tail now finds a hook's borrowed plate (`plateFrom`). Before, it faded into the procedural valley. No earlier hook borrows a plate, so earlier episodes are unchanged.

## 3. Narration (77 words, measured 30.94 s)

> In one kingdom, refusing a gift is an insult. In another, accepting it is. / In Adren, a gift binds two families. Refusing says you'll never need them. / Across the river, in Vesk, a gift is a debt. Accepting says you can be bought. / So the envoy offers. The magistrate refuses. / Both are polite. Both are insulted. / Write the rule and the reason, and the conflict writes itself. / Share this with a writer who wants believable cultural differences.

The first draft (78 words, "Both are being polite") measured 31.4 s. I dropped "being" and tightened four pauses, then gave "insulted" a full second so both reactions hold on screen.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–5.43 | "In one kingdom, refusing a gift is an insult. In another, accepting it is." | Split frame: Adren doorway above, Vesk hall below, the seam drawn across like a border; "ONE KINGDOM / Refuse it [INSULT]", "ANOTHER / Accept it [INSULT]" | The whole idea in one frame |
| 2 | `adren` | 5.43–10.33 | "In Adren, a gift binds two families. Refusing says you'll never need them." | The hill doorway: the host receives the box with both hands; tag "ADREN · THE HILLS / a gift is a bond"; callout "THE REASON / Hill winters are shared." | Rule 1, from the inside |
| 3 | `vesk` | 10.33–15.31 | "Across the river, in Vesk, a gift is a debt. Accepting says you can be bought." | The magistrate's hall: the same box, a raised palm; tag "VESK · THE RIVER CITY / a gift is a debt"; callout "THE REASON / Debts get called in." | Rule 2, equally sensible |
| 4 | `border` | 15.31–18.61 | "So the envoy offers. The magistrate refuses." | The bridge between hills and city; callouts "OFFERS" (amber) and "REFUSES" (rust) | The collision |
| 5 | `both` | 18.61–21.74 | "Both are polite. Both are insulted." | The bridge plate split, top framed on the envoy, bottom on the magistrate; "POLITE" on each, then "“You scorn us.”" / "“You think I'm for sale.”" | One exchange, as each side heard it |
| 6 | `lesson` | 21.74–25.69 | "Write the rule and the reason, and the conflict writes itself." | `mirrorLedger`: ADREN / VESK; THE RULE (Accept / Refuse the gift); THE REASON (Gifts bind families / Gifts are debts); arrows meet in a rust spark; "The conflict *writes itself.*" | Lesson |
| 7 | `cta` | 25.69–30.94 | "Share this with a writer who wants believable cultural differences." | The bridge at dusk; CTA card with "Share this" pill | Share CTA; loops to the split hook |

Motif colour: none beyond the series palette, though the sky-blue gift is the one recurring accent in every plate.
- Amber marks each culture's rule and the offer.
- Rust marks insult and refusal (the stamps, "REFUSES", what each side heard, the clash spark).

## 5. Generated assets

- The plates, from the Figma file "Worldcraft Shorts EP13 plates" in your drafts:
  - `plates/adren.jpg`: the hill doorway;
  - `plates/vesk.jpg`: the magistrate's hall (re-roll; the rejected first take is still in the Figma file but not in the repo);
  - `plates/border.jpg`: the bridge.
- The Adren and Vesk prompts share one composition paragraph (giver left third, host right third, heads about 38 % down, gift centred at chest height), so the two halves of the hook line up.
- The hook, the two-sided replay and the CTA reuse these plates.
- `ep13.srt` (17 cues) and `Worldcraft_Short_E13_cover.jpg` (the hook at 4.9 s, both stamps down).

## 6. Final video and verification

- `out/ep13.mp4` (master, 35.5 MB) and `out/ep13_compat.mp4` (H.264 Main, CRF 20, 20.5 MB): sent with SendUserFile.
- `ep13_download.mp4` (two-pass 3300k, 13.9 MB) and `ep13_player.mp4` (CRF 26, 6.3 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four files: 1080×1920, 30 fps, 30.98 s, −14.1 LUFS, true peak −1.4 dB.
- Fixes made after inspecting the sheet and beat frames:
  - the loop tail faded into the procedural valley, because the hook borrows its plate; fixed in `Episode.tsx`;
  - the bottom INSULT stamp fired on the first "is" of the hook line; it now cues the second (`nth: 2`), as does the music duck;
  - the two-sided split first used 1.25× crops that both showed both people; it's now 1.6× on each person;
  - the rust "heard" lines were lost over the bright river, so each half's label block got a soft dark band;
  - "insulted" was on screen for about half a second before the dissolve, so its pause is now a full second;
  - the lesson's last line collided with the captions, so the ledger moved up;
  - the reason callouts collided with the tags and then ran past x 920. They now rise straight up from the gift with a backdrop;
  - the "REFUSES" callout was lost against the pale city, so it's lighter and level with "OFFERS";
  - the last caption of the border shot spilled into the split, so captions now stop at any captions-off shot.
- **Accepted compromises:**
  - In the hook's bottom half, the Vesk gift sits at about y 1600, inside the zone platforms overlay, for those 5 seconds. Keeping both faces clear of the label means the gift can't go higher. The top half's gift, and every later shot, are clear.
  - The two split shots have captions off; their half labels carry the line.
- **Not verifiable by me:** how the narration and mix sound, including the new `giftSet` and `seam`. Please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `splitFrame` | Any "two sides at once": EP14 (two honour codes), EP15 invisible details, rival kingdoms, before/after, one event from two points of view |
| `mirrorLedger` | Comparing two peoples, factions or systems row by row, ending on what their difference produces |
| `callout` `side: "up"`, `dx`, `backdrop` | Notes too wide for a side leader; labels over bright windows and skies |
| Captions stop at captions-off shots | Any shot where on-screen type replaces captions mid-episode |
| SFX `giftSet`, `seam` | Gifts, offerings, ceramics; any split or border drawn across the frame |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 4 stills generated, 3 used (Figma AI credits, 4 of the approved 6) | $0 / ₱0 cash |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)** + 4 Figma generations |

On the paid primary stack: about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 13`. The AI label is ON for every platform. The pinned comments ask viewers for one of their own cultures' rules *and* its reason, and what a polite visitor would get wrong.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | Split frame with both stamps by 0:05 | Adren full frame first, then the split slams in on "In another" | Viewed vs swiped away; average % viewed |
| 2 | Collision | The bridge, then the split replay ("You scorn us." / "You think I'm for sale.") | Skip the full bridge shot; go straight to the split on "So the envoy offers" | Retention 15–22 s; rewatch rate |
| 3 | CTA | Share: "a writer who wants believable cultural differences" | Comment: "What does your culture refuse that its neighbour expects?" | Shares per 1,000 views (A) vs comments per 1,000 (B) |

Also track how many comments give a rule **with** its reason. That shows the lesson landed, not just the image.

## 11. How to produce EP14 ("Give Every Nation a Different Definition of Honor")

1. Branch `claude/worldcraft-ep14` from the branch with EP12 and EP13 merged, and EP11 too if it's pushed by then. Read:
   - `CLAUDE.md`, `docs/STYLE.md` and `docs/SERIES_PLAN.md`;
   - this brief and the EP11 and EP12 briefs.
2. **Ask before spending Figma credits.** Plan about 4 stills, up to 6 with re-rolls. Other episode sessions share the 150-a-day Starter allowance, so generate early in the day. The default is no public release.
3. Story:
   - Hook: "What if two honorable people could consider each other evil?"
   - Mechanism: one society prizes individual freedom, another collective duty. Both have understandable reasons, and neither is entirely right.
   - Scope: EP13 was etiquette (what's *polite*); EP14 is morality (what's *right*). Use one concrete dilemma that both sides answer honourably but oppositely: a deserter, a broken oath, a debt of blood. Don't reuse the gift.
   - Keep both sides sympathetic. No villain framing, no real-culture stand-ins.
4. Vary the rhythm again. `splitFrame` is the obvious tool, but don't repeat EP13's top/bottom mirror as the spine. Options:
   - a verdict scale or ledger that tips one way, then the other;
   - one person's choice shown first as heroism, then re-captioned as betrayal on the same plate (`callout` with two notes).
5. CTA: "Which matters more: personal freedom or collective responsibility?" This is a comment CTA (`ctaCard`, the default comment icon).
6. Narration should be about 70–78 words. Measure it with `cd pipeline && python tts.py ep14` before you lock the cues. Check names in the G2P, and use `nth` for repeated words in cues.
7. Then:
   - `pipeline/build.sh ep14` → stills → render → `qa.py` → sheet and beat frames (including the loop tail);
   - encodes: compat, a two-pass download copy and a player copy, all with `-c:a copy`;
   - `srt.py`, `storyboard.py`, the cover, and this brief's 11 sections;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
