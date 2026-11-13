"""Dream scenes: the places of Mira's dreams as little rooms, 312x152 (same pixel size as the guests).
Layers, back to front:  dream_<place>.png (room)  ->  the guest (64x76 bust)  ->  dream_<place>_fg.png
(whatever hides the bottom of the bust: a counter, a desk...)  ->  mira_back.png (Mira, seen from behind).
Style = the office room: muted mid-dark ramps, flat slabs with a light top/left edge and a dark bottom/right
edge, 1px dark outline on objects, very little dither.
Run: python gen_dream.py   (writes .px, then out/*.png)"""
import math
import os
import subprocess
import sys

import gen_visitors as gv
from pxlib import Cv, Pal, sphere, strands, texture, lvl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
RENDER = os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'pixel-art-studio', 'scripts', 'render.py')
W, H = 312, 152
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def bayer(x, y, t):
    return (BAYER[y % 4][x % 4] + 0.5) / 16 < t


def png(name):
    subprocess.run([sys.executable, os.path.join(HERE, 'grid2json.py'), os.path.join(HERE, f'{name}.px'),
                    os.path.join(OUT, f'{name}.json')], check=True)
    subprocess.run([sys.executable, RENDER, os.path.join(OUT, f'{name}.json'), '-o', os.path.join(OUT, f'{name}.png'),
                    '-p', '1', '--no-grid-lines'], check=True, stdout=subprocess.DEVNULL)


def slab(c, x0, y0, x1, y1, r, top=None):
    """Flat panel from a ramp (dark..light): base r[2], light top/left r[3], dark bottom/right r[1], outline r[0]."""
    c.rect(x0, y0, x1, y1, r[2])
    c.rect(x0 + 1, y0 + 1, x1 - 1, y0 + 1, r[3] if top is None else top)
    c.rect(x0 + 1, y0 + 1, x0 + 1, y1 - 1, r[3])
    c.rect(x0 + 1, y1 - 1, x1 - 1, y1 - 1, r[1])
    c.rect(x1 - 1, y0 + 1, x1 - 1, y1 - 1, r[1])
    box(c, x0, y0, x1, y1, r[0])


def box(c, x0, y0, x1, y1, ch):
    c.rect(x0, y0, x1, y0, ch)
    c.rect(x0, y1, x1, y1, ch)
    c.rect(x0, y0, x0, y1, ch)
    c.rect(x1, y0, x1, y1, ch)


