# EP11 production brief: Culture Is More Than Clothing

**Series:** Worldcraft Shorts, Episode 11 / 50. Opens **Arc 3: Civilization and Culture**.
**Plan entry** (`docs/SERIES_PLAN.md`): hook "Giving every nation a different outfit doesn't give them different cultures." Topic: building distinct cultures. CTA: "Follow if you want your fictional nations to feel genuinely different."
**Deliverable:** 31.2 s vertical Short (1080×1920, 30 fps) for YouTube Shorts, TikTok and Facebook Reels, plus Instagram Reels captions. AI disclosure on everywhere.
**Shot list, timings and prompts:** [`STORYBOARD.md`](STORYBOARD.md), generated from `episode.json` and the measured `timing.json`.

## The brief

- **One idea:** an outfit tells you where someone is from; a culture tells you who they are. Culture is a system of values: what people laugh at, who counts as family, and what makes someone good.
- **One example:** one invented people, the **Varenni** (the only name), and one ordinary moment a visitor misreads: a funeral where everyone is laughing.
  - **What a visitor sees:** laughter at a funeral. Cruel?
  - **What a Varenni sees:** a send-off. Three layers:
    1. **humour:** each mourner tells one of the dead man's funniest failures;
    2. **what makes a good person:** a good life leaves good stories;
    3. **family structure:** the neighbours sit closest, because the whole street raised him.
