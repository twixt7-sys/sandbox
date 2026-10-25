# EP12 production brief: Invent a Tradition With a Dark History

**Series:** Worldcraft Shorts, Episode 12 / 50. The second episode of **Arc 3: Civilization and Culture**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "What if a kingdom's most beloved festival began as a punishment?" Topic: cultural traditions with historical origins. CTA: "Invent a tradition and tell us how it began."
**Deliverable:** 30.6 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** a tradition gets compelling when what it means now differs from what it meant then. People keep the custom and lose the reason.
- **One example:** one festival and one town.
  - **Bellnight:** every winter the town of **Dunmere** camps outside its own walls, with hand bells, bonfires and a cheer when the gates open at dawn.
  - **The origin:** three hundred years ago, a king locked the whole town out for one winter night as a punishment.
  - **The mirror:**
    - bells → how people found each other in the snow;
    - bonfires → how they lived till morning;
    - the cheer at dawn → a head count.
- **One shareable thought:** "The custom survived. The reason was forgotten."
- **Scope guard:**
  - Not EP05's "build backward": this is a *living* tradition whose meaning drifted, not ruins.
  - No lanterns, so there's no echo of EP01's lantern river.
  - No contested history (EP31) and no old war that still matters (EP32).
  - EP11 isn't pushed yet, so I couldn't check its example. EP12 uses no clothing, greeting or meal moment, which is EP11's territory.
- **Platform safety:** the darkness is implied only by the barred gate, the blizzard, the huddled figures and four empty outlines in the head count. Nobody is shown hurt, and nothing on screen is violent.

### How EP12 varies the series rhythm

