from shapely.geometry import Point, LineString
from shapely.ops import unary_union

import cairo
import math
import random

import sys
import os
sys.path.append(os.path.abspath('..'))
from lib import palettes

# Final image dimensions
IMG_HEIGHT = 2160
IMG_WIDTH = 3840


def reed(ctx, width, height, color=palettes.BRIGHT_GREEN, vary_colors=True):
    x_min_increment = width // 100
    x_max_increment = 4 * x_min_increment
    y_min_increment = height // 12
    y_max_increment= 5 * y_min_increment

    # Draw curve
    x1 = random.randint(0, width)
    y1 = height
    lean_to_side = -1 if random.random() < 0.5 else 1
    x2 = snap_to_edges(x1 + lean_to_side * random.randint(x_min_increment, x_max_increment), width)
    y2 = height - random.randint(y_min_increment, y_max_increment)
    x3 = snap_to_edges(x1 - 1 * lean_to_side * random.randint(x_min_increment, x_max_increment), width)
    y3 = y2 - random.randint(y_min_increment, y_max_increment)
    ctx.curve_to(x1, y1, x2, y2, x3, y3)
    line_width = random.randint(8, x_min_increment)
    ctx.set_line_width(line_width)
    current_color = color_variant(color) if vary_colors else palettes.hex_to_tuple(color)
    ctx.set_source_rgb(*current_color)
    ctx.stroke()

    # Ball
    ctx.arc(x3, y3, random.randint(line_width + 2, 2 * x_min_increment), 0, 2 * math.pi)
    ctx.set_source_rgb(*current_color)
    ctx.fill()

def snap_to_edges(x, width):
    if x < 0:
        return 0
    if x > width:
        return width
    return x

def color_variant(color):
    original = palettes.hex_to_tuple(color)
    adjust_by = random.uniform(0.01, 0.5)
    return tuple((c * adjust_by + c // 2) for c in original)


def main(filename="output.png", palette=random.choice(palettes.PALETTES), reed_count=30, vary_colors=False):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ims.set_fallback_resolution(300.0, 300.0)
    ctx = cairo.Context(ims)

    # Black background
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    for _ in range(reed_count):
        reed(ctx, width=IMG_WIDTH, height=IMG_HEIGHT, color=random.choice(palette['colors']), vary_colors=vary_colors)

    ims.write_to_png(filename)


if __name__ == "__main__":
    p = { 'background': palettes.LIGHT_BLUE, 'colors': [palettes.BRIGHT_GREEN]}
    for idx, count in enumerate([10, 20, 30, 40]):
        main(filename="output-{}.png".format(idx), palette=random.choice(palettes.PALETTES), reed_count=count, vary_colors=False)
