# Builds pixfix-400.ttf / pixfix-600.ttf: replacement glyphs for the
# Pixelify Sans characters that read badly (2 5 7, Ш Щ Д К в д ш щ; О П are missing from Pixelify entirely;
# lowercase е ё ъ ы ь э ю looked like capitals; capital Е Ё looked like a mirrored Э).
# Same pixel grid as Pixelify: 1 module = 0.09386 em, cap height = 7 modules.
# Used via @font-face unicode-range in front of Pixelify Sans.
import os
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

M = 93.86         # Pixelify module in font units (cap 657 = 7 modules)
B = -16           # bottom of the lowest cap row (Pixelify sits slightly below baseline)
LSB = 47          # 0.5 module left bearing, like Pixelify

G = {  # char: (rows top->bottom, top row index, advance400, advance600)
 '2': (['.###.',
        '#...#',
        '....#',
        '...#.',
        '..#..',
        '.#...',
        '#####'], 0, 586, 597),
 '5': (['#####',
        '#....',
        '####.',
        '....#',
        '....#',
        '#...#',
        '.###.'], 0, 586, 597),
 '7': (['#####',
        '....#',
        '...#.',
        '..#..',
        '..#..',
        '..#..',
        '..#..'], 0, 586, 597),
 'Ш': (['#..#..#',
        '#..#..#',
        '#..#..#',
        '#..#..#',
        '#..#..#',
        '#..#..#',
        '#######'], 0, 767, 775),
 'Щ': (['#..#..#.',
        '#..#..#.',
        '#..#..#.',
        '#..#..#.',
        '#..#..#.',
        '#..#..#.',
        '########',
        '.......#'], 0, 767, 774),
 'Д': (['.####.',
        '.#..#.',
        '.#..#.',
        '.#..#.',
        '.#..#.',
        '######',
        '#....#'], 0, 676, 686),
 'К': (['#...#',
        '#..#.',
        '#.#..',
        '##...',
        '#.#..',
        '#..#.',
        '#...#'], 0, 586, 597),
 'в': (['####.',
        '#...#',
        '####.',
        '#...#',
        '####.'], 2, 586, 597),
 'д': (['.###.',
        '.#.#.',
        '.#.#.',
        '.#.#.',
        '#####',
        '#...#'], 2, 676, 686),
 'О': (['.###.',
        '#...#',
        '#...#',
        '#...#',
        '#...#',
        '#...#',
        '.###.'], 0, 586, 597),
 'П': (['#####',
        '#...#',
        '#...#',
        '#...#',
        '#...#',
        '#...#',
        '#...#'], 0, 586, 597),
 'ш': (['#..#..#',
        '#..#..#',
        '#..#..#',
        '#..#..#',
        '#######'], 2, 767, 775),
 'щ': (['#..#..#.',
        '#..#..#.',
        '#..#..#.',
        '#..#..#.',
        '########',
        '.......#'], 2, 767, 774),
 'е': (['.###.',
        '#...#',
        '#####',
        '#....',
        '.####'], 2, 586, 597),
 'ё': (['.#.#.',
        '.....',
        '.###.',
        '#...#',
        '#####',
        '#....',
        '.####'], 0, 586, 597),
 'ь': (['#....',
        '#....',
        '####.',
        '#...#',
        '####.'], 2, 586, 597),
 'ъ': (['##....',
        '.#....',
        '.####.',
        '.#...#',
        '.####.'], 2, 676, 686),
 'ы': (['#....#',
        '#....#',
        '###..#',
        '#..#.#',
        '###..#'], 2, 676, 686),
 'э': (['.###.',
        '#...#',
        '..###',
        '#...#',
        '.###.'], 2, 586, 597),
 'ю': (['#..##.',
        '#.#..#',
        '###..#',
        '#.#..#',
        '#..##.'], 2, 676, 686),
 'Е': (['#####',
        '#....',
        '#....',
        '####.',
        '#....',
        '#....',
        '#####'], 0, 586, 597),
 'Ё': (['.#.#.',
        '.....',
        '#####',
        '#....',
        '#....',
        '####.',
        '#....',
        '#....',
        '#####'], -2, 586, 597),
}


def glyph(rows, top, bold):
    pen = TTGlyphPen(None)
    for r, row in enumerate(rows):
        y0 = B + (6 - (top + r)) * M
        y1 = y0 + M
        x = 0
        while x < len(row):
            if row[x] == '#':
                e = x
                while e < len(row) and row[e] == '#':
                    e += 1
                # bold: every run gets 0.7 module wider (Pixelify bold stems ~1.7)
                xa = LSB + x * M
                xb = LSB + e * M + (0.7 * M if bold else 0)
                pts = [(xa, y0), (xa, y1), (xb, y1), (xb, y0)]
                pen.moveTo((round(pts[0][0]), round(pts[0][1])))
                for p in pts[1:]:
                    pen.lineTo((round(p[0]), round(p[1])))
                pen.closePath()
                x = e
            else:
                x += 1
    return pen.glyph()


def build(weight):
    bold = weight == 600
    names = ['.notdef'] + ['g%04X' % ord(c) for c in G]
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap({ord(c): 'g%04X' % ord(c) for c in G})
    glyphs = {'.notdef': TTGlyphPen(None).glyph()}
    metrics = {'.notdef': (500, 0)}
    for c, (rows, top, a4, a6) in G.items():
        n = 'g%04X' % ord(c)
        glyphs[n] = glyph(rows, top, bold)
        metrics[n] = (a6 if bold else a4, LSB)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-300)
    fb.setupNameTable({'familyName': 'PixFix', 'styleName': 'Bold' if bold else 'Regular'})
    fb.setupOS2(sTypoAscender=900, sTypoDescender=-300, usWinAscent=900, usWinDescent=300,
                usWeightClass=weight)
    fb.setupPost()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pixfix-%d.ttf' % weight)
    fb.save(out)
    print('wrote', out)


build(400)
build(600)
