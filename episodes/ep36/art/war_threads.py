"""EP36: tie the war room's threads to the field-card sprite. The generated tent (seed 7) is a plain canvas tent with
a pole; the model can't draw "three coloured threads meeting at a knot", so it is done in code on the re-gridded sprite:
the pole's top fitting becomes the flashpoint knot (flashpoint lime, outlined) and three threads, one per side (red,
blue, gold), are strung from it down to the sprite's edges, each two pixels wide with a dark outline pixel under it.
Usage: python episodes/ep36/art/war_threads.py <re-gridded.png> <out.png>"""
import sys
from PIL import Image

KNOT = (30, 5)                    # the pole's top, in the re-gridded sprite's coordinates (64 wide)
THREADS = [((0, 34), (192, 87, 60)), ((63, 30), (79, 127, 191)), ((63, 70), (212, 178, 63))]
LIME = [(122, 150, 36), (200, 240, 74), (232, 252, 170)]
OUT = (18, 21, 28)

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGBA")
W, H = im.size
px = im.load()


def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        px[x, y] = c + (255,)


# clear the old pole fitting (the bluish-grey pixels above the ridge) back to the pole's brown
for y in range(0, 18):
    for x in range(20, 40):
        r, g, b, a = px[x, y]
        if a > 128 and b > r:
            px[x, y] = (0, 0, 0, 0)
for (ex, ey), c in THREADS:
    n = max(abs(ex - KNOT[0]), abs(ey - KNOT[1]))
    for k in range(n + 1):
        x = round(KNOT[0] + (ex - KNOT[0]) * k / n)
        y = round(KNOT[1] + (ey - KNOT[1]) * k / n + 2.5 * (k / n) * (1 - k / n) * 4)   # a little sag
        put(x, y + 2, OUT)
        put(x, y, c)
        put(x, y + 1, c)
# the knot: a 6x6 lime blob with a dark outline, light top-left
for y in range(-4, 4):
    for x in range(-4, 4):
        d = max(abs(x + 0.5), abs(y + 0.5))
        if d <= 3.5:
            put(KNOT[0] + x, KNOT[1] + y, OUT if d > 2.6 else LIME[2] if (x < -1 and y < -1) else LIME[1] if d < 1.6 else LIME[0] if (x > 0 and y > 0) else LIME[1])
im.save(dst)
print(f"[war_threads] knot and three threads -> {dst} {im.size}")
