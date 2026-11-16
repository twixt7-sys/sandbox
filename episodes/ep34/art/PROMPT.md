# EP34 art: the field-card sprite (free, local)

The user asked to try free tools first and use Figma only if none was good enough. EP34's one generated image (the field card's sprite for THE FIRST LAMP, the Lamplight faith's creation myth) was made with the **free local SDXL-Lightning pipeline with the pixel-art LoRA** (`pipeline/local_stills.py --sprite`: SDXL 1.0 text encoders and VAE, ByteDance's 4-step Lightning UNet, nerijs/pixel-art-xl fused in; CreativeML OpenRAIL++-M / OpenRAIL-M, commercial use allowed). **No Figma credits were used.** About 75 s an image on 4 CPU cores; it ran alone (about 10 GB of RAM).

## Two prompts, two seeds each: the falling lantern, seed 7, used

    python pipeline/local_stills.py ep34 star --sprite --prompt "a glowing falling star with a long bright golden tail streaking diagonally down, a white hot core, single object, centered, simple" --seeds 34 7
    python pipeline/local_stills.py ep34 lamp --sprite --prompt "an old brass lantern falling through the air, tilted, a warm glowing flame inside, a trail of golden light behind it, single object, centered, plain, no emblem" --seeds 34 7

- **Why a falling lantern:** the myth says the First Lamp "fell from the sky, and the world began", and the twist says it was a star. A lantern with a trail of light behind it is the myth exactly, and its trail is the fair-play clue (it falls like a comet). A lantern is a plain, secular object: no faith uses it as its symbol and it carries no emblem.
- **Checked for real symbols:** none of the four candidates shows any mark, cross, star of a real faith, crescent, wheel, script or other sign; nothing reads as a real faith's lamp, vessel or monument.
- `star` seed 34: a jagged vertical streak that reads as lightning. Rejected.
- `star` seed 7: a smear of tail cropped by the frame with a small four-point star under it. Rejected (no subject).
- `lamp` seed 34: an upright lantern with fire bursting out of its top on a pale backdrop. Rejected (reads as burning, not falling).
- `lamp` seed 7: a brass kerosene-style lantern with a ring handle and a warm flame behind its panes, a broad trail of golden light running up and away from it. Used. Saved as `lamp_sdxl_seed7.png` (1024×1024).

Then:

    python pipeline/pixelate.py episodes/ep34/art/lamp_sdxl_seed7.png <tmp>/lamp_px76.png --width 76 --colors 28 --tol 60
    python episodes/ep34/art/fade_trail.py <tmp>/lamp_px76.png episodes/ep34/assets/firstlamp_sprite.png

(76×124; a first try at width 84 came out 138 px tall.) The trail runs off the generated image's top-right corner, so after `pixelate.py` keyed the backdrop it ended in a hard edge. `fade_trail.py` removes trail pixels with a 4×4 ordered dither whose threshold rises along the line from the lantern to that corner (786 pixels), so the trail thins out into single pixels, like the trail painted on the dome. Shown at ×3 on the field card.

## Everything else is code
The painted sky itself (its lapis bands, gilt four-point stars, clouds, gold wave band and the First Lamp with its rays, trail and drops) is drawn pixel by pixel in `src/s2/world/Sky.tsx`, so it carries no generated imagery. Its only motifs are a lantern, four-point sparkles, clouds and a wave band; no halo, sun face, eye, real star shape or script.

## Notes for the next episode
- Ask for an object, not an event: "a falling star" alone gave a streak or a smear; "a lantern falling, a trail of light behind it" gave a subject with motion.
- A trail or ray that runs off the image's edge survives `pixelate.py` (it isn't background) and ends in a hard cut; dither it out in code.
- No readable text in any generated image; all type is code.
