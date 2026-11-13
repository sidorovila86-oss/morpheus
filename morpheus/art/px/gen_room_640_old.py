"""Office background 640x360 in the approved muted style -> room.px.
Top: our booth wall framing a big window onto the hallway (queue side left, dream door right).
Middle: metal counter with document tray slot and speaker grille. Bottom: wooden desk.
No text baked in (door plaque and poster are blank / pictorial)."""
import math
from pxlib import Cv

W, H = 640, 360
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def bayer(x, y, t):
    """True if ordered-dither threshold passes for intensity t in [0,1]."""
    return (BAYER[y % 4][x % 4] + 0.5) / 16 < t


LEG = {
    # our booth wall
    "W": "#3e3546", "V": "#2e222f", "U": "#4b4256",
    # hallway
    "A": "#92a984", "C": "#b2ba90", "c": "#c7dcd0", "B": "#547e64", "b": "#374e4a",
    "F": "#625565", "f": "#3e3546", "G": "#7f708a",
    "L": "#e8f0ea",
    # dream door
    "D": "#484a77", "d": "#323353", "E": "#4d65b4", "P": "#eaaded", "p": "#a884f3",
    "Q": "#ab947a", "q": "#8a7560",
    # poster
    "n": "#323353", "Y": "#ab947a", "y": "#7f708a",
    # metal (frame, counter)
    "1": "#c7dcd0", "2": "#9babb2", "3": "#7f708a", "4": "#625565",
    # desk
    "r": "#4c3e24", "R": "#57472c", "s": "#2e222f", "t": "#694f62",
}
c = Cv(W, H, LEG)

WIN = (14, 12, 625, 158)       # outer window frame box
GL = (20, 18, 619, 152)        # glass area (hallway visible)
FLOOR_Y = 118                  # hallway floor starts
VP = (320, 40)                 # vanishing point for floor tiles

# --- our wall ---------------------------------------------------------------
c.rect(0, 0, W - 1, 175, "W")
for y in range(0, 176):
    for x in range(W):
        if bayer(x, y, 0.18 * (1 - y / 176)):
            c.put(x, y, "U")

# --- hallway (behind glass) -----------------------------------------------------
gx0, gy0, gx1, gy1 = GL
for y in range(gy0, gy1 + 1):
    for x in range(gx0, gx1 + 1):
        if y < gy0 + 6:
            ch = "b"                                       # ceiling edge
        elif y < 84:
            ch = "A"                                       # upper wall paint
        elif y == 84:
            ch = "C"                                       # chair rail
        elif y == 85:
            ch = "b"
        elif y < FLOOR_Y:
            ch = "B"                                       # wainscot
            if (x - gx0) % 40 == 0:
                ch = "b"                                   # panel seams
        elif y == FLOOR_Y:
            ch = "b"                                       # skirting
        else:
            ch = "F"
        c.put(x, y, ch)

# floor tiles in one-point perspective: clean 1px grout lines
prev = None
for y in range(FLOOR_Y + 1, gy1 + 1):
    row = int(520 / (y - VP[1]))
    if prev is not None and row != prev:
        for x in range(gx0, gx1 + 1):
            c.put(x, y, "f")
    prev = row
    for k in range(-40, 41):
        xb = VP[0] + k * 56
        x = round(VP[0] + (xb - VP[0]) * (y - VP[1]) / (gy1 - VP[1]))
        if gx0 <= x <= gx1:
            c.put(x, y, "f")

# fluorescent tube + its light falling on the wall
c.rect(120, gy0 + 6, 520, gy0 + 8, "L")
c.rect(118, gy0 + 9, 522, gy0 + 9, "c")
for y in range(gy0 + 10, 84):
    for x in range(gx0, gx1 + 1):
        dx = max(0, abs(x - 320) - 200) / 120
        t = max(0, 0.55 - (y - gy0 - 10) / 90 - dx)
        if c.get(x, y) == "A" and bayer(x, y, t):
            c.put(x, y, "C")

# poster on the back wall (night sky, moon, stars; no text)
c.rect(150, 34, 196, 80, "V")
c.rect(152, 36, 194, 78, "n")
for y in range(36, 79):
    for x in range(152, 195):
        a = (x - 168) ** 2 + (y - 52) ** 2
        b = (x - 172) ** 2 + (y - 49) ** 2
        if a <= 81 and b > 56:
            c.put(x, y, "Y")
