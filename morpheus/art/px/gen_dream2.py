"""The other dream places, built like the kitchen in gen_dream.py: dream_<place>.png (back) and
dream_<place>_fg.png (front layer that hides the bottom of the guest's bust). Same frame, same scale:
guest busts stand at x 166..294 with their bottom at y 112, Mira (from behind) sits at the lower left.
Run: python gen_dream2.py [place ...]"""
import math
import os
import random
import sys

from pxlib import Cv, Pal, sphere, texture, lvl
from gen_dream import W, H, HERE, slab, box, bayer, png

O_HEX = '#313638'


# ------------------------------------------------------------------------------------------ helpers
def grad(c, x0, y0, x1, y1, ramp):
    """Vertical gradient through a ramp (top = ramp[0]), a short checker at each step."""
    n = len(ramp)
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0) * (n - 1)
        k0, fr = int(t), t - int(t)
        for x in range(x0, x1 + 1):
            k = k0 + (1 if fr > 0.62 and bayer(x, y, (fr - 0.62) / 0.38) else 0)
            c.put(x, y, ramp[min(n - 1, k)])


def halo(c, cx, cy, r0, r1, ramp):
    """Lift the sky one step in a dithered ring around a moon or a lamp."""
    for y in range(int(cy - r1), int(cy + r1) + 1):
        for x in range(int(cx - r1), int(cx + r1) + 1):
            d = math.hypot(x + .5 - cx, y + .5 - cy)
            k = ramp.find(c.get(x, y))
            if r0 <= d < r1 and 0 <= k < len(ramp) - 1 and (d < r0 + 4 or bayer(x, y, (r1 - d) / (r1 - r0) * .45)):
                c.put(x, y, ramp[k + 1])


def puffs(c, lst, ramp, amb=.32):
    for cx, cy, rx, ry in sorted(lst, key=lambda q: q[1]):    # lower puffs in front
        sphere(c, cx, cy, rx, ry, ramp, amb=amb)


def star(c, x, y, ch, big=False):
    c.rect(x, y, x + 1, y, ch)
    if big:
        c.put(x, y - 1, ch)
        c.put(x, y + 1, ch)
        c.put(x - 1, y, ch)


FONT = {'2': '111001111100111', '5': '111100111001111', '+': '000010111010000', '=': '000111000111000',
        '?': '111001011000010', 'x': '000101010101000', '4': '101101111001001', 'A': '010101111101101'}


