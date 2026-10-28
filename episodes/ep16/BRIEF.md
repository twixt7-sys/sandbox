# EP16 production brief: Who Really Rules Your Kingdom?

**Series:** Worldcraft Shorts, Episode 16 / 50. Opens **Arc 4: Kingdoms and Power**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "The king wears the crown. But who controls the food supply?" Topic: power beyond the throne. CTA: "Who would secretly control your fictional kingdom?"
**Deliverable:** 29.7 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** separate formal authority (the title) from actual power (control of what people need). Show the title, then follow the essential thing to whoever really holds it.
- **One kingdom, one holder:** in **Orvane** the king signs every law, but every sack of grain passes through the **Granary Guild**. If the guild shuts its doors, the city starves in a week, so every new law is quietly shown to the guild first.
- **One shareable thought:** "Separate the title from the power." On screen, one crown splits in two: a dashed crown (THE TITLE / wears the crown) ≠ a gold crown (THE POWER / holds what people need).
- **Inverts EP15:** EP15 never showed a palace. EP16 opens on the throne, then leaves it to follow the grain.
- **Power is an institution, not a geography:** the map shows grain roads converging on the guild, but the answer is the guild and its keeper's keys, not a chokepoint (EP10's bridge). The resource is grain, not water (EP08).
- **No villain:** the guild isn't evil and the king isn't a fool. Nobody is threatened on screen; the leverage is shown through objects (keys, a law arrow, a crown that moves). This keeps clear of EP17 (why people support an evil empire).

### How EP16 varies the series rhythm

| | EP10 | EP13–EP14 | EP15 | EP16 |
|---|---|---|---|---|
| Hook | The palace on a map | Split frame / re-captioned verdict | A plain street, no palace | **The throne itself:** callout THE CROWN / *the title*, then "BUT WHO CONTROLS / *the grain?*" |
| Spine | Map zoom to the bridge | Mirrored plates / verdict scale | Three ink chains on one plate | **Follow the thing:** map of grain roads → the guild's hall → back to the map |
| Turn | The gate shut at night | Both sides right | Pull back to the street | **The crown moves:** it lifts off the palace and settles on the granary; a dashed outline stays on the throne |
| Lesson | The gate | `mirrorLedger` / level scale | `reverseCard` | `titlePower`: one crown splits into TITLE ≠ POWER, then MERCHANTS · PRIESTS · GENERALS · LANDLORDS |
| CTA | Follow | Share / Comment | Follow | Comment, over the same hall at dusk with the throne empty |

One `inferChain` only (HER KEYS / the city's bread / ∴ REAL POWER), as the EP15 hand-off asked.

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`); nothing in the last week suggested otherwise, so not re-researched. Title 58/100 characters; TikTok caption under 300; Instagram hook line is the first 24 characters.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026), six days old, not re-checked.
- Figma: the Starter plan is out of AI credits until **1 Nov 2026** (today is 28 Oct), so the free local route was used without asking.
- No Runway, ElevenLabs or Creatomate keys. AWS credentials exist in the environment but weren't used.
- The idea: the gap between formal authority and real power (grain merchants, temple estates, army commanders, landed nobles, creditors) is a standard point in political history and fantasy craft writing. The episode makes no claim about a specific real state; Orvane and its guild are invented.

## 2. Stack

Same stack as EP11–EP15:
- 3 stills from **local SDXL-Lightning** (`pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). Licences: SDXL base 1.0 under CreativeML OpenRAIL++-M, ByteDance SDXL-Lightning under OpenRAIL++; both allow commercial use with use-based restrictions, which this series meets.
- Remotion graphics (all code), including the `atlas` map.
- Kokoro `af_heart` narration. "Orvane" → /ˈɔɹvAn/ (OR-vane) in the G2P; "Granary" → /ɡɹˈAnəɹi/ (GRAY-nuh-ree, a standard pronunciation).
- Synthesized score (D minor → D major) and SFX.
- `qa.py`, a contact sheet and beat frames.

