"""Office background 480x270 (x4 = 1920x1080), muted mid-dark palette -> room.px.
Scale on the hallway back wall: door 90x200cm ~ 30x61px (1px ~ 3cm).
Top: booth wall with a big window onto the hallway (bench + clock left, poster, cooler, dream door right).
Middle: metal counter with document slot and speaker grille. Bottom: wooden desk.
No text baked in."""
import math
import random
from pxlib import Cv

W, H = 480, 270
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def bayer(x, y, t):
    return (BAYER[int(y) % 4][int(x) % 4] + 0.5) / 16 < t


LEG = {
    # booth wall (our side)
    "V": "#26222b", "W": "#302b36", "U": "#38323f",
    # hallway
    "k": "#252c2b",                                   # ceiling
    "A": "#4f5c55", "a": "#5b695f", "Á": "#677566",   # upper wall base / lit / most lit
    "r": "#6c7768", "j": "#323c38",                   # chair rail top / under
    "B": "#3a4741", "b": "#2f3a35", "X": "#45534c",   # wainscot base / seam / panel hi
    "K": "#232a28",                                   # skirting
    "F": "#3f3a46", "f": "#332f3a",                   # floor / grout
    "L": "#c9d3c8", "l": "#8f9a8e",                   # tube / housing
    # door
    "D": "#373d60", "d": "#2b3050", "E": "#454d75", "e": "#20233a",
    "T": "#2a2f3a", "t": "#3d4352",                   # door casing
    "P": "#c7b3e6", "p": "#8e7bb0", "g": "#4f4760", "G": "#6d5f82",   # dream light
    "Q": "#8a7a5c", "q": "#6b5e47",                   # brass plaque
    "1": "#a3aca9", "2": "#7e8886", "3": "#5f6866", "4": "#454c4b",   # metal ramp
    # bench
    "w": "#7a5f48", "v": "#634c3a", "u": "#4a3829", "M": "#2a272e", "N": "#45414b",
    # cooler
    "C": "#7f9aa3", "c": "#617c86", "Ç": "#a5bec4", "h": "#a04a3e", "i": "#3f6f9a",
    # clock + poster
    "Z": "#b4bbae", "z": "#959c90", "n": "#2b2f4a", "m": "#a8936a", "s": "#7a7fa0", "S": "#3e4466",
    # desk
    "R": "#3f3326", "Y": "#4a3d2e", "y": "#2a221b", "H": "#56473a",
    # dream frame: plum wood + gold inlay
    # Morpheus' shop kiosk in the hallway
    "I": "#8a5aa8", "x": "#5a3a78", "J": "#e8dcc0", "o": "#f0b860", "Ö": "#b89ae0", "Ü": "#7ac8a8", "ä": "#e0708a",
    "5": "#57446a", "6": "#3e3050", "7": "#2a2036", "8": "#c9a24a", "9": "#8a6a34", "0": "#f0d890",
}
c = Cv(W, H, LEG)

GX0, GY0, GX1, GY1 = 118, 12, 465, 104      # glass (hallway visible)
RC = 20                                      # rounded top corners of the dream window (the game clips guests the same way)


def in_glass(x, y):
    if not (GX0 <= x <= GX1 and GY0 <= y <= GY1):
        return False
    gx, gy = x - GX0, y - GY0
    if gy < RC:
        for cx in (RC, GX1 - GX0 + 1 - RC):
            if (gx < RC and cx == RC) or (gx >= GX1 - GX0 + 1 - RC and cx != RC):
                return math.hypot(gx + .5 - cx, gy + .5 - RC) <= RC
    return True
CEIL, RAIL, FLOOR = 17, 62, 88              # hallway rows
VPX, VPY = 240, 30

# --- booth wall -----------------------------------------------------------------
c.rect(0, 0, W - 1, 113, "W")
for y in range(0, 114):
    for x in range(W):
        if bayer(x, y, 0.22 * (1 - y / 114)):
            c.put(x, y, "U")

# --- hallway --------------------------------------------------------------------
for y in range(GY0, GY1 + 1):
    for x in range(GX0, GX1 + 1):
        if not in_glass(x, y):
            continue
        if y < CEIL:
            ch = "k"
        elif y < RAIL:
            ch = "A"
        elif y == RAIL:
            ch = "r"
        elif y == RAIL + 1:
            ch = "j"
        elif y < FLOOR - 1:
            ch = "B"
            if (x - GX0) % 34 == 0:
                ch = "b"
            elif (x - GX0) % 34 == 1:
                ch = "X"
        elif y < FLOOR + 1:
            ch = "K"
        else:
            ch = "F"
        c.put(x, y, ch)

