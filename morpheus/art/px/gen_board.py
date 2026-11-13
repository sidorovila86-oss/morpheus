"""Storyboard sprites: film strip, place cards (memory settings), sticky pad + notes, desk bell.
Same look as gen_items.py: 1px #313638 outline, light from upper-left, hard bands + checker dither.
"""
import math
from pxlib import Cv, Pal, sphere

OUT = "#313638"


def mk(p, w, h):
    c = Cv(w, h, {})
    c.leg = p.leg
    p.leg["O"] = OUT
    return c


def dith(c, x0, y0, x1, y1, a, b, f):
    """Vertical two-colour blend: f(y) in [0,1] -> b share, ordered dither."""
    B = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c.put(x, y, b if (B[y & 3][x & 3] + .5) / 16 < f(y) else a)


# 1. film strip with three frames -----------------------------------------------------------
# frame layouts per reel length: pitch, frame width, place-card slot (x, y, w, h) relative to the frame
FILM_LAY = {3: (88, 82, (49, 14, 30, 24)), 4: (66, 60, (38, 18, 21, 17)), 5: (52, 46, (25, 33, 18, 14))}


def film(N=3):
    p = Pal()
    k0, k1, k2, k3 = p.ramp("#17131c", "#231d2a", "#2f2838", "#433a4e")
    hole = p.col("#0d0a10")
    hi = p.col("#5d536a")
    win = p.ramp("#1c1822", "#26212e")
    slot = p.col("#6d5f82")
    pip = p.col("#b9a8d6")
    star = p.col("#e8c85a")
    W, H = 266, 70
    c = mk(p, W, H)
    c.rect(0, 0, W - 1, H - 1, k1)
    c.rect(0, 0, W - 1, 0, k3)
    c.rect(0, H - 1, W - 1, H - 1, k0)
    for x in range(0, W, 2):                       # celluloid sheen line
        c.put(x, 1, k2)
    for x in range(5, W - 4, 8):                   # sprocket holes
        for y0 in (3, H - 7):
            c.rect(x, y0, x + 3, y0 + 3, hole)
            c.rect(x, y0, x + 3, y0, k0)
    pitch, fw0, (ox, oy, sw, sh) = FILM_LAY[N]
    for i in range(N):
        fx, fy, fw, fh = 4 + i * pitch, 9, fw0, 52
        c.rect(fx - 1, fy - 1, fx + fw, fy + fh, k0)       # dark rim
        c.rect(fx, fy, fx + fw - 1, fy + fh - 1, win[1])
        c.rect(fx, fy, fx + fw - 1, fy, win[0])
        c.rect(fx, fy, fx, fy + fh - 1, win[0])
        c.rect(fx - 1, fy + fh + 1, fx + fw, fy + fh + 1, hi)  # bottom lip catches the light
        # dashed slot where the place card goes
        sx, sy = fx + ox, fy + oy
        for x in range(sx, sx + sw):
            if x % 3:
                c.put(x, sy, slot)
                c.put(x, sy + sh - 1, slot)
        for y in range(sy, sy + sh):
            if y % 3:
                c.put(sx, y, slot)
                c.put(sx + sw - 1, y, slot)
        # frame number as pips in the top band, finale gets a star
        for n in range(i + 1):
            c.put(fx + 2 + n * 3, 7, pip)
            c.put(fx + 3 + n * 3, 7, pip)
        if i == N - 1:
            cx = fx + fw - 6
            for dx, dy in ((0, -2), (0, -1), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (0, 1), (-1, 2), (1, 2)):
                c.put(cx + dx, 6 + dy, star)
    c.save(f"film_{N}.px", f"Storyboard film strip, 266x70, {N} frames")


# 2. place cards: small mounted slides, 30x24 --------------------------------------------------
def card_base(p):
    m = p.ramp("#8f8672", "#bdb397", "#ddd4b6")
    c = mk(p, 30, 24)
    c.bevel(0, 0, 29, 23, m[2], m[1], m[0], dither=False)
    return c


