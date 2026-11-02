"""Tile a folder of stills into one contact image for review: python pipeline/tile.py out/ep26_beats out/ep26_beats.jpg [cols] [width]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

src, dst = Path(sys.argv[1]), sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 5
w = int(sys.argv[4]) if len(sys.argv) > 4 else 360
files = sorted(src.glob("*.jpg"))
h = int(w * 16 / 9)
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), (0, 0, 0))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS)
    x, y = (i % cols) * w, (i // cols) * h
    sheet.paste(im, (x, y))
    frame = int(f.stem.split("_")[-1])
    d.rectangle([x, y, x + 74, y + 22], fill=(0, 0, 0))
    d.text((x + 4, y + 4), f"{frame / 30:.1f}s", fill=(255, 255, 0))
sheet.save(dst, quality=88)
print(f"[tile] {len(files)} -> {dst}")