# floor tiles in perspective
prev = None
for y in range(FLOOR + 1, GY1 + 1):
    row = int(300 / (y - VPY))
    if prev is not None and row != prev:
        for x in range(GX0, GX1 + 1):
            c.put(x, y, "f")
    prev = row
    for k in range(-30, 31):
        xb = VPX + k * 44
        x = round(VPX + (xb - VPX) * (y - VPY) / (GY1 - VPY))
        if GX0 <= x <= GX1:
            c.put(x, y, "f")

# ceiling tube light and its pool on the wall
c.rect(150, CEIL - 3, 330, CEIL - 1, "l")
c.rect(152, CEIL - 1, 328, CEIL - 1, "l")   # tube is off at night
# pendant lamp above the visitor (light itself is done by the game's lighting layer)
LX = 232
c.rect(LX, GY0, LX, CEIL + 3, "M")                    # cord
for y in range(CEIL + 4, CEIL + 10):                  # conical metal shade
    hw = 2 + (y - CEIL - 4) * 1.4
    for x in range(int(LX - hw), int(LX + hw) + 1):
        u = (x - LX) / max(hw, 1)
        c.put(x, y, "1" if u < -0.4 else ("2" if u < 0.3 else "3"))
c.rect(LX - 9, CEIL + 10, LX + 9, CEIL + 10, "4")     # rim
c.rect(LX - 3, CEIL + 11, LX + 3, CEIL + 11, "L")     # bulb
c.rect(LX - 1, CEIL + 12, LX + 1, CEIL + 12, "L")

# --- clock (left wall) -----------------------------------------------------------
CX, CY, CR = 270.5, 32.5, 8.5
for y in range(int(CY - CR) - 1, int(CY + CR) + 2):
    for x in range(int(CX - CR) - 1, int(CX + CR) + 2):
        d = math.hypot(x + 0.5 - CX, y + 0.5 - CY)
        if d <= CR:
            ch = "M" if d > CR - 1.6 else ("z" if (x + 0.5 - CX) + (y + 0.5 - CY) > 4 else "Z")
            c.put(x, y, ch)
for k in range(12):
    a = k * math.pi / 6
    c.put(CX - 0.5 + 5.6 * math.cos(a), CY - 0.5 + 5.6 * math.sin(a), "M" if k % 3 == 0 else "z")
c.line(CX, CY, CX - 3, CY - 3, "M")          # 10:10-ish
c.line(CX, CY, CX + 4, CY - 2, "M")
c.put(CX, CY, "h")

# --- Morpheus' shop: a little night kiosk on the left (clickable in the game) ---------
KX0, KX1 = 130, 188
for y in range(FLOOR + 1, FLOOR + 5):        # shadow on the floor
    for x in range(KX0, KX1 + 3):
        if bayer(x, y, 0.6 - (y - FLOOR) * 0.12):
            c.put(x, y, "f")
for y in range(36, FLOOR + 1):               # warm light from the kiosk on the wall behind
    for x in range(KX0 - 8, KX1 + 9):
        d = max(KX0 - x, x - KX1, 0) + max(40 - y, 0)
        if 0 < d < 6 and c.get(x, y) in "ABaXb" and bayer(x, y, 0.2 - d * 0.03):
            c.put(x, y, "q")
c.rect(KX0 + 3, 46, KX1 - 3, 69, "n")        # dark inside
c.rect(KX0 + 3, 46, KX1 - 3, 47, "M")
for sy in (56, 66):                          # shelves with little wares
    c.rect(KX0 + 4, sy, KX1 - 4, sy, "u")
    c.rect(KX0 + 4, sy + 1, KX1 - 4, sy + 1, "M")
wares = "oÖÜäoJÜÖäo"
for i, x in enumerate(range(KX0 + 6, KX1 - 6, 5)):
    col = wares[i % len(wares)]
    c.rect(x, 52, x + 2, 55, col)            # jars / lamps on the top shelf
    c.put(x + 1, 51, "J" if col != "J" else "Q")
    col2 = wares[(i + 3) % len(wares)]
    c.rect(x, 62, x + 3, 65, col2)           # cassettes / mugs on the lower shelf
    c.put(x + 1, 63, "M")
for px_ in (KX0 + 2, KX1 - 3):               # posts
    c.rect(px_, 42, px_ + 1, FLOOR, "M")
    c.put(px_, 42, "N")