def place_sky():
    p = Pal()
    c = card_base(p)
    s0, s1, s2 = p.ramp("#2b2f4a", "#4d65b4", "#8fa6d8")
    dith(c, 2, 2, 27, 21, s0, s1, lambda y: (y - 2) / 17)
    w = p.ramp("#9aa3c0", "#d6dcef", "#f4f6ff")
    for cx, cy, r in ((9, 16, 4), (14, 15, 5), (19, 17, 3.5), (21, 8, 2.5), (24, 8, 3)):
        sphere(c, cx, cy, r, r * .8, w, only=(s0, s1))
    moon = p.ramp("#c9b46a", "#f0e2a0")
    c.ell(7, 6, 3, 3, moon[1])
    c.ell(8, 5, 2.4, 2.4, s0, only=(moon[1],))
    for x, y in ((14, 4), (17, 7), (25, 3)):
        c.put(x, y, w[2])
    c.save("place_sky.px", "Place card: the sky, 30x24")


def place_school():
    p = Pal()
    c = card_base(p)
    b0, b1, b2 = p.ramp("#1f3a2c", "#2f5a44", "#3f6e54")
    c.rect(2, 2, 27, 21, b1)
    c.rect(2, 2, 27, 3, p.col("#5a4636"))           # wooden frame
    c.rect(2, 18, 27, 21, p.col("#7a5e46"))
    c.rect(2, 18, 27, 18, p.col("#9a7a5a"))
    ch = p.col("#c8d6cc")
    c.line(5, 7, 12, 7, ch)                          # chalk scribbles (not letters)
    c.line(5, 10, 9, 10, ch)
    c.line(14, 11, 22, 6, ch)
    c.line(14, 11, 22, 11, ch)
    c.ell(20, 14, 2.2, 2, ch)
    c.ell(20, 14, 1.2, 1, b1)
    c.rect(22, 16, 25, 17, p.col("#e8e4d4"))         # chalk stick on the ledge
    c.save("place_school.px", "Place card: the school, 30x24")


def place_home():
    p = Pal()
    c = card_base(p)
    n0, n1 = p.ramp("#1b1828", "#2b2f4a")
    dith(c, 2, 2, 27, 21, n0, n1, lambda y: (y - 2) / 19)
    wall = p.ramp("#3a2e2a", "#5a4636", "#7a5e46")
    roof = p.ramp("#4a2a2a", "#6e3a34")
    for y in range(5, 12):                           # roof
        hw = (y - 5) * 1.6 + 1
        for x in range(int(15 - hw), int(15 + hw) + 1):
            c.put(x, y, roof[1] if x < 15 else roof[0])
    c.rect(6, 12, 24, 21, wall[1])
    c.rect(6, 12, 6, 21, wall[2])
    lit = p.ramp("#c98a3a", "#f0c870")
    c.rect(9, 14, 13, 18, lit[1])
    c.rect(11, 14, 11, 18, lit[0])
    c.rect(9, 16, 13, 16, lit[0])
    c.rect(17, 15, 21, 21, p.col("#2a2020"))          # door
    c.put(20, 18, lit[1])
    c.rect(20, 4, 21, 7, wall[0])                     # chimney
    c.save("place_home.px", "Place card: home, 30x24")


def place_studio():
    p = Pal()
    c = card_base(p)
    w0, w1 = p.ramp("#5a5068", "#6e6280")
    dith(c, 2, 2, 27, 21, w1, w0, lambda y: (y - 2) / 19)
    wood = p.ramp("#5a3e26", "#8a6a45")
    c.line(9, 20, 15, 4, wood[0])                     # easel legs
    c.line(21, 20, 15, 4, wood[0])
    c.line(15, 6, 15, 21, wood[1])
    cv = p.ramp("#c9c0a8", "#efe8d2")
    c.rect(8, 6, 22, 15, cv[1])
    c.rect(8, 15, 22, 15, cv[0])
    c.rect(7, 16, 23, 16, wood[1])
    for (x, y, col) in ((10, 8, "#d0705a"), (11, 8, "#d0705a"), (10, 9, "#d0705a"), (14, 10, "#6fa0c8"), (15, 10, "#6fa0c8"),
                        (15, 11, "#6fa0c8"), (18, 8, "#e8c85a"), (19, 8, "#e8c85a"), (19, 9, "#e8c85a"), (12, 12, "#4f8a5e"), (13, 12, "#4f8a5e")):
        c.put(x, y, p.col(col))
    c.save("place_studio.px", "Place card: the art studio, 30x24")