New in this episode (`src/graphics/Power.tsx`, plus two atlas kinds):
- `titlePower`: the lesson card. One crown splits into a dashed TITLE crown and a gold POWER crown with a rust ≠, column kickers and italic lines on cues, then chips that light on cues.
- Atlas `crown` (`at`, `from`, `ghost`, `size`, `lift`): a crown on the map; with `from` it flies along an arc to `at` and glows on landing; `ghost` is the dashed outline left behind.
- Atlas `granary`: a storehouse between two silos, ringed like a town, with a pulse.
- `keyRing`: a code-drawn iron key ring (SDXL didn't paint keys on the keeper).
- `grainSack`: a code-drawn tied burlap sack (on the dais of the empty throne at the end).
- SFX `grainPour` (the grain's signature) and `crownShift` (the crown changing hands).
- Merged first: the finished EP14 (`claude/worldcraft-ep14`, `b874755`). One conflict, in `docs/DISTRIBUTION.md`, resolved by keeping both caption sections (EP14 before EP15); EP14's cost section was moved before EP15's. `tsc` passed and an ep14 and an ep15 still both rendered before the merge was committed.

## 3. Narration (74 words, measured 29.68 s)

> The king wears the crown. But who controls the food supply? / In Orvane, the king signs every law. / But follow the grain. Every sack passes through the Granary Guild. / If the guild shuts its doors, the city starves in a week. / So every new law is quietly shown to the guild first. / Separate the title from the power. / Merchants, priests, generals, landlords: whoever controls what people need. / Who would secretly control your fictional kingdom?

The first measurement was 28.48 s, so I lengthened six pauses (by 0.15–0.25 s each) rather than adding words.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.22 | "The king wears the crown. But who controls the food supply?" | The king on his throne at the end of a long hall; callout THE CROWN / *the title*; then BUT WHO CONTROLS / *the grain?* | The obvious answer, questioned |
| 2 | `decree` | 4.22–6.86 | "In Orvane, the king signs every law." | Punch-in on the king; tag ORVANE · THE THRONE / *Signs every law.* | Formal authority |
| 3 | `route` | 6.86–10.99 | "But follow the grain. Every sack passes through the Granary Guild." | Map: the palace with its crown; farmland lights; grain roads flow from four villages into the guild's granary, then one road to the capital | Follow the essential thing |
| 4 | `granary` | 10.99–14.77 | "If the guild shuts its doors, the city starves in a week." | The guild's keeper among the sacks; ink loop round her keys: HER KEYS / *the city's bread* / ∴ REAL POWER | The real holder, and the evidence |
| 5 | `permission` | 14.77–18.36 | "So every new law is quietly shown to the guild first." | Map: a dashed law arrow runs palace → guild; the crown lifts off the palace and settles, glowing, on the granary; a dashed crown stays on the throne | Actual power vs formal power |
| 6 | `lesson` | 18.36–25.69 | "Separate the title from the power. Merchants, priests, generals, landlords: whoever controls what people need." | `titlePower`: one crown splits, THE TITLE / wears the crown ≠ THE POWER / holds what people need; four chips light | Lesson |
| 7 | `cta` | 25.69–29.68 | "Who would secretly control your fictional kingdom?" | The same kind of hall at dusk, the throne empty, a grain sack on its dais; CTA card with a "Comment below" pill; cross-fades to the king | Comment CTA; loops |

Motif: no new colour. Gold is the crown (power), the dashed mist outline is the title, ember dots are the grain moving. Rust appears once, on the ≠.

## 5. Generated assets

- Plates, from local SDXL-Lightning (prompts in each shot's `sdxlPrompt`):
  - `plates/hook.jpg`: the king in the throne hall, seed 5 (round 2);
  - `plates/granary.jpg`: the guild keeper among the sacks, seed 11 (round 1);
  - `plates/cta.jpg`: the empty throne at the end of the hall, seed 8 (round 2).
- **12 candidates in two rounds:**
  - round 1, 6 images (seeds 11, 23). The granary keeper was usable first time. Both throne halls had gilded statues instead of a living king, plus rose windows that read as a cathedral. The prompts were also over CLIP's 77-token limit, so the style tail was cut.
  - round 2, 6 images (seeds 5, 8, 31) with shorter prompts ("a living bearded king", "round-arched", "plain banners"). Seed 5 has a clear crowned king and seed 8 an empty throne on a dais.
- **Code-drawn:** the keys, the grain sack, the map (crowns, granary, grain roads, law arrow), the lesson card and all type.
- No lettering was found in the three plates, so none needed painting out.
- `ep16.srt` (17 cues) and `Worldcraft_Short_E16_cover.jpg` (the hook at 3.4 s, with "BUT WHO CONTROLS / the grain?").

## 6. Final video and verification

- `out/ep16.mp4` (master, 36.7 MB) and `out/ep16_compat.mp4` (H.264 Main, CRF 20, `+faststart`, 20.9 MB): sent with SendUserFile.
- `ep16_download.mp4` (two-pass 3300k, 13.3 MB) and `ep16_player.mp4` (CRF 26, 6.3 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 29.72 s, −14.1 LUFS, true peak −1.4 dB (the compat copy, whose AAC is re-encoded, measures −1.3 dB). The download copy published on the preview page was read back and QA'd too (see the page's Checks).
- I inspected the contact sheet plus beat frames at the callout, the title, the tag, both map shots (including the crown in flight and landed), the chain, both lesson states, the CTA and the loop tail. Fixes made after that:
  - the granary chain's "means" line wrapped into four short lines, so it's now "the city's bread" at a larger size, moved in from the left edge;
  - the keys were dark iron on a dark coat, so they're lighter with a bright highlight;
  - a small "THE THRONE" map label collided with the hills, so I removed it;
  - the king sat in the caption band at the plate's own framing, so the hook is raised and scaled (s 1.40 → 1.46, y −340 → −370; the margin covers the shift).
- **Accepted compromises:**
  - The captions sit over the king's chest in the hook. His face is just above the band, at about y 1080–1130.
  - The throne halls are generic stone, round-arched with heavy curtains, rather than a strongly invented architecture. They read as no specific real palace, and the king's dress is invented (indigo and rust robes).
  - The CTA plate is warm sunset rather than night, so it's graded down with `plateLook`. The grain sack on the dais is small and mostly sits behind the CTA card: a detail for rewatchers, not a beat.
  - Kokoro says "GRAY-nuh-ree", the American pronunciation of granary.
- **Not verifiable by me:** how the narration and mix sound, including the new `grainPour` and `crownShift`. Please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| `titlePower` | Any "two kinds of X" lesson with a split: law vs custom, official vs real religion, the face vs the hand of an empire (EP17) |
| atlas `crown` (`from` / `ghost`) | Power, legitimacy or a claim moving across a map: succession, a coup, a vassal switching sides |
| atlas `granary` | Stores and supply nodes: tithe barns, salt stores, armouries |
| `keyRing`, `grainSack` | Props SDXL won't place: keys of office, tribute, rations, a famine's last sack |
| SFX `grainPour`, `crownShift` | Grain, trade or tribute; any moment power changes hands |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 3 stills (12 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (out until 1 Nov 2026) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 16`. The AI label is ON for every platform. The pinned comments ask who secretly holds power in the viewer's kingdom *and what they hold*, so answers carry the lesson (a resource, not just a name).

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook | The king on the throne, "BUT WHO CONTROLS / the grain?" | Open on the guild keeper's keys, same line | Viewed vs swiped away; average % viewed |
| 2 | The turn | The crown flies to the granary on the map | Cut back to the keeper with the crown drawn over her (no map) | Retention 14–19 s; rewatch rate |
| 3 | CTA | Comment: "Who would secretly control your fictional kingdom?" | Comment with a prompt: "Name the holder and what they hold." | Comments per 1,000 views; share of comments naming a resource |

Also track saves: a "title vs power" split is the kind of frame people save as a worldbuilding note.

## 11. How to produce EP17 ("Why Would Anyone Support an Evil Empire?")

1. Branch `claude/worldcraft-ep17` from `claude/worldcraft-ep16`, which has EP01–EP16 including the finished EP14. Read:
   - `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`;
   - this brief and the EP14 brief (EP14 keeps both sides sympathetic; EP17 needs the same care with the empire's supporters).
2. **Stills:** Figma credits reset on **1 Nov 2026**. If it's on or after that date and Figma would clearly be better (invented imperial costume and architecture), ask with AskUserQuestion before spending credits (about 4 images, up to 6; plan key `team::1384938462301182142`). Otherwise use `python pipeline/local_stills.py ep17 <shots> --seeds 5 8 11`, then `--pick`, then `plates.py --register`, with no Remotion running while it does. Keep `sdxlPrompt` under ~50 words: the style tail is appended and CLIP stops at 77 tokens. "A living …" helps SDXL paint a person rather than a statue.
3. Story (plan): hook "If your empire is so evil, why hasn't everyone rebelled?" Governments survive through force, loyalty, stability, propaganda, prosperity, fear and no better alternative; supporters often have understandable reasons. CTA: "Share this with someone writing a one-dimensional villainous empire." This is a share CTA (`ctaCard` `icon: "share"`).
   - Show ordinary supporters with real reasons (the baker whose roads are finally safe, the clerk with a pension, the mother afraid of the last war), not soldiers or cruelty. No violence on screen.
   - Don't reuse EP16's crown split as the lesson. A natural new shape: one imperial banner with several threads holding it up (one per reason), each tied to a different person, or a `reasonTally`-style row of reasons that fills as supporters speak.
   - `titlePower` could show the empire's face vs its foundation once, but vary it.
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep17`. Check names in the G2P, and use `nth` for repeated words in cues. If it comes in short, lengthen pauses before adding words.
5. Then:
   - `pipeline/build.sh ep17` → render → `qa.py` → sheet and beat frames, including the loop tail;
   - compat, two-pass download and player encodes, all `-c:a copy` except compat, with `qa.py` on each;
   - `srt.py`, `storyboard.py`, the cover, and an 11-section brief;
   - docs (COSTS, DISTRIBUTION, README, STYLE);
   - a new preview page with a Download MP4 button, then SendUserFile;
   - commit and push to the episode branch.
