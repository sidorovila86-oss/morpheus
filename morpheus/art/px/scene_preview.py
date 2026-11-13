"""Preview: 480x270 room with desk items at game scale, roughly as laid out in the game."""
from PIL import Image

room = Image.open("out/room.png").convert("RGBA")
place = [  # name, x, y
    ("sheet", 10, 134), ("imprint_admit", 32, 222), ("idcard", 122, 144), ("sticky", 128, 204),
    ("notebook", 210, 136), ("lens", 58, 196),
    ("stamp_admit", 298, 132), ("stamp_deny", 346, 132), ("mug", 396, 182),
]
for n, x, y in place:
    im = Image.open(f"out/{n}.png").convert("RGBA")
    a = im.split()[3].point(lambda v: 120 if v else 0)
    sh = Image.new("RGBA", im.size, (24, 18, 22, 255))
    sh.putalpha(a)
    if not n.startswith("imprint"):
        room.alpha_composite(sh, (x + 3, y + 3))
    room.alpha_composite(im, (x, y))
room.save("out/scene.png")
room.resize((1440, 810), Image.NEAREST).save("out/scene_x3.png")
