"""Visitor portraits, 64x76 busts, volumetric style matching the room and the desk items:
5-tone ramps lit from the upper-left, 1px checker on tone boundaries, textures
(hair strands, wool curls, fabric grain, fold lines), detailed faces, dark outline."""
import math
import random
from pxlib import Cv, Pal, sphere, strands, texture, lvl

W, H = 64, 76

SKIN = ("#5e3a30", "#8a5a4a", "#b27860", "#d29a7c", "#ebbfa2")
EYE_W, PUPIL, LID = "#e8e4dc", "#1a1620", "#2a1e22"
LIP_D, LIP = "#6e2e36", "#a4545a"
BLUSH = "#c9786c"


def new(*_):
    p = Pal()
    p.leg["O"] = "#313638"   # outline colour shared with the desk items
    return p


def mk(p):
    c = Cv(W, H, {})
    c.leg = p.leg            # share: colours added later still reach the saved legend
    return c


def eye(c, p, x, y, iris, mood="open"):
    """4x3 eye at (x,y) top-left. moods: open, tired, wide, angry."""
    lid, wht, pup, irs = p.col(LID), p.col(EYE_W), p.col(PUPIL), p.col(iris)
    if mood == "tired":
        c.rect(x - 1, y, x + 4, y, lid)                 # heavy lid
        c.rect(x, y + 1, x + 3, y + 1, wht)
        c.rect(x + 1, y + 1, x + 2, y + 1, irs)
        c.put(x + 2, y + 1, pup)
        return
    c.rect(x, y, x + 3, y, lid)
    c.rect(x, y + 1, x + 3, y + 2, wht)
    c.rect(x + 1, y + 1, x + 2, y + 2, irs)
    c.put(x + 2, y + 2, pup)
    c.put(x + 1, y + 1, wht)                            # glint
    if mood == "wide":
        c.rect(x, y - 1, x + 3, y - 1, lid)
    if mood == "angry":
        c.put(x if x < 32 else x + 3, y, wht)


def person(p, c, skin, cx=32, cy=37, rx=11, ry=13, ears=True):
    sphere(c, cx, cy + 15, 5.5, 9, skin, amb=0.05)     # neck (darker, under chin)
    if ears:
        sphere(c, cx - rx - 0.5, cy + 1, 2.2, 3.6, skin)
        sphere(c, cx + rx + 0.5, cy + 1, 2.2, 3.6, skin)
    sphere(c, cx, cy, rx, ry, skin, amb=0.3, lift=0.1)


def features(c, p, skin, cx=32, ey=35, iris="#4a6a78", brow="#2e2532", mood="open",
             mouth="flat", blush=True, gap=10):
    lx, rxx = cx - gap // 2 - 3, cx + gap // 2
    eye(c, p, lx, ey, iris, "tired" if mood == "tired" else ("angry" if mood == "angry" else mood))
    eye(c, p, rxx, ey, iris, "tired" if mood == "tired" else ("angry" if mood == "angry" else mood))
    b = p.col(brow)
    if mood == "angry":
        c.line(lx - 1, ey - 4, lx + 3, ey - 2, b)
        c.line(rxx + 4, ey - 4, rxx, ey - 2, b)
    elif mood == "raised":
        c.rect(lx - 1, ey - 4, lx + 3, ey - 4, b)
        c.rect(rxx, ey - 5, rxx + 4, ey - 5, b)
    else:
        c.rect(lx - 1, ey - 3, lx + 3, ey - 3, b)
        c.rect(rxx, ey - 3, rxx + 4, ey - 3, b)
    if mood == "tired":                                  # bags under the eyes
        for x in range(lx, lx + 4):
            c.put(x, ey + 3, skin[2])
        for x in range(rxx, rxx + 4):
            c.put(x, ey + 3, skin[2])
    c.rect(cx + 1, ey + 3, cx + 1, ey + 6, skin[1])       # nose shadow side
    c.put(cx, ey + 4, skin[4])                           # nose highlight
    c.put(cx - 1, ey + 7, skin[1])
    c.put(cx + 1, ey + 7, skin[0])
    my = ey + 10
    ld, li = p.col(LIP_D), p.col(LIP)
    if mouth == "grin":
        c.rect(cx - 4, my, cx + 4, my, ld)
        c.rect(cx - 3, my + 1, cx + 3, my + 1, p.col("#e8e4dc"))
        c.rect(cx - 2, my + 2, cx + 2, my + 2, ld)
        c.put(cx - 5, my - 1, ld)
        c.put(cx + 5, my - 1, ld)
    elif mouth == "smile":
        c.rect(cx - 3, my, cx + 3, my, ld)
        c.put(cx - 4, my - 1, ld)
        c.put(cx + 4, my - 1, ld)
        c.rect(cx - 2, my + 1, cx + 2, my + 1, li)
    elif mouth == "pursed":
        c.rect(cx - 2, my, cx + 2, my, ld)
        c.rect(cx - 1, my + 1, cx + 1, my + 1, li)
    else:
        c.rect(cx - 3, my, cx + 2, my, ld)
        c.rect(cx - 2, my + 1, cx + 1, my + 1, li)
    if blush:
        bl = p.col(BLUSH)
        for x0 in (lx - 1, rxx + 1):
            for x in range(x0, x0 + 4):
                if (x + my - 3) % 2 == 0:
                    c.put(x, my - 3, bl)


def fold(c, ramp, pts):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        c.line(x0, y0, x1, y1, ramp[1], only=ramp)


def finish(c, name, title, keep=""):
    c.cleanup(keep="." + keep)
    c.outline()
    c.save(f"v_{name}.px", title)