| | EP09 | EP10 | EP12 |
|---|---|---|---|
| Hook | The wrong image struck out | The obvious answer, targeted | **Pure joy, undercut:** the festival in full swing, "A KINGDOM'S FAVOURITE NIGHT / began as a punishment." |
| Spine | Layers rebuilt as cause → effect | Map zoom in, then pull back | **Then/now mirror:** two pairs of matched plates (same gate, same fire ring, three centuries apart) dissolve into each other on the line (`eraShift`). An `originLedger` card lists the customs under NOW, then writes each one's original purpose under THEN |
| Darkest beat | (none) | The realm goes dark | **Absence, not harm:** 20 small hooded figures light up one by one in a head count, and the last four stay as empty dashed outlines |
| Lesson | Over the designed person | Over the consequence | Over the punishment night, and on "The reason was forgotten." **the festival grows back over it** |
| CTA | Share | Comment | Comment (the festival again, now that you know) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`).
  - The YouTube title is 54/100 characters.
  - The TikTok caption is 260 characters.
  - The Instagram hook line is 40 characters.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). It's two days old, so I didn't re-check it.
- Still no Runway, ElevenLabs or Creatomate keys. AWS credentials exist but weren't used.
- Figma: you approved up to 6 generations for EP12, and 4 were used (no re-rolls).
- The idea: festivals whose modern cheer hides a grim or practical origin are a common pattern in folklore studies. The episode uses it only through an invented example and makes no claims about any real festival.
- Environment note: the headless shell is now `/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`. The `-1194` path in earlier notes no longer exists.

## 2. Stack

Same stack as EP09 and EP10:
- 4 Figma stills (`gemini-3.1-flash-lite-image`, lanczos to 1080×1920);
- Remotion graphics (all code);
- Kokoro `af_heart` narration;
- synthesized score and SFX;
- `qa.py` plus a contact sheet and beat frames.

Names checked in Kokoro's G2P:
- "Bellnight" → /bˈɛlnIt/.
- "Dunmere" → /dˈʌnmɪɹ/ (DUN-meer).
- The first choice, "Halvren", came out as /hˈævɹən/ ("HAV-ren", with no L), so I replaced it.

New in this episode:
- graphics: `eraShift`, `originLedger` and `headCount` (`src/graphics/Tradition.tsx`);
- SFX: `timeFold` and `headCount`.

## 3. Narration (78 words, measured 30.55 s)

> What if a kingdom's most beloved festival began as a punishment? / On Bellnight, Dunmere camps outside its own walls: bells, bonfires, a cheer when the gates open at dawn. / Three hundred years ago, a king locked them out for one winter night. / Bells, to find each other in the snow. Fires, to live till morning. / The cheer at dawn? A head count. / The custom survived. The reason was forgotten. / Invent a tradition and tell us how it began.

How I got there:
- The first draft measured 31.6 s, at 82 words.
- I cut "all of", "and" and the "And" that opened the count line, and tightened two pauses.
- The final cut measures 30.55 s.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.56 | "What if a kingdom's most beloved festival began as a punishment?" | Bellnight: bonfires, children dancing in a ring, the garlanded gate; "A KINGDOM'S FAVOURITE NIGHT / began as a punishment." | Joy, undercut |
| 2 | `festival` | 4.56–11.63 | "On Bellnight, Dunmere camps outside its own walls: bells, bonfires, a cheer when the gates open at dawn." | Closer on the festival; the ledger card opens with "BELLNIGHT, TODAY" and writes Bells / Bonfires / A cheer at dawn | The three customs |
| 3 | `then` | 11.63–15.95 | "Three hundred years ago, a king locked them out for one winter night." | The festival dissolves out of the same frame: the barred gate in a blizzard, a few huddled figures; `gateSlam` on "locked"; tag "THREE HUNDRED YEARS EARLIER / Locked out." | The turn |
| 4 | `mirror` | 15.95–20.37 | "Bells, to find each other in the snow. Fires, to live till morning." | The bonfire ring dissolves into the same ring huddled at a few sticks; the ledger's THEN column writes "to find each other", "to live till morning" | Each custom's purpose |
| 5 | `count` | 20.37–22.93 | "The cheer at dawn? A head count." | The barred gate; the last row reads "a head count"; 20 figures light up, 4 stay empty | The darkest beat, as absence |
| 6 | `lesson` | 22.93–26.42 | "The custom survived. The reason was forgotten." | Punishment night under a heavy scrim; on "reason" the festival dissolves back over it; "The custom survived." ↓ "The reason was forgotten." | Lesson |
| 7 | `cta` | 26.42–30.55 | "Invent a tradition and tell us how it began." | The festival; CTA card | Comment CTA; loops to frame 1 |

Motif colours:
- Festival gold (the plates' firelight) against the punishment's cold blue.
- In the graphics, amber marks the customs and ember italic marks their original purposes.
- No extra motif colour.

## 5. Generated assets

- Plates, from the Figma file "Worldcraft Shorts EP12 plates" in your drafts:
  - `plates/hook.jpg`: the festival outside the walls;
  - `plates/then.jpg`: the same gate, barred, in a blizzard;
  - `plates/fire.jpg`: the bonfire ring;
  - `plates/fireThen.jpg`: the same ring huddled at a dying fire.
- How well the pairs line up:
  - In the wide pair, the gates sit within about 60 px of each other and the towers within about 30 px, so the dissolve reads as the same place.
  - In the close pair, the fire and its pole match; the wall differs (left side versus behind), which reads as the same camp from a slightly different spot.
- `ep12.srt` (18 cues) and `Worldcraft_Short_E12_cover.jpg` (the hook frame at 3.5 s).

## 6. Final video and verification

- `out/ep12.mp4` (master, 40.0 MB) and `out/ep12_compat.mp4` (H.264 Main, CRF 20, 24.7 MB): sent with SendUserFile.
- `ep12_download.mp4` (two-pass 3300k, 13.7 MB) and `ep12_player.mp4` (CRF 26, 8.4 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four files: 1080×1920, 30 fps, 30.57 s, −14.0 LUFS, true peak −1.4 dB.
- Checked by eye: the contact sheet and 12 beat frames (0.3, 4.9, 8.5, 12.9, 13.8, 16.3, 18.6, 21.4, 22.4, 24.2, 26.9 and 30.3 s).
- Fixes made after inspecting the frames:
  - `plates.json` was empty on the first stills, so I re-registered the plates;
  - the missing head-count outlines barely showed and arrived after the shot had cut, so I started the count on "cheer" and drew the outlines brighter in mist;
  - the hook kicker ran past x 920, so I shortened it to "A KINGDOM'S FAVOURITE NIGHT" and enlarged the title.
- Known compromise: the festival crowd fills the lower half of the hook plate, so small figures pass behind the caption band. Their faces are tiny and mostly turned away.
- **Not verifiable by me:** how the narration and mix sound, including the new `timeFold` and `headCount`. Please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `eraShift` | Any then/now or before/after on matched plates: EP15 invisible details, EP19 collapse, EP31 contested history, EP47 aftermath |
| `originLedger` | Any "what it means now ↔ what it meant then" pairing: EP13 taboos (gesture ↔ why), EP14 honour codes (act ↔ meaning on each side) |
| `headCount` | Losses shown as absence (a census, a muster, a returning fleet) in war and disaster episodes |
| SFX `timeFold`, `headCount` | Time jumps; roll calls and counts |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 4 stills, Figma AI credits (4 of the approved 6) | $0 / ₱0 cash |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)** + 4 Figma generations |

On the paid primary stack: about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 12`. The AI label is ON for every platform. The pinned comments ask viewers for a custom from their world, what it means now, and how it began.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | Festival plate with "began as a punishment." | Open on the barred gate in the blizzard with "This is how the party started." | Viewed vs swiped away; average % viewed |
| 2 | Darkest beat | Head count with 4 empty outlines | Hold 1 s longer on the empty outlines with no narration | Retention 20–24 s; rewatch rate |
| 3 | CTA prompt | "Invent a tradition and tell us how it began." | "What's a tradition in your world nobody remembers the reason for?" | Comments per 1,000 views; replies to the pinned comment |

