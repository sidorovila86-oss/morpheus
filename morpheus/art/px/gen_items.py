"""Desk items in the approved muted style, at one consistent game scale (screen 480x270).
Scale rule: ID card 8.5cm = 74px is the reference; physical objects ~7px/cm
(mug ~7cm wide, stamp 9cm tall, lens 7cm glass, notebook A6, sticky 7.6cm, sheet A5).
No text baked in: labels, names and stamp words are drawn by the game (EN/JA/RU).
Writes <name>.px next to this file."""
import math
import random
from pxlib import Cv

PAPER = {"p": "#d8e2d6", "q": "#c7dcd0", "r": "#9babb2", "l": "#b2ba90"}   # hi, base, shade, ruled line
MANILA = {"a": "#cbb894", "b": "#ab947a", "d": "#8a7560", "e": "#694f62"}
CARD = {"1": "#b2ba90", "2": "#92a984", "3": "#547e64", "4": "#374e4a"}
METAL = {"w": "#d8e2d6", "m": "#9babb2", "n": "#7f708a", "N": "#625565"}
WOOD = {"h": "#ab947a", "i": "#8a6a55", "j": "#694f62", "J": "#4c3e24"}
INK = {"k": "#2e222f"}
GREEN = {"G": "#8fb58c", "H": "#4f8a5e", "I": "#2f5a44"}
RED = {"R": "#c96a5a", "S": "#9e4539", "T": "#6e2727"}
BLUE = {"x": "#4d65b4", "y": "#484a77", "z": "#323353"}
MOON = {"Y": "#ab947a", "Z": "#966c6c"}


def L(*ds):
    out = {}
    for d in ds:
        out.update(d)
    return out