# --- Mira, the client -------------------------------------------------------------------
def mira():
    p = new()
    skin = p.ramp(*SKIN)
    hair = p.ramp("#1c1720", "#2a2230", "#3a2f40", "#504253", "#6a5a6c")
    swe = p.ramp("#4a3f22", "#6a5b30", "#8b7a42", "#aa9655", "#c6b26e")
    c = mk(p)
    sphere(c, 32, 50, 15, 22, hair)                       # hair falling behind shoulders
    sphere(c, 32, 84, 31, 24, swe)                        # sweater
    texture(c, swe, 0.05, 1)
    for x in range(20, 45, 2):                            # ribbed collar
        for y in range(58, 62):
            if c.get(x, y) in swe:
                c.put(x, y, swe[1])
    sphere(c, 32, 59, 9, 3.2, swe, lift=0.1, clip=lambda x, y: x % 2 == 1)
    fold(c, swe, [(12, 70), (17, 75)])
    fold(c, swe, [(52, 68), (48, 75)])
    person(p, c, skin)
    sphere(c, 33, 16, 7.5, 6.5, hair)                     # messy bun
    pen = p.ramp("#6a5320", "#a8853a", "#d8b45a")
    c.line(37, 11, 42, 5, pen[1])                         # pencil stuck in the bun
    c.line(38, 11, 43, 5, pen[2])
    c.put(43, 4, p.col("#2a2430"))
    sphere(c, 29, 27, 12, 6.5, hair, only=skin + ".")     # fringe
    sphere(c, 21.5, 36, 3, 10, hair)                      # side locks
    sphere(c, 42.5, 36, 3, 10, hair)
    strands(c, hair, step=4, slope=1, seed=2)
    features(c, p, skin, iris="#5a6e4a", brow="#2a2230", mood="tired", mouth="flat")
    fr = p.col("#94584a")
    for x, y in ((24, 42), (26, 43), (38, 43), (40, 42), (25, 41)):
        c.put(x, y, fr)
    finish(c, "mira", "Mira Holt, the client")


# --- Kevin ---------------------------------------------------------------------------------
def kevin():
    p = new()
    skin = p.ramp(*SKIN)
    hair = p.ramp("#2a1c12", "#43301f", "#5f452c", "#7e603c", "#9c7c52")
    hood = p.ramp("#232c1d", "#34422a", "#485c3b", "#61784e", "#7e9668")
    bag = p.ramp("#6a4e1c", "#9a7a2c", "#c8a240", "#e3c25a", "#f4dc88")
    red = p.ramp("#4a1a16", "#7a2a22", "#a04a3e", "#c26a52")
    c = mk(p)
    sphere(c, 32, 84, 31, 25, hood)
    texture(c, hood, 0.05, 3)
    sphere(c, 32, 60, 15, 5.5, hood, lift=0.08)          # hood bunched round the neck
    fold(c, hood, [(18, 66), (22, 75)])
    fold(c, hood, [(46, 66), (42, 75)])
    dr = p.ramp("#a8aca0", "#d8dcd0")
    c.rect(28, 60, 28, 70, dr[1])                          # drawstrings
    c.rect(36, 60, 36, 68, dr[1])
    c.put(28, 71, dr[0])
    c.put(36, 69, dr[0])
    person(p, c, skin)
    for i in range(9):                                     # messy spikes
        x = 21 + i * 2.7
        sphere(c, x, 24 - (i % 3) * 1.5, 3.2, 4.5, hair)
    sphere(c, 32, 27, 12.5, 6, hair)
    sphere(c, 21, 31, 2.5, 4, hair)
    sphere(c, 43, 31, 2.5, 4, hair)
    strands(c, hair, step=3, slope=2, seed=4)
    features(c, p, skin, iris="#6a4a2a", brow="#43301f", mood="raised", mouth="grin")
    st = skin[2]
    for y in range(44, 50):                                # stubble
        for x in range(24, 41):
            if c.get(x, y) in skin[2:] and (x * 3 + y) % 4 == 0:
                c.put(x, y, skin[1])
    # bag of chips held up on the right
    for y in range(52, 76):
        for x in range(41, 60):
            if y < 55 and (x + y) % 3 == 0:
                continue                                    # crinkled top edge
            u = (x - 41) / 19
            c.put(x, y, lvl(bag, 0.95 - u * 0.75, x, y))
    for y in range(61, 66):
        for x in range(41, 60):
            c.put(x, y, lvl(red, 0.9 - (x - 41) / 25, x, y))
    c.line(44, 69, 50, 69, bag[1])
    sphere(c, 50, 70, 3, 2, bag, lift=0.1)                 # a chip on the bag art
    finish(c, "kevin", "Kevin")


# --- Mom -------------------------------------------------------------------------------------
def mom():
    p = new()
    skin = p.ramp(*SKIN)
    hair = p.ramp("#3a322c", "#574a40", "#776858", "#978778", "#b6a896")
    card = p.ramp("#33242f", "#4f394b", "#6e5568", "#8c7086", "#a98ea2")
    blouse = p.ramp("#9a978c", "#c4c0b2", "#e2ddd0", "#f2eee4")
    c = mk(p)
    sphere(c, 32, 86, 31, 26, card)
    texture(c, card, 0.06, 5)
    sphere(c, 32, 70, 7, 14, blouse, lift=0.1)
    c.line(25, 58, 31, 64, card[1])                         # cardigan edges
    c.line(39, 58, 33, 64, card[1])
    for y in (66, 72):                                      # buttons
        sphere(c, 25, y, 1.5, 1.5, hair, lift=0.2)
        sphere(c, 39, y, 1.5, 1.5, hair, lift=0.2)
    sphere(c, 32, 26, 16, 13, hair)                         # bob volume
    sphere(c, 18.5, 38, 5, 12, hair)
    sphere(c, 45.5, 38, 5, 12, hair)
    person(p, c, skin, ears=False)
    sphere(c, 30, 27, 12, 6, hair, only=skin + ".")         # side-swept fringe
    strands(c, hair, step=4, slope=-1, seed=6)
    pearl = p.ramp("#a8a498", "#e2ddd0", "#f8f6f0")
    for i in range(-5, 6):                                   # pearl necklace
        x, y = 32 + i * 1.6, 57 + abs(i) * -0.5 + (i * i) * 0.12
        c.put(x, y, pearl[1 if i % 2 else 2])
    features(c, p, skin, iris="#6a5040", brow="#574a40", mood="open", mouth="pursed", blush=False)
    g, gl = p.col("#2a2430"), p.col("#d8e2d6")
    for ex in (24, 37):                                     # glasses with glare (centred on both eyes)
        c.rect(ex - 1, 33, ex + 4, 33, g)
        c.rect(ex - 1, 38, ex + 4, 38, g)
        c.rect(ex - 1, 33, ex - 1, 38, g)
        c.rect(ex + 4, 33, ex + 4, 38, g)
        c.put(ex + 3, 34, gl)
        c.put(ex + 2, 35, gl)
    c.rect(29, 34, 35, 34, g)
    c.put(23, 36, skin[1])                                  # smile lines
    c.put(41, 36, skin[1])
    sphere(c, 20.5, 45, 1.3, 1.3, pearl)                    # earrings
    sphere(c, 43.5, 45, 1.3, 1.3, pearl)
    finish(c, "mom", "Mom")


