#!/usr/bin/env python
import time
import math
import cairo
import flask
import numpy as np
import io
from time import time, sleep

WIDTH, HEIGHT = 256, 256
FRAMERATE = 24

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas

memory_buffer = io.BytesIO()

app = flask.Flask(__name__)


@app.route('/')
def index():
    return flask.render_template('index3.html')


@app.route("/next_img")
def next_img():
    return flask.Response(img_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')


def img_generator():
    i = -1
    while True:
        # frame = camera.get_frame()
        i +=1
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
        memory_buffer.seek(0)
        surface.write_to_png(memory_buffer)
        memory_buffer.seek(0)
        sleep(1/FRAMERATE)
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + memory_buffer.read() + b'\r\n')


if __name__ == "__main__":
    app.run(port=8212, debug=True)