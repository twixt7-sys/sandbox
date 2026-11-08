# EP29 art prompts (Figma `generate_image`)

File "Worldcraft Shorts EP26 art" (`7wHdle0cigAS8MhVmZzZYJ`, the season's sprite file), 8 Nov 2026. Requested 1536×1024. The user approved up to 2 generations for EP29; 1 was used.

## The Undying Queen field-card sprite: used (`gpt-image-2.5-sunburst`, 1 generation, first try)

> Detailed 16-bit pixel art sprite of an original fantasy character, full body, side view facing right, standing tall and perfectly still with calm upright posture. An ageless immortal queen: a long flowing deep violet robe with a lighter lavender inner lining and a simple gold trim at the hem and cuffs, a high collar, long straight silver-white hair falling down her back, a youthful serene pale face with a faint knowing smile, a thin plain gold circlet crown on her brow, hands folded in front holding a small closed hourglass. Timeless, regal, gentle, not menacing. Limited palette, crisp dark one-pixel outline, clean readable silhouette, centred with generous empty space around it, on a plain flat dark navy background. No ground, no scenery, no text, no letters, no labels, no watermark.

- Output: `queen_sunburst.png` (1536×1024, node `4:2`).
- Re-gridded with `python pipeline/pixelate.py episodes/ep29/art/queen_sunburst.png episodes/ep29/assets/queen_sprite.png --width 56 --colors 22 --tol 70` (56×107, transparent). At the default `--tol 40`, navy background specks stayed in her hair.
- The voxel Queen (`src/s2/world/People.tsx`) was built to its palette: robe `#6a43a0` / `#4c3070` (brighter than the sprite's `#54346c` so it reads in daylight), lavender lining `#bba4c7`, silver hair `#ece2e0`, gold circlet and hourglass `#e9b85a`, rose-gold hem `#d7a9a3`.