# --- Captain Comet (original cartoon hero) ------------------------------------------------------
def comet():
    p = new()
    skin = p.ramp(*SKIN)
    suit = p.ramp("#191d3a", "#26305c", "#38488a", "#5370b8", "#7e9ad8")
    cape = p.ramp("#3a1614", "#622420", "#8a382e", "#b0503e", "#cc7058")
    gold = p.ramp("#5a4220", "#8a6a2e", "#b8913f", "#dcb85a", "#f4dc8c")
    c = mk(p)
    sphere(c, 32, 70, 32, 18, cape)                          # high cape collar
    sphere(c, 32, 86, 30, 24, suit)
    fold(c, suit, [(14, 66), (20, 75)])                        # muscle/fold lines
    fold(c, suit, [(50, 66), (44, 75)])
    star = [(0, -7), (2, -2), (7, -2), (3, 1), (5, 6), (0, 3), (-5, 6), (-3, 1), (-7, -2), (-2, -2)]

    def in_star(x, y, cx, cy, s):
        pts = [(cx + a * s, cy + b * s) for a, b in star]
        ins = False
        j = len(pts) - 1
        for i in range(len(pts)):
            xi, yi = pts[i]
            xj, yj = pts[j]
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                ins = not ins
            j = i
        return ins
    for y in range(58, 76):                                    # chest star
        for x in range(22, 43):
            if in_star(x + 0.5, y + 0.5, 32, 67, 1.25):
                d = ((x - 32) * -0.5 + (y - 67) * -0.6) / 8
                c.put(x, y, lvl(gold, 0.55 + d, x, y))
    person(p, c, skin, cy=38, rx=11.5, ry=13.5)
    sphere(c, 32, 46, 9, 5, skin, only=skin)                    # square heroic jaw
    sphere(c, 32, 27, 14, 10, suit)                             # helmet dome
    for y in range(14, 24):
        for x in range(25, 40):
            if in_star(x + 0.5, y + 0.5, 32, 20, 0.75):
                c.put(x, y, lvl(gold, 0.8 - (y - 14) / 20, x, y))
    c.rect(20, 31, 44, 31, suit[0])                              # helmet rim
    features(c, p, skin, cy if False else 32, ey=36, iris="#3a5a9a", brow="#26305c", mood="open", mouth="grin")
    c.rect(30, 51, 34, 51, skin[1])                              # chin dimple
    finish(c, "comet", "Captain Comet, original cartoon hero")


# --- Sheep #47, union rep ------------------------------------------------------------------------
def sheep():
    p = new()
    wool = p.ramp("#6a655c", "#948e84", "#bab4a8", "#d8d3c6", "#efebe0")
    face = p.ramp("#16121a", "#221c28", "#322a38", "#443a4c", "#5a4f62")
    c = mk(p)
    rnd = random.Random(47)
    for cx, cy, r in ((32, 70, 22), (12, 64, 9), (52, 64, 9), (18, 56, 8), (46, 56, 8), (32, 56, 9),
                      (24, 60, 8), (40, 60, 8)):
        sphere(c, cx, cy, r, r * 0.9, wool)
    for _ in range(60):                                          # curls
        x, y = rnd.randrange(4, 60), rnd.randrange(50, 76)
        if c.get(x, y) in wool[2:]:
            sphere(c, x, y, 2.2, 1.8, wool, only=wool)
            c.put(x - 1, y + 1, wool[1])
    for cx, cy, r in ((24, 22, 6), (32, 18, 7), (40, 22, 6), (28, 26, 5), (36, 26, 5)):
        sphere(c, cx, cy, r, r * 0.85, wool)                     # tuft
    for ex, d in ((17, -1), (47, 1)):                             # ears
        sphere(c, ex, 32, 7, 3.2, face)
        c.rect(ex - 3 + d, 32, ex + 2 + d, 32, p.col("#9a6a72"))
    sphere(c, 32, 37, 10, 13, face)
    sphere(c, 32, 46, 6.5, 5, face, lift=0.12)                   # muzzle
    sphere(c, 32, 28, 9, 4, wool, only=face + ".")               # tuft over forehead
    yel, pup, lid = p.col("#c9b46a"), p.col("#0e0b10"), p.col("#0e0b10")
    for ex in (24, 36):                                          # sleepy goat eyes, horizontal pupils
        c.rect(ex - 1, 34, ex + 4, 34, lid)
        c.rect(ex, 35, ex + 3, 36, yel)
        c.rect(ex, 35, ex + 3, 35, lid)                           # half-closed lid
        c.rect(ex + 1, 36, ex + 2, 36, pup)
        c.rect(ex, 38, ex + 3, 38, face[1])                       # bags
    n = p.col("#0e0b10")
    c.rect(31, 46, 33, 46, n)                                     # Y-shaped nose/mouth
    c.put(32, 47, n)
    c.put(31, 49, n)
    c.put(33, 49, n)
    c.put(32, 48, n)
    red = p.ramp("#4a1a16", "#7a2a22", "#a04a3e", "#c26a52", "#e0907a")
    gold = p.ramp("#5a4220", "#b8913f", "#e0c070")
    sphere(c, 46, 66, 5, 5, gold)                                 # union pin
    sphere(c, 46, 66, 3.6, 3.6, red)
    finish(c, "sheep", "Sheep #47, union rep")


