# EP33 art: the field-card sprite (free, local)

The user asked to try free tools first and use Figma only if none was good enough. EP33's one generated image (the field card's sprite for THE LAMPLIGHT) was made with the **free local SDXL-Lightning pipeline with the pixel-art LoRA** (`pipeline/local_stills.py --sprite`: SDXL 1.0 text encoders and VAE, ByteDance's 4-step Lightning UNet, nerijs/pixel-art-xl fused in; CreativeML OpenRAIL++-M / OpenRAIL-M, commercial use allowed). **No Figma credits were used.** About 90 s an image on 4 CPU cores; it ran alone (about 10 GB of RAM).

## One round (seeds 33, 8): seed 8 used

    python pipeline/local_stills.py ep33 lamp --sprite --prompt "an old iron hanging lantern with a glowing warm yellow candle flame inside, glass panes, a ring handle on top, single object, centered, plain, no emblem" --seeds 33 8

- **Why a lantern:** a religion has no body to draw, and EP33's device says a belief is a light that answers a fear. A plain iron lantern is a secular, everyday object: no faith uses it as its symbol, it carries no emblem, and its warm flame is the episode's motif colour, lamplight `#ffe45c`.
- **Checked for real symbols:** neither candidate shows any mark, cross, star, crescent, wheel, script or other sign; no shape reads as a real faith's lamp or vessel. The series shows no real religion, so this was checked first.
- Seed 33: a small lantern on a stand inside a pale square backdrop that the model drew as part of the image (a frame artifact). Rejected.
- Seed 8: a round iron cage lantern with a ring handle and a tall candle behind pale glass. Generic, symmetrical, no marks. Used.
- Saved as `lantern_sdxl_seed8.png` (1024×1024).

Then:

    python pipeline/pixelate.py episodes/ep33/art/lantern_sdxl_seed8.png episodes/ep33/assets/lamp_sprite.png --width 60 --colors 24 --tol 60

(60×130; the first try at width 84 came out 186 px tall, which would have pushed the intro card's text off its panel.) `pixelate.py` keys the backdrop from the edges, so the grey seen *through* the cage (inside the handle ring and between the bars) stayed; a small step in code then keyed every pale, unsaturated pixel (min channel > 185, spread < 22) to transparent, 1,392 pixels, which turns the panes into an open cage over the card's navy. Shown at ×3 on the field card.

## Notes for the next episode
- Ask for an object that is secular by nature when the subject is a belief: the model then has nothing religious to borrow.
- `pixelate.py` only keys background connected to the edge; anything seen through a frame or handle needs the extra keying step.
- No readable text in any generated image; all type is code.