def place_sea():
    p = Pal()
    c = card_base(p)
    s0, s1 = p.ramp("#3a4a78", "#7a90c8")
    dith(c, 2, 2, 27, 12, s1, s0, lambda y: (y - 2) / 12)
    w0, w1, w2 = p.ramp("#1e3a58", "#2f5f86", "#5c8fb4")
    dith(c, 2, 13, 27, 21, w1, w0, lambda y: (y - 13) / 8)
    sun = p.ramp("#d08a4a", "#f0c070")
    c.ell(20, 12, 4, 3, sun[1], only=(s0, s1))
    c.rect(16, 13, 24, 13, sun[0])
    for x in range(4, 27, 4):                       # wave crests
        c.put(x, 15, w2)
        c.put(x + 1, 15, w2)
        c.put(x + 2, 18, w2)
    sand = p.ramp("#b89a62", "#d8c08a")
    c.rect(2, 20, 27, 21, sand[1])
    c.rect(2, 19, 9, 19, sand[0])
    c.save("place_sea.px", "Place card: the sea, 30x24")


def place_attic():
    p = Pal()
    c = card_base(p)
    d0, d1 = p.ramp("#241c1a", "#3e302a")
    c.rect(2, 2, 27, 21, d0)
    beam = p.ramp("#4a3628", "#6a4e38")
    for y in range(2, 12):                          # sloped roof beams
        c.put(2 + (y - 2), y, beam[1])
        c.put(27 - (y - 2), y, beam[1])
    c.rect(2, 19, 27, 21, beam[0])
    lw = p.ramp("#8aa0c8", "#c8d6ef")
    c.rect(13, 5, 16, 8, lw[0])                     # round little window
    c.put(14, 5, lw[1]); c.put(13, 6, lw[1])
    box = p.ramp("#6a5236", "#8e7048", "#b08e5e")
    c.bevel(5, 13, 12, 18, box[2], box[1], box[0], dither=False)
    c.bevel(16, 11, 25, 18, box[2], box[1], box[0], dither=False)
    c.rect(16, 14, 25, 14, box[0])
    dust = p.col("#c9b48a")
    for x, y in ((9, 6), (19, 4), (22, 9), (7, 10)):
        c.put(x, y, dust)
    c.save("place_attic.px", "Place card: the attic, 30x24")


def place_fair():
    p = Pal()
    c = card_base(p)
    n0, n1 = p.ramp("#1c1630", "#33285a")
    dith(c, 2, 2, 27, 21, n0, n1, lambda y: (y - 2) / 19)
    rim = p.col("#c9a8e6")
    c.ell(15, 11, 7, 7, rim)
    c.ell(15, 11, 6, 6, n1, only=(rim,))
    spoke = p.col("#8a72b0")
    for dx, dy in ((0, -6), (0, 6), (-6, 0), (6, 0), (-4, -4), (4, 4), (-4, 4), (4, -4)):
        c.line(15, 11, 15 + dx, 11 + dy, spoke)
    bulbs = ("#e8c85a", "#e0708a", "#6fa0c8", "#9ad08a")
    for k, (dx, dy) in enumerate(((0, -7), (5, -5), (7, 0), (5, 5), (0, 7), (-5, 5), (-7, 0), (-5, -5))):
        c.put(15 + dx, 11 + dy, p.col(bulbs[k % 4]))
    leg = p.col("#5a4a78")
    c.line(15, 11, 10, 21, leg)
    c.line(15, 11, 20, 21, leg)
    c.put(15, 11, p.col("#f0e2a0"))
    c.save("place_fair.px", "Place card: the night fair, 30x24")


