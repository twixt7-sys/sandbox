# EP30 art prompts (Figma `generate_image`)

File "Worldcraft Shorts EP26 art" (`7wHdle0cigAS8MhVmZzZYJ`, the season's sprite file), 12 Nov 2026. Requested 1536×1024. The user approved up to 2 generations for EP30; 1 was used.

## The worshipped Grimmaw field-card sprite: used (`gpt-image-2.5-sunburst`, 1 generation, first try)

> Detailed 16-bit pixel art sprite of an original fantasy creature, full body, side view facing right, standing calmly and proudly with mouth closed, head slightly raised. The creature is a huge four-legged apex predator of grassy highlands that a farming village honours: heavy hunched shoulders, long powerful front legs, lower hips, short thick tail, an oversized bony head with a wide underslung jaw, a ridge of rust-orange bony plates along the spine, charcoal-slate hide with faint darker stripes, pale bone-coloured jaw ridge and claws, small glowing amber eyes. It wears a thick braided garland of golden wheat ears around its neck, and simple painted rose-pink stripe markings on its shoulder and flank. Majestic, sacred, dangerous but calm. Limited palette, crisp dark one-pixel outline, clean readable silhouette, centred with generous empty space around it, on a plain flat dark navy background. No ground, no scenery, no people, no symbols, no text, no letters, no labels, no watermark.

- The prompt is EP26's Grimmaw prompt (`episodes/ep26/art/PROMPT.md`) plus the garland and the painted markings, so it is the same creature, honoured. "No symbols" keeps any real-world religious sign out of it.
- Output: `grimmaw_worshipped_sunburst.png` (1536×1024, node `5:2`).
- Re-gridded with `python pipeline/pixelate.py episodes/ep30/art/grimmaw_worshipped_sunburst.png episodes/ep30/assets/grimmaw30_sprite.png --width 168 --colors 28` (168×112, transparent).
- The voxel adornment (`ADORN` in `src/s2/world/Creatures.tsx`) follows its palette: wheat `#e3c27a` / `#b98a4e` (sprite `#c4a076` / `#946548`, brightened to read in daylight) and painted stripes `#e0687f` (sprite `#94544b`, pushed toward the episode's madder).