# --- Biscuit, childhood beagle ---------------------------------------------------------------------
def biscuit():
    p = new()
    tan = p.ramp("#4a2c1c", "#6e4429", "#93603a", "#b8804f", "#d6a46e")
    wht = p.ramp("#7a776e", "#a29e92", "#c6c1b2", "#e0dbcd", "#f4f0e6")
    ear = p.ramp("#1e120c", "#2e1d14", "#432b1e", "#583a29", "#6e4a34")
    red = p.ramp("#4a1a16", "#7a2a22", "#a04a3e", "#c26a52")
    gold = p.ramp("#5a4220", "#8a6a2e", "#c8a24a", "#ecd27e")
    c = mk(p)
    sphere(c, 32, 76, 21, 16, wht)                                # chest
    sphere(c, 13, 72, 8, 12, tan)
    sphere(c, 51, 72, 8, 12, tan)
    for y in range(58, 62):                                       # collar
        for x in range(16, 49):
            c.put(x, y, lvl(red, 0.95 - (x - 16) / 40 - (y - 58) * 0.08, x, y))
    sphere(c, 32, 65, 3.2, 3.2, gold)                             # tag
    sphere(c, 32, 38, 15.5, 14.5, tan)                            # head
    strands(c, tan, step=5, slope=0, seed=9)
    sphere(c, 32, 47, 9.5, 7.5, wht)                              # muzzle
    sphere(c, 32, 38, 15.5, 14.5, wht, clip=lambda x, y: 30 <= x <= 34 and 24 <= y <= 44)   # blaze
    for ex in (15, 49):                                           # floppy ears
        sphere(c, ex, 45, 7, 14.5, ear)
        c.line(ex, 36, ex + (2 if ex < 32 else -2), 55, ear[0])
    nose = p.ramp("#0e0b10", "#2a2430", "#4a4256", "#8a8296")
    sphere(c, 32, 45, 4, 2.8, nose)
    c.rect(32, 48, 32, 50, nose[0])
    c.line(27, 51, 31, 51, nose[0])
    c.line(33, 51, 37, 51, nose[0])
    tng = p.ramp("#7a3040", "#b0506a", "#d87a90")
    sphere(c, 33.5, 54, 2.5, 3, tng)
    eyes = p.ramp("#0e0b10", "#3a2a20")
    for ex in (25, 38):                                            # big puppy eyes
        sphere(c, ex + 0.5, 38.5, 2.2, 2.2, eyes)
        c.put(ex - 1, 37, p.col("#f4f0e6"))
        c.put(ex + 1, 39, p.col("#c6c1b2"))
    sp = p.col("#e8e0ff")                                          # a little dream sparkle
    for x, y in ((8, 20), (56, 14), (52, 28)):
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            c.put(x + dx, y + dy, sp)
    finish(c, "biscuit", "Biscuit, childhood beagle")


# --- The D-minus: offended physics test ----------------------------------------------------------------
def dminus():
    p = new()
    paper = p.ramp("#6f7d80", "#9babb2", "#c0cdcc", "#d8e2d6", "#eef3ec")
    red = p.ramp("#5a1a16", "#8a2a24", "#b33831", "#d65a48")
    line = p.col("#a6b8c8")
    pencil = p.ramp("#2a2a30", "#4a4a52", "#6a6a74")
    c = mk(p)
    for y in range(12, 76):                                         # gently curled sheet
        for x in range(11, 54):
            u = (x - 32.5) / 21.5
            v = 0.82 - 0.35 * u * u - u * 0.12 - (y - 12) / 400
            c.put(x, y, lvl(paper, v, x, y))
    texture(c, paper, 0.02, 11)
    for y in range(22, 76, 6):
        c.rect(14, y, 50, y, line)
    for i in range(10):                                             # dog-ear
        for j in range(10 - i):
            c.put(53 - j, 12 + i, ".")
        c.put(53 - (9 - i), 12 + i, paper[0])
        for j in range(9 - i):
            c.put(44 + j, 12 + i, paper[2] if j < 9 - i - 1 else paper[1])
    for k in range(0, 360, 4):                                      # red grade circle (2px)
        a = math.radians(k)
        for r in (8.5, 9.5):
            c.put(30 + r * math.cos(a), 27 + r * 0.78 * math.sin(a), red[2] if k < 200 else red[1])
    c.rect(25, 26, 35, 28, red[2])                                   # "minus" stroke
    c.rect(25, 28, 35, 28, red[1])
    for x0, y0 in ((17, 56), (36, 62), (19, 68)):                    # crosses
        c.line(x0, y0, x0 + 4, y0 + 4, red[2])
        c.line(x0 + 4, y0, x0, y0 + 4, red[2])
        c.line(x0 + 1, y0, x0 + 5, y0 + 4, red[1])
    c.line(19, 40, 26, 44, pencil[0])                                # furious brows
    c.line(19, 41, 26, 45, pencil[0])
    c.line(45, 40, 38, 44, pencil[0])
    c.line(45, 41, 38, 45, pencil[0])
    w, k = p.col("#f8f8f4"), p.col("#16141a")
    for ex in (22, 38):
        c.rect(ex, 45, ex + 3, 47, w)
        c.rect(ex + 1 if ex < 32 else ex + 1, 46, ex + 2, 47, k)
        c.rect(ex - 1, 44, ex + 4, 44, pencil[0])
    c.rect(26, 52, 38, 52, pencil[0])                                # gritted teeth
    c.rect(26, 53, 38, 55, w)
    for x in range(28, 38, 3):
        c.rect(x, 53, x, 55, pencil[1])
    c.rect(26, 56, 38, 56, pencil[0])
    for (x0, y0), (x1, y1), (x2, y2) in (((11, 50), (4, 56), (11, 62)), ((53, 50), (60, 56), (53, 62))):
        c.line(x0, y0, x1, y1, pencil[0])                             # stick arms on hips
        c.line(x1, y1, x2, y2, pencil[0])
        c.line(x0, y0 + 1, x1, y1 + 1, pencil[1])
    finish(c, "dminus", "The D-minus, offended physics test (no letters)")


