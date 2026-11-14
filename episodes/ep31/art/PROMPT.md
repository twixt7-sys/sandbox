# EP31 art: the statue field-card sprite (free, local)

The user asked to try free tools first and use Figma only if none was good enough. EP31's one generated image (the field card's statue sprite) was made with the **free local SDXL-Lightning pipeline** (`pipeline/local_stills.py`: SDXL 1.0 text encoders and VAE plus ByteDance's 4-step Lightning UNet, CreativeML OpenRAIL++-M, commercial use allowed). **No Figma credits were used.** Each image took 94–109 s on the container's 4 CPU cores, and the run needs about 10 GB of RAM, so it ran alone (alongside a Kokoro TTS build it was killed for memory).

The call was `local_stills.generate()` with `STYLE` set to `", 16-bit pixel art sprite, dark outline, flat dark navy background, no text"` and 768×1344 output.

## Round 1: rejected (seeds 31 and 47)

> pixel art sprite of a weathered stone statue of a heroic woman holding a torch raised high, standing on a square plinth, full body, front view, the left half of the statue gilded bright gold with flower garlands, the right half blackened with dark tar and scratched

- Both came back as gold, crowned classical figures in a painted-illustration style, not pixel art. Seed 47 (crown, raised torch, draped robe, stepped plinth) reads as a famous real monument, which the series must not imitate.
- Neither did the split: the model ignored "left half gilded, right half tarred". A diffusion model at 4 steps doesn't follow layout instructions like that.

## Round 2: used (seed 62)

> grey stone statue of a hooded shepherd woman in a plain long cloak, one arm raising a burning torch, bare head under the hood, standing on a square stone plinth, full body, front view, symmetrical

- No crown and a plain hood, so it resembles no real statue. Seed 5 held one torch with its flame running down the staff; seed 62 held **a torch in each hand** on a two-step plinth, symmetrical, which suits a figure two peoples remember differently. The voxel statue in the world (`Statue` in `src/s2/world/People.tsx`) is built to it: hood, two torches, two-step plinth.
- Saved as `statue_sdxl_seed62.png` (768×1344).

## The split, in code
`python episodes/ep31/art/split_statue.py` keys the flat grey backdrop to the series navy (only background connected to the image border counts, because the statue's own mid-greys match the backdrop), gilds the left half (dark bronze to bright gold by luminance), tars the right half (near-black to warm grey), keeps the torch flames, draws three rust scratches across the tarred half, and crops. Output: `statue_split.png` (674×1344).

Then: `python pipeline/pixelate.py episodes/ep31/art/statue_split.png episodes/ep31/assets/statue_sprite.png --width 62 --colors 24 --tol 18` (62×127, transparent; shown at ×3 on the field card).

## Notes for the next episode
- Ask the model for the plain subject on a flat background; make any compositional change (a split, a recolour, a mark) in code. It is exact, repeatable and free.
- Look at every candidate before using it. A "heroic woman with a torch on a plinth" will drift toward a real landmark.
- A pixel-art LoRA for SDXL was tested afterwards for future sprites; the result is recorded in `episodes/ep31/BRIEF.md` §5.
- No readable text in any generated image; all type is code.
