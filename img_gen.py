#!/usr/bin/env python
import time
import math
import cairo

WIDTH, HEIGHT = 256, 256

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas


i = 0
while True:
    pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
    pat.add_color_stop_rgba(1, 0.7, 0, 0, 0.5)  # First stop, 50% opacity
    pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity
    ctx.rectangle(0, 0, 1, 1)  # Rectangle(x0, y0, x1, y1)
    ctx.set_source(pat)
    ctx.fill()

    # Arc(cx, cy, radius, start_angle, stop_angle)
    ctx.arc(0.5, 0.5, .3, math.pi*i/2 - 5,  math.pi*i/2)

    ctx.set_source_rgb(0.3, 0.2, 0.5)  # Solid color
    ctx.set_line_width(0.02)
    ctx.stroke()

    surface.write_to_png("example.png")  # Output to PNG
    time.sleep(0.5)
    i +=1