# --- Mr. Grayline, the boss ------------------------------------------------------------------------
def grayline():
    p = new()
    skin = p.ramp("#5a3a32", "#86584a", "#ac7864", "#cc9a80", "#e4b89c")
    hair = p.ramp("#4a4a4e", "#6a6a70", "#8c8c92", "#acacb2", "#c8c8cc")
    suit = p.ramp("#1e2226", "#2c3238", "#3e464e", "#525c66", "#6a7680")
    shirt = p.ramp("#9aa0a4", "#c4cace", "#e0e4e6", "#f2f4f4")
    tie = p.ramp("#3a1418", "#5e2026", "#842e34", "#a8423e")
    c = mk(p)
    sphere(c, 32, 86, 31, 25, suit)                          # suit shoulders
    texture(c, suit, 0.04, 21)
    for y in range(57, 76):                                    # shirt V
        hw = (y - 57) * 0.42 + 4
        for x in range(int(32 - hw), int(32 + hw) + 1):
            c.put(x, y, lvl(shirt, 0.85 - abs(x - 32) / 18, x, y))
    for y in range(57, 76):                                    # lapels
        hw = (y - 57) * 0.42 + 4
        c.line(32 - hw - 1, y, 32 - hw + 1, y, suit[3])
        c.line(32 + hw - 1, y, 32 + hw + 1, y, suit[1])
    for y in range(59, 76):                                    # tie, knot then blade
        hw = 2 if y < 62 else 2 + (y - 62) * 0.12
        for x in range(int(32 - hw), int(32 + hw) + 1):
            c.put(x, y, lvl(tie, 0.8 - (x - 32 + hw) / (2 * hw + 1) * 0.6, x, y))
    c.rect(31, 62, 33, 62, tie[0])
    for y in range(64, 76, 4):                                 # tie stripes
        c.line(30, y + 1, 34, y - 1, tie[3], only=tie)
    pen = p.col("#b8913f")
    c.rect(44, 64, 44, 69, pen)                                # pen in the breast pocket
    c.rect(41, 69, 47, 69, suit[0])
    person(p, c, skin, rx=11.5, ry=13)
    sphere(c, 32, 46, 9.5, 5, skin, only=skin)                 # heavy jaw
    sphere(c, 32, 26, 12.5, 6, hair, only=skin + ".")          # receding hair
    sphere(c, 32, 31, 8.5, 6, skin, only=hair)                 # bald forehead patch
    for x in range(24, 41):                                    # comb-over strands
        if x % 3 == 0:
            c.line(x - 2, 25, x + 2, 28, hair[3], only=skin)
    sphere(c, 21, 33, 2.4, 5, hair)                            # grey temples
    sphere(c, 43, 33, 2.4, 5, hair)
    strands(c, hair, step=3, slope=-1, seed=22)
    features(c, p, skin, iris="#5a6068", brow="#5a5a60", mood="angry", mouth="flat", blush=False)
    m = p.ramp("#3a3a3e", "#5a5a60", "#7a7a80")
    c.rect(27, 44, 37, 44, m[1])                               # moustache
    c.rect(28, 45, 36, 45, m[0])
    c.put(27, 45, m[2])
    for i in range(4):                                         # shirt collar points (filled)
        c.rect(27 - i, 56 + i, 29, 56 + i, shirt[3] if i < 3 else shirt[1])
        c.rect(35, 56 + i, 37 + i, 56 + i, shirt[2] if i < 3 else shirt[1])
    c.put(23, 42, skin[1])                                     # frown lines
    c.put(41, 42, skin[1])
    finish(c, "grayline", "Mr. Grayline, the boss")


# --- Ms. Okafor, the old art teacher ---------------------------------------------------------------
def okafor():
    p = new()
    skin = p.ramp("#2a1812", "#45291e", "#64402c", "#86593c", "#a8774f")
    hair = p.ramp("#5a5658", "#7c787a", "#9e9a9a", "#bebaba", "#dad6d4")
    smock = p.ramp("#2a3a4a", "#3a5068", "#4e6a88", "#6888a8", "#88a6c4")
    wrap = p.ramp("#5a2a10", "#8a4416", "#b8641e", "#d88a2e", "#eeb052")
    c = mk(p)
    sphere(c, 32, 86, 31, 25, smock)                           # paint smock
    texture(c, smock, 0.05, 31)
    fold(c, smock, [(15, 66), (20, 75)])
    fold(c, smock, [(49, 66), (44, 75)])
    sphere(c, 32, 60, 8, 3, smock, lift=0.1)                   # collar
    rnd = random.Random(31)
    paint = [p.col(h) for h in ("#d65a48", "#e3c25a", "#6aa060", "#e8e4dc", "#b05aa0")]
    for _ in range(14):                                        # paint splotches
        x, y = rnd.randrange(8, 56), rnd.randrange(63, 76)
        if c.get(x, y) in smock:
            col = rnd.choice(paint)
            c.put(x, y, col)
            if rnd.random() < .5 and c.get(x + 1, y) in smock:
                c.put(x + 1, y, col)
    sphere(c, 32, 31, 18, 15, hair)                            # big grey curls behind
    for _ in range(70):
        x, y = rnd.randrange(12, 52), rnd.randrange(16, 48)
        if c.get(x, y) in hair[2:]:
            sphere(c, x, y, 1.8, 1.5, hair, only=hair)
            c.put(x - 1, y + 1, hair[1])
    person(p, c, skin)
    sphere(c, 32, 21, 15, 6.5, wrap)                           # orange headwrap band
    for x in range(18, 47, 3):
        c.line(x, 16, x + 2, 25, wrap[1], only=wrap)
    sphere(c, 42, 15, 4.5, 3.5, wrap, lift=0.1)                # knot
    brush = p.ramp("#5a3a1c", "#8a6030", "#b88a48")
    c.line(45, 30, 54, 18, brush[1])                           # brush behind the ear
    c.line(46, 30, 55, 18, brush[2])
    c.rect(54, 16, 56, 17, p.col("#3a6ab0"))                   # blue tip
    features(c, p, skin, iris="#3a2618", brow="#7c787a", mood="open", mouth="smile", blush=False)
    g, gl = p.col("#9a2a2a"), p.col("#e8d8c8")
    for ex in (24, 37):                                        # rounded red glasses, one per eye
        c.rect(ex, 33, ex + 3, 33, g); c.rect(ex, 38, ex + 3, 38, g)            # top / bottom rims
        c.rect(ex - 1, 34, ex - 1, 37, g); c.rect(ex + 4, 34, ex + 4, 37, g)    # sides (corners left open = round)
        c.put(ex + 3, 34, gl)
    c.rect(29, 35, 35, 35, g)                                  # bridge
    for ex in (22, 42):                                        # laugh lines
        c.put(ex, 39, skin[1])
    sphere(c, 20.5, 45, 1.5, 2, wrap)                          # earrings
    sphere(c, 43.5, 45, 1.5, 2, wrap)
    finish(c, "okafor", "Ms. Okafor, the old art teacher")


# ======================= meme-parody guests (all original characters) =======================
def anime_eye(c, p, x, y, iris, left=True):
    """5x6 anime eye at (x,y) top-left: thick lash line, tall iris, two glints."""
    k, w = p.col("#1a1420"), p.col("#f6f4f0")
    ir = p.ramp(*iris)
    c.rect(x, y + 1, x + 4, y + 5, w)
    c.rect(x + 1, y + 1, x + 4, y + 5, ir[1]) if left else c.rect(x, y + 1, x + 3, y + 5, ir[1])
    xi = x + 1 if left else x
    c.rect(xi, y + 3, xi + 3, y + 5, ir[2])
    c.rect(xi + 1, y + 2, xi + 2, y + 4, k)
    c.put(xi, y + 1, w)
    c.put(xi + 3, y + 4, w)
    c.rect(x - (1 if left else 0), y, x + 4 + (0 if left else 1), y, k)          # lash line
    c.put(x - 1 if left else x + 5, y - 1, k)                                     # flick


