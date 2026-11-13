"""Contact sheet of all sprites on a dark desk, nearest-neighbour upscaled."""
import sys
from PIL import Image

names = sys.argv[2:]
scale = 4
imgs = [Image.open(f"out/{n}.png").convert("RGBA") for n in names]
pad = 8
W = 330
rows, x, y, rh = [], pad, pad, 0
pos = []
for im in imgs:
    if x + im.width + pad > W:
        x, y, rh = pad, y + rh + pad, 0
    pos.append((x, y))
    x += im.width + pad
    rh = max(rh, im.height)
H = y + rh + pad
bg = Image.new("RGBA", (W, H), "#4c3e24")
for yy in range(0, H, 12):
    for xx in range(W):
        bg.putpixel((xx, yy), (46, 34, 47, 255))
for im, (px, py) in zip(imgs, pos):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    a = im.split()[3].point(lambda v: 110 if v else 0)
    sh.putalpha(a)
    bg.alpha_composite(Image.new("RGBA", im.size, (46, 34, 47, 0)), (px, py))
    blk = Image.new("RGBA", im.size, (30, 20, 28, 255))
    blk.putalpha(a)
    bg.alpha_composite(blk, (px + 2, py + 2))
    bg.alpha_composite(im, (px, py))
bg.resize((W * scale, H * scale), Image.NEAREST).save(sys.argv[1])
