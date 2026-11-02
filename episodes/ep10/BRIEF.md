# EP10 production brief: The Most Important Place on Your Map

**Series:** Worldcraft Shorts, Episode 10 / 50. Closes **Arc 2: Geography and Nature**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "The most important location in your world might not be a capital." Topic: strategic geography. CTA: "What location would every kingdom fight to control?"
**Deliverable:** 30.0 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** power sits where everyone has to pass. A palace gives orders, but the one place the whole realm depends on decides whether anything arrives.
- **One example:** two names only.
  - **Solenne:** the capital, with its gilded palace, in the dry south.
  - **The Kestrel:** the only bridge over a gorge that cuts the realm in two. Every road from the farmland and towns of the north funnels onto it.
  - What flows through it: grain rolls south, soldiers march north, and every cart pays the bridge.
  - What happens when it closes: the capital starves in nine days.
- **One shareable thought:** "A palace gives the orders. Whoever holds the crossing decides if they arrive."
- **Scope guard:** this is the single-chokepoint payoff that EP06 and EP07 held back.
  - EP06's range had three gaps; here there is exactly one crossing.
  - EP07's ford was one reason of four; here the bridge is the whole story.
  - No water source as the key: EP08 is water-as-power.
  - No settlement reasons: EP07 covered them.

### How EP10 varies the series rhythm

| | EP06 | EP07 | EP10 |
|---|---|---|---|
| Hook | Skyline trace and "empire?" | The finished city, "NO GREAT CITY / by accident." | **The obvious answer, targeted:** the gilded palace in a survey ring, "THE MOST IMPORTANT PLACE / isn't the palace." |
| Spine | Map → plates → map | Survey on a before/after plate | **Zoom in, then pull back.** The map opens at 2.5× on the capital's palace glyph (the world seems to revolve around it), then pulls back on "Pull back" until the gorge and the one bridge appear and every road converges on it. The palace's glow fades and a new one spreads from the bridge |
| Consequence | (none) | (none) | **The realm goes dark:** a rust ✕ slams onto the bridge, the road to the capital empties, the whole south dims, "Nine days." |
| Lesson | Map key | Tally bracket | `lessonStack` over the consequence itself (the gate shut at night, carts stalled): "The palace gives orders." ↓ "*The crossing decides.*" |
| CTA | Share | Comment | Comment (the palace at dusk) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The title is 52/100 characters and the TikTok caption is 251 characters.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). It's a day old, so I didn't re-check it.
- Still no Runway, ElevenLabs or Creatomate keys. AWS credentials exist but weren't used.
- Figma: you approved up to 6 generations for EP10, and 3 were used (no re-rolls).
- The idea itself: chokepoints (straits, mountain passes, river crossings, harbours) are a standard concept in historical and military geography. The episode uses it only through an invented example.

## 2. Stack

Same stack as EP06 and EP07:
- 3 Figma stills (`gemini-3.1-flash-lite-image`, lanczos to 1080×1920);
- Remotion graphics (all code);
- Kokoro `af_heart` narration, with both names checked in Kokoro's G2P:
  - "Solenne" → /sOlˈɛn/ (soh-LEN);
  - "Kestrel" → /kˈɛstɹəl/;
- synthesized score and SFX;
- `qa.py` plus a contact sheet and beat frames.

New in this episode:
- `atlas` features:
  - `gorge` and `bridge`;
  - `palace: true` on a town;
  - `size` on `cut`;
  - a cue-timed shot `zoom` (`at`, `dur`).
- `lessonStack` `size`/`restSize`.
- `gateSlam` SFX.

## 3. Narration (75 words, measured 30.00 s)

> The most important location in your world might not be a capital. / Everyone looks at the palace in Solenne. / Pull back. Every road in the realm crosses one gorge, at one bridge: the Kestrel. / Grain rolls south. Soldiers march north. Every cart pays the bridge. / Close it, and the capital starves in nine days. / A palace gives the orders. Whoever holds the crossing decides if they arrive. / What location would every kingdom fight to control?

The first draft measured 30.0 s, right in the middle of the 27–33 s window, so I didn't trim or pad it.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.32 | "The most important location in your world might not be a capital." | Gilded palace over the capital; survey ring closes on it; "THE MOST IMPORTANT PLACE / isn't the palace." | The obvious answer, questioned |
| 2 | `crown` | 4.32–6.77 | "Everyone looks at the palace in Solenne." | Map at 2.5× on the domed palace glyph; amber wash spreads; "Solenne" | The world seems to revolve around the capital |
| 3 | `pullback` | 6.77–12.21 | "Pull back. Every road in the realm crosses one gorge, at one bridge: the Kestrel." | Map pulls back to the whole realm: the north's towns and fields, five roads converging, the gorge drawing across, one bridge lighting up; "The Kestrel" | The reveal: the real key |
| 4 | `bridge` | 12.21–17.09 | "Grain rolls south. Soldiers march north. Every cart pays the bridge." | The bridge over its chasm, carts and soldiers; amber and rust dashed lanes; ring on the gatehouse | Dependence: what flows, who pays |
| 5 | `closed` | 17.09–20.52 | "Close it, and the capital starves in nine days." | Map: ✕ on the bridge, the road to Solenne empties, the south goes dark; "Nine days." | The consequence |
| 6 | `lesson` | 20.52–25.79 | "A palace gives the orders. Whoever holds the crossing decides if they arrive." | Gate shut at night, keeper with a lantern, carts stalled; "The palace gives orders." ↓ "The crossing decides." | Lesson |
| 7 | `cta` | 25.79–30.00 | "What location would every kingdom fight to control?" | The palace at dusk, windows lit; CTA card | Comment CTA; loops to frame 1 |