for sx, sy in ((184, 44), (180, 64), (160, 70), (188, 58)):
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
        c.put(sx + dx, sy + dy, "y")
c.rect(152, 72, 194, 78, "y")                      # caption band (blank, text in game if any)

# bench for the queue (left)
c.rect(40, 100, 132, 104, "q")
c.rect(40, 100, 132, 100, "Q")
for lx in (46, 126):
    c.rect(lx, 105, lx + 3, 117, "V")

# dream door (right)
DX0, DY0, DX1, DY1 = 500, 46, 568, FLOOR_Y
c.rect(DX0 - 5, DY0 - 5, DX1 + 5, DY1, "b")        # frame
c.rect(DX0 - 2, DY0 - 2, DX1 + 2, DY1, "P")        # light leak around the door
c.bevel(DX0, DY0, DX1, DY1, "E", "D", "d")
for py in (54, 84):                                 # two raised panels
    c.bevel(DX0 + 8, py, DX1 - 8, py + 24, "d", "D", "E", dither=False)
c.ell(DX1 - 9, 88, 2.5, 2.5, "2")                   # knob
c.put(DX1 - 10, 87, "1")
c.bevel(DX0 + 6, 30, DX1 - 6, 38, "Q", "q", "V", dither=False)   # blank plaque
# glow from under/around the door onto floor and wall
for y in range(gy0 + 6, gy1 + 1):
    for x in range(430, gx1 + 1):
        if DX0 - 5 <= x <= DX1 + 5 and y <= DY1:
            continue
        d = math.hypot((x - 534) / 1.8, (y - DY1) * 1.3)
        t = 0.5 if d < 26 else (0.25 if d < 44 else 0)
        if t > 0 and bayer(x, y, t):
            ch = c.get(x, y)
            c.put(x, y, {"F": "G", "f": "F", "B": "p", "A": "p", "C": "P", "b": "B"}.get(ch, ch))

# --- window frame (metal) --------------------------------------------------------
wx0, wy0, wx1, wy1 = WIN
for y in range(wy0, wy1 + 1):
    for x in range(wx0, wx1 + 1):
        inside = gx0 <= x <= gx1 and gy0 <= y <= gy1
        if not inside:
            top_left = (y - wy0) < (x - wx0) if y < gy0 else False
            if y < gy0:
                ch = "1" if y == wy0 else "2"
            elif x < gx0:
                ch = "1" if x == wx0 else "2"
            elif x > gx1:
                ch = "4" if x == wx1 else "3"
            else:
                ch = "4" if y == wy1 else "3"
            c.put(x, y, ch)
for x in range(gx0, gx1 + 1):                       # inner shadow on glass top
    c.put(x, gy0, "V")
for y in range(gy0, gy1 + 1):
    c.put(gx0, y, "V")

# --- counter / sill ----------------------------------------------------------------
c.bevel(0, 158, W - 1, 176, "1", "2", "3")
for x in range(W):
    c.put(x, 177, "4")
    c.put(x, 178, "V")
# document tray slot (centre)
c.rect(250, 163, 390, 172, "V")
c.rect(252, 165, 388, 172, "s")
for x in range(252, 389):
    c.put(x, 165, "4" if x % 2 else "s")
# speaker grille (left)
for i in range(6):
    c.rect(36 + i * 9, 163, 41 + i * 9, 164, "4")
    c.rect(36 + i * 9, 165, 41 + i * 9, 165, "1")

# --- desk -----------------------------------------------------------------------
for y in range(179, H):
    for x in range(W):
        ch = "r"
        if (y - 179) % 30 == 0:
            ch = "s"                                         # plank joints
        elif (y - 179) % 30 == 1:
            ch = "t" if x % 2 == 0 else "r"
        c.put(x, y, ch)
import random
rnd = random.Random(11)
for _ in range(260):                                          # wood grain: short streaks
    gx, gy, ln = rnd.randrange(0, W - 12), rnd.randrange(183, H - 1), rnd.randrange(4, 12)
    for x in range(gx, gx + ln):
        if c.get(x, gy) == "r":
            c.put(x, gy, "R")
for y in range(179, 186):                                    # front edge lit by window
    for x in range(W):
        if c.get(x, y) == "r" and bayer(x, y, 0.5 - (y - 179) / 14):
            c.put(x, y, "t")
c.cleanup(keep=".fGpPCR")   # keep thin grout lines, glow dither, tube light, grain
c.save("room.px", "Office background 640x360: booth wall, window onto hallway with dream door, counter, desk")
