# EP32 art: the field-card sprite (free, local)

The user asked to try free tools first and use Figma only if none was good enough. EP32's one generated image (the field card's sprite for THE SEAM WAR) was made with the **free local SDXL-Lightning pipeline with the pixel-art LoRA** (`pipeline/local_stills.py --sprite`: SDXL 1.0 text encoders and VAE, ByteDance's 4-step Lightning UNet, nerijs/pixel-art-xl fused in; CreativeML OpenRAIL++-M / OpenRAIL-M, commercial use allowed). **No Figma credits were used.** About 75–85 s an image on 4 CPU cores; it ran alone (about 10 GB of RAM).

## Round 1: rejected (seeds 32, 7, 41)

    python pipeline/local_stills.py ep32 banner --sprite --prompt "a tattered old war banner on a tall wooden pole planted in a mound of earth, torn cloth, side view, single object, centered" --seeds 32 7 41

- **Seed 41 came back as a real national flag** (stars and stripes). Rejected: the series never shows a real-world symbol, least of all in an episode about a war.
- Seed 7 carried a white star on a dark canton, which reads as a real flag too. Rejected.
- Seed 32 was a plain hanging cloth between two posts: no emblem, but it reads as a sign, not a war banner.
- Lesson: "war banner" pulls the model toward real flags. Ask for an object that has no emblem by nature.

## Round 2: used (seed 32)

    python pipeline/local_stills.py ep32 helmet --sprite --prompt "an ancient corroded bronze war helmet with green verdigris patina and a short crest, resting in dark soil, side view, single object, centered, no emblem" --seeds 32 12

- Seed 32: a rounded bronze helmet with a nasal bar and a brow band, green with verdigris and rusty flecks, its cheek pieces brown. It is a generic shape (no plume, no crest of a known culture, no marks), so it resembles no real artefact. Its green is EP32's motif colour, verdigris `#46c2a0`: the war's bronze, turned green in the ground. It is what the strata hold: a war that is buried, not gone.
- Seed 12 came back as a riveted bucket. Rejected.
- Saved as `helmet_sdxl_seed32.png` (1024×1024).

Then: `python pipeline/pixelate.py episodes/ep32/art/helmet_sdxl_seed32.png episodes/ep32/assets/war_sprite.png --width 84 --colors 24 --tol 60` (84×126, the flat grey backdrop keyed out; shown at ×3 on the field card). No compositional change was needed in code this time.

## Notes for the next episode
- The pixel-art LoRA draws a true pixel grid; `pixelate.py` only has to re-grid and key it.
- Look at every candidate before using it: two of three "war banner" seeds were real flags.
- No readable text in any generated image; all type is code.
