"""Decoy guests: look-alikes of people (and a dog) from Mira's life who are NOT hers.
Made from the real sprites by recolouring exactly one detail, so the player has to compare with the dossier photos.
  fakedog     <- biscuit   : collar red -> blue
  fakemom     <- mom       : lilac cardigan -> sage green
  fakeboss    <- grayline  : red tie -> navy tie
  faketeacher <- okafor    : orange beret -> green beret
Run: python gen_decoys.py   (reads/writes art/px/out/v_*.png)"""
import colorsys
from PIL import Image

OUT = 'out/'
# (new id, source id, region (x0, y0, x1, y1), hue window (lo, hi) in degrees, min saturation, target hue, sat multiplier, max lightness)
DECOYS = [
    ('fakedog', 'biscuit', (6, 55, 58, 64), (345, 14), .35, 215, 1.0, .55),
    ('fakemom', 'mom', (0, 52, 64, 76), (260, 345), .08, 150, 1.1, 1),
    ('fakeboss', 'grayline', (24, 54, 44, 76), (340, 20), .30, 222, 1.0, 1),
    ('faketeacher', 'okafor', (0, 0, 64, 30), (18, 50), .40, 140, .55, 1),
]


def in_window(h, lo, hi):
    return lo <= h <= hi if lo <= hi else (h >= lo or h <= hi)


def make(new, src, box, win, smin, hue, sm, lmax):
    im = Image.open(f'{OUT}v_{src}.png').convert('RGBA')
    px = im.load()
    x0, y0, x1, y1 = box
    n = 0
    for y in range(y0, min(y1, im.height)):
        for x in range(x0, min(x1, im.width)):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if s < smin or l > lmax or not in_window(h * 360, *win):
                continue
            nr, ng, nb = colorsys.hls_to_rgb(hue / 360, l, min(1, s * sm))
            px[x, y] = (round(nr * 255), round(ng * 255), round(nb * 255), a)
            n += 1
    im.save(f'{OUT}v_{new}.png')
    print(new, 'recoloured', n, 'px')


if __name__ == '__main__':
    for d in DECOYS:
        make(*d)
