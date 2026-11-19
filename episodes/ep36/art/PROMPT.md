# EP36 art: the field-card sprite (free, local)

The user asked to try free tools first and use Figma only if none was good enough. EP36's one generated image (the field card's sprite for THE RUIN WAR) was made with the **free local SDXL-Lightning pipeline with the pixel-art LoRA** (`pipeline/local_stills.py --sprite`). **No Figma credits were used.** About 75 s an image on 4 CPU cores; it ran alone (it peaked near 14 GB of RAM; a first attempt with three seeds in one call died silently, so run one or two seeds per call).

## Two prompts, three candidates: the canvas tent, seed 7, used

    python pipeline/local_stills.py ep36 tent --sprite --prompt "a small plain canvas camp tent, simple ridge tent with wooden poles and ropes, single object, centered, plain, no flag, no emblem, no text" --seeds 36
    python pipeline/local_stills.py ep36 camp --sprite --prompt "pixel art sprite of a small canvas army tent with a tall plain wooden pole beside it, side view, crisp dark one-pixel outline, warm beige canvas, plain flat dark navy background, single object, centered, no flag, no emblem, no text" --seeds 7 12

- **Why a tent:** the Ruin War hasn't started; what exists is three camps. A plain canvas tent belongs to no army, uniform or nation. Flags were never asked for (EP32's "war banner" prompts came back as real national flags).
- **Checked for flags, emblems, symbols and real uniforms:** none in the three candidates.
- `tent` seed 36: a pale ridge tent on grey, almost no contrast. Rejected (reads as a paper fold at card size).
- `camp` seed 12: a broken lean-to on a tall pole. Rejected (no silhouette).
- `camp` seed 7: a warm canvas tent with a dark open front and a plain pole fitting on top. Used. Saved as `camp_sdxl_seed7.png`.

Then:

    python pipeline/pixelate.py episodes/ep36/art/camp_sdxl_seed7.png <tmp>/c64.png --width 64 --colors 24 --tol 60
    python episodes/ep36/art/war_threads.py <tmp>/c64.png episodes/ep36/assets/war_sprite.png

(64×116.) `war_threads.py` makes the compositional change in code: the pole's bluish top fitting is cleared and replaced by the flashpoint knot (flashpoint lime), and three threads, red, blue and gold, are strung from it to the sprite's edges, so the card carries the episode's device. Shown at ×3 on the field card.

## Everything else is code
The camps (plain canvas tents with a door flap in the side's colour), the standards (plain single colours, no device), the threads and the knot, the armies, the war room strip and its pixel icons (pin, anchor, shield, crown, clasp, spark, fume, host) and all type are drawn in code (`src/s2/world/WarRoom.tsx`, `src/s2/overlays/Pixel.tsx`).

## Notes for the next episode
- Ask for "plain flat dark navy background" and "crisp dark outline": the first prompt without them came back pale on grey.
- Run one or two seeds per call.
- No readable text in any generated image; all type is code.