def spikes(c, ramp, tips, base_y):
    """Spiky hair: triangles from base_y up to each (x, y) tip, ~5px wide at the base."""
    for tx, ty in tips:
        for y in range(ty, base_y + 1):
            hw = (y - ty) / (base_y - ty + 1) * 4
            for x in range(int(tx - hw), int(tx + hw) + 1):
                c.put(x, y, lvl(ramp, 0.8 - (x - tx) / 12 - (y - ty) / 30, x, y))


# --- Max Giveaway: giveaway-video YouTuber --------------------------------------------------------
def giveaway():
    p = new()
    skin = p.ramp(*SKIN)
    hair = p.ramp("#2a1a10", "#46301c", "#644628", "#86603a", "#a47a4e")
    hood = p.ramp("#122a52", "#1c3c72", "#28529a", "#3a6cc0", "#5a8ad8")
    chq = p.ramp("#8a948a", "#c2cabc", "#e6ece0", "#f8fbf4")
    c = mk(p)
    sphere(c, 32, 84, 31, 25, hood)
    sphere(c, 32, 60, 15, 5, hood, lift=0.08)                  # hood round the neck
    fold(c, hood, [(17, 66), (21, 75)])
    sphere(c, 24, 70, 4, 4, p.ramp("#8a6a10", "#d8a820", "#f8d850"))   # round logo patch
    person(p, c, skin)
    sphere(c, 32, 26, 13, 7, hair)                             # short hair with a quiff
    sphere(c, 28, 22, 6, 4, hair)
    sphere(c, 21, 31, 2.5, 4, hair)
    sphere(c, 43, 31, 2.5, 4, hair)
    strands(c, hair, step=3, slope=1, seed=51)
    features(c, p, skin, iris="#4a6a9a", brow="#46301c", mood="wide", mouth="grin")
    for y in range(54, 76):                                    # giant novelty cheque on the right
        for x in range(36, 64):
            c.put(x, y, lvl(chq, 0.85 - (x - 36) / 70 - (y - 54) / 90, x, y))
    g = p.col("#2e8a4a")
    c.rect(36, 54, 63, 55, g)
    c.rect(36, 74, 63, 75, g)
    c.rect(39, 59, 50, 59, chq[0])
    c.rect(39, 63, 58, 64, p.col("#2a3a2a"))                   # the big number
    c.rect(52, 68, 60, 68, p.col("#3a4a8a"))                   # signature
    c.put(51, 69, p.col("#3a4a8a"))
    sphere(c, 37, 66, 3, 4, skin)                              # hand holding it
    finish(c, "giveaway", "Max Giveaway, giveaway YouTuber (original)")


# --- Magical Girl Hoshiko ------------------------------------------------------------------------
def magical():
    p = new()
    skin = p.ramp("#6a4038", "#9a6858", "#c89078", "#e8b49a", "#f8d4bc")
    hair = p.ramp("#6a1a4a", "#962a68", "#c24a8a", "#e070aa", "#f49ac8")
    dress = p.ramp("#7a2a5a", "#b04a82", "#d870a8", "#f09ac4", "#fac4dc")
    wht = p.ramp("#a4a0b0", "#d0ccd8", "#eeeaf2", "#fcfaff")
    gold = p.ramp("#6a4a1a", "#b8913f", "#e8c860", "#fae8a0")
    c = mk(p)
    for sx in (13, 51):                                        # twin tails
        sphere(c, sx, 46, 5, 20, hair)
        sphere(c, sx + (2 if sx < 32 else -2), 64, 3.5, 9, hair)
    sphere(c, 32, 86, 29, 25, dress)
    sphere(c, 32, 62, 14, 5, wht, lift=0.1)                    # frilled collar
    for x in range(19, 46, 3):
        c.put(x, 66, wht[1])
    sphere(c, 32, 68, 3.5, 3.5, p.ramp("#6a1a2a", "#c83a5a", "#f07a9a"))   # heart brooch
    sphere(c, 32, 30, 15, 13, hair)                            # hair volume, behind the head
    person(p, c, skin, ears=False)
    sphere(c, 32, 30, 13, 8, hair, only=skin, clip=lambda x, y: y < 30)   # hairline
    sphere(c, 32, 27, 12, 4.5, hair, only=skin + ".")          # straight bangs, above the eyes
    for x in (25, 29, 35, 39):                                 # bang points
        c.put(x, 31, hair[2]) if c.get(x, 30) in hair else None
    sphere(c, 20, 40, 3, 9, hair)                              # side locks
    sphere(c, 44, 40, 3, 9, hair)
    for sx in (18, 46):                                        # ribbons holding the tails
        sphere(c, sx, 25, 2.6, 2, wht)
    strands(c, hair, step=4, slope=1, seed=52)
    anime_eye(c, p, 24, 34, ("#3a2a6a", "#6a4ab0", "#a07ae0"), left=True)
    anime_eye(c, p, 35, 34, ("#3a2a6a", "#6a4ab0", "#a07ae0"), left=False)
    c.put(32, 42, skin[1])                                     # tiny nose
    c.rect(31, 45, 33, 45, p.col("#a4545a"))                   # small open smile
    c.put(32, 46, p.col("#6e2e36"))
    for x in (23, 25, 39, 41):
        c.put(x, 42, p.col("#f08a9a"))
    for y in range(50, 76):                                    # star wand on the right
        c.put(51, y, gold[1])
        c.put(52, y, gold[2])
    star = [(0, -5), (1, -2), (5, -2), (2, 1), (3, 5), (0, 2), (-3, 5), (-2, 1), (-5, -2), (-1, -2)]
    for y in range(40, 52):
        for x in range(46, 58):
            pts = [(51.5 + a, 46 + b) for a, b in star]
            ins, j = False, len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]; xj, yj = pts[j]
                if (yi > y + .5) != (yj > y + .5) and x + .5 < (xj - xi) * (y + .5 - yi) / (yj - yi) + xi:
                    ins = not ins
                j = i
            if ins:
                c.put(x, y, lvl(gold, 0.9 - (y - 40) / 16, x, y))
    finish(c, "magical", "Magical Girl Hoshiko (original)")