- **One shareable thought:** "An outfit is the surface. Culture is what people laugh at, who's family, and what makes someone good."
- **Scope guard:**
  - Clothing appears only as the thing the lesson dismisses: one empty costume, and the same costume worn at the end. No costume parade.
  - No climate link (EP09), no single ordinary detail as the point (EP04's rain bowl), no taboo or gift insult (EP13), no clash of honour codes (EP14). The funeral is a whole value system, not a taboo.
  - EP15 will cover everyday behaviour as a technique; EP11 uses one moment only to show that values sit under the surface.

### How EP11 varies the series rhythm

| | EP09 | EP10 | EP11 |
|---|---|---|---|
| Hook | The wrong image (robes in a blizzard) | The obvious answer, targeted | **The thing being dismissed:** a magnificent costume on an empty dress form, "A NEW OUTFIT / isn't a culture." |
| Spine | Strike and rebuild, layer by layer | Zoom in, then pull back on a map | **The same scene, read twice.** The funeral appears in a cold, grey "visitor" grade with a rust verdict ("cruel?"); on "Look again" an amber seam wipes the warm "insider" grade across the identical frame, and amber callouts name what the laughter means |
| Running device | Callouts + tally | Map glow and ✕ | `plateLook` (new): two grades of one plate, swapped by a cue-timed wipe |
| Lesson | Tally bracket | `lessonStack` over the consequence | A peeled `lessonStack` over the empty costume, now greyed: surface ↓ laughter ↓ family ↓ goodness |
| CTA | Share | Comment | Follow, over the same costume now worn by a laughing elder; the loop returns to the empty one |

## 1. Research note (only what could have changed)

- Platform limits, hashtags and AI-disclosure rules: unchanged since the 2026-10-19 research (`docs/DISTRIBUTION.md`). The YouTube title is 45/100 characters; the TikTok caption is 264 characters. `#FantasyCulture` replaces `#FantasyMap`.
- Exchange rate: ₱63.35 = $1 (BSP reference, 22 Oct 2026). Five days old; not re-checked.
- **Figma AI credits are exhausted until 1 Nov 2026.** The user approved 3 generations; the first call was refused ("Insufficient Figma AI credits") and nothing was charged.
- Google AI was not usable: the Google Cloud token in the environment doesn't authenticate to any project, and there is no Gemini/Imagen key. Still no Runway, ElevenLabs or Creatomate keys. AWS credentials exist but weren't used.
- Replacement chosen with the user ("try other options"): **SDXL-Lightning** (ByteDance, 4-step distillation of SDXL 1.0) run locally on the container's CPU. Licences: SDXL base under CreativeML OpenRAIL++-M, SDXL-Lightning under OpenRAIL++; both allow commercial use with use-based restrictions (no harmful content), which this series meets.
- The idea itself: anthropology treats culture as shared values, norms, kinship and practices, not dress. Joyful or story-telling funeral customs exist in several real traditions; the Varenni version (failures retold as the eulogy, neighbours seated before kin) is invented and not modelled on any one people.

## 2. Stack

- 3 stills from **local SDXL-Lightning** (new `pipeline/local_stills.py`, 768×1344, lanczos to 1080×1920). 11 candidates rendered (no cost); 3 kept.
- Remotion graphics (all code), including a code-drawn **`shroud`**, because SDXL would not paint a shrouded body in any of 5 funeral seeds.
- Kokoro `af_heart` narration ("Varenni" → /vəɹˈɛni/, vuh-REN-ee, checked in the G2P; "Teyo" was rejected because it came out as "tow").
- Synthesized score and SFX; `qa.py` plus a contact sheet and beat frames.

New in this episode:
- shot option `plateLook` (`src/scenes/registry.tsx`): named or raw CSS grades (`cold`, `warm`) and a cue-timed left-to-right wipe with an amber seam;
- `shroud` graphic (`src/graphics/Culture.tsx`);
- `relook` SFX (a swept breath blooming into a warm D-major triad);
- `pipeline/local_stills.py` and the per-shot `sdxlPrompt` field.

Local generation notes: about 2.5 min per image on 4 CPU cores. The container's 14 GB memory limit OOM-killed the naive pipeline three times, so the tool stages memory: it encodes prompts and frees the text encoders, casts the UNet to fp32 tensor by tensor, denoises every latent, then frees the UNet before the VAE decode. Don't run a Remotion render at the same time.

## 3. Narration (76 words, measured 31.16 s)

> Giving every nation a different outfit doesn't give them different cultures. / At a Varenni funeral, a visitor sees everyone laughing. Cruel? / Look again, as a Varenni. / Each mourner tells his funniest failure. A good life leaves good stories. / The neighbours sit closest. The whole street raised him. / An outfit is the surface. Culture is what people laugh at, who's family, and what makes someone good. / Follow if you want your fictional nations to feel genuinely different.

The first draft (78 words) measured 32.8 s. I tightened two lines and the pauses, which brought it to 31.16 s, inside the 27–33 s window but about a second longer than EP09 and EP10.

## 4. Timed storyboard

| # | Shot | Time | Narration | Picture | Purpose |
|---|---|---|---|---|---|
| 1 | `hook` | 0:00–4.71 | "Giving every nation a different outfit doesn't give them different cultures." | An ornate teal-and-rust costume on a headless dress form in a dim workshop, dust in the window light; "A NEW OUTFIT / isn't a culture." | The surface, dismissed |
| 2 | `visitor` | 4.71–9.17 | "At a Varenni funeral, a visitor sees everyone laughing. Cruel?" | Lamp-lit courtyard, mourners laughing round a shrouded body on a draped bier, all in a cold grey grade; tag WHAT A VISITOR SEES / Laughter at a funeral.; rust callout VISITOR'S VERDICT / cruel? | The outsider's misreading |
| 3 | `again` | 9.17–11.05 | "Look again, as a Varenni." | Same frame; an amber seam wipes the warm grade across; tag WHAT A VARENNI SEES / A send-off. | The re-read |
| 4 | `stories` | 11.05–15.77 | "Each mourner tells his funniest failure. A good life leaves good stories." | Punch-in on the laughing ring; callouts HUMOUR / his funniest failure, then A GOOD PERSON / leaves good stories | Layers 1–2 |
| 5 | `street` | 15.77–19.28 | "The neighbours sit closest. The whole street raised him." | Pull back; amber dashed ring around the inner circle; callout FAMILY / the whole street | Layer 3 |
| 6 | `lesson` | 19.28–25.78 | "An outfit is the surface. Culture is what people laugh at, who's family, and what makes someone good." | The empty costume, greyed and dimmed; stack "An outfit is the surface." ↓ "What they laugh at." ↓ "Who counts as family." ↓ "What makes someone good." | Lesson, peeled from the outside in |
| 7 | `cta` | 25.78–31.16 | "Follow if you want your fictional nations to feel genuinely different." | The same costume worn by a laughing elder; CTA card with Follow pill; loop cross-fades to the empty costume | Follow CTA; loops to frame 1 |

Motif: no new colour. Grey stands for the outsider's read, warm lamp light for the insider's. Rust marks the wrong verdict, and amber marks the meanings.

## 5. Generated assets

- `plates/hook.jpg` (empty costume), `plates/visitor.jpg` (the funeral courtyard, reused by `again`, `stories` and `street`) and `plates/cta.jpg` (the costume worn), all from local SDXL-Lightning. The prompts are in each shot's `sdxlPrompt`. Kept seeds: hook 11, funeral 9 (`funeral2` prompt), cta 11.
- Rejected candidates: three closing-card seeds put the face behind the logo, so `cta_11` is reframed instead (face top-right, above the card). Four funeral seeds were dropped: they had no body, or read as a real religious order.
- The shrouded body on the bier is code (`shroud`), not generated.
- `ep11.srt` (16 cues) and `Worldcraft_Short_E11_cover.jpg` (hook frame at 3.5 s).

## 6. Final video and verification

- `out/ep11.mp4` (master, 36.8 MB) and `out/ep11_compat.mp4` (H.264 Main, CRF 20, 21.1 MB): sent with SendUserFile.
- `ep11_download.mp4` (two-pass 3300k, 13.9 MB) and `ep11_player.mp4` (CRF 26, 7.1 MB), both with the master's audio copied: used on the preview page.
- `qa.py` **passed** on all four local files: 1080×1920, 30 fps, 31.17 s, −14.1 LUFS, true peak −1.4 dB.
- Fixes made after inspecting the frames:
  - the hook title crossed the dress form's finial, so the plate is lowered (scale 1.17, +160 px);
  - the lesson stack sat on the bright window, so the lesson grade is darker (`brightness(0.42)`);
  - the elder's face sat behind the CTA logo, so the plate is scaled 1.3 and shifted so the face is top-right, above the card;
  - the shroud first read as a flat loaf, then vanished (a taper bug), and was redrawn from a smooth profile;
  - the street ring cut across faces, so it's lowered to chest height;
  - the verdict ring sat on a face, so it moved to the chest.
- Known compromise: the generated mourners wear pale, loose robes. They read as invented, but less distinctive than a Figma plate would have been. A few back-row faces sit just under the caption band in the funeral shots; they're small and distant.
- **Not verifiable by me:** how the narration and mix sound, including the new `relook`. Please give it one listen.

## 7. Reusable components added

| Component | Use later for |
|---|---|
| shot `plateLook` (`from`, `to`, `at`, `dur`) | Any "look again" re-read: outsider vs insider (EP13 taboos), propaganda vs truth, then vs now, a forgotten origin (EP12) |
| `shroud` | Funerals, wakes, plague and battle aftermaths, when the image model avoids bodies |
| SFX `relook` | The turn of every perspective flip |
| `pipeline/local_stills.py` + `sdxlPrompt` | Free plates whenever Figma credits run out; drafts and re-rolls at no cost |

## 8. Cost (₱63.35 = $1)

| Item | Cash |
|---|---|
| 3 stills (11 candidates), local SDXL-Lightning on the session's CPU | $0 / ₱0 |
| Figma AI credits | 0 used (the call was refused: plan out of credits until 1 Nov) |
| Everything else (graphics, voice, music, render, QA) | $0 / ₱0 |
| **Total** | **$0 (₱0)**, no credits |

On the paid primary stack, with 3 stills: about **$1.05 (₱67)**, or **$1.94 (₱123)** with one retry per asset, plus ElevenLabs Starter at $6 (₱380) a month.

## 9. Platform metadata

Source of truth: `episode.json → metadata`, pasted into `docs/DISTRIBUTION.md → Episode 11`. The AI label is ON for every platform. The pinned comments ask viewers which of the three layers (laughter, family, goodness) they've built for their nations, and what a visitor would misread in their world.

## 10. Experiments and metrics

| # | Variable | A (as shipped) | B | Primary metric |
|---|---|---|---|---|
| 1 | Hook image | Empty costume, "A NEW OUTFIT / isn't a culture." | Open on the grey funeral with "Laughter at a funeral." and move the outfit line to second | Viewed vs swiped away; average % viewed |
| 2 | The re-read | Grade wipe with an amber seam | A hard cut to the warm grade on "again" | Retention 9–12 s; rewatch rate |
| 3 | CTA | Follow (from the plan) | Comment: "What would a visitor get wrong about your people?" | Follows per 1,000 views vs comments per 1,000 views |

Also track how many comments describe a custom *and* what it means. That shows the "two readings" idea landed.

## 11. How to produce EP12 ("Invent a Tradition With a Dark History")

1. Branch `claude/worldcraft-ep12` from `claude/worldcraft-ep11`. Read `CLAUDE.md`, `docs/STYLE.md`, `docs/SERIES_PLAN.md`, this brief, and EP09's and EP10's.
2. **Stills:** Figma credits reset on 1 Nov 2026. Ask before spending them (about 4 images, up to 6). If they're still out, or the user prefers, use `python pipeline/local_stills.py ep12 <shots> --seeds 11 23` (free, about 2.5 min per image; keep `sdxlPrompt` under about 70 words), then `--pick <seed>` and `plates.py --register`. Don't render with Remotion while it runs (memory).
3. Story (plan): hook "What if a kingdom's most beloved festival began as a punishment?" Mechanism: a tradition whose original purpose differs from its modern meaning, the origin now forgotten. CTA: "Invent a tradition and tell us how it began." (comment CTA, `button: "Comment below"`).
   - One invented festival, one people. Show the joyful present first, then the origin.
   - `plateLook` is built for exactly this: the festival plate in warm colour, then an amber or rust wipe to a cold "then" grade over the same frame, as the forgotten origin surfaces. Use it once; don't repeat EP11's two-pass structure beat for beat.
   - Keep it from turning into EP13 (taboo) or EP14 (honour). The point is origin vs meaning.
4. Narration about 70–78 words, measured with `cd pipeline && python tts.py ep12`; aim nearer 30 s than EP11's 31.2 s. Check invented names in the G2P.
5. Then: `pipeline/build.sh ep12` → render → `qa.py` → sheet and beat frames → compat, two-pass download and player encodes (`-c:a copy`) → `srt.py`, `storyboard.py`, cover, 11-section brief → docs → a new preview page with a Download MP4 button → SendUserFile → commit and push.
