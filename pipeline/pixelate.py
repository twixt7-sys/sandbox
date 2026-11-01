"""Turn generated creature art into clean, season-palette pixel art (Season 2).

Image models paint "pixel art" on an irregular grid with soft, noisy edges. This script re-grids it:
crop to the subject, sample each block by its most common colour (no blending), reduce to a small palette,
and key the flat background out to transparency. The output is a small PNG that Remotion upscales with
`image-rendering: pixelated`, so it sits beside the low-resolution 3D diorama without looking pasted in.

Usage:
  python pipeline/pixelate.py episodes/ep26/art/grimmaw_sunburst.png public-src.png --width 160 --colors 20
Options:
  --width N     sprite width in output pixels (height follows the crop's aspect)
  --colors N    palette size after quantisation (median cut)
  --tol N       background key tolerance (sum of RGB differences), default 40
  --margin N    crop margin around the subject, in sprite pixels, default 2
  --flip        mirror horizontally (e.g. to face left)
"""
from __future__ import annotations

import argparse
from collections import Counter

import numpy as np
from PIL import Image
from scipy import ndimage


def background_colour(a: np.ndarray) -> np.ndarray:
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    return np.median(border, axis=0)


def background_mask(img: np.ndarray, bg: np.ndarray, tol: int) -> np.ndarray:
    """Background = close to the backdrop colour *and* the same hue cast, connected to the image border.

    The hue test keeps a creature's own near-black shading (neutral greys) from being keyed out with a navy backdrop.
    """
    close = np.abs(img - bg).sum(axis=2) <= tol
    cast = (img[..., 2] - img[..., 0]) - (bg[2] - bg[0])
    near = close & (np.abs(cast) <= 14)
    lab, _ = ndimage.label(near)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(border))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--width", type=int, default=160)
    ap.add_argument("--colors", type=int, default=20)
    ap.add_argument("--tol", type=int, default=40)
    ap.add_argument("--margin", type=int, default=2)
    ap.add_argument("--flip", action="store_true")
    args = ap.parse_args()

    img = np.asarray(Image.open(args.src).convert("RGB")).astype(np.int32)
    bg = background_colour(img)
    bgmask = background_mask(img, bg, args.tol)
    fg = ~bgmask
    ys, xs = np.where(fg)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1

    block = (x1 - x0) / (args.width - 2 * args.margin)
    pad = int(round(args.margin * block))
    y0, x0 = max(0, y0 - pad), max(0, x0 - pad)
    y1, x1 = min(img.shape[0], y1 + pad), min(img.shape[1], x1 + pad)
    crop = img[y0:y1, x0:x1]
    cmask = bgmask[y0:y1, x0:x1]
    w = args.width
    h = max(1, int(round(crop.shape[0] / block)))

    # Mode-sample each block (the most common quantised colour), so edges stay hard instead of averaging to mud.
    small = np.zeros((h, w, 3), np.int32)
    alpha = np.zeros((h, w), np.uint8)
    for j in range(h):
        for i in range(w):
            ys_, xs_ = slice(int(j * block), max(int(j * block) + 1, int((j + 1) * block))), slice(int(i * block), max(int(i * block) + 1, int((i + 1) * block)))
            b, m = crop[ys_, xs_].reshape(-1, 3), cmask[ys_, xs_].reshape(-1)
            if m.size == 0 or m.mean() > 0.5:
                small[j, i] = bg
                continue
            alpha[j, i] = 255
            q = (b[~m] // 8) * 8 + 4
            small[j, i] = Counter(map(tuple, q)).most_common(1)[0][0]

    pal_img = Image.fromarray(small.astype(np.uint8)).quantize(colors=args.colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    rgb = np.asarray(pal_img.convert("RGB")).astype(np.int32)
    out = np.dstack([rgb.astype(np.uint8), alpha])
    res = Image.fromarray(out, "RGBA")
    if args.flip:
        res = res.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    res.save(args.dst)
    print(f"[pixelate] {args.src} -> {args.dst}: {w}x{h} px, {args.colors} colours, block {block:.2f} src px")


if __name__ == "__main__":
    main()
