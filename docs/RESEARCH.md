# Research & stack decision (checked 2026-10-19)

Official documentation was the primary source; third-party figures are marked. Prices change, so re-check before you budget.

## What this session can actually reach

| Capability | Status in this session |
|---|---|
| Claude Pro | Gives you Claude (chat, Claude Code, connectors). It does **not** include credits for Runway, ElevenLabs, Creatomate or AWS. Each is a separate account and bill. |
| Cloud compute | Claude Code's cloud container (4 vCPU, 15 GB RAM) and GitHub Actions (public repo: standard runners free). Neither touches your computer. |
| Runway / ElevenLabs / Creatomate | No API keys present. Endpoints are reachable; calls need your keys. |
| Figma (connected) | Starter plan, Full seat, Figma AI enabled: 500 AI credits/month, 150/day ([Figma help](https://help.figma.com/hc/en-us/articles/35865276858647-Manage-AI-credits)). `generate_image` works from here; per-image credit cost is not published. |
| Figma Weave | Model runner (Runway, Kling, Veo, …) is available **after** you link Figma at app.weavy.ai → Settings → Profile. Not linked yet. |
| Google Drive / Gmail / Notion | Connected, but not needed for production. |

## Candidates

| Category | Option | Verified facts | Fit |
|---|---|---|---|
| Video gen | **Runway API** | $0.01/credit. gen4_turbo 5 cr/s ($0.05/s), gen4.5 12 cr/s, veo3.1_fast 10 cr/s (no audio), kling3.0_standard 9 cr/s. Image-to-video `720:1280`, 2–10 s. ([pricing](https://docs.dev.runwayml.com/guides/pricing/), [API](https://docs.dev.runwayml.com/api/)) | **Primary.** One key covers video, stills and (resold) ElevenLabs voices. |
| Image gen | Runway `gen4_image` | 8 credits at 1080p ($0.08); `1080:1920` ratio supported. Also nano_banana_2.1 $0.04–0.06, gpt_image_2 from $0.01. | **Primary** for plates. |
| Image gen | Figma `generate_image` | Gemini / GPT image models, billed in Figma AI credits you already have. | **Zero-cash option**, available now. |
| TTS | ElevenLabs | API: Multilingual v2 / v3 $0.08 per 1K chars, Flash $0.04. Starter $6/mo is the lowest tier with commercial rights. Music $0.15/min, SFX $0.12/min. ([pricing](https://elevenlabs.io/pricing/api)) | **Primary** voice (≈430 chars ≈ $0.04 per take). |
| TTS | Kokoro-82M | Apache-2.0 open weights, 82M params, CPU-friendly ([model card](https://huggingface.co/hexgrad/Kokoro-82M)). | **Fallback / default.** Used for this render. |
| Assembly | **Remotion** | React video, free for individuals and companies ≤3 people; $25/seat Creators or $0.01/render Automators otherwise ([license](https://www.remotion.dev/docs/pricing)). Lambda ≈ $0.017 for a 1-min video ([cost example](https://www.remotion.dev/docs/lambda/cost-example)). | **Chosen.** Full control of typography, maps and captions; renders in CI for $0. |
| Assembly | Creatomate | Credits = W×H×fps×s / 100M → **19 credits** for a 30 s 1080×1920@30 render ([docs](https://creatomate.com/docs/account/how-are-credits-calculated)). 50 free trial credits; plans are monthly (docs mention Essential $54; third-party lists conflict). | Good no-code templating, but a fixed monthly fee and weaker custom animation. |
| Assembly | Motion Canvas | Canvas-only, imperative generator timelines; excellent hand-made explainers; server rendering via the Revideo fork ([comparison](https://www.remotion.dev/docs/compare/motion-canvas), vendor-authored). | Not needed: the series needs DOM typography and data-driven templates. |
| Storage | Cloudflare R2 | $0.015/GB-mo, free egress, 10 GB free ([pricing](https://developers.cloudflare.com/r2/pricing/)). | Add when you want permanent public links. |
| Storage | GitHub Actions artifacts | Free on public repos, 30-day retention here. | Used now for render delivery. |

Sources: [Runway pricing](https://docs.dev.runwayml.com/guides/pricing/) · [Runway API reference](https://docs.dev.runwayml.com/api/) · [ElevenLabs API pricing](https://elevenlabs.io/pricing/api) · [Creatomate credits](https://creatomate.com/docs/account/how-are-credits-calculated) · [Creatomate pricing](https://creatomate.com/pricing) · [Remotion license](https://www.remotion.dev/docs/pricing) · [Remotion Lambda cost](https://www.remotion.dev/docs/lambda/cost-example) · [Remotion vs Motion Canvas](https://www.remotion.dev/docs/compare/motion-canvas) · [R2 pricing](https://developers.cloudflare.com/r2/pricing/) · [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) · [Figma AI credits](https://help.figma.com/hc/en-us/articles/35865276858647-Manage-AI-credits) · Safe-zone guidance (no official spec; third-party): [reap.video](https://reap.video/blog/short-form-video-safe-zones)

## Decision

**Primary architecture (paid quality, ~$1–2 per episode):**
Claude writes `episode.json` → Runway `gen4_image` plates (4 stills) + `gen4_turbo` image-to-video for the 2 hero shots → ElevenLabs narration with timestamps → synthesized score/SFX (or ElevenLabs Music) → Remotion composition → **GitHub Actions** render → QA → MP4 artifact (later R2).

**Fallback architecture (zero cost, used for this first render):**
Same pipeline with Kokoro TTS, procedural "matte painting" scenes drawn in code, synthesized score, GitHub Actions or Claude cloud render.

Why: one config file drives everything; the expensive parts (AI plates and clips) are optional and replace backgrounds per shot, so a failed generation never blocks an episode. Rendering on GitHub Actions removes Lambda/AWS setup and the fixed monthly fee of a template service. Nothing heavy runs on your laptop.
