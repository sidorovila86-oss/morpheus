"""Shared helpers for the muted Papers-Please-style sprites (same look as gen_mug48.py).

Look rules: 1px dark outline, light from upper-left, hard shade bands with a 1px checker
dither strip on interior band edges, no stray single pixels.
"""
import math
import random
from collections import Counter

OUT = "#313638"


class Cv:
    def __init__(self, w, h, legend):
        self.w, self.h = w, h
        self.leg = dict(legend)
        self.leg.setdefault("O", OUT)
        self.g = [["."] * w for _ in range(h)]

    # --- basic drawing -------------------------------------------------
    def put(self, x, y, ch):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = ch

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.g[y][x]
        return "."

    def rect(self, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, ch)

    def ell(self, cx, cy, rx, ry, ch, only=None):
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                if dx * dx + dy * dy <= 1 and (only is None or self.get(x, y) in only):
                    self.put(x, y, ch)

    def line(self, x0, y0, x1, y1, ch, only=None):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            if only is None or self.get(x0, y0) in only:
                self.put(x0, y0, ch)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def cut(self, x, y):
        self.put(x, y, ".")

    # --- shading ----------------------------------------------------------
    @staticmethod
    def band(u, bands, x, y, dither=True):
        """bands: [(edge, ch), ...] ascending; checker strip before interior edges."""
        for i, (edge, ch) in enumerate(bands):
            if u < edge:
                if dither and 0 < i and i + 1 < len(bands) and edge - u < 0.07 and (x + y) % 2 == 0:
                    return bands[i + 1][1]
                return ch
        return bands[-1][1]

    def bevel(self, x0, y0, x1, y1, hi, base, sh, dither=True):
        """Flat slab: light top/left edge, shaded bottom/right edge with a checker strip."""
        self.rect(x0, y0, x1, y1, base)
        for x in range(x0, x1 + 1):
            self.put(x, y0, hi)
            self.put(x, y1, sh)
            if dither and (x + y1 - 1) % 2 == 0:
                self.put(x, y1 - 1, sh)
        for y in range(y0, y1 + 1):
            self.put(x0, y, hi)
            self.put(x1, y, sh)
            if dither and (x1 - 1 + y) % 2 == 0 and y0 < y < y1:
                self.put(x1 - 1, y, sh)

    def speckle(self, x0, y0, x1, y1, on, ch, p, seed):
        """Sparse paired-pixel texture (pairs, so cleanup keeps them)."""
        rnd = random.Random(seed)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1):
                if self.get(x, y) == on and self.get(x + 1, y) == on and rnd.random() < p:
                    self.put(x, y, ch)
                    self.put(x + 1, y, ch)

    # --- finishing --------------------------------------------------------
    def cleanup(self, keep="."):
        """Recolour isolated pixels to the majority neighbour; keeps checker dither."""
        g = self.g
        for _ in range(2):
            for y in range(1, self.h - 1):
                for x in range(1, self.w - 1):
                    ch = g[y][x]
                    if ch in keep or ch == "O":
                        continue
                    nb = [g[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                    if ch in nb or "." in nb:
                        continue
                    if nb[0] == nb[1] and nb[0] != nb[2]:   # horizontal checker
                        continue
                    if nb[2] == nb[3] and nb[2] != nb[0]:   # vertical checker
                        continue
                    g[y][x] = Counter(nb).most_common(1)[0][0]

    def outline(self, ch="O", diag=False):
        filled = [[c != "." for c in row] for row in self.g]
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if diag:
            dirs += [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for y in range(self.h):
            for x in range(self.w):
                if not filled[y][x] and any(
                    0 <= x + dx < self.w and 0 <= y + dy < self.h and filled[y + dy][x + dx] for dx, dy in dirs
                ):
                    self.g[y][x] = ch

    def save(self, path, title):
        used = {c for row in self.g for c in row} - {"."}
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {title}. Generated by gen_items.py (pxlib), then hand-touched.\n")
            for k, v in self.leg.items():
                if k in used:
                    f.write(f"{k} {v}\n")
            f.write("---\n")
            for row in self.g:
                f.write("".join(row) + "\n")


# --- volumetric helpers (portraits) ------------------------------------------------
POOL = "ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijklmnpqrstuvwxyz0123456789@$%&*+=?!<>~^;:"


class Pal:
    """Auto-assigns one grid char per colour. ramp() returns a dark->light string."""
    def __init__(self):
        self.leg, self.i = {}, 0

    def col(self, hexcol):
        for k, v in self.leg.items():
            if v == hexcol:
                return k
        ch = POOL[self.i]
        self.i += 1
        self.leg[ch] = hexcol
        return ch

    def ramp(self, *cols):
        return "".join(self.col(h) for h in cols)


LIGHT = (-0.55, -0.62, 0.56)


def lvl(ramp, v, x, y):
    """Intensity v in [0,1] -> ramp char with a 1px checker on level boundaries."""
    n = len(ramp)
    f = max(0.0, min(0.999, v)) * n
    b = int(f)
    fr = f - b
    if fr > 0.82 and b + 1 < n and (x + y) % 2 == 0:
        b += 1
    return ramp[b]


def sphere(c, cx, cy, rx, ry, ramp, only=None, clip=None, amb=0.16, lift=0.0):
    """Ellipsoid lit from upper-left (front-facing normals)."""
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            dx, dy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            r2 = dx * dx + dy * dy
            if r2 > 1:
                continue
            if only is not None and c.get(x, y) not in only:
                continue
            if clip is not None and not clip(x, y):
                continue
            nz = math.sqrt(1 - r2)
            d = LIGHT[0] * dx + LIGHT[1] * dy + LIGHT[2] * nz
            c.put(x, y, lvl(ramp, amb + (1 - amb) * max(0, d) + lift, x, y))


def strands(c, ramp, step=4, slope=1, seed=0, only_levels=None):
    """Darken one level along diagonal lines -> hair / fur texture."""
    rnd = random.Random(seed)
    for y in range(c.h):
        for x in range(c.w):
            ch = c.g[y][x]
            i = ramp.find(ch)
            if i <= 0:
                continue
            if (x * slope + y + (rnd.random() < 0.15)) % step == 0:
                c.g[y][x] = ramp[i - 1]


def texture(c, ramp, p, seed, up=False):
    """Scatter paired pixels one level darker (or lighter) -> fabric/paper grain."""
    rnd = random.Random(seed)
    for y in range(c.h):
        for x in range(c.w - 1):
            a, b = ramp.find(c.g[y][x]), ramp.find(c.g[y][x + 1])
            if a >= 1 and a == b and a < len(ramp) - 1 and rnd.random() < p:
                k = a + 1 if up else a - 1
                c.g[y][x] = c.g[y][x + 1] = ramp[k]
