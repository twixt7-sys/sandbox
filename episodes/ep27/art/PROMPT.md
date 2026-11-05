# EP27 art prompts (Figma `generate_image`)

File "Worldcraft Shorts EP26 art" (`7wHdle0cigAS8MhVmZzZYJ`, reused for the season's sprites), plan `team::1384938462301182142`, 5 Nov 2026. Requested 1536×1024. The user approved up to 2 generations for EP27; 1 was used.

## Dragon field-card sprite: used (`gpt-image-2.5-sunburst`, 1 generation, first try)

> Detailed 16-bit pixel art sprite of an original fantasy creature, full body, side view facing right, standing on all fours with mouth closed and both wings raised and half-spread above its back. The creature is a lean wyvern-like dragon of rocky coasts: long neck, narrow horned head with two swept-back pale horns, rust-red scaled hide shading to deep brick-red on the back, a paler ochre belly, broad bat-like wings with dark rust membranes and pale bone-coloured wing fingers, a long tapering tail ending in a small spade, pale bone claws, one small glowing amber eye. Limited palette, crisp dark one-pixel outline, clean readable silhouette, centred with generous empty space around it, on a plain flat dark navy background. No ground, no fire, no scenery, no text, no letters, no labels, no watermark.

- Output: `dragon_sunburst.png` (1536×1024, node `2:2` in the file).
- Re-gridded with `python pipeline/pixelate.py episodes/ep27/art/dragon_sunburst.png episodes/ep27/assets/dragon_sprite.png --width 168 --colors 28` (168×116, transparent).
- The voxel dragon (`src/s2/world/Dragon.tsx`) was built to match its palette and silhouette: rust-red hide, ochre belly, dark rust membranes on pale bone fingers, swept-back pale horns, amber eye, spade tail.
