# EP26 art prompts (Figma `generate_image`)

File "Worldcraft Shorts EP26 art" (`7wHdle0cigAS8MhVmZzZYJ`), plan `team::1384938462301182142`, 1 Nov 2026. Requested 1536×1024.

## Grimmaw field-card sprite: used (`gpt-image-2.5-sunburst`, 1 generation, first try)

> Detailed 16-bit pixel art sprite of an original fantasy creature, full body, side view facing right, standing calmly with mouth closed. The creature is a huge four-legged apex predator of grassy highlands: heavy hunched shoulders, long powerful front legs, lower hips, short thick tail, an oversized bony head with a wide underslung jaw, a ridge of rust-orange bony plates along the spine, charcoal-slate hide with faint darker stripes, pale bone-coloured jaw ridge and claws, small glowing amber eyes. Limited palette, crisp dark one-pixel outline, clean readable silhouette, centred with generous empty space around it, on a plain flat dark navy background. No ground, no scenery, no text, no letters, no labels, no watermark.

- Output: `grimmaw_sunburst.png` (1536×1024).
- Re-gridded with `python pipeline/pixelate.py episodes/ep26/art/grimmaw_sunburst.png episodes/ep26/assets/grimmaw_sprite.png --width 168 --colors 28` (168×108, transparent).
- The same prompt on `gpt-image-2.5-flare` and `gemini-3.1-flash-image` (for a model comparison) was blocked by the session's permission check before it ran, so it used no credits.