# striped awning with a scalloped edge
for y in range(38, 46):
    for x in range(KX0 - 2, KX1 + 3):
        if y < 40 and (x < KX0 + (40 - y) - 2 or x > KX1 - (40 - y) + 2):
            continue
        stripe = ((x - KX0) // 5) % 2
        c.put(x, y, ("I" if stripe else "J") if y > 38 else "x")
for x in range(KX0 - 2, KX1 + 3):
    stripe = ((x - KX0) // 5) % 2
    if (x - KX0) % 5 in (1, 2, 3):
        c.put(x, 46, "I" if stripe else "J")
    c.put(x, 45, "x" if stripe else "u")
c.rect(KX0 - 2, 37, KX1 + 2, 37, "M")
# counter in front
c.rect(KX0, 69, KX1, FLOOR, "v")
c.rect(KX0, 69, KX1, 70, "w")
c.rect(KX0, 71, KX1, 71, "u")
c.rect(KX0, FLOOR, KX1, FLOOR, "u")
for x in range(KX0 + 8, KX1 - 6, 14):        # panel seams
    c.rect(x, 73, x, FLOOR - 2, "u")
# sign on top: brass board with a crescent and a coin
c.rect(KX0 + 14, 28, KX1 - 14, 36, "M")
c.rect(KX0 + 15, 29, KX1 - 15, 35, "q")
c.rect(KX0 + 15, 29, KX1 - 15, 29, "Q")
for y in range(30, 35):
    for x in range(KX0 + 20, KX0 + 26):
        a_ = (x + .5 - (KX0 + 23)) ** 2 + (y + .5 - 32) ** 2
        b_ = (x + .5 - (KX0 + 24.3)) ** 2 + (y + .5 - 31.2) ** 2
        if a_ <= 6.5 and b_ > 4:
            c.put(x, y, "o")
for x, y in ((KX0 + 33, 31), (KX0 + 35, 33), (KX0 + 37, 31)):
    c.put(x, y, "o")
    c.put(x + 1, y, "J")
# a lantern hanging from the awning
c.put(KX1 + 1, 46, "M")
c.rect(KX1, 47, KX1 + 2, 50, "o")
c.put(KX1 + 1, 48, "J")
c.rect(KX1, 51, KX1 + 2, 51, "M")

# --- poster (no text) -----------------------------------------------------------
PX0, PY0, PX1, PY1 = 322, 24, 348, 56
c.rect(PX0 - 1, PY0 - 1, PX1 + 1, PY1 + 1, "M")
c.rect(PX0, PY0, PX1, PY1, "n")
for y in range(PY0, PY1 + 1):
    for x in range(PX0, PX1 + 1):
        a = (x - 332) ** 2 + (y - 36) ** 2
        b = (x - 335) ** 2 + (y - 34) ** 2
        if a <= 36 and b > 22:
            c.put(x, y, "m")
for sx, sy in ((341, 30), (340, 43), (326, 45)):
    c.put(sx, sy, "s")
    c.put(sx + 1, sy, "s")
c.rect(PX0, PY1 - 6, PX1, PY1, "S")
c.rect(PX0 + 3, PY1 - 4, PX1 - 3, PY1 - 3, "s")    # blank caption bar
c.rect(PX0, PY1 + 2, PX1 + 2, PY1 + 2, "j")       # shadow

# --- water cooler -----------------------------------------------------------------
WX0, WX1 = 290, 309
WCX = (WX0 + WX1 + 1) / 2
for y in range(38, 56):                              # bottle
    for x in range(WX0 + 2, WX1 - 1):
        u = (x + 0.5 - WCX) / 8
        if y < 41 and abs(u) > 0.75:
            continue
        ch = "C" if u < 0.3 else "c"
        if -0.7 < u < -0.45:
            ch = "Ç"
        if y < 42:
            ch = "Ç" if u < 0 else "C"
        c.put(x, y, ch)
c.rect(WX0 + 7, 56, WX1 - 7, 57, "3")                # neck
c.bevel(WX0, 58, WX1, FLOOR, "1", "2", "3")          # cabinet
c.rect(WX0 + 3, 63, WX1 - 3, 70, "4")                # tap recess
c.rect(WX0 + 5, 64, WX0 + 6, 66, "i")                # cold tap
c.rect(WX1 - 6, 64, WX1 - 5, 66, "h")                # hot tap
c.rect(WX0 + 3, 69, WX1 - 3, 70, "3")                # drip tray
c.rect(WX0 + 2, 74, WX1 - 2, 74, "3")                # door seam
c.rect(WX1 - 4, 78, WX1 - 4, 82, "4")                # door handle
for x in range(WX0, WX1 + 4):
    for y, t in ((FLOOR + 1, 0.6), (FLOOR + 2, 0.3)):
        if bayer(x, y, t):
            c.put(x, y, "f")

# --- dream door (right) ----------------------------------------------------------
DX0, DX1, DY0, DY1 = 398, 427, 28, FLOOR      # slab 30x61
for y in range(FLOOR + 1, GY1 + 1):           # light pool on the floor
    for x in range(GX0, GX1 + 1):
        d = math.hypot((x - 412) / 2.6, (y - FLOOR) * 1.0)
        if d < 7 and bayer(x, y, 0.55):
            c.put(x, y, "G")
        elif d < 13 and bayer(x, y, 0.35):
            c.put(x, y, "g")
for y in range(DY0 - 8, FLOOR):               # faint glow on the wall around the casing
    for x in range(DX0 - 12, DX1 + 13):
        d = max(DX0 - 4 - x, x - DX1 - 4, DY0 - 4 - y, 0)
        if 0 < d < 7 and c.get(x, y) in "ABa" and bayer(x, y, 0.32 - d * 0.045):
            c.put(x, y, "g")
c.rect(DX0 - 4, DY0 - 4, DX1 + 4, DY1, "T")   # casing
c.rect(DX0 - 3, DY0 - 3, DX1 + 3, DY1, "t")
c.rect(DX0 - 3, DY0 - 3, DX1 + 3, DY0 - 3, "2")
c.rect(DX0 - 3, DY0 - 3, DX0 - 3, DY1, "3")
c.rect(DX0 - 1, DY0 - 1, DX1 + 1, DY1, "e")   # gap
c.rect(DX1 + 1, DY0, DX1 + 1, DY1, "p")       # light through the gap (ajar)
c.rect(DX1 + 1, DY0 + 10, DX1 + 1, DY1 - 6, "P")
c.rect(DX0, DY0, DX1, DY1 - 1, "D")           # slab
c.rect(DX0, DY0, DX1, DY0, "E")
c.rect(DX0, DY0, DX0, DY1 - 1, "E")
c.rect(DX1 - 1, DY0 + 1, DX1, DY1 - 1, "d")
OX, OY = (DX0 + DX1 + 1) / 2, DY0 + 12        # porthole with dream light
for y in range(DY0 + 4, DY0 + 21):
    for x in range(DX0 + 4, DX1 - 3):
        dx_, dy_ = x + 0.5 - OX, y + 0.5 - OY
        d = math.hypot(dx_, dy_)
        if d <= 7:
            if d > 5.6:
                ch = "2" if dx_ + dy_ < 0 else "4"
            elif d > 4.8:
                ch = "e"
            else:
                ch = "P" if dx_ + dy_ < -1.5 else "p"
            c.put(x, y, ch)
c.rect(DX0 + 5, DY0 + 26, DX1 - 5, DY1 - 9, "D")   # lower recessed panel
c.rect(DX0 + 5, DY0 + 26, DX1 - 5, DY0 + 26, "d")
c.rect(DX0 + 5, DY0 + 26, DX0 + 5, DY1 - 9, "d")
c.rect(DX1 - 5, DY0 + 27, DX1 - 5, DY1 - 9, "E")
c.rect(DX0 + 6, DY1 - 9, DX1 - 5, DY1 - 9, "E")
c.rect(DX1 - 7, DY0 + 36, DX1 - 3, DY0 + 36, "1")  # lever handle
c.rect(DX1 - 3, DY0 + 35, DX1 - 3, DY0 + 38, "2")
c.rect(DX1 - 7, DY0 + 37, DX1 - 4, DY0 + 37, "3")
c.rect(DX0 + 1, DY1 - 5, DX1 - 1, DY1 - 2, "2")    # kick plate
c.rect(DX0 + 1, DY1 - 5, DX1 - 1, DY1 - 5, "1")
c.rect(DX0 + 1, DY1 - 2, DX1 - 1, DY1 - 2, "3")
c.rect(DX0, DY1 - 1, DX1 + 1, DY1 - 1, "P")        # light under the door
c.rect(DX0 + 4, DY0 - 10, DX1 - 4, DY0 - 6, "q")   # blank brass plaque
c.rect(DX0 + 4, DY0 - 10, DX1 - 4, DY0 - 10, "Q")
c.rect(DX0 + 4, DY0 - 10, DX0 + 4, DY0 - 6, "Q")
c.put(DX0 + 6, DY0 - 8, "u")
c.put(DX1 - 6, DY0 - 8, "u")

# --- window frame -------------------------------------------------------------------
# the window is not a checkpoint: an arched frame of plum wood with gold inlay, a moon keystone,
# and the lower edge melting onto the counter (the border between waking and the dream)
FX0, FY0, FX1, FY1 = 112, 6, 471, 110
def near_glass(x, y, d):
    return any(in_glass(x + dx, y + dy) for dx in range(-d, d + 1) for dy in range(-d, d + 1))
for y in range(FY0, FY1 + 1):
    for x in range(FX0, FX1 + 1):
        if in_glass(x, y):
            continue
        # rounded outer corners too
        ox, oy = x - FX0, y - FY0
        orc = RC + 6
        if oy < orc:
            if ox < orc and math.hypot(ox + .5 - orc, oy + .5 - orc) > orc:
                continue
            if ox > FX1 - FX0 - orc and math.hypot(ox + .5 - (FX1 - FX0 + 1 - orc), oy + .5 - orc) > orc:
                continue
        if near_glass(x, y, 1):
            ch = "8" if (x + y) % 2 == 0 or y > GY1 else "9"      # gold bead along the glass
        elif near_glass(x, y, 2):
            ch = "7"
        elif y <= FY0 + 1 or x <= FX0 + 1:
            ch = "5"
        elif y >= FY1 - 1 or x >= FX1 - 1:
            ch = "7"
        else:
            ch = "6"
        c.put(x, y, ch)
# outer edge highlight on the rounded top
for x in range(FX0, FX1 + 1):
    for y in range(FY0, FY0 + RC + 7):
        if c.get(x, y) in "56" and c.get(x, y - 1) not in "5678":
            c.put(x, y, "5")
            break
# little gold stars along the sides
for y in range(30, 100, 14):
    for x in (FX0 + 3, FX1 - 3):
        c.put(x, y, "8")
        c.put(x, y - 1, "9")
        c.put(x, y + 1, "9")
# moon keystone at the top centre
KX, KY = 412, 6                                # above the dream door
for y in range(KY - 6, KY + 7):
    for x in range(KX - 7, KX + 8):
        d = math.hypot(x + .5 - KX, y + .5 - KY)
        if d <= 6.5:
            c.put(x, y, "7" if d > 5.5 else "6")
for y in range(KY - 5, KY + 6):
    for x in range(KX - 5, KX + 6):
        a = math.hypot(x + .5 - KX, y + .5 - KY)
        b = math.hypot(x + .5 - KX - 2.2, y + .5 - KY + 1.2)
        if a <= 4.2 and b > 3.4:
            c.put(x, y, "0" if x < KX - 1 else "8")
c.rect(FX0, FY1 + 1, FX1, FY1 + 2, "V")

# --- counter ----------------------------------------------------------------------------
c.rect(0, 113, W - 1, 120, "2")
c.rect(0, 113, W - 1, 113, "1")
c.rect(0, 121, W - 1, 124, "3")
c.rect(0, 125, W - 1, 125, "4")
c.rect(0, 126, W - 1, 126, "V")
c.rect(180, 115, 300, 119, "V")                      # document slot
c.rect(181, 116, 299, 119, "e")
c.rect(180, 120, 300, 120, "1")
for i in range(5):                                   # speaker grille
    c.rect(24 + i * 7, 115, 27 + i * 7, 116, "4")
    c.rect(24 + i * 7, 117, 27 + i * 7, 117, "1")

# melting drips of the frame over the counter (drawn after the counter)
for dx, ln in ((131, 5), (150, 9), (165, 4), (312, 7), (338, 11), (361, 5), (433, 8), (452, 4)):
    for y in range(FY1 - 1, FY1 + 3 + ln):
        w = 2 if y < FY1 + ln else 1
        if y == FY1 + 2 + ln:
            w = 0
        for x in range(dx - w, dx + w + 1):
            ch = "5" if x == dx - w else ("7" if x == dx + w else "6")
            c.put(x, y, ch)
    c.put(dx, FY1 + 2 + ln, "8")                     # a gold drop at the tip
    c.put(dx - 1, FY1 + 3 + ln, "V")

# --- desk -------------------------------------------------------------------------------
for y in range(127, H):
    for x in range(W):
        c.put(x, y, "y" if (y - 127) % 36 == 35 else "R")
rnd = random.Random(11)
for _ in range(220):
    gx, gy, ln = rnd.randrange(0, W - 12), rnd.randrange(130, H - 1), rnd.randrange(4, 12)
    for x in range(gx, gx + ln):
        if c.get(x, gy) == "R":
            c.put(x, gy, "Y")
c.rect(0, 127, W - 1, 127, "H")                     # front edge lit by window

c.cleanup(keep=".fGgPpÁaYHjz890oJÖÜäIxq")
c.save("room.px", "Office background 480x270: booth wall, window onto hallway with dream door, counter, desk")
