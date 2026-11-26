#!/usr/bin/env python3
"""App icons: a gold wireframe globe on the deep-ocean gradient.   python3 tools/make_icons.py

docs/icon-192.png, docs/icon-512.png  full-bleed squares, globe inside the maskable safe zone
                                      (central 80% circle), so they serve as "any maskable"
docs/icon-mono.png                    white globe on transparent ("monochrome" purpose)
docs/badge-96.png                     small white globe for Android notification badges (alpha only)
Drawn at 4x and scaled down for smooth lines. Needs Pillow."""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
GOLD = (246, 195, 68, 255)
WHITE = (255, 255, 255, 255)


def globe_on(img, cx, cy, r, w, col):
    """Draw the globe on img, with every line clipped to the outer ring."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    globe(ImageDraw.Draw(layer), cx, cy, r, w, col)
    mask = Image.new("L", img.size, 0)
    o = r - 1                      # PIL draws the ring inward, so its outer edge is r
    ImageDraw.Draw(mask).ellipse([cx - o, cy - o, cx + o, cy + o], fill=255)
    img.alpha_composite(Image.composite(layer, Image.new("RGBA", img.size, (0, 0, 0, 0)), mask))


def globe(d, cx, cy, r, w, col):
    """Circle, 3 meridian ellipses, the equator and two parallels."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)
    for f in (0.0, 0.42, 0.78):           # meridians: a line, then narrower-to-wider ellipses
        rx = r * f
        if rx < w:
            d.line([(cx, cy - r), (cx, cy + r)], fill=col, width=w)
        else:
            d.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=col, width=w)
    d.line([(cx - r, cy), (cx + r, cy)], fill=col, width=w)
    for k in (-1, 1):                      # parallels at +-45 degrees latitude
        y = cy + k * r * 0.7071
        half = r * 0.7071 + w
        d.line([(cx - half, y), (cx + half, y)], fill=col, width=w)


def ocean(size):
    img = Image.new("RGBA", (size, size))
    top, bot = (11, 42, 74), (14, 53, 96)
    px = img.load()
    for y in range(size):
        t = y / (size - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,)
        for x in range(size):
            px[x, y] = c
    return img


def app_icon(size):
    K = 4
    S = size * K
    img = ocean(S)
    globe_on(img, S / 2, S / 2, S * 0.30, max(2, int(S * 0.024)), GOLD)
    return img.resize((size, size), Image.LANCZOS)


def mono(size, frac=0.40, wfrac=0.05):
    K = 4
    S = size * K
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    globe_on(img, S / 2, S / 2, S * frac, max(2, int(S * wfrac)), WHITE)
    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    for n in (192, 512):
        app_icon(n).save(os.path.join(OUT, "icon-%d.png" % n), optimize=True)
    mono(512, 0.30, 0.024).save(os.path.join(OUT, "icon-mono.png"), optimize=True)
    mono(96, 0.42, 0.045).save(os.path.join(OUT, "badge-96.png"), optimize=True)
    print("icons written to", os.path.abspath(OUT))
