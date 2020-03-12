#!/usr/bin/env python
import time
import math
import cairo
import flask
import numpy as np
import io
from time import time, sleep
import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go

WIDTH, HEIGHT = 256, 256
FRAMERATE = 0.1

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

def img_generator2():
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

def img_generator():
    n_vertices = 3
    while True:
        print('called')
        if n_vertices > 100:
            n_vertices=3
        n_children_per_node = 2
        vertex_labels = [str(x) for x in range(n_vertices)]

        G = Graph.Tree(n_vertices, n_children_per_node)

        # Defines a layout algorithm
        layout = G.layout('rt')

        position = {k: layout[k] for k in range(n_vertices)}
        Y = [layout[k][1] for k in range(n_vertices)]
        M = max(Y)

        es = EdgeSeq(G) # sequence of edges
        E = [e.tuple for e in G.es] # list of edges

        L = len(position)
        Xn = [position[k][0] for k in range(L)]
        Yn = [2*M-position[k][1] for k in range(L)]
        Xe = []
        Ye = []
        for edge in E:
            Xe+=[position[edge[0]][0],position[edge[1]][0], None]
            Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

        labels = vertex_labels

        print('called2')
        fig = go.Figure()

        print('called3')
        # Plot Vertices
        fig.add_trace(go.Scatter(x=Xn,
                        y=Yn,
                        mode='markers',
                        name='bla',
                        marker=dict(symbol='circle-dot',
                                        size=18,
                                        color='#DB4551',
                                        line=dict(color='rgb(50,50,50)', width=1)
                                        ),
                        text=labels,
                        hoverinfo='text',
                        opacity=0.8
                        ))

        # Plot Edges
        fig.add_trace(go.Scatter(x=Xe,
                        y=Ye,
                        mode='lines',
                        line=dict(color='rgb(210,210,210)', width=1),
                        hoverinfo='none'
                        ))

        print('called3')
        img_bytes = fig.to_image(format="png")
        print('called4')
        sleep(1/FRAMERATE)
        yield (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + img_bytes + b'\r\n')
        n_vertices+=1


if __name__ == "__main__":
    app.run(port=8212, debug=True)