Also track how many comments give *both* meanings (now and then). That shows the lesson landed, not just the twist.

## 11. How to produce EP13 ("Every Culture Has Something It Considers Shameful")

1. Branch `claude/worldcraft-ep13` from the branch with EP11 and EP12 merged. Read:
   - `CLAUDE.md`, `docs/STYLE.md` and `docs/SERIES_PLAN.md`;
   - the EP10, EP11 and EP12 briefs.
2. **Ask before spending Figma credits.** Plan about 4 stills, up to 6 with re-rolls. The default is no public release.
3. Story:
   - Hook: "In one kingdom, refusing a gift is an insult. In another, accepting it is."
   - Mechanism: respect, honesty, privacy, hospitality and loyalty mean different things in different cultures, so misunderstandings arise naturally.
   - Use **two** invented peoples and **one** gift exchanged between them. Show the same act read two ways, then the conflict that grows from it.
   - Keep it a misunderstanding with understandable reasons on both sides, not a villain.
4. Vary the rhythm again. Options:
   - a split-frame or two-panel mirror: the same gesture, one meaning per side;
   - `originLedger` repurposed as "THEY MEANT ↔ THEY SAW", with `eraShift` swapping between two points of view instead of two centuries.
   - Avoid EP12's festival-then-origin shape.
5. CTA: "Share this with a writer who wants believable cultural differences." This is a share CTA (`ctaCard` `icon: "share"`).
6. Narration should be about 70–78 words. Measure it with `cd pipeline && python tts.py ep13` before you lock the cues, and check any invented names in the G2P.
7. Then:
   - `pipeline/build.sh ep13`, then stills (run `plates.py --register` *after* `episode.json` exists), render, `qa.py`, sheet and beat frames;
   - encodes: compat, a two-pass download copy, and a player copy, all with `-c:a copy`;
   - `srt.py`, `storyboard.py`, the cover, and this brief's 11 sections;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
