# EP08 production brief: What If a Desert Had No Water?

**Series:** Worldcraft Shorts, Episode 08 / 50 (Arc 2: Geography and Nature).
**Plan entry** (`docs/SERIES_PLAN.md`): hook "How does a civilization survive where water is worth more than gold?" Topic: environmental pressure and adaptation. CTA: "Follow for more ways to turn geography into storytelling."
**Deliverable:** 30.7 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** scarcity reorganizes everyday life around one resource, and power gathers around whoever controls it.
- **One example:** **Sarrun** (the only name), a desert city where one cup of water costs a day's wage. The mechanism, one scale at a time:
  1. **architecture:** houses turn inward, and every roof spout drains to the cistern;
  2. **law:** rations are measured at locked spouts, and spilling is a crime;
  3. **roads:** caravans bend from well to well, never straight;
  4. **power:** every well in the region is locked, and one family holds the keys. They never needed an army.
- **One shareable thought:** "Make anything scarce, and whoever holds it rules the region."
- **Scope guard:**
  - EP07 used water as a reason to *settle*; here water is about *rules and control*.
  - EP10 is the single key location, so EP08 shows a *system* of eight wells, with no decisive spot.
  - EP03 did a shared-reservoir allocation crisis, so there is no split-supply graphic and no shortage plot. The angle is ownership: who holds the keys.

### How EP08 varies the series rhythm

| | EP06 | EP07 | EP08 |
|---|---|---|---|
| Hook | Skyline trace and "empire?" | The finished city | **One object:** a cup of water beside gold coins, "WATER, WORTH MORE / than gold." |
| Spine | Map → plates → map | Before/after survey on one plate | **A pull-back across scales.** Cup → house → street → road → region. The new `pullBack` shrinks the cup into the house's cistern and the caravan photo onto its route on the map |
| Running device | Map key at the end | Reason tally | **Scale tags** (SARRUN → ARCHITECTURE → LAW → ROADS), then the map itself |
| Lesson | The map's key | Tally bracket over the city | Back to the **same cup**, now glowing: "MAKE ANYTHING SCARCE / whoever holds it, rules." |
| CTA | Share | Comment | Follow (the cup at dusk, city lights behind it) |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The YouTube title is 56/100 characters and the TikTok caption is 249 characters (limit 4,000).
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026), the same as EP06 and EP07. Not re-checked: it was set yesterday.
- Still no Runway, ElevenLabs or Creatomate keys. AWS credentials exist but weren't used.
- Figma: you approved up to 6 generations for EP08, and 4 were used.
- Desert adaptation: the episode uses familiar real-world patterns: inward-facing courtyard houses, cisterns, wind towers, rationing, and routes that follow wells. It presents them only through an invented example.

## 2. Stack

Same stack as EP07:
- 4 Figma stills (`gemini-3.1-flash-lite-image`, lanczos to 1080×1920);
- Remotion graphics (all code), including the `atlas` map scene from EP06;
- Kokoro `af_heart` narration ("Sarrun" → /ˈsæɹʌn/, SARR-un, checked with the G2P);
- synthesized score (E minor resolving to E major) and SFX;
- `qa.py` plus a contact sheet and beat frames.

New in this episode:
- the `pullBack` graphic (`src/graphics/Scale.tsx`);
- atlas kinds `dunes`, `well` and `lock`;
- the `drop` and `lock` SFX.

## 3. Narration (77 words, measured 30.73 s)

> How does a civilization survive where water is worth more than gold? / In Sarrun, one cup is a day's wage. / Houses turn inward, catching every drop of dew. / Rations are measured. Spilling is a crime. / Roads bend from well to well, never straight. / And every well is locked. One family holds the keys. / They never needed an army. / Make anything scarce, and whoever holds it rules the region. / Follow for more ways to turn geography into storytelling.

The first measurement ran 31.73 s. I tightened the pauses by 0.1–0.15 s each and left the words alone, which brought it to 30.73 s.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.60 | "How does a civilization survive where water is worth more than gold?" | Clay cup brimming with water on a sandstone ledge, gold coins tossed beside it; "WATER, WORTH MORE / than gold." | The whole episode in one object |
| 2 | `cup` | 4.60–7.36 | "In Sarrun, one cup is a day's wage." | Same cup; ember ring; tag SARRUN / one cup, one day's wage | Name and price |
| 3 | `house` | 7.36–10.65 | "Houses turn inward, catching every drop of dew." | The cup shrinks into the cistern of a windowless courtyard house; water-blue lines run from every spout to the cistern; ARCHITECTURE | Scale 1: architecture |
| 4 | `law` | 10.65–13.53 | "Rations are measured. Spilling is a crime." | Locked public spout; a guard pours one ration from a bronze ladle; a queue with jars; ring on the ladle; LAW | Scale 2: law |
| 5 | `caravan` | 13.53–16.54 | "Roads bend from well to well, never straight." | Dune sea; the amber route bends through water-ringed wells; a rust straight line is struck out; ROADS | Scale 3: transport |
| 6 | `map` | 16.54–22.36 | "And every well is locked. One family holds the keys. They never needed an army." | The dune photo shrinks onto its map route. Eight wells, the caravan loop and Sarrun; padlocks snap on, ember threads run to the city, an amber wash covers the region | Scale 4: power (payoff) |
| 7 | `lesson` | 22.36–26.13 | "Make anything scarce, and whoever holds it rules the region." | Dissolve back to the cup, its water glowing; lesson lockup | Lesson |
| 8 | `cta` | 26.13–30.73 | "Follow for more ways to turn geography into storytelling." | The cup at dusk, city lights behind; CTA card (`icon: "follow"`) | Follow CTA; loops to frame 1 |