def text(c, x, y, s, ch, sc=2):
    for s_ in s:
        g = FONT.get(s_)
        if g:
            for i, b in enumerate(g):
                if b == '1':
                    c.rect(x + (i % 3) * sc, y + (i // 3) * sc, x + (i % 3) * sc + sc - 1, y + (i // 3) * sc + sc - 1, ch)
        x += 4 * sc


def thick(c, x0, y0, x1, y1, ch, w=2):
    for k in range(w):
        c.line(x0 + k, y0, x1 + k, y1, ch)


def new():
    p = Pal()
    O = p.col(O_HEX)
    c = Cv(W, H, {})
    c.leg = p.leg
    f = Cv(W, H, {})
    f.leg = p.leg
    return p, O, c, f


def covered(f, name):
    """The front layer must hide the bottom of every bust (x 166..294, from y 110 down)."""
    gaps = [x for x in range(168, 293) if f.get(x, 110) == '.' or f.get(x, 112) == '.']
    if gaps:
        print(f'  !! {name}: fg gap at x {gaps[0]}..{gaps[-1]} ({len(gaps)} px)')


def finish(p, c, f, name, title, oc=None):
    c.save(os.path.join(HERE, f'dream_{name}.px'), f'Dream: {title}')
    f.outline(oc or p.col(O_HEX))
    covered(f, name)
    f.save(os.path.join(HERE, f'dream_{name}_fg.px'), f'Dream: {title}, foreground')


# ------------------------------------------------------------------------------------------ the sky
def sky():
    p, O, c, f = new()
    sk = p.ramp('#181634', '#201c42', '#2a244f', '#36295c', '#463166', '#5a3a70', '#723f74', '#8c4c78')
    moon = p.ramp('#8a86a8', '#b4b0c8', '#d8d4e4', '#f2eef6')
    far = p.ramp('#3a3058', '#4e4170', '#685686', '#866e9c', '#a68aae')
    near = p.ramp('#4a3c68', '#6a5888', '#8c78a6', '#ae98c0', '#d0bad4')
    st, st2 = p.col('#ece4f6'), p.col('#a89cc8')
    grad(c, 0, 0, W - 1, H - 1, sk)
    halo(c, 252, 30, 14, 30, sk)
    sphere(c, 252, 30, 14, 14, moon, amb=.5)
    for x, y, r in ((247, 25, 3), (258, 36, 2.4), (256, 23, 1.6), (245, 35, 1.8)):
        c.ell(x, y, r, r * .8, moon[1])
    rnd = random.Random(3)
    c.rect(0, 108, W - 1, H - 1, far[1])
    lst = []
    for i in range(15):
        lst.append((i * 23 + rnd.randint(-5, 5), 104 + rnd.randint(-3, 4), rnd.randint(16, 24), rnd.randint(7, 10)))
    puffs(c, lst, far, amb=.35)
    for i in range(6):                                                # a few thin cloud streaks up high
        x0, y0 = rnd.randint(0, 280), rnd.randint(54, 84)
        c.rect(x0, y0, x0 + rnd.randint(24, 50), y0 + 1, sk[min(7, sk.find(c.get(x0, y0)) + 1)])
    c.cleanup(keep='.' + O)
    for x, y, b in ((14, 10, 1), (40, 26, 0), (70, 8, 0), (96, 30, 1), (128, 14, 0), (160, 6, 1), (186, 24, 0),
                    (204, 50, 0), (290, 12, 1), (300, 48, 0), (226, 60, 0), (120, 54, 0), (60, 46, 1), (8, 40, 0)):
        star(c, x, y, st if b else st2, b)
    pl = p.col('#e6e0ee')                                             # a paper plane, still flying
    pd = p.col('#a49cbc')
    for k in range(9):
        c.rect(140 + k, 46 - k // 3, 140 + k, 46, pl)
    c.line(140, 46, 152, 42, pd)
    c.line(143, 47, 149, 47, pd)
    # front: a cloud bank they stand in
    f.rect(0, 140, W - 1, H - 1, near[1])
    puffs(f, [(150, 130, 26, 16), (168, 118, 18, 11), (188, 116, 24, 13), (222, 113, 26, 12), (258, 115, 26, 13),
              (292, 112, 24, 13), (322, 120, 24, 16), (122, 138, 30, 16), (204, 134, 34, 16), (272, 134, 36, 18),
              (40, 142, 40, 16), (84, 136, 30, 15), (238, 124, 22, 10)], near, amb=.3)
    finish(p, c, f, 'sky', 'the sky above the clouds', near[0])


# ------------------------------------------------------------------------------------------ school
def school():
    p, O, c, f = new()
    wall = p.ramp('#3e4a40', '#505e50', '#627262', '#768676')
    board = p.ramp('#162019', '#1d2a22', '#24352b', '#2e4235')
    wood = p.ramp('#2e2019', '#46301f', '#5c3f29', '#734f33', '#8a6040')
    metal = p.ramp('#3a3e44', '#5a6068', '#7e868e', '#a4acb2', '#c6ccd0')
    chalk, chalk2 = p.col('#d6dccc'), p.col('#5e7466')
    red = p.ramp('#5a1e1e', '#8a2e2a', '#b4443a', '#d0644e')
    paper = p.ramp('#8c8676', '#b4ae9a', '#d4cebc', '#ece6d4')
    c.rect(0, 0, W - 1, H - 1, wall[2])
    texture(c, wall, .03, 2)
    c.rect(0, 100, W - 1, H - 1, wall[1])                            # painted lower wall
    c.rect(0, 99, W - 1, 99, wall[3])
    slab(c, 120, -3, 294, 5, metal)                                  # fluorescent lamp
    c.rect(124, 5, 290, 6, p.col('#eef4ea'))
    slab(c, 92, 14, 306, 97, wood)                                   # the blackboard
    c.rect(96, 18, 302, 93, board[2])
    texture(c, board, .05, 7)
    rnd = random.Random(5)
    for _ in range(16):                                               # half-erased smears
        x0, y0 = rnd.randint(98, 270), rnd.randint(20, 90)
        c.rect(x0, y0, x0 + rnd.randint(14, 34), y0 + rnd.randint(1, 3), board[3])
    slab(c, 90, 96, 308, 101, wood)                                  # chalk tray
    c.cleanup(keep='.' + O)
    text(c, 114, 24, '2+2=5', chalk)
    text(c, 250, 24, 'x=?', chalk)
    c.rect(114, 37, 152, 37, chalk2)
    c.line(114, 84, 134, 50, chalk)                                  # a triangle and its sum
    c.line(134, 50, 160, 84, chalk)
    c.rect(114, 84, 160, 84, chalk)
    text(c, 118, 64, 'A', chalk2, 1)
    c.rect(100, 94, 104, 95, chalk)
    c.rect(150, 94, 152, 95, p.col('#d07a6a'))
    # wall clock: five to midnight
    sphere(c, 42, 22, 15, 15, metal, amb=.3)
    c.ell(42, 22, 12, 12, paper[3])
    for a in range(12):
        an = a / 12 * 6.283
        c.put(42 + math.cos(an) * 10, 22 + math.sin(an) * 10, paper[0])
    c.line(42, 22, 41, 13, O)
    c.line(42, 22, 40, 15, O)
    c.line(42, 22, 42, 12, red[2])
    # front: the teacher's desk, homework, an apple
    slab(f, 148, 106, W + 2, 114, wood)
    slab(f, 152, 114, W + 2, H + 2, wood[:1] + wood[1:4])
    slab(f, 160, 120, 230, H + 2, wood[:1] + wood[1:4])
    slab(f, 172, 101, 216, 106, paper)                                # open exercise book
    for y in (102, 104):
        f.rect(174, y, 214, y, p.col('#8a9ab8'))
    f.rect(194, 101, 194, 105, paper[0])
    text(f, 204, 101, '2', red[2], 1)
    f.rect(220, 104, 238, 105, red[1])                                # red pen
    f.rect(236, 104, 238, 105, red[3])
    for i, col in enumerate((red, p.ramp('#1e2c4a', '#2c4070', '#40589a', '#5a74b4'), p.ramp('#2a3a1e', '#3e5630', '#567444', '#6e9058'))):
        slab(f, 268 + i % 2 * 3, 99 - i * 5, 304 - i * 2, 104 - i * 5 + 2, col)   # a stack of notebooks
    sphere(f, 252, 101, 5, 5, red, amb=.3)                            # the apple
    f.rect(252, 94, 253, 96, wood[1])
    finish(p, c, f, 'school', 'school, the classroom at night')


# ------------------------------------------------------------------------------------------ the studio
def studio():
    p, O, c, f = new()
    wall = p.ramp('#4a3e34', '#5e5040', '#726250', '#887660')
    wood = p.ramp('#2e2019', '#46301f', '#5c3f29', '#734f33', '#8a6040')
    paper = p.ramp('#8c8676', '#b0a894', '#d0c8b2', '#e8e0cc')
    plaster = p.ramp('#6e6a64', '#9a958c', '#c2bcb0', '#e2dcd0')
    char = p.col('#3c3a3a')
    blue = p.ramp('#24345a', '#304a7a', '#3e6098', '#5a7cb0')
    sun = p.ramp('#a04a20', '#d0702c', '#ec9a40', '#f6c060')
    paints = [p.ramp('#5a1e1e', '#8a2e2a', '#b4443a', '#d0644e'), p.ramp('#24345a', '#3e6098', '#5a7cb0', '#7a9ccc'),
              p.ramp('#6a5a18', '#a88c28', '#d8b440', '#ecd070'), p.ramp('#24401e', '#3e6a30', '#5a8c44', '#78aa5e'),
              p.ramp('#5a2a50', '#86407a', '#a8609c', '#c482b8')]
    c.rect(0, 0, W - 1, H - 1, wall[2])
    texture(c, wall, .04, 4)
    rnd = random.Random(11)
    for _ in range(26):                                               # old paint splashes on the wall
        r = rnd.choice(paints)
        x, y = rnd.randint(4, 308), rnd.randint(4, 148)
        c.ell(x, y, rnd.uniform(1.5, 3.5), rnd.uniform(1.2, 2.5), r[1])
    slab(c, -2, 28, 92, 33, wood)                                     # shelf over Mira: a plaster head, jars
    sphere(c, 70, 16, 8, 10, plaster, amb=.35)
    slab(c, 62, 24, 78, 28, plaster)
    for i, jx in enumerate((14, 30, 46)):
        slab(c, jx - 5, 16, jx + 5, 28, paints[i])
    # the easel with the painting she never finished
    thick(c, 142, 26, 120, 151, wood[1], 3)
    thick(c, 144, 26, 166, 151, wood[1], 3)
    thick(c, 143, 22, 143, 151, wood[2], 2)
    slab(c, 112, 92, 174, 96, wood)
    c.rect(116, 38, 170, 90, paper[3])
    grad(c, 117, 39, 152, 89, blue[::-1] + blue)                      # painted part
    sphere(c, 136, 70, 11, 11, sun, amb=.5)
    c.rect(117, 76, 152, 89, p.col('#2e4a3a'))
    for y in range(39, 90, 3):                                        # the rest: just pencil lines
        c.rect(154, y, 154 + (y * 7) % 13, y, paper[1])
    c.line(156, 80, 168, 60, paper[0])
    box(c, 115, 37, 171, 91, wood[0])
    # pinned drawings
    for x0, y0, x1, y1 in ((182, 6, 214, 30), (250, 4, 286, 30), (100, 4, 126, 24)):
        slab(c, x0, y0, x1, y1, paper)
        c.rect((x0 + x1) // 2, y0 + 1, (x0 + x1) // 2 + 1, y0 + 2, paints[0][2])
    c.cleanup(keep='.' + O)
    c.ell(198, 18, 7, 7, char)
    c.ell(198, 18, 5.5, 5.5, paper[2])
    c.rect(194, 16, 195, 17, char)
    c.rect(200, 16, 201, 17, char)
    c.line(195, 21, 201, 21, char)
    c.line(256, 26, 268, 12, char)
    c.line(268, 12, 280, 26, char)
    c.rect(258, 26, 278, 26, char)
    c.line(104, 20, 112, 10, char)
    c.line(112, 10, 120, 18, char)
    # front: the work table, a palette, brushes in a jar
    slab(f, 108, 106, W + 2, 114, wood)
    slab(f, 112, 114, W + 2, H + 2, wood[:1] + wood[1:4])
    for _ in range(12):
        r = rnd.choice(paints)
        f.ell(rnd.randint(118, 306), rnd.randint(118, 148), rnd.uniform(2, 4), 1.6, r[1])
    pal = p.ramp('#5a4228', '#86643a', '#a8824e', '#c4a066')
    sphere(f, 196, 106, 22, 6, pal, amb=.5)
    f.ell(186, 104, 3, 2, '.')
    for i, (dx, dy) in enumerate(((-12, 2), (-4, 4), (4, 3), (12, 2), (16, 6))):
        f.ell(196 + dx, 106 + dy, 2.5, 1.5, paints[i][2])
    jar = p.ramp('#4a5a5e', '#6a8086', '#8aa2a6', '#b0c4c4')
    for i, (bx, top) in enumerate(((296, 72), (300, 66), (304, 76))):
        f.rect(bx, top + 4, bx + 1, 96, wood[3 if i % 2 else 2])
        f.rect(bx, top, bx + 1, top + 4, paints[i][1])
    slab(f, 292, 88, 310, 108, jar)
    for tx, r in ((248, paints[1]), (262, paints[2])):                 # paint tubes
        slab(f, tx, 103, tx + 11, 107, r)
        f.rect(tx + 12, 104, tx + 13, 106, p.col('#c6ccd0'))
    finish(p, c, f, 'studio', 'the art studio, the abandoned easel')


# ------------------------------------------------------------------------------------------ the sea
def sea():
    p, O, c, f = new()
    sky = p.ramp('#0e1428', '#141c34', '#1a2440', '#222e4e', '#2c3a5c')
    sea_ = p.ramp('#0c1626', '#122034', '#182a42', '#203650', '#2c4662')
    moon = p.ramp('#8a96b0', '#b4bed0', '#d8dee8', '#f2f4f8')
    path1, path2 = p.col('#7a90b8'), p.col('#c4d0e6')
    land = p.col('#10182a')
    st, st2 = p.col('#e6ecf6'), p.col('#8c9cc0')
    HZ = 72
    grad(c, 0, 0, W - 1, HZ, sky)
    halo(c, 150, 26, 11, 26, sky)
    sphere(c, 150, 26, 11, 11, moon, amb=.5)
    c.ell(146, 23, 2.4, 2, moon[1])
    c.ell(154, 30, 2, 1.6, moon[1])
    for x in range(0, 86):                                             # a far island behind Mira
        h = 6 + 4 * math.sin(x / 13) + 3 * math.sin(x / 5)
        c.rect(x, int(HZ - h), x, HZ, land)
    c.rect(0, HZ + 1, W - 1, H - 1, sea_[2])
    for y in range(HZ + 1, H):                                        # waves get bigger toward us
        d = (y - HZ) / (H - HZ)
        if y % (2 + int(d * 6)) == 0:
            per, ln = 9 + int(d * 26), 2 + int(d * 12)
            off = (y * 7) % per
            for x in range(W):
                if (x + off) % per < ln:
                    c.put(x, y, sea_[3])
                    c.put(x, y + 1, sea_[1])
    c.rect(0, HZ + 1, W - 1, HZ + 1, sea_[4])
    for y in range(HZ + 2, H):                                        # the moon path
        d = (y - HZ) / (H - HZ)
        hw = 6 + d * 46
        if y % 2 == 0:
            for x in range(int(150 - hw), int(150 + hw) + 1):
                if (x * 5 + y * 3) % (4 + int(d * 6)) < 2 + int(d * 4) and abs(x - 150) < hw * (.6 + .4 * math.sin(y * 1.7 + x * .2) ** 2):
                    c.put(x, y, path2 if abs(x - 150) < hw * .45 else path1)
    # the lighthouse
    tw = p.ramp('#5a5450', '#8a8278', '#b4ac9c', '#d6ceba')
    rd = p.ramp('#4a1a1a', '#7a2a26', '#a03c32')
    for y in range(44, HZ + 1):
        w = 3 + (y - 44) * .08
        for x in range(int(292 - w), int(292 + w) + 1):
            r = rd if ((y - 44) // 6) % 2 else tw
            c.put(x, y, r[2] if x < 292 else r[1])
    c.rect(288, 38, 296, 43, p.col('#f2d88a'))
    c.rect(287, 37, 297, 37, O)
    c.rect(289, 35, 295, 36, rd[1])
    c.rect(270, 70, 312, HZ, land)
    c.cleanup(keep='.' + O)
    for x, y, b in ((14, 8, 1), (44, 30, 0), (80, 12, 0), (110, 40, 0), (196, 10, 1), (226, 34, 0), (260, 14, 0),
                    (304, 24, 1), (178, 50, 0), (60, 52, 0)):
        star(c, x, y, st if b else st2, b)
    # front: a sand dune with grass, a shell, a child's bucket
    sand = p.ramp('#4a3e34', '#6a5a46', '#8a785c', '#a69474', '#c0ae8c')
    grass = p.ramp('#24301e', '#3a4a2c', '#56683e')
    for x in range(W):
        top = 104 + 3 * math.sin(x / 23) + 2 * math.sin(x / 9 + 1)
        for y in range(int(top), H):
            t = (y - top)
            f.put(x, y, sand[4] if t < 1 else sand[3] if t < 4 else lvl(sand[1:4], .75 - t / 60, x, y))
    texture(f, sand, .05, 9)
    for gx in (118, 136, 160, 244, 282):
        for k in range(-4, 5, 2):
            top = 104 + 3 * math.sin(gx / 23) + 2 * math.sin(gx / 9 + 1)
            f.line(gx, int(top) + 2, gx + k * 2, int(top) - 8 + abs(k), grass[1 + k % 2])
    sphere(f, 214, 124, 5, 4, p.ramp('#8a6a6a', '#b48c88', '#d6b0a8', '#ecd0c6'), amb=.4)
    bk = p.ramp('#5a1e1e', '#8a2e2a', '#b4443a', '#d0644e')
    slab(f, 294, 96, 308, 110, bk)
    f.line(293, 96, 301, 88, p.col('#c6ccd0'))
    f.line(301, 88, 309, 96, p.col('#c6ccd0'))
    finish(p, c, f, 'sea', 'the sea at night, from the shore')


# ------------------------------------------------------------------------------------------ the attic
def attic():
    p, O, c, f = new()
    wood = p.ramp('#241a14', '#34261c', '#463324', '#58412e', '#6c5238')
    beam = p.ramp('#1e1510', '#2e2118', '#40301f', '#52402a')
    card = p.ramp('#4a3a28', '#685236', '#86704a', '#a08a60')
    glass = p.ramp('#1a2040', '#24305a', '#344678', '#4a5e94')
    for x in range(W):                                                # back wall: vertical planks
        k = x % 15
        ch = wood[3] if k == 0 else wood[1] if k == 14 else wood[2]
        c.rect(x, 0, x, H - 1, ch)
    texture(c, wood, .05, 4)
    rnd = random.Random(2)
    for _ in range(9):
        c.ell(rnd.randint(0, 311), rnd.randint(20, 150), 1.5, 1, wood[1])
    for x in range(W):                                                # the roof slopes in from both sides
        yl = 54 - x * .5
        yr = 60 - (W - 1 - x) * .5
        for y in range(0, int(max(yl, yr))):
            c.put(x, y, beam[1] if (x + y) % 11 else beam[0])
    for k in range(-4, 5):                                            # rafters along the slopes
        c.line(0, 54 + k, 112, k - 2, beam[2] if k < 2 else beam[0])
        c.line(W - 1, 60 + k, 194, k - 7, beam[2] if k < 2 else beam[0])
    c.line(0, 50, 108, -4, beam[3])
    # the round window
    sphere(c, 156, 30, 17, 17, wood, amb=.4)
    c.ell(156, 30, 13, 13, glass[1])
    grad(c, 143, 17, 169, 43, glass)
    for y in range(14, 47):
        for x in range(140, 173):
            if math.hypot(x + .5 - 156, y + .5 - 30) > 13 and c.get(x, y) in glass:
                c.put(x, y, wood[2])
    c.ell(161, 24, 3, 3, p.col('#dfe4f0'))
    c.rect(155, 17, 157, 43, wood[1])
    c.rect(143, 29, 169, 31, wood[1])
    # boxes stacked at the back, between Mira and the guest
    for x0, y0, x1, y1 in ((112, 80, 150, 112), (118, 56, 146, 80), (148, 88, 176, 112)):
        slab(c, x0, y0, x1, y1, card)
        c.rect((x0 + x1) // 2 - 2, y0 + 1, (x0 + x1) // 2 + 2, y1 - 1, card[3])
    c.line(124, 66, 138, 66, p.col('#2a2a30'))
    c.line(124, 68, 134, 68, p.col('#2a2a30'))
    c.cleanup(keep='.' + O)
    # the bare bulb on a wire
    c.rect(230, 0, 230, 22, O)
    slab(c, 227, 22, 233, 26, p.ramp('#3a3e44', '#5a6068', '#7e868e', '#a4acb2'))
    sphere(c, 230, 30, 4.5, 5, p.ramp('#c09a50', '#e8c878', '#f8e8b0', '#fffaea'), amb=.6)
    cw = p.col('#8a8070')                                             # cobweb in the corner
    for a in range(5):
        c.line(312, 62, 312 - 26 * math.cos(a * .35), 62 - 26 * math.sin(a * .35) + 3, cw)
    for r in (8, 16):
        for a in range(4):
            c.line(312 - r * math.cos(a * .35), 62 - r * math.sin(a * .35) + 1,
                   312 - r * math.cos((a + 1) * .35), 62 - r * math.sin((a + 1) * .35) + 1, cw)
    # front: an old trunk, a box with a teddy bear
    lea = p.ramp('#2a1c1c', '#3e2826', '#563632', '#6e4640', '#865a50')
    brass = p.ramp('#5a4628', '#8a6c38', '#b89450', '#d8b86c')
    slab(f, 164, 104, W + 2, 112, lea)                                 # lid
    slab(f, 166, 112, W + 2, H + 2, lea[:1] + lea[1:4])
    for sx in (196, 268):
        slab(f, sx, 104, sx + 8, H + 2, wood)                          # straps
        slab(f, sx - 1, 116, sx + 9, 124, brass)
    slab(f, 164, 104, 172, 112, brass)
    f.rect(226, 116, 236, 124, brass[2])
    box(f, 226, 116, 236, 124, O)
    f.rect(231, 120, 231, 122, O)
    slab(f, 104, 116, 164, H + 2, card)                                 # open box
    f.rect(104, 116, 164, 117, card[3])
    bear = p.ramp('#4a3020', '#6e4a30', '#946642', '#b4845a')
    sphere(f, 134, 104, 10, 9, bear, amb=.3)
    sphere(f, 125, 95, 3.5, 3.5, bear, amb=.3)
    sphere(f, 143, 95, 3.5, 3.5, bear, amb=.3)
    sphere(f, 134, 109, 4, 3, p.ramp('#8a6a4a', '#b49270', '#d0b08a'), amb=.4)
    f.rect(130, 101, 131, 102, O)
    f.rect(137, 101, 138, 102, O)
    f.rect(133, 107, 135, 108, O)
    finish(p, c, f, 'attic', 'the attic, boxes of old things')


# ------------------------------------------------------------------------------------------ the night fair
def fair():
    p, O, c, f = new()
    sky = p.ramp('#120c24', '#181030', '#20163c', '#2a1c48', '#362352')
    steel = p.ramp('#2e2a44', '#443e5e', '#5e5878', '#7e7896')
    bulbs = [p.col('#ffd070'), p.col('#ff7aa8'), p.col('#80d0ff'), p.col('#a8f0a0')]
    tr = p.ramp('#3e1a22', '#5a2630', '#76343a', '#8e4440')
    tc = p.ramp('#5e5446', '#7a6e5a', '#968a70', '#b0a486')
    grad(c, 0, 0, W - 1, H - 1, sky)
    halo(c, 132, 58, 30, 60, sky)
    # the Ferris wheel
    cx, cy, R = 132, 58, 46
    thick(c, cx, cy, 104, 151, steel[1], 3)
    thick(c, cx, cy, 158, 151, steel[1], 3)
    for a in range(12):
        an = a / 12 * 6.283
        c.line(cx, cy, cx + math.cos(an) * R, cy + math.sin(an) * R, steel[2])
    for r in (R, R - 1, R - 2, 22):
        for a in range(360):
            an = a / 180 * math.pi
            c.put(cx + math.cos(an) * r, cy + math.sin(an) * r, steel[3] if r == R else steel[2])
    gcols = [p.ramp('#5a2030', '#8a3446', '#b4505e', '#d0727a'), p.ramp('#1e3a5a', '#2e5a86', '#4a7aa8', '#6e9ac4'),
             p.ramp('#5a4a18', '#8a7428', '#b49a3a', '#d4bc5a')]
    for a in range(12):                                                # gondolas hang straight down
        an = a / 12 * 6.283 + .26
        gx, gy = cx + math.cos(an) * R, cy + math.sin(an) * R
        slab(c, int(gx) - 4, int(gy) + 2, int(gx) + 4, int(gy) + 8, gcols[a % 3])
        c.rect(int(gx), int(gy), int(gx), int(gy) + 2, steel[1])
    sphere(c, cx, cy, 4, 4, steel, amb=.4)
    # the striped tent
    for y in range(14, H):
        for x in range(212, 312):
            if y < 46:
                hw = (y - 14) * 1.7
                if abs(x - 262) > hw:
                    continue
                k = int((x - 262) / max(1, hw) * 5 + 5)
            else:
                k = (x - 212) // 9
            r = tr if k % 2 else tc
            c.put(x, y, r[2] if (x + y) % 23 else r[1])
    c.rect(212, 46, 311, 47, tr[0])
    for x in range(212, 312, 6):
        c.rect(x, 48, x + 2, 50, tr[1])
    c.rect(262, 4, 262, 14, steel[1])
    for k in range(6):
        c.rect(263, 4 + k // 2, 263 + 6 - k, 4 + k // 2, tr[3])
    c.rect(236, 70, 288, H - 1, p.col('#1a1020'))                     # the dark opening
    c.cleanup(keep='.' + O)
    for a in range(24):                                                # lamps on the rim
        an = a / 24 * 6.283
        bx, by = int(cx + math.cos(an) * R), int(cy + math.sin(an) * R)
        c.rect(bx, by, bx + 1, by + 1, bulbs[a % 3])
    for x in range(0, W, 2):                                           # a garland of lights across the top
        y = int(6 + 4 * x / W + 16 * (1 - (2 * x / W - 1) ** 2))
        c.put(x, y, O)
        c.put(x + 1, y, O)
        if x % 14 == 0:
            c.rect(x, y + 1, x + 1, y + 2, bulbs[(x // 14) % 4])
    # front: a booth counter, candy floss, a goldfish in a bag
    slab(f, 156, 104, W + 2, 111, p.ramp('#2e2019', '#46301f', '#5c3f29', '#734f33', '#8a6040'))
    for x in range(158, W):
        r = tr if ((x - 158) // 10) % 2 else tc
        f.rect(x, 111, x, H - 1, r[2] if (x - 158) % 10 else r[1])
    f.rect(156, 111, W - 1, 112, tr[0])
    pink = p.ramp('#8a4a6a', '#b46a8e', '#d890b0', '#f0b8d0')
    f.rect(300, 92, 300, 104, p.col('#e0d8c8'))
    puffs(f, [(300, 84, 9, 8), (294, 80, 5, 5), (306, 80, 5, 5), (300, 77, 6, 5), (300, 90, 7, 4)], pink, amb=.4)
    bag = p.ramp('#5a7488', '#7e9aac', '#a6c0cc', '#cce0e6')
    sphere(f, 182, 98, 7, 7, bag, amb=.6)
    f.rect(181, 88, 183, 91, p.col('#c04040'))
    f.ell(181, 99, 2.5, 1.6, p.col('#f08030'))
    f.put(184, 99, p.col('#f08030'))
    finish(p, c, f, 'fair', 'the night fair')


# ------------------------------------------------------------------------------------------ the night train
def train():
    p, O, c, f = new()
    pan = p.ramp('#2a1c14', '#3e2a1c', '#523824', '#66482e', '#7c5a3a')
    night = p.ramp('#0a1024', '#101830', '#162040', '#1e2a4e', '#28365c')
    trees = p.col('#070b16')
    cur = p.ramp('#3e1a1e', '#5a2428', '#763234', '#8e4240')
    metal = p.ramp('#3a3e44', '#5a6068', '#7e868e', '#a4acb2', '#c6ccd0')
    brass = p.ramp('#5a4628', '#8a6c38', '#b89450', '#d8b86c')
    c.rect(0, 0, W - 1, H - 1, pan[2])
    for x0 in range(-10, W, 46):                                       # wood panelling
        slab(c, x0, 10, x0 + 44, H + 2, pan)
        slab(c, x0 + 5, 16, x0 + 39, H + 2, pan[:1] + pan[1:4])
    for x in range(0, W, 4):                                           # luggage rack
        c.rect(x, 0, x + 1, 6, metal[1])
    c.rect(0, 6, W - 1, 8, metal[3])
    c.rect(0, 9, W - 1, 9, O)
    # the window and the night going by
    wx0, wy0, wx1, wy1 = 104, 16, 300, 100
    grad(c, wx0, wy0, wx1, wy1, night)
    sphere(c, 254, 28, 7, 7, p.ramp('#8a96b0', '#b4bed0', '#d8dee8', '#f2f4f8'), amb=.5)
    rnd = random.Random(8)
    x = wx0
    while x <= wx1:                                                    # a forest running past
        h = rnd.randint(8, 20)
        for k in range(h):
            c.rect(x - (h - k) // 3, 86 - k, x + (h - k) // 3, 86 - k, trees)
        x += rnd.randint(5, 11)
    c.rect(wx0, 80, wx1, wy1, trees)
    for lx, ly in ((128, 90), (132, 90), (210, 92), (262, 89), (266, 89), (284, 94)):
        c.rect(lx, ly, lx + 1, ly, p.col('#f0c060'))                   # windows of a far village
    c.rect(170, 26, 171, wy1, trees)                                  # a telegraph pole and its wires
    c.rect(164, 39, 177, 40, trees)
    for wy in (40, 43):
        for xx in range(wx0, wx1):
            c.put(xx, wy + int(6 * (1 - (2 * (xx - wx0) / (wx1 - wx0) - 1) ** 2)) if xx > 171 else wy, trees)
    for y in range(wy0, wy1, 9):                                        # glass reflection
        c.line(wx0 + 30 + y, y, wx0 + 36 + y, y - 6, night[2])
    slab(c, wx0 - 5, wy0 - 5, wx1 + 5, wy0 - 1, pan)                   # frame
    slab(c, wx0 - 5, wy1 + 1, wx1 + 5, wy1 + 5, pan)
    slab(c, wx0 - 5, wy0 - 1, wx0 - 1, wy1 + 1, pan)
    slab(c, wx1 + 1, wy0 - 1, wx1 + 5, wy1 + 1, pan)
    for x0, d in ((wx0, 1), (wx1, -1)):                                 # curtains, tied back
        for y in range(wy0, wy1 + 1):
            w = 16 - (y - wy0) * .22 if y < 62 else 6 + (y - 62) * .12
            for k in range(int(w)):
                xx = x0 + d * k
                kk = k % 5
                c.put(xx, y, cur[3] if kk == 0 else cur[1] if kk == 4 else cur[2])
        c.rect(min(x0, x0 + d * 8), 60, max(x0, x0 + d * 8), 62, brass[2])
    c.cleanup(keep='.' + O)
    # the sconce lamp
    slab(c, 72, 34, 82, 38, brass)
    sphere(c, 77, 27, 8, 7, p.ramp('#b49a70', '#e0c898', '#f6e6c0', '#fff8e8'), amb=.6)
    # front: the little table, tea in a glass holder, sugar
    cloth = p.ramp('#8c8476', '#b0a896', '#d0c8b4', '#e8e0cc')
    slab(f, 146, 102, W + 2, 110, cloth)
    f.rect(146, 110, W + 2, 124, cloth[2])
    for x in range(146, W, 4):
        f.rect(x, 124, x + 1, 126, cloth[3])
        f.rect(x, 111, x, 123, cloth[1])
    seat = p.ramp('#2a1416', '#3e1c20', '#56282a', '#6e3634')
    f.rect(146, 127, W + 2, H + 2, seat[1])
    for x in range(150, W, 18):
        slab(f, x, 128, x + 16, H + 2, seat)
    tea = p.ramp('#5a2a10', '#8a4a1a', '#b06a2a', '#d08a40')
    slab(f, 290, 80, 304, 100, p.ramp('#8a9aa4', '#b4c4cc', '#d6e2e6', '#eef4f6'))   # glass
    f.rect(292, 84, 302, 98, tea[2])
    f.rect(292, 84, 302, 84, tea[3])
    for y in range(90, 103):                                            # the metal holder
        for x in range(289, 306):
            if y > 92 or (x - 289) % 4 < 2:
                f.put(x, y, metal[3] if x < 297 else metal[2])
    f.rect(306, 88, 309, 89, metal[2])
    f.rect(308, 89, 309, 98, metal[2])
    f.rect(306, 98, 309, 99, metal[2])
    f.line(299, 74, 296, 86, metal[4])
    for sx in (270, 276):
        slab(f, sx, 96, sx + 5, 101, cloth)
    finish(p, c, f, 'train', 'the night train, a compartment')


ALL = {'sky': sky, 'school': school, 'studio': studio, 'sea': sea, 'attic': attic, 'fair': fair, 'train': train}

if __name__ == '__main__':
    names = sys.argv[1:] or list(ALL)
    for n in names:
        ALL[n]()
        png(f'dream_{n}')
        png(f'dream_{n}_fg')
        print('ok', n)
