# EP35 art: the field-card sprite (free, local)

The user asked to try free tools first and use Figma only if none was good enough. EP35's one generated image (the field card's sprite for THE BUILDERS, the lost civilization) was made with the **free local SDXL-Lightning pipeline with the pixel-art LoRA** (`pipeline/local_stills.py --sprite`: SDXL 1.0 text encoders and VAE, ByteDance's 4-step Lightning UNet, nerijs/pixel-art-xl fused in; CreativeML OpenRAIL++-M / OpenRAIL-M, commercial use allowed). **No Figma credits were used.** About 77 s an image on 4 CPU cores; it ran alone (about 10–12 GB of RAM).

## Two prompts, five candidates: the heap of blocks, seed 35, used

    python pipeline/local_stills.py ep35 wall --sprite --prompt "a short broken section of an old wall built from large plain squared grey stone blocks, moss on the broken top, one clean new pale stone block set into it, single object, centered, plain, no carvings" --seeds 35 7 12
    python pipeline/local_stills.py ep35 block --sprite --prompt "a small heap of old mossy grey stone blocks with one clean bright new stone block on top, single object, centered, plain, no carvings" --seeds 35 7

- **Why a heap of plain blocks:** the Builders are known only by what they left, and the episode's mystery is a stone that is newer than the rest. Plain squared stone is secular and belongs to no real culture: no columns, capitals, arches, carvings, glyphs or script, and no pyramid, ziggurat, henge or temple shape.
- **Checked for real monuments and symbols:** none of the five shows a carving, script, symbol or a silhouette that reads as a real monument. None drew the new stone either (the model can't follow "one block is new").
- `wall` seeds 35 and 12: a flat, full-frame brick texture with no silhouette. Rejected (no subject at card size).
- `wall` seed 7: a mossy beehive of stacked blocks. Rejected (reads as a hut, not a ruin).
- `block` seed 7: a rounded heap of cobbles. Rejected (reads as a dry-stone well or hut).
- `block` seed 35: a stepped, tapering heap of squared mossy grey blocks with a capstone. Used. Saved as `builders_sdxl_seed35.png` (1024×1024).

Then:

    python pipeline/pixelate.py episodes/ep35/art/builders_sdxl_seed35.png <tmp>/b72.png --width 72 --colors 24 --tol 60
    python episodes/ep35/art/fresh_stone.py <tmp>/b72.png episodes/ep35/assets/builders_sprite.png

(72×135.) `fresh_stone.py` makes the compositional change in code: the top tier (the capstone and the two blocks under it, a fixed box in the re-gridded sprite) is mapped by brightness onto a quartz-cyan ramp, keeping the dark outline and any moss, so the sprite carries the episode's clue: the newest stones are at the top. Shown at ×3 on the field card.

## Everything else is code
The wall itself (every block, its age, the repair log's colours, last night's and tonight's stones), the gear, the kitchen, the wells, the handprints, the dig pits, the standards, the pixel icons in the finds tray (gear, pot, well, handprint, stone, question mark, three banners) and all type are drawn in code (`src/s2/world/Ruins.tsx`, `src/s2/overlays/Pixel.tsx`).

## Notes for the next episode
- A prompt about a *texture* ("a wall built from blocks") fills the frame with texture; ask for a small *object* with a silhouette ("a small heap of …").
- The model ignores "one block is different": ask for the plain object and make the change in code.
- No readable text in any generated image; all type is code.