# --- Ryuu the Hero: shonen protagonist --------------------------------------------------------------
def shonen():
    p = new()
    skin = p.ramp(*SKIN)
    hair = p.ramp("#14121c", "#221e2e", "#342e44", "#4a425e", "#625a7a")
    jak = p.ramp("#4a1012", "#74181c", "#9c2a28", "#c44438", "#e06a50")
    band = p.ramp("#5a5a62", "#8a8a94", "#b8b8c2", "#e0e0e8")
    c = mk(p)
    sphere(c, 32, 84, 31, 25, jak)
    fold(c, jak, [(16, 66), (21, 75)])
    fold(c, jak, [(48, 66), (43, 75)])
    sphere(c, 32, 61, 13, 4.5, band, lift=0.1)                 # white collar
    c.rect(31, 62, 33, 75, jak[0])                             # zip
    person(p, c, skin)
    sphere(c, 32, 25, 14.5, 9, hair)                           # hair mass
    spikes(c, hair, [(18, 14), (23, 7), (30, 5), (36, 10), (42, 6), (47, 13), (15, 22), (50, 22)], 21)
    for x0, x1, y1 in ((24, 21, 36), (40, 43, 36)):            # sharp side bangs
        c.line(x0, 28, x1, y1, hair[2]); c.line(x0 + 1, 28, x1 + 1, y1, hair[2])
    red = p.col("#c83a3a")
    c.line(30, 7, 31, 20, red)                                 # one red streak
    features(c, p, skin, iris="#b8423a", brow="#221e2e", mood="angry", mouth="grin", blush=False)
    c.rect(38, 44, 41, 44, skin[1])                            # little cheek plaster
    c.rect(38, 43, 41, 43, p.col("#e8d8c0"))
    finish(c, "shonen", "Ryuu the Hero, shonen protagonist (original)")


# --- Truck-san: the truck driver who sends people to other worlds ------------------------------------------
def truck():
    p = new()
    skin = p.ramp(*SKIN)
    cap = p.ramp("#1a3a1e", "#28562c", "#3a7a3c", "#58a04c")
    capf = p.ramp("#a8a498", "#d6d2c6", "#f2eee4")
    plaid = p.ramp("#4a1418", "#7a2026", "#a8302e", "#c8483e", "#e06a58")
    stub = p.ramp("#3a2c26", "#5a463c")
    c = mk(p)
    sphere(c, 32, 84, 31, 25, plaid)
    for y in range(58, 76):                                    # flannel plaid, regular grid
        for x in range(0, 64):
            if c.get(x, y) in plaid and (x % 8 in (0, 1) or y % 8 in (0, 1)):
                c.put(x, y, plaid[0] if (x % 8 in (0, 1) and y % 8 in (0, 1)) else plaid[1])
    sphere(c, 32, 62, 8, 3, p.ramp("#2a2a2e", "#4a4a52", "#6a6a74"))     # undershirt
    person(p, c, skin)
    sphere(c, 32, 25, 14, 8, capf, clip=lambda x, y: y <= 27)  # cap front panel (white)
    sphere(c, 32, 25, 14, 8, cap, clip=lambda x, y: y <= 27 and (x < 25 or x > 39))   # green mesh sides
    for x in range(18, 47):                                    # brim
        c.put(x, 28, cap[1]); c.put(x, 29, cap[0])
    c.rect(28, 21, 36, 24, cap[2])                             # truck-shaped badge
    c.rect(34, 22, 35, 23, capf[2])
    c.put(29, 25, p.col("#1a1a1e")); c.put(35, 25, p.col("#1a1a1e"))
    features(c, p, skin, iris="#5a4a3a", brow="#3a2c26", mood="tired", mouth="flat", blush=False)
    for y in range(43, 51):                                    # stubble, regular
        for x in range(23, 42):
            if c.get(x, y) in skin[1:] and (x + y) % 2 == 0:
                c.put(x, y, stub[1])
    c.rect(27, 44, 37, 44, stub[0])                            # moustache
    c.rect(26, 45, 27, 46, stub[0]); c.rect(37, 45, 38, 46, stub[0])
    finish(c, "truck", "Truck-san, isekai truck driver (original)")


# --- The Sigma -----------------------------------------------------------------------------------
def sigma():
    p = new()
    skin = p.ramp("#4a3a36", "#76605a", "#a08a82", "#c6b2a8", "#e0d0c6")   # desaturated, black-and-white look
    hair = p.ramp("#0e0e12", "#1c1c22", "#2c2c34", "#40404a", "#585862")
    tn = p.ramp("#16161a", "#24242a", "#34343c", "#484852", "#5e5e6a")
    c = mk(p)
    sphere(c, 32, 84, 31, 25, tn)
    sphere(c, 32, 58, 9, 7, tn, lift=0.05)                     # turtleneck
    for y in (56, 58, 60):
        c.rect(25, y, 39, y, tn[1], ) if True else None
    person(p, c, skin, rx=13, ry=13.5)
    sphere(c, 32, 46, 11, 6, skin, only=skin, amb=0.1)          # broad jaw
    c.rect(32, 49, 32, 50, skin[1])                            # chin cleft
    sphere(c, 32, 25, 13.5, 6.5, hair)                         # slicked back
    for x in range(21, 44, 3):
        c.line(x, 21, x + 2, 27, hair[3], only=hair)
    features(c, p, skin, iris="#3a3a44", brow="#1c1c22", mood="open", mouth="flat", blush=False)
    c.rect(36, 31, 40, 31, p.col("#1c1c22"))                    # one raised brow
    c.rect(36, 32, 40, 32, skin[2])
    finish(c, "sigma", "The Sigma (original)")


