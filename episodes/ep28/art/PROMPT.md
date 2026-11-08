# EP28 art prompts (Figma `generate_image`)

File "Worldcraft Shorts EP26 art" (`7wHdle0cigAS8MhVmZzZYJ`, the season's sprite file), plan `team::1384938462301182142`, 7 Nov 2026. Requested 1536×1024. The user approved up to 2 generations for EP28; 1 was used.

## Fenn field-card sprite: used (`gpt-image-2.5-sunburst`, 1 generation, first try)

> Detailed 16-bit pixel art sprite of an original fantasy creature, full body, side view facing right, standing upright and holding a small round grey stone in both hands at chest height. The creature is a small slender two-legged intelligent amphibious species of lakeshores: smooth glossy teal-green skin shading to deep sea-green on the back, a pale mint belly, very large dark round night-adapted eyes with a tiny bright highlight, a small flat nose, no hair, two soft fin-like frills on the sides of the head instead of ears, a row of small glowing aqua spots along its arms and cheeks, long thin fingers, wide flat webbed feet, a short simple woven reed sash across the body. Calm, curious, gentle expression. Limited palette, crisp dark one-pixel outline, clean readable silhouette, centred with generous empty space around it, on a plain flat dark navy background. No ground, no scenery, no text, no letters, no labels, no watermark.

- Output: `fenn_sunburst.png` (1536×1024, node `3:2`).
- Re-gridded with `python pipeline/pixelate.py episodes/ep28/art/fenn_sunburst.png episodes/ep28/assets/fenn_sprite.png --width 52 --colors 24` (52×127, transparent). The figure is tall and slim, so it's narrower than the Grimmaw's and the dragon's sprites; the field card takes any sprite size (`spriteW` / `spriteH`).
- The voxel Fenn (`src/s2/world/Folk.tsx`) was built to match it: teal skin with a darker back and mint belly, big dark eyes, fin frills, glow spots, a reed sash, webbed feet.