def place_train():
    p = Pal()
    c = card_base(p)
    n0, n1 = p.ramp("#161a28", "#28304a")
    dith(c, 2, 2, 27, 21, n0, n1, lambda y: (y - 2) / 19)
    st = p.col("#d6dcef")
    for x, y in ((5, 4), (12, 3), (20, 5), (25, 3), (9, 7)):
        c.put(x, y, st)
    car = p.ramp("#3a2a3a", "#5e4256", "#7e5a72")
    c.rect(3, 10, 26, 17, car[1])
    c.rect(3, 10, 26, 10, car[2])
    c.rect(3, 17, 26, 17, car[0])
    lit = p.ramp("#c98a3a", "#f0c870")
    for x in (5, 11, 17, 22):                       # lit windows
        c.rect(x, 12, x + 3, 14, lit[1])
        c.put(x, 14, lit[0])
    rail = p.col("#5a5262")
    c.rect(2, 20, 27, 20, rail)
    wh = p.col("#1a1620")
    for x in (6, 12, 18, 23):
        c.rect(x, 18, x + 1, 19, wh)
    c.save("place_train.px", "Place card: the night train, 30x24")


# 3. sticky pad and loose notes ------------------------------------------------------------------
NOTE_COLS = {"y": ("#efe1a0", "#e3d58a", "#cdbb6a", "#a8954f"),
             "p": ("#efc6c6", "#e3aeb0", "#c98c92", "#9e6670"),
             "g": ("#cfe6c4", "#b6d6aa", "#93b886", "#6e9264")}


def note(key):
    a, b, cc, d = NOTE_COLS[key]
    p = Pal()
    hi, base, sh, dk = p.ramp(a, b, cc, d)
    N = 36
    c = mk(p, N, N)
    c.bevel(1, 1, N - 2, N - 2, hi, base, sh)
    c.rect(2, 2, N - 3, 6, hi)                       # adhesive strip is a touch lighter
    for x in range(2, N - 2, 2):
        c.put(x, 7, base)
    c.put(N - 3, N - 3, dk)                          # tiny curl
    c.put(N - 4, N - 3, sh)
    c.put(N - 3, N - 4, sh)
    c.outline()
    c.save(f"note_{key}.px", f"Loose sticky note {key}, {N}x{N}")


def pad():
    p = Pal()
    a, b, cc, d = NOTE_COLS["y"]
    hi, base, sh, dk = p.ramp(a, b, cc, d)
    edge = p.ramp("#8a7a40", "#b8a65e")
    W, H = 42, 44
    c = mk(p, W, H)
    for k in range(5, 0, -1):                       # stacked sheets, offset down-right
        c.rect(1 + k, 1 + int(k * 1.2), W - 7 + k, H - 9 + int(k * 1.2), edge[k % 2])
    c.bevel(1, 1, W - 7, H - 9, hi, base, sh)
    c.rect(2, 2, W - 8, 6, hi)
    for x in range(2, W - 7, 2):
        c.put(x, 7, base)
    c.outline()
    c.save("pad.px", f"Sticky note pad, {W}x{H}")


# 4. desk bell (dismiss the visitor) ----------------------------------------------------------
def bell():
    p = Pal()
    brass = p.ramp("#4a3416", "#7a5a26", "#a8823a", "#d0aa58", "#ecd28a")
    base = p.ramp("#1e1a22", "#3a3440", "#5a5262")
    W, H = 26, 20
    c = mk(p, W, H)
    sphere(c, 13, 17, 12, 2.6, base)
    sphere(c, 13, 14, 9, 9, brass, clip=lambda x, y: y <= 14)
    c.rect(4, 15, 22, 15, brass[1])
    c.rect(12, 3, 14, 5, brass[2])
    c.rect(11, 2, 15, 2, brass[3])
    c.cleanup(keep=".")
    c.outline()
    c.save("bell.px", f"Desk bell, {W}x{H}")


if __name__ == "__main__":
    for n in (3, 4, 5):
        film(n)
    place_sky()
    place_school()
    place_home()
    place_studio()
    place_sea()
    place_attic()
    place_fair()
    place_train()
    for k in NOTE_COLS:
        note(k)
    pad()
    bell()
