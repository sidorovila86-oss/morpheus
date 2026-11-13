"""Generate Morpheus' mug at game scale (S x the approved 44x48 design) -> mug.px.
Scale rule: ID card 8.5cm = 74px; physical objects ~7px/cm. Mug body ~7cm wide -> ~51px.
The .px output is meant to be hand-touched afterwards; rerunning overwrites it.
Approved look: checker dither on band edges, textured moon print, zigzag steam."""
import math
import sys

S = 1.35
W, H = int(44 * S) + 1, int(48 * S) + 1
LEG = {
    "O": "#313638",  # outline
    "1": "#c7dcd0",  # ceramic highlight
    "2": "#b2ba90",  # ceramic light
    "3": "#92a984",  # ceramic base
    "4": "#547e64",  # ceramic shadow
    "5": "#374e4a",  # ceramic deep shadow
    "k": "#2e222f",  # coffee dark / inner wall
    "c": "#4c3e24",  # coffee
    "g": "#966c6c",  # coffee glint
    "m": "#ab947a",  # moon print
    "n": "#966c6c",  # moon print shade (faded)
    "s": "#9babb2",  # steam
    "t": "#c7dcd0",  # steam core
}
g = [["."] * W for _ in range(H)]
cx, rx = 18.0 * S, 14.5 * S         # cylinder centre x and half width
top, bot, ry = round(13 * S), round(42 * S), 4.2 * S  # rim centre y, bottom centre y, ellipse half height


def put(x, y, ch):
    x, y = int(x), int(y)
    if 0 <= x < W and 0 <= y < H:
        g[y][x] = ch


def ramp(u, x, y):
    """Cylinder shade for normalised u in [-1,1]; light from upper-left. Dither on band edges."""
    bands = [(-0.93, "2"), (-0.62, "1"), (-0.25, "2"), (0.30, "3"), (0.72, "4"), (2.0, "5")]
    for i, (edge, ch) in enumerate(bands):
        if u < edge:
            # checker dither within a thin strip just before the edge
            if 0 < i and i + 1 < len(bands) and edge - u < 0.07 and (x + y) % 2 == 0:
                return bands[i + 1][1]
            return ch
    return "5"


# body
for y in range(top, int(bot + ry) + 2):
    for x in range(W):
        u = (x + 0.5 - cx) / rx
        if abs(u) > 1:
            continue
        ybot = bot + ry * math.sqrt(max(0, 1 - u * u))
        if y > ybot:
            continue
        ch = ramp(u, x, y)
        if ybot - y < 2.2 * S:  # contact shadow near the base
            ch = {"1": "2", "2": "3", "3": "4", "4": "5"}.get(ch, ch)
        put(int(x), int(y), ch)

# handle (elliptic ring, right side)
hx, hy, hrx, hry = cx + rx - S, 27.5 * S, 9.0 * S, 9.5 * S
for y in range(H):
    for x in range(W):
        dx, dy = (x + 0.5 - hx) / hrx, (y + 0.5 - hy) / hry
        r = dx * dx + dy * dy
        ix, iy = (x + 0.5 - hx) / (hrx - 4.2 * S), (y + 0.5 - hy) / (hry - 4.5 * S)
        if x + 0.5 > cx + rx - 0.5 and r <= 1 and ix * ix + iy * iy > 1:
            ch = "3" if dy < -0.35 else ("4" if dy < 0.45 else "5")
            if dx > 0.75 and dy < 0.2:
                ch = "4"
            if dy < -0.6 and dx < 0.5:
                ch = "2"
            put(int(x), int(y), ch)

# rim: lip ring, then opening with inner wall and coffee
for y in range(int(top - ry) - 1, int(top + ry) + 2):
    for x in range(W):
        u = (x + 0.5 - cx) / rx
        v = (y + 0.5 - top) / ry
        if u * u + v * v <= 1:
            iu, iv = (x + 0.5 - cx) / (rx - 2.3 * S), (y + 0.5 - top) / (ry - 1.2 * S)
            if iu * iu + iv * iv <= 1:
                cu, cv = (x + 0.5 - cx) / (rx - 2.8 * S), (y + 0.5 - top - 1.2 * S) / (ry - 1.9 * S)
                if cu * cu + cv * cv <= 1:
                    ch = "c"
                    if cv < -0.2 and -0.75 < cu < -0.1:
                        ch = "g"
                    if cu > 0.55:
                        ch = "k"
                else:
                    ch = "k"  # back inner wall in shadow
                put(int(x), int(y), ch)
            else:
                put(int(x), int(y), "1" if (u < 0.15 and v < 0.3) else ("2" if u < 0.6 else "3"))

# moon + stars print (faded ochre), front-left
mx, my = cx - 3.5 * S, 27.0 * S
for y in range(H):
    for x in range(W):
        a = (x + 0.5 - mx) ** 2 + (y + 0.5 - my) ** 2
        b = (x + 0.5 - mx - 2.6 * S) ** 2 + (y + 0.5 - my + 1.4 * S) ** 2
        if a <= (5.6 * S) ** 2 and b > (4.9 * S) ** 2 and g[y][x] in "123":
            put(int(x), int(y), "n" if (x + 0.5 - mx) > 1.5 * S or (y + 0.5 - my) > 3.2 * S else "m")
for sx, sy in ((cx + 5 * S, 22 * S), (cx + 2 * S, 33 * S), (cx + 8 * S, 30 * S)):
    sx, sy = int(sx), int(sy)
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0), (0, 2), (0, -2)):
        put(sx + dx, sy + dy, "m")

# cleanup: recolour isolated pixels (no 4-neighbour of the same colour) to their majority neighbour
from collections import Counter
for _ in range(2):
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            ch = g[y][x]
            if ch in ".s t":
                continue
            nb = [g[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if ch not in nb and "." not in nb:
                # keep the deliberate checker dither on band edges
                if ch in "12345" and sum(n in "12345" for n in nb) == 4 and nb[0] == nb[1] and nb[0] != nb[2]:
                    continue
                g[y][x] = Counter(nb).most_common(1)[0][0]

# outline every transparent pixel touching the sprite (4-neighbour)
filled = [[g[y][x] != "." for x in range(W)] for y in range(H)]
for y in range(H):
    for x in range(W):
        if not filled[y][x] and any(
            0 <= x + dx < W and 0 <= y + dy < H and filled[y + dy][x + dx]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
        ):
            g[y][x] = "O"

# steam: two wisps above the rim (drawn after outline: no outline on steam)
for k, (x0, ph) in enumerate(((cx - 5 * S, 0.0), (cx + 3 * S, 2.1))):
    for y in range(0, int(7 * S)):
        x = int(round(x0 + 1.8 * S * math.sin(y * 0.75 / S + ph)))
        for dx in range(3):
            if g[y][x + dx] == ".":
                put(x + dx, y, "t" if (int(2 * S) <= y <= int(4 * S) and dx == 1) else "s")

out = sys.argv[1] if len(sys.argv) > 1 else "mug.px"
with open(out, "w", encoding="utf-8") as f:
    f.write("# Morpheus' mug, game scale, muted office palette. Generated by gen_mug48.py, then hand-touched.\n")
    for k, v in LEG.items():
        f.write(f"{k} {v}\n")
    f.write("---\n")
    for row in g:
        f.write("".join(row) + "\n")