# --- Nika Live: streamer ---------------------------------------------------------------------------------
def streamer():
    p = new()
    skin = p.ramp(*SKIN)
    hair = p.ramp("#2a1446", "#3e1e66", "#582c8c", "#7646b2", "#9a6ad2")
    hood = p.ramp("#14141c", "#20202c", "#30303e", "#444456", "#5c5c72")
    head = p.ramp("#1a1a22", "#2c2c38", "#40404e")
    cy_, mg = p.col("#3ae0e8"), p.col("#e83ac8")
    c = mk(p)
    sphere(c, 32, 84, 31, 25, hood)
    c.line(5, 70, 59, 70, cy_, only=hood)                      # RGB stripe on the hoodie
    sphere(c, 32, 33, 15, 13, hair)                            # bob, behind the head
    person(p, c, skin)
    sphere(c, 32, 30, 13, 8, hair, only=skin, clip=lambda x, y: y < 30)   # hairline
    sphere(c, 19, 41, 4, 8, hair)
    sphere(c, 45, 41, 4, 8, hair)
    sphere(c, 32, 27, 12, 4.5, hair, only=skin + ".")          # blunt bangs, above the eyes
    strands(c, hair, step=3, slope=0, seed=56)
    for y in range(17, 22):                                    # headset band
        for x in range(18, 47):
            if abs((x - 32) ** 2 / 210 + (y - 33) ** 2 / 270 - 1) < 0.07:
                c.put(x, y, head[1])
    for sx in (18, 46):                                        # cat-ear cups + ear muffs
        sphere(c, sx, 38, 3.5, 5, head)
        c.put(sx, 37, cy_ if sx < 32 else mg)
    for i, sx in enumerate((20, 44)):
        for k_ in range(5):
            c.rect(sx - 2 + k_ // 2 if i == 0 else sx - k_ // 2, 15 + k_, sx + 2 - k_ // 2 if i == 0 else sx + 2 - k_ // 2, 15 + k_, head[1])
    c.line(19, 42, 26, 48, head[1])                            # mic boom
    sphere(c, 27, 48, 1.5, 1.5, head)
    features(c, p, skin, iris="#5a3a8a", brow="#3e1e66", mood="open", mouth="smile")
    finish(c, "streamer", "Nika Live, streamer (original)")


# --- Brayden Moon: crypto bro -------------------------------------------------------------------------
def crypto():
    p = new()
    skin = p.ramp(*SKIN)
    hair = p.ramp("#6a5020", "#9a7a34", "#c8a44c", "#e2c46a", "#f4dc92")
    vest = p.ramp("#14181e", "#20262e", "#2e3640", "#424c58", "#5a6674")
    shirt = p.ramp("#5a7a9a", "#7a9ab8", "#a0bcd4", "#c8dcec")
    c = mk(p)
    sphere(c, 32, 84, 31, 25, shirt)
    for side in (-1, 1):                                       # puffer vest panels
        for y in range(57, 76):
            for x in range(64):
                if c.get(x, y) in shirt and (x - 32) * side > 6 + (y - 57) * 0.15:
                    c.put(x, y, lvl(vest, 0.7 - (x - 8) / 90 - ((y - 57) % 6) / 14, x, y))
    for y in range(62, 76, 6):
        c.rect(4, y, 60, y, vest[0], ) if False else c.line(0, y, 63, y, vest[1], only=vest)
    person(p, c, skin)
    sphere(c, 32, 26, 13.5, 7, hair)                           # slicked-back blond
    for x in range(21, 44, 3):
        c.line(x, 20, x + 3, 27, hair[4], only=hair)
    sphere(c, 21, 31, 2.5, 4, hair); sphere(c, 43, 31, 2.5, 4, hair)
    features(c, p, skin, iris="#4a6a8a", brow="#9a7a34", mood="open", mouth="grin", blush=False)
    sh = p.ramp("#0a0a10", "#1a1a26", "#2c2c3e")
    for ex in (22, 34):                                        # sunglasses at night
        for y in range(33, 38):
            for x in range(ex, ex + 8):
                c.put(x, y, sh[2] if y == 33 else sh[1] if (x - ex + y) % 5 else sh[2])
    c.rect(30, 34, 33, 34, sh[0])
    c.rect(20, 34, 21, 34, sh[0]); c.rect(42, 34, 43, 34, sh[0])
    ph = p.ramp("#0a0a10", "#1e1e28")
    c.rect(44, 52, 55, 72, ph[0])                              # phone with a green chart
    c.rect(45, 53, 54, 71, ph[1])
    up = p.col("#3adc6a")
    for i, (x, y) in enumerate(((46, 68), (48, 66), (50, 67), (52, 61), (53, 56))):
        if i:
            c.line(px0, py0, x, y, up)
        px0, py0 = x, y
    sphere(c, 44, 64, 3, 4, skin)                              # thumb
    finish(c, "crypto", "Brayden Moon, crypto bro (original)")


# --- Grandma Valya: good-morning cards ----------------------------------------------------------------
def grandma():
    p = new()
    skin = p.ramp("#6a463a", "#946654", "#bc8c74", "#dcae94", "#f0cab2")
    hair = p.ramp("#7a7676", "#a09c9c", "#c4c0c0", "#e0dcdc", "#f4f2f2")
    shawl = p.ramp("#2a1a3a", "#44285a", "#62387c", "#80509a", "#a070b8")
    card = p.ramp("#a89a7a", "#d4c8a8", "#f0e8cc", "#fcf8e8")
    rose = p.ramp("#5a1020", "#9a1a34", "#d03a52", "#f07088")
    c = mk(p)
    sphere(c, 32, 86, 31, 26, shawl)
    for y in range(60, 76, 4):                                 # knitted rows
        c.line(0, y, 63, y, shawl[1], only=shawl)
    person(p, c, skin, ears=False)
    for cx_, cy_ in ((20, 26), (26, 21), (32, 19), (38, 21), (44, 26), (18, 33), (46, 33), (19, 40), (45, 40)):
        sphere(c, cx_, cy_, 5, 4.5, hair)                      # tight perm curls
    sphere(c, 32, 26, 12, 5, hair, only=skin + ".")
    features(c, p, skin, iris="#5a4a3a", brow="#a09c9c", mood="open", mouth="smile", blush=True)
    g = p.col("#7a5a2a")
    for ex in (23, 36):                                        # round gold glasses (centred on both eyes)
        c.rect(ex, 33, ex + 5, 33, g); c.rect(ex, 38, ex + 5, 38, g)
        c.rect(ex, 34, ex, 37, g); c.rect(ex + 5, 34, ex + 5, 37, g)
    c.rect(29, 34, 35, 34, g)
    for y in range(52, 76):                                    # the good-morning card
        for x in range(38, 63):
            c.put(x, y, lvl(card, 0.85 - (x - 38) / 70 - (y - 52) / 100, x, y))
    for cx_, cy_ in ((44, 64), (51, 61), (57, 66)):            # roses
        sphere(c, cx_, cy_, 3.5, 3.2, rose)
        c.put(cx_, cy_, rose[0]); c.put(cx_ - 1, cy_ - 1, rose[3])
    lf = p.col("#3a7a3a")
    for x, y in ((47, 67), (54, 64), (41, 67)):
        c.rect(x, y, x + 1, y, lf)
    gl = p.col("#e8c040")
    c.rect(41, 55, 59, 56, gl)                                 # glitter title line
    for x in range(41, 60, 3):
        c.put(x, 57, p.col("#fff4b0"))
    c.rect(43, 71, 57, 71, gl)
    sphere(c, 38, 64, 3, 4, skin)                              # hand
    finish(c, "grandma", "Grandma Valya, good-morning cards (original)")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for n in sys.argv[1:]:
            globals()[n]()
        raise SystemExit
    mira()
    kevin()
    mom()
    comet()
    sheep()
    biscuit()
    dminus()