Motif colour: water `#7fd3ec` (spout lines, well rings, map wells). The power threads and wash use ember and amber, and the struck straight road uses rust, so everything else stays on the series palette.

## 5. Generated assets

- `plates/hook.jpg` (the cup), `house.jpg`, `law.jpg`, `caravan.jpg`, from the Figma file "Worldcraft Shorts EP08 plates" in your drafts (https://www.figma.com/design/nN5r7Nw0V4kISMh3DXwI0h). The cup, lesson and CTA shots reuse the cup plate. The map is drawn entirely in code.
- `ep08.srt` (17 cues) and `Worldcraft_Short_E08_cover.jpg` (the hook frame at 3.4 s).

## 6. Final video and verification

- `out/ep08.mp4` (master, 38.5 MB) and `out/ep08_compat.mp4` (H.264 Main, CRF 20, 22.9 MB): sent to you with SendUserFile.
- `ep08_download.mp4` (two-pass 3300k, 13.7 MB) and `ep08_player.mp4` (CRF 26, audio copied from the master, 7.5 MB) are used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 30.74 s, −14.1 LUFS, true peak −1.5 dB.
- I viewed the contact sheet and 20 beat frames: both pull-back insets, the spout lines, the rings, the struck straight road, the locks, the threads, the wash, the lesson, the CTA and the loop tail. All four plates were usable on the first generation (no text, and no faces in the caption band), so no re-rolls and no fixes were needed after the first render.
- **I can't verify** how the narration and mix sound. Please give it one listen, especially the four quick `lock` clicks under "locked".

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `pullBack` (`src`, `from` = the previous shot's last framing, `to: [cx,cy,w]`, `dur`, `hold`) | Any "zoom out to the system" cut: EP09 climate (one coat → the whole culture), EP19 collapse (one ruin → the empire), EP46 hidden places |
| Atlas `dunes`, `well`, `lock` | Desert and resource maps; `lock` on any controlled point (ports, passes, mines; EP10's key location) |
| SFX `drop`, `lock` | Water beats; anything seized, sealed or controlled |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 4 stills, Figma AI credits (4 of the approved 6) | $0 / ₱0 cash |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)** + 4 Figma generations |

On the paid primary stack it would be about **$1.15 (₱73)**, or **$2.12 (₱134)** with one retry per asset. ElevenLabs Starter adds $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata` (pasted in `docs/DISTRIBUTION.md → Episode 08`). The AI label is ON for every platform. The pinned comments ask what is scarce in the viewer's world and who holds it.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook framing | The cup and coins with the "worth more than gold" title | The locked region map first ("Who holds the keys?"), then the cup | Viewed vs swiped away; 3-second hold |
| 2 | Pull-back insets | `pullBack` on two cuts | Plain hard cuts | Retention between 7 and 18 s (do the scale jumps keep people?) |
| 3 | CTA | Follow ("more ways to turn geography into storytelling") | Comment ("What's scarce in your world?") with the same pinned comment | Follows per 1,000 views vs comments per 1,000 views |

Also track how many comments name a scarce resource *and* who controls it. That signals the lesson landed.

## 11. How to produce EP09 ("Your Climate Should Affect Your Culture")

1. Branch `claude/worldcraft-ep09` from `claude/worldcraft-ep08`. Read `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`, and the EP07 and EP08 briefs.
2. **Ask before spending Figma credits** (about 4 stills). The default is no public release.
3. Story: hook "Why would people living in a frozen wasteland dress like desert nomads?" One invented cold-climate people, and one mechanism: weather shapes clothing, housing, food preservation, festivals and migration. CTA: share ("Share this with a friend creating a fantasy civilization", so `ctaCard` with `icon: "share"`).
   - Good fits:
     - `reasonTally` with new icons (coat, house, food, festival) as a checklist of adaptations;
     - `snowfall` (EP06);
     - `pullBack` from one garment out to the whole camp.
   - Don't repeat EP08's scarcity → power payoff or EP06's mountains-as-barrier. EP09 is about *culture*, not control.
4. Vary the rhythm again: for example, a wrong-then-right opener (the "desert nomad" clothing struck in rust, then the real answer), or a seasonal cycle across shots.
5. Narration about 70–78 words. Measure it with `cd pipeline && python tts.py ep09` before you lock the cues.
6. Then:
   - `pipeline/build.sh ep09` → stills → render → `qa.py` → sheet and beat frames;
   - encodes (compat, download, and a player copy with `-c:a copy`);
   - `srt.py`, `storyboard.py`, cover;
   - a new preview page with a Download MP4 button, SendUserFile;
   - commit and push to the episode branch.