# ------------------------------------------------------------------------------------------ home: the kitchen, 1999
# Scale follows the guests: a head is ~28px, so 1px ~ 0.8cm. We see the kitchen close up, from the table:
# the bottoms of the wall cabinets at the top, 10cm tiles (12px), Mom from the chest up behind the counter.
def home():
    p = Pal()
    O = p.col('#313638')
    wall = p.ramp('#4a3a30', '#5e4a3a', '#735a44', '#86694e')
    stripe = p.col('#6a533f')
    tile = p.ramp('#3e4c4a', '#5a6c66', '#76897e', '#93a597', '#adbcac')
    wood = p.ramp('#2e2019', '#46301f', '#5c3f29', '#734f33', '#8a6040')
    frame = p.ramp('#5e5a50', '#8a8474', '#aea692', '#c8c0aa')
    sky = p.ramp('#1a1f38', '#232b4c', '#2f3a60', '#3d4a74')
    cur = p.ramp('#4a2424', '#663330', '#83443a', '#9c5a48', '#b2745c')
    ctr = p.ramp('#4a4644', '#66605c', '#837c74', '#a0988c', '#b8b0a2')
    metal = p.ramp('#3a3e44', '#5a6068', '#7e868e', '#a4acb2', '#c6ccd0')
    brass = p.ramp('#5a4628', '#8a6c38', '#b89450', '#d8b86c')
    green = p.ramp('#24341e', '#365030', '#4c6c40', '#688a52')
    terra = p.ramp('#5a2e22', '#7e4430', '#9c5a40', '#b47456')
    c = Cv(W, H, {})
    c.leg = p.leg

    # wallpaper (only under/around the window)
    for y in range(H):
        for x in range(W):
            c.put(x, y, wall[2])
    for x in range(6, 100, 16):
        for y in range(0, H):
            c.put(x, y, stripe)
            if y % 9 == 4:
                c.put(x - 4, y, stripe)
                c.put(x + 4, y, stripe)

    # tiled backsplash, 12px tiles
    TX = 96
    for y in range(30, 116):
        for x in range(TX, W):
            gx, gy = (x - TX) % 12, (y - 30) % 12
            if gx == 11 or gy == 11:
                ch = tile[1]
            elif (gx == 0 and gy < 10) or (gy == 0 and gx < 10):
                ch = tile[4]
            elif gx == 10 or gy == 10:
                ch = tile[2]
            else:
                ch = tile[3]
            c.put(x, y, ch)
    c.rect(TX - 1, 30, TX - 1, 115, O)

    # wall cabinets: we only see their bottoms
    for x0, x1 in ((TX, 160), (162, 226), (228, 292), (294, 340)):
        slab(c, x0, -4, x1, 28, wood)
        slab(c, x0 + 5, -4, x1 - 5, 23, wood[:1] + wood[1:4])
        kx = x1 - 10 if (x0 // 2) % 2 else x0 + 9
        c.rect(kx, 14, kx + 2, 19, brass[2])
        c.put(kx, 14, brass[3])
    c.rect(TX, 29, W - 1, 29, wood[0])
    for x in range(TX + 2, W, 2):                                     # under-cabinet shadow on the tiles
        c.put(x, 30, tile[1])

    # big window on the left, cut by the frame
    wx1, wy1 = 74, 88
    for y in range(0, wy1 + 1):
        for x in range(0, wx1 + 1):
            t = y / wy1
            c.put(x, y, sky[min(3, int(t * 3.4 + (0.45 if bayer(x, y, (t * 3.4) % 1) else 0)))])
    for sx, sy in ((10, 12), (30, 6), (58, 20), (18, 40), (50, 52), (64, 8), (8, 66)):
        c.put(sx, sy, frame[3])
    sphere(c, 46, 22, 9, 9, frame[1:] + frame[3])                       # moon
    sphere(c, 50, 19, 8, 8, sky[1] * 2, only=frame)                     # crescent bite
    c.rect(0, 43, wx1, 43, frame[3])
    c.rect(0, 44, wx1, 46, frame[2])
    c.rect(0, 47, wx1, 47, frame[0])
    c.rect(33, 0, 33, wy1, frame[3])
    c.rect(34, 0, 36, wy1, frame[2])
    c.rect(37, 0, 37, wy1, frame[0])
    c.rect(wx1 + 1, 0, wx1 + 5, wy1, frame[1])
    c.rect(wx1 + 1, 0, wx1 + 1, wy1, frame[3])
    c.rect(wx1 + 6, 0, wx1 + 6, wy1, O)
    slab(c, -2, wy1, wx1 + 10, wy1 + 7, frame)                          # sill
    for y in range(0, 100):                                           # curtain, gathered on the right
        w = 16 - max(0, y - 70) * 0.25
        x0 = 62
        for x in range(x0, int(x0 + w)):
            k = (x - x0) % 5
            c.put(x, y, cur[3] if k == 0 else cur[1] if k == 4 else cur[2])
        c.put(x0 - 1, y, O)
        c.put(int(x0 + w), y, O)
    c.rect(62, 99, 78, 99, O)
    slab(c, 16, 70, 38, 88, terra)                                      # geranium in a clay pot
    c.rect(14, 68, 40, 71, terra[3])
    box(c, 14, 67, 40, 71, O)
    for cx, cy, r in ((19, 60, 7), (31, 58, 7), (25, 52, 6.5), (14, 54, 5)):
        sphere(c, cx, cy, r, r * 0.85, green)
    for cx, cy in ((21, 54), (32, 52), (25, 46), (14, 49)):
        sphere(c, cx, cy, 2.6, 2.6, cur[2:])

    # shelf with jars and hanging ladles on the right
    slab(c, 244, 72, W + 2, 77, wood)
    for jx, col in ((256, cur[:4]), (276, brass), (296, green)):
        slab(c, jx - 8, 50, jx + 8, 71, col)
        slab(c, jx - 9, 46, jx + 9, 50, metal[:4])
        c.rect(jx - 5, 57, jx + 5, 63, p.col('#e2d8c2'))
        box(c, jx - 5, 57, jx + 5, 63, col[0])
    for hx, kind in ((258, 'ladle'), (278, 'spat'), (298, 'ladle')):
        c.rect(hx, 78, hx + 1, 98, metal[3])
        c.rect(hx + 1, 78, hx + 1, 98, metal[1])
        if kind == 'ladle':
            sphere(c, hx + 1, 102, 5, 4, metal)
        else:
            slab(c, hx - 3, 98, hx + 4, 108, metal[:4])
    c.cleanup(keep='.' + O)
    c.save(os.path.join(HERE, 'dream_home.px'), 'Dream: home, the kitchen from 1999 (close up)')

    # ---------------- foreground: counter top, stove, the soup pot, and the gingham table
    f = Cv(W, H, {})
    f.leg = p.leg
    slab(f, -2, 112, W + 2, 120, ctr)                                 # counter top (hides Mom below the chest)
    for x0, x1 in ((-4, 70), (72, 170), (172, 270), (272, 340)):       # cabinet doors under it
        slab(f, x0, 120, x1, 160, wood)
        slab(f, x0 + 6, 125, x1 - 6, 160, wood[:1] + wood[1:4])
    slab(f, 94, 106, 168, 114, metal)                                 # stove top
    for kx in (104, 118, 132, 146, 160):
        f.rect(kx - 1, 116, kx + 1, 118, O)                             # knobs on the counter edge
    pot = p.ramp('#2a3238', '#3e4c54', '#56707a', '#72909a', '#96b4ba')
    PX, PW = 130, 25
    for y in range(76, 108):                                          # the soup pot
        for x in range(PX - PW, PX + PW + 1):
            nx = (x + .5 - PX) / PW
            f.put(x, y, lvl(pot, 0.88 - (nx + 1) * 0.42, x, y))
    for y in range(71, 79):
        for x in range(PX - PW - 3, PX + PW + 4):
            if ((x + .5 - PX) / (PW + 3)) ** 2 + ((y + .5 - 75) / 3.6) ** 2 <= 1:
                f.put(x, y, pot[4] if y < 75 else pot[3])
    f.rect(PX - PW - 7, 82, PX - PW - 1, 85, pot[1])
    f.rect(PX + PW + 1, 82, PX + PW + 7, 85, pot[1])
    slab(f, PX - 6, 65, PX + 6, 70, pot[1:])                           # lid knob
    f.rect(PX - PW + 3, 79, PX - PW + 4, 104, pot[4])                  # highlight down the lit side
    gw, gr, gd = p.col('#cbbfa8'), p.col('#a5524a'), p.col('#7e3a36')
    for y in range(136, H):
        for x in range(W):
            a, b = (x // 7) % 2, ((y - 136) // 5) % 2
            f.put(x, y, gd if a and b else gr if a or b else gw)
    f.rect(0, 135, W - 1, 135, O)
    f.rect(0, 136, W - 1, 136, p.col('#e2d8c2'))
    bowl = p.ramp('#6a6458', '#a09888', '#c8c0ae', '#e6dfcc')
    soup = p.ramp('#8a5a2a', '#b07a3a', '#d09a50')
    BX = 236
    for y in range(126, 152):
        for x in range(BX - 30, BX + 31):
            nx, ny = (x + .5 - BX) / 29, (y + .5 - 131) / 7
            if nx * nx + ny * ny <= 1:
                f.put(x, y, soup[1] if nx * nx + (ny / .75) ** 2 < .78 else bowl[3 if nx < 0 else 2])
            elif y > 131 and abs(nx) <= .95 - (y - 131) * .025:
                f.put(x, y, lvl(bowl, 0.85 - (nx + 1) * .35, x, y))
    for x, y in ((226, 129), (240, 128), (233, 133)):
        f.rect(x, y, x + 2, y, soup[2])
    f.rect(270, 140, 294, 141, metal[3])                              # spoon
    f.rect(266, 138, 271, 143, metal[2])
    f.cleanup(keep='.' + O)
    f.outline(O)
    f.save(os.path.join(HERE, 'dream_home_fg.px'), 'Dream: home, foreground (counter, stove, pot, table)')


# ------------------------------------------------------------------------------------------ Mira from behind
def mira_back():
    """96x112: closer to the camera than the guests, so a little bigger."""
    p = gv.new()
    skin = p.ramp(*gv.SKIN)
    hair = p.ramp("#1c1720", "#2a2230", "#3a2f40", "#504253", "#6a5a6c")
    swe = p.ramp("#4a3f22", "#6a5b30", "#8b7a42", "#aa9655", "#c6b26e")
    c = Cv(96, 112, {})
    c.leg = p.leg
    sphere(c, 48, 122, 47, 52, swe)                                   # sweater: shoulders and back
    texture(c, swe, 0.05, 3)
    gv.fold(c, swe, [(16, 96), (22, 111)])
    gv.fold(c, swe, [(80, 96), (74, 111)])
    gv.fold(c, swe, [(48, 84), (47, 111)])                            # spine crease
    sphere(c, 29.5, 42, 3, 5, skin)                                   # ears peeking out
    sphere(c, 66.5, 42, 3, 5, skin)
    for y in range(42, 76):                                           # hair down to the shoulder blades
        hw = 17 + (y - 42) * 0.1 - max(0, y - 66) * 1.6
        for x in range(int(48 - hw), int(48 + hw) + 1):
            c.put(x, y, lvl(hair, 0.55 - (x - 48 + hw) / (2 * hw + 1) * 0.45 - (y - 42) / 110, x, y))
    sphere(c, 48, 38, 18, 21, hair, amb=0.14)                         # back of the head
    sphere(c, 50, 14, 11, 9, hair, amb=0.2)                           # messy bun
    strands(c, hair, step=4, slope=-1, seed=5)
    pen = p.ramp("#6a5320", "#a8853a", "#d8b45a")
    c.line(56, 11, 64, 1, pen[1])                                    # the pencil in the bun
    c.line(57, 11, 65, 1, pen[2])
    c.line(56, 12, 57, 12, pen[0])
    c.put(65, 0, p.col("#2a2430"))
    c.cleanup(keep=".")
    c.outline()
    c.save(os.path.join(HERE, "v_mira_back.px"), "Mira from behind, watching her dream")


if __name__ == '__main__':
    home()
    mira_back()
    for n in ('dream_home', 'dream_home_fg'):
        png(n)
    png('v_mira_back')
    print('done')
