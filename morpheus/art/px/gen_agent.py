"""Agent Doze: a dream-infiltration spy who tries to get into Mira's dream every night.
  agent   - Monday: himself. Black suit, sunglasses, earpiece. Calls himself her cousin.
  agent2  - Tuesday: a Captain Comet costume over the suit. Sunglasses and earpiece still on.
  agent3  - Wednesday: Mom. Almost perfect: only the earpiece wire and a five-o'clock shadow give him away.
  (Thursday and Friday he is a perfect copy: the game reuses the real sprite, only questions catch him.)
Run: python gen_agent.py   (writes v_agent.px, then out/v_agent*.png)"""
import os
import subprocess
import sys

from PIL import Image

import gen_visitors as gv
from pxlib import sphere, strands, texture, lvl

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
RENDER = os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'pixel-art-studio', 'scripts', 'render.py')

WIRE = ((214, 222, 232), (150, 160, 176))      # clear coiled earpiece wire: light / shade
GLASS = ((10, 10, 16), (26, 26, 38), (44, 44, 62))


def agent():
    p = gv.new()
    skin = p.ramp("#5e3a30", "#8a5a4a", "#b27860", "#d29a7c", "#ebbfa2")
    hair = p.ramp("#0e0c10", "#1a161c", "#2a242c", "#3c3440", "#524858")
    suit = p.ramp("#08080c", "#121218", "#1c1c24", "#2a2a34", "#3a3a46")
    shirt = p.ramp("#9aa0a4", "#c4cace", "#e0e4e6", "#f6f8f8")
    tie = p.ramp("#040406", "#0c0c10", "#16161c")
    c = gv.mk(p)
    sphere(c, 32, 86, 31, 25, suit)                          # suit shoulders
    texture(c, suit, 0.03, 31)
    for y in range(57, 76):                                    # shirt V
        hw = (y - 57) * 0.36 + 3.5
        for x in range(int(32 - hw), int(32 + hw) + 1):
            c.put(x, y, lvl(shirt, 0.9 - abs(x - 32) / 16, x, y))
    for y in range(57, 76):                                    # sharp lapels
        hw = (y - 57) * 0.36 + 3.5
        c.line(32 - hw - 1, y, 32 - hw + 1, y, suit[4])
        c.line(32 + hw - 1, y, 32 + hw + 1, y, suit[2])
    for y in range(59, 76):                                    # thin black tie
        hw = 1 if y < 62 else 1.5
        for x in range(int(32 - hw), int(32 + hw) + 1):
            c.put(x, y, tie[2] if x < 32 else tie[1])
    c.rect(31, 61, 33, 61, tie[0])
    gv.person(p, c, skin, rx=11.5, ry=13.5)
    sphere(c, 32, 47, 10, 5.5, skin, only=skin)                 # square jaw
    sphere(c, 32, 26, 13, 6.5, hair, only=skin + ".")           # short slicked hair
    sphere(c, 21, 31, 2.4, 4, hair)
    sphere(c, 43, 31, 2.4, 4, hair)
    for x in range(22, 43, 3):
        c.line(x, 21, x + 3, 26, hair[3], only=hair)
    gv.features(c, p, skin, iris="#3a3a44", brow="#1a161c", mood="open", mouth="flat", blush=False)
    sh = [p.col('#%02x%02x%02x' % g) for g in GLASS]
    for ex in (22, 34):                                         # black sunglasses
        for y in range(33, 38):
            for x in range(ex, ex + 8):
                c.put(x, y, sh[2] if y == 33 or (x - ex == 1 and y == 34) else sh[1])
    c.rect(30, 34, 33, 34, sh[0])
    c.rect(20, 34, 21, 34, sh[0])
    c.rect(42, 34, 43, 34, sh[0])
    for i in range(4):                                          # shirt collar points
        c.rect(28 - i, 56 + i, 30, 56 + i, shirt[3] if i < 3 else shirt[1])
        c.rect(34, 56 + i, 36 + i, 56 + i, shirt[2] if i < 3 else shirt[1])
    w0, w1 = p.col('#%02x%02x%02x' % WIRE[0]), p.col('#%02x%02x%02x' % WIRE[1])
    c.rect(44, 37, 45, 38, w0)                                  # earpiece in the right ear
    for i, y in enumerate(range(39, 58)):                       # coiled wire down into the collar
        x = 45 + (1 if (y // 2) % 2 else 0)
        c.put(x, y, w0 if i % 2 else w1)
    gv.finish(c, "agent", "Agent Doze, dream infiltration (original)")


def png(name):
    subprocess.run([sys.executable, os.path.join(HERE, 'grid2json.py'), os.path.join(HERE, f'v_{name}.px'),
                    os.path.join(OUT, f'v_{name}.json')], check=True)
    subprocess.run([sys.executable, RENDER, os.path.join(OUT, f'v_{name}.json'), '-o', os.path.join(OUT, f'v_{name}.png'),
                    '-p', '1', '--no-grid-lines'], check=True, stdout=subprocess.DEVNULL)


def wire(px, top, bottom, x0):
    for i, y in enumerate(range(top, bottom)):
        x = x0 + (1 if (y // 2) % 2 else 0)
        px[x, y] = WIRE[0 if i % 2 else 1] + (255,)
        px[x + 1, y] = (49, 54, 56, 255) if i % 3 == 0 else px[x + 1, y]   # a hint of outline so it reads on light cloth


def disguise_comet():
    """Comet costume over the agent: sunglasses over the hero's eyes, earpiece, black tie and white collar at the neck."""
    im = Image.open(os.path.join(OUT, 'v_comet.png')).convert('RGBA')
    px = im.load()
    for ex in (22, 34):
        for y in range(35, 39):
            for x in range(ex, ex + 8):
                px[x, y] = GLASS[2] + (255,) if y == 35 else GLASS[1] + (255,)
    for x in list(range(30, 34)) + [20, 21, 42, 43]:
        px[x, 36] = GLASS[0] + (255,)
    for y in range(53, 61):                                     # white shirt collar and a thin black tie under the costume
        hw = 1 + (y - 53) * 0.5
        for x in range(int(32 - hw) - 1, int(32 + hw) + 2):
            if px[x, y][3]:
                edge = x in (int(32 - hw) - 1, int(32 + hw) + 1)
                px[x, y] = (49, 54, 56, 255) if edge else (14, 14, 20, 255) if x == 32 else (240, 242, 244, 255)
    wire(px, 40, 56, 44)
    im.save(os.path.join(OUT, 'v_agent2.png'))


def disguise_mom():
    """Mom, almost perfect: earpiece wire down the neck and a faint stubble on the chin."""
    im = Image.open(os.path.join(OUT, 'v_mom.png')).convert('RGBA')
    px = im.load()
    for y in range(47, 52):                                     # stubble: sparse dark dots on skin around the chin
        for x in range(25, 40):
            r, g, b, a = px[x, y]
            if a and r > 150 and g > 100 and r - b > 40 and (x + y) % 2 == 0 and 26 <= x <= 38 and not (28 <= x <= 36 and y <= 47):
                px[x, y] = (round(r * .62), round(g * .6), round(b * .62), 255)
    wire(px, 44, 58, 40)
    im.save(os.path.join(OUT, 'v_agent3.png'))


if __name__ == '__main__':
    agent()
    png('agent')
    disguise_comet()
    disguise_mom()
    print('agent, agent2, agent3 written')