def crescent(c, cx, cy, r, ch, only):
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            a = (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2
            b = (x + 0.5 - cx - r * 0.45) ** 2 + (y + 0.5 - cy + r * 0.25) ** 2
            if a <= r * r and b > (r * 0.85) ** 2 and c.get(x, y) in only:
                c.put(x, y, ch)


def dog_ear(c, x1, y1, size, flap, edge):
    """Fold the bottom-right corner: cut the corner, show the flap triangle."""
    d = x1 + y1 - size
    for y in range(y1 - size, y1 + 1):
        for x in range(x1 - size, x1 + 1):
            s = x + y
            if s > d:
                c.cut(x, y)
            elif s == d:
                c.put(x, y, edge)
            elif s > d - size and x >= x1 - size and y >= y1 - size:
                c.put(x, y, flap)


# 1. dossier folder (holds A5 sheets), portrait ------------------------------------
def folder():
    c = Cv(120, 156, L(PAPER, MANILA, INK, MOON))
    c.bevel(14, 2, 106, 26, "p", "q", "r")                 # sheets peeking out
    c.bevel(18, 0, 100, 8, "p", "q", "r")
    c.bevel(4, 9, 42, 20, "a", "b", "d")                   # tab
    c.bevel(2, 16, 117, 153, "a", "b", "d")                # front cover
    for x in range(3, 117):                                 # flap crease
        c.put(x, 23, "d")
        if x % 2 == 0:
            c.put(x, 24, "a")
    c.bevel(30, 42, 90, 62, "p", "q", "r")                 # label (text in game)
    for x in range(34, 87):
        c.put(x, 57, "l")
    c.ell(106, 80, 4, 4, "d")                              # string-tie button
    c.ell(105.5, 79.5, 2, 2, "a")
    for k in range(0, 360, 3):                             # coffee ring stain
        if 200 < k < 250:
            continue
        a = math.radians(k)
        x, y = 34 + 11 * math.cos(a), 118 + 8 * math.sin(a)
        if (int(x) + int(y)) % 2 == 0 or k % 9 == 0:
            c.put(x, y, "d")
    crescent(c, 20, 44, 7, "d", "b")                       # faded department moon
    c.speckle(4, 26, 114, 150, "b", "d", 0.012, 7)
    c.cleanup()
    c.outline()
    c.save("folder.px", "Dossier folder, closed, 120x156 (A5 sheets inside)")


# 2. dossier sheet, A5 ------------------------------------------------------------------
def sheet():
    W, H = 104, 146
    c = Cv(W, H, L(PAPER, METAL, INK))
    c.bevel(0, 0, W - 1, H - 1, "p", "q", "r")
    c.rect(6, 8, 36, 46, "r")                              # photo box
    c.rect(7, 9, 35, 45, "l")
    c.rect(8, 10, 34, 44, "q")
    for y in (14, 22, 30, 38, 46):                         # field lines beside photo
        c.rect(42, y, W - 8, y, "l")
    for y in range(60, H - 8, 8):                          # ruled lines for text
        c.rect(6, y, W - 8, y, "l")
    dog_ear(c, W - 1, H - 1, 12, "r", "N")
    pts = [(84, -1), (84, 18), (88, 22), (92, 18), (92, 2), (89, 0), (87, 2), (87, 15)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):            # paperclip
        c.line(x0, max(y0, 0), x1, max(y1, 0), "N")
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        c.line(x0 + 1, max(y0, 0), x1 + 1, max(y1, 0), "m", only="pqrl")
    c.speckle(2, 2, W - 4, H - 14, "q", "p", 0.01, 3)
    c.cleanup()
    c.outline()
    c.save("sheet.px", f"Dossier page, A5, {W}x{H} (text and photo drawn in game)")


# 3. ID card (scale reference: 8.5cm = 74px) ---------------------------------------------
def idcard():
    c = Cv(74, 48, L(CARD, PAPER, MOON, INK))
    c.bevel(1, 1, 72, 46, "1", "2", "3")
    c.rect(2, 2, 71, 9, "4")                               # header band (title in game)
    for x in range(2, 72, 2):
        c.put(x, 9, "3")
    c.rect(5, 13, 25, 40, "4")                             # photo slot
    c.rect(6, 14, 24, 39, "q")
    for y, ln in ((15, 34), (22, 30), (29, 36)):           # data lines (text in game)
        c.rect(30, y, 30 + ln, y + 1, "3")
    c.ell(63, 38, 6.5, 6.5, "Y", only="23")                # dream seal
    c.ell(63, 38, 4.5, 4.5, "2", only="Y")
    crescent(c, 63, 38, 3.6, "Z", "2")
    for x, y in ((1, 1), (72, 1), (1, 46), (72, 46)):      # rounded corners
        c.cut(x, y)
    c.cleanup()
    c.outline()
    c.save("idcard.px", "Dreamer ID card, 74x48 = 8.5cm, scale reference")


# 4. rubber stamps, 9cm tall --------------------------------------------------------------
def stamp(name, col, hi, base, sh):
    W, H = 50, 68
    c = Cv(W, H, L(WOOD, INK, METAL, col))
    cx = W / 2
    for y in range(1, 22):                                 # knob
        for x in range(W):
            dx, dy = (x + 0.5 - cx) / 12, (y + 0.5 - 11) / 10
            if dx * dx + dy * dy <= 1:
                ch = Cv.band(dx, [(-0.55, "h"), (0.1, "i"), (0.6, "j"), (2, "J")], x, y)
                if dy < -0.55 and dx < 0.2:
                    ch = "h"
                c.put(x, y, ch)
    for y in range(18, 37):                                # neck
        for x in range(W):
            u = (x + 0.5 - cx) / 7.5
            if abs(u) <= 1:
                c.put(x, y, Cv.band(u, [(-0.5, "h"), (0.15, "i"), (0.6, "j"), (2, "J")], x, y))
    for x in range(W):                                     # knob/neck seam
        u = (x + 0.5 - cx) / 7.5
        if abs(u) <= 1:
            c.put(x, 20, "J" if x % 2 else "j")
    c.bevel(2, 36, W - 3, 55, hi, base, sh)                # coloured block
    for x in range(3, W - 3):
        c.put(x, 40, sh if x % 2 else base)
    c.bevel(3, 56, W - 4, 60, "w", "m", "n")               # metal ferrule
    c.rect(4, 61, W - 5, 65, "k")                          # rubber pad
    for x in range(4, W - 4, 2):
        c.put(x, 65, sh)
    c.cleanup()
    c.outline()
    c.save(f"{name}.px", f"Rubber stamp {name}, {W}x{H}")


# 5. stamp imprints = pad size (word drawn in game) ------------------------------------------
def imprint(name, col, base):
    W, H = 46, 24
    c = Cv(W, H, col)
    rnd = random.Random(name)
    for y in range(H):
        for x in range(W):
            outer = x in (1, 2, W - 3, W - 2) or y in (1, 2, H - 3, H - 2)
            inner = (x in (5, W - 6) and 5 <= y <= H - 6) or (y in (5, H - 6) and 5 <= x <= W - 6)
            inside = 1 <= x <= W - 2 and 1 <= y <= H - 2
            if inside and (outer or inner) and rnd.random() > 0.13:
                c.put(x, y, base)
    c.cleanup()
    c.save(f"{name}.px", f"Stamp imprint {name}, {W}x{H}, transparent inside")


# 6. notebook, A6 ------------------------------------------------------------------------
def notebook():
    W, H = 76, 106
    c = Cv(W, H, L(BLUE, PAPER, METAL, INK, {"u": "#45293f"}))
    c.bevel(5, 9, W - 2, H - 2, "p", "q", "r")             # page block, offset
    c.bevel(2, 5, W - 6, H - 5, "x", "y", "z")             # cover
    c.speckle(3, 7, W - 8, H - 7, "y", "z", 0.015, 5)
    c.bevel(12, 30, 50, 46, "p", "q", "r")                 # label (text in game)
    for x in range(16, 47):
        c.put(x, 42, "l")
    c.rect(58, 5, 62, H - 5, "u")                          # elastic band
    for y in range(5, H - 4, 2):
        c.put(62, y, "k")
    for x in range(6, W - 10, 7):                          # spiral rings on top
        c.rect(x, 0, x + 2, 8, "m")
        c.put(x, 0, "w")
        c.put(x, 1, "w")
        c.put(x + 2, 7, "n")
        c.put(x + 2, 8, "n")
        c.put(x + 1, 9, "k")
    c.cleanup()
    c.outline()
    c.save("notebook.px", f"Morpheus' notebook, A6, {W}x{H}")


# 7. magnifying lens, 7cm glass -------------------------------------------------------------
def lens():
    W, H = 68, 98
    c = Cv(W, H, L(METAL, WOOD, INK, {"g": "#b6c8c4", "f": "#e8f0ea"}))
    cx, cy, RO, RI = 28.0, 28.0, 25.0, 20.0
    x0, y0, x1, y1 = 44.0, 44.0, 61.0, 94.0                # handle (under the ring)
    L_ = math.hypot(x1 - x0, y1 - y0)
    nx, ny = (y1 - y0) / L_, -(x1 - x0) / L_
    for y in range(H):
        for x in range(W):
            px, py = x + 0.5 - x0, y + 0.5 - y0
            t = (px * (x1 - x0) + py * (y1 - y0)) / (L_ * L_)
            d = px * nx + py * ny
            if 0 <= t <= 1 and abs(d) <= 4.6:
                ch = Cv.band(-d / 4.6, [(-0.4, "h"), (0.2, "i"), (0.65, "j"), (2, "J")], x, y)
                if t < 0.18:
                    ch = Cv.band(-d / 4.6, [(-0.3, "w"), (0.3, "m"), (2, "n")], x, y)
                c.put(x, y, ch)
    for y in range(H):                                     # metal ring + glass
        for x in range(W):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            r = math.hypot(dx, dy)
            if r <= RO:
                if r > RI:
                    lit = -math.cos(math.atan2(dy, dx) + math.pi * 0.75)
                    c.put(x, y, Cv.band(-lit, [(-0.5, "w"), (0.0, "m"), (0.55, "n"), (2, "N")], x, y))
                else:
                    c.put(x, y, "g")
    for y in range(H):                                     # glass highlights
        for x in range(W):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            r = math.hypot(dx, dy)
            if r <= RI:
                if 14.5 < r < 17.5 and dx < -2.5 and dy < -2.5:
                    c.put(x, y, "f")
                if abs((dx + dy) - 8) < 2 and dx > 0 and r < 17:
                    c.put(x, y, "f")
    c.cleanup()
    c.outline()
    c.save("lens.px", f"Magnifying lens, {W}x{H}")


# 8. sticky note, 7.6cm ------------------------------------------------------------------------
def sticky():
    N = 54
    c = Cv(N, N, {"s": "#e3d58a", "t": "#cdbb6a", "v": "#a8954f", "V": "#7d6c3c"})
    c.bevel(1, 1, N - 2, N - 2, "s", "t", "v")
    for x in range(2, N - 2, 2):                           # adhesive strip edge
        c.put(x, 9, "t")
    dog_ear(c, N - 2, N - 2, 10, "v", "V")
    c.cleanup()
    c.outline()
    c.save("sticky.px", f"Sticky note, {N}x{N} (handwriting drawn in game)")


# 9. banker's desk lamp (green glass shade) ---------------------------------------------
def lamp():
    """Banker's desk lamp, 104x78."""
    from pxlib import Pal, sphere
    p = Pal()
    p.leg["O"] = "#313638"
    green = p.ramp("#16301f", "#244a32", "#346846", "#4c8a5e", "#7ab48a")
    brass = p.ramp("#4a3416", "#7a5a26", "#a8823a", "#d0aa58", "#ecd28a")
    glow = p.ramp("#e8c870", "#fff2c0")
    W, H = 104, 78
    cx = 52
    c = Cv(W, H, {})
    c.leg = p.leg
    sphere(c, cx, 71, 25, 6, brass)                          # base
    for y in range(31, 67):                                  # stem
        for x in range(cx - 4, cx + 4):
            u = (x + 0.5 - cx) / 4
            c.put(x, y, brass[4] if u < -0.4 else (brass[2] if u < 0.5 else brass[1]))
    c.rect(cx - 6, 61, cx + 5, 62, brass[2])                 # collar on the stem
    c.rect(cx - 6, 61, cx + 5, 61, brass[3])
    sphere(c, cx, 34, 43, 22, green, clip=lambda x, y: y <= 33)   # half-cylinder glass shade
    for x in range(13, 92, 9):                               # glass ribs
        for y in range(14, 33):
            if c.get(x, y) in green and c.get(x, y) != green[0]:
                c.put(x, y, green[max(0, green.find(c.get(x, y)) - 1)])
    for x in range(18, 40):                                  # glass highlight streak
        y = 17 + (x - 18) // 5
        if c.get(x, y) in green:
            c.put(x, y, green[4])
    c.rect(9, 33, 94, 33, brass[3])                          # brass rim
    c.rect(9, 34, 94, 34, brass[1])
    c.rect(16, 35, 87, 35, glow[1])                          # bulb glow under the shade
    c.rect(22, 36, 81, 36, glow[0])
    c.rect(75, 35, 75, 48, brass[2])                         # pull chain
    sphere(c, 75.5, 51, 2.5, 2.5, brass)
    c.cleanup(keep=".")
    c.outline()
    c.save("lamp.px", "Banker's desk lamp, 104x78")


if __name__ == "__main__":
    lamp()
    folder()
    sheet()
    idcard()
    stamp("stamp_admit", GREEN, "G", "H", "I")
    stamp("stamp_deny", RED, "R", "S", "T")
    imprint("imprint_admit", GREEN, "H")
    imprint("imprint_deny", RED, "S")
    notebook()
    lens()
    sticky()
