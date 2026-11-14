"""EP31 field-card sprite: take the free local SDXL statue (statue_sdxl_seed62.png), key its flat grey background to
the series navy, gild the left half and tar the right half (rust scratches), keeping the torch flames, then hand the
result to pipeline/pixelate.py. Run from the repo root: python episodes/ep31/art/split_statue.py"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = Path(__file__).resolve().parent
im = Image.open(HERE / "statue_sdxl_seed62.png").convert("RGB")
a = np.asarray(im).astype(float)
h, w, _ = a.shape
bg = np.median(np.concatenate([a[:40, :40].reshape(-1, 3), a[:40, -40:].reshape(-1, 3)]), axis=0)
close = np.abs(a - bg).sum(axis=2) < 34
# only background that connects to the image border counts: the statue's own mid-greys match the backdrop
lab, _ = ndimage.label(close)
edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
is_bg = np.isin(lab, edge[edge > 0])
mx, mn = a.max(axis=2), a.min(axis=2)
sat = (mx - mn) / np.maximum(mx, 1)
flame = (sat > 0.38) & (a[..., 0] > 150) & (a[..., 0] > a[..., 2] + 40)
lum = (a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11) / 255
cols = np.where(~is_bg.all(axis=0))[0]
cx = (cols.min() + cols.max()) // 2
out = a.copy()
t = np.clip((lum - 0.08) / 0.5, 0, 1)[..., None] ** 0.85
gold = np.array([96, 60, 22]) * (1 - t) + np.array([255, 214, 122]) * t
tar = np.array([44, 34, 30]) * (1 - t) + np.array([98, 88, 84]) * t
left = np.zeros((h, w), bool)
left[:, :cx] = True
body = ~is_bg & ~flame
out[body & left] = gold[body & left]
out[body & ~left] = tar[body & ~left]
out[is_bg] = np.array([13, 22, 48])
res = Image.fromarray(out.clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(res)
for k in range(3):  # rust scratches across the tarred half
    x0, y0 = cx + 60 + k * 26, int(h * 0.42) + k * 70
    d.line([(x0, y0), (x0 + 120, y0 + 50)], fill=(208, 96, 63), width=9)
rows = np.where(~is_bg.all(axis=1))[0]
m = 30
res = res.crop((max(0, cols.min() - m), max(0, rows.min() - m), min(w, cols.max() + m), min(h, rows.max() + m)))
res.save(HERE / "statue_split.png")
print("wrote statue_split.png", res.size, "centre x", cx)
