"""EP35: set last night's stone into the Builders' sprite. The generated heap of old blocks has no new stone (the model
can't follow "one block is new"), so the top block (pixels in BOX, the re-gridded sprite's coordinates) is recoloured
in code: every stone-grey pixel inside it is mapped by its brightness onto a quartz-cyan ramp, and the dark outline is
kept. Usage: python episodes/ep35/art/fresh_stone.py <re-gridded.png> <out.png>"""
import sys
from PIL import Image

BOX = (25, 1, 49, 21)  # x0, y0, x1, y1 (exclusive): the top tier (a capstone and the two blocks under it)
RAMP = [(31, 92, 122), (53, 156, 196), (79, 214, 255), (196, 246, 255)]

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGBA")
px = im.load()
n = 0
for y in range(BOX[1], BOX[3]):
    for x in range(BOX[0], BOX[2]):
        r, g, b, a = px[x, y]
        if a < 128:
            continue
        lum = 0.3 * r + 0.59 * g + 0.11 * b
        if lum < 70 or abs(g - r) > 30:  # the outline and any moss stay
            continue
        k = min(3, int((lum - 70) / 40))
        px[x, y] = RAMP[k] + (255,)
        n += 1
im.save(dst)
print(f"[fresh_stone] {n} pixels set in quartz -> {dst} {im.size}")