Motif colour: none beyond the series palette.
- Amber marks flow and influence.
- Rust marks the closing (the ✕, the soldiers' lane, "Nine days.").
- The gorge is the darkest thing on the map.

## 5. Generated assets

- The plates, from the Figma file "Worldcraft Shorts EP10 plates" in your drafts:
  - `plates/hook.jpg`: the palace city;
  - `plates/bridge.jpg`;
  - `plates/lesson.jpg`: the shut gate at night. Its sky happens to have two small crescent moons. I kept it, since this is a fantasy world and the lesson type sits over that sky.
- The CTA reuses the palace plate. The crown, pull-back and closed shots are all one code-drawn map.
- `ep10.srt` (18 cues) and `Worldcraft_Short_E10_cover.jpg` (the hook frame at 3.5 s).

## 6. Final video and verification

- `out/ep10.mp4` (master, 38.7 MB) and `out/ep10_compat.mp4` (H.264 Main, CRF 20, 23.1 MB): sent with SendUserFile.
- `ep10_download.mp4` (two-pass 3300k, 13.4 MB) and `ep10_player.mp4` (CRF 26, 7.3 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four files: 1080×1920, 30 fps, 30.02 s, −14.1 LUFS, true peak −1.4 dB.
- Fixes made after inspecting the frames:
  - the bridge's two flow lanes were too thin and overlapped, so I widened them and moved them apart;
  - the ✕ was lost on the bridge glyph, so it's now larger with a shadow;
  - the zoomed capital was a generic town icon, so it's now a domed palace glyph that echoes the plate;
  - "The Kestrel" collided with the eastern hills, so I moved the hills;
  - `duskGrade`'s reflecting pool painted a blue glow on the plaza, so I moved it off-frame.
- **Not verifiable by me:** how the narration and mix sound, including the new `gateSlam`. Please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `atlas` `gorge` + `bridge` | Any single crossing: EP19 collapse (the bridge falls), EP46 hidden places, trade-route episodes |
| `atlas` cue-timed `zoom` (`at`, `dur`) | "Zoom out to see the real picture" reveals on any map |
| `atlas` `town` `palace: true`, `cut` `size` | Capitals; dramatic closures (a pass sealed, a port blockaded) |
| `lessonStack` `size` / `restSize` | Lesson lines longer than about 20 characters |
| SFX `gateSlam` | Sieges, blockades, sealed vaults, any door that matters |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 3 stills, Figma AI credits (3 of the approved 6) | $0 / ₱0 cash |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)** + 3 Figma generations |

On the paid primary stack, with 3 stills instead of 4: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 10`. The AI label is ON for every platform. The pinned comments ask viewers to name their map's chokepoint and say what flows through it.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | Palace plate with "isn't the palace." | Open directly on the zoomed map and start the pull-back by 0:02 | Viewed vs swiped away; average % viewed |
| 2 | Consequence | Map goes dark, "Nine days." | Cut to the shut-gate plate for the consequence and keep the map for the lesson | Retention 17–21 s; rewatch rate |
| 3 | CTA prompt | "What location would every kingdom fight to control?" | "What's the one place on your map that could starve a capital?" | Comments per 1,000 views; replies to the pinned comment |

Also track how many comments name a *kind* of place (pass, strait, harbour, bridge) together with what flows through it. That shows the lesson landed, not just the image.

## 11. How to produce EP11 ("Culture Is More Than Clothing")

1. EP11 opens **Arc 3: Civilization and Culture**. Branch `claude/worldcraft-ep11` from the branch with EP08–EP10 merged. Read:
   - `CLAUDE.md`, `docs/STYLE.md` and `docs/SERIES_PLAN.md`;
   - the EP07 and EP10 briefs, plus EP08's and EP09's if they're merged.
2. **Ask before spending Figma credits.** Plan about 4 stills, up to 6 with re-rolls. The default is no public release.
3. Story:
   - Hook: "Giving every nation a different outfit doesn't give them different cultures."
   - Mechanism: culture is values, family structure, taboos, traditions, humour, manners, and what counts as a good person.
   - Pick **one** invented people. Show two or three of those layers through one everyday moment (a meal, a greeting, a funeral) that a visitor misreads.
   - Avoid a costume parade. Clothing should appear only as the thing the lesson dismisses.
4. Vary the rhythm again. This is the first non-geography episode, so leave the map behind. Options:
   - the same scene shown twice, as an outsider sees it and then as an insider understands it (`ghostLines` annotations on the second pass);
   - a "layers" stack that peels from clothes down to values (`lessonStack` with `restSize`, or `detailChain` from EP04).
5. CTA: "Follow if you want your fictional nations to feel genuinely different." This is a follow CTA (`ctaCard` `icon: "follow"`).
6. Narration should be about 70–78 words. Measure it with `cd pipeline && python tts.py ep11` before you lock the cues, and check any invented names in the G2P.
7. Then:
   - `pipeline/build.sh ep11` → stills → render → `qa.py` → sheet and beat frames;
   - encodes: compat, a two-pass download copy, and a player copy, all with `-c:a copy`;
   - `srt.py`, `storyboard.py`, the cover, and this brief's 11 sections;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
