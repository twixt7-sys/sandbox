"""EP34: dissolve the end of the falling lantern's trail (it runs off the generated image's corner).

    python episodes/ep34/art/fade_trail.py <pixelated.png> episodes/ep34/assets/firstlamp_sprite.png

pipeline/pixelate.py keys the backdrop and crops to the subject, so the trail ends in a hard edge at the sprite's top
right. This removes trail pixels with a 4x4 ordered (Bayer) dither whose threshold rises along the line from the
lantern towards that corner, so the trail thins out into single pixels like the painted one on the dome. The lantern
itself (the lower part of the sprite) is untouched.
"""
import sys

from PIL import Image

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def main(src, dst, start=0.5, span=0.42):
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    px = im.load()
    ox, oy = w * 0.45, h * 0.78          # the lantern's body
    vx, vy = w - ox, -oy                 # towards the top-right corner
    L2 = vx * vx + vy * vy
    removed = 0
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0:
                continue
            t = ((x - ox) * vx + (y - oy) * vy) / L2
            k = (t - start) / span
            if k > 0 and BAYER[y % 4][x % 4] / 16 < k:
                px[x, y] = (0, 0, 0, 0)
                removed += 1
    im.save(dst)
    print(f"[fade_trail] {dst}: {w}x{h}, {removed} trail pixels dissolved")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
