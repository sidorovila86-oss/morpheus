"""Convert a character-grid sprite (.px) into pixel-art-studio JSON.

.px format:
    # comment
    @palette resurrect-64
    O #2e222f          <- legend: one char, one hex color
    L #eaaded
    ---                <- separator
    ..OOOO..           <- grid rows; '.' = transparent
Usage: python grid2json.py sprite.px out.json
"""
import json
import sys


def convert(src):
    legend, rows, palette, in_grid = {}, [], None, False
    for raw in open(src, encoding="utf-8").read().splitlines():
        if not in_grid:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line == "---":
                in_grid = True
            elif line.startswith("@palette"):
                palette = line.split()[1]
            else:
                ch, col = line.split()
                legend[ch] = col
        elif raw.strip():
            rows.append(raw.rstrip())
    w = max(len(r) for r in rows)
    pixels = []
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == ".":
                continue
            if ch not in legend:
                raise SystemExit(f"{src}: unknown char {ch!r} at {x},{y}")
            pixels.append({"x": x, "y": y, "color": legend[ch]})
    out = {"width": w, "height": len(rows), "background": "transparent", "pixel_size": 1, "pixels": pixels}
    if palette:
        out["palette_ref"] = palette
    return out


if __name__ == "__main__":
    json.dump(convert(sys.argv[1]), open(sys.argv[2], "w"), indent=0)
