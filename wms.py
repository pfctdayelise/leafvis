from flask import Flask, request
import numpy as np
import StringIO

from joblib import Memory

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

mem = Memory(cachedir='/tmp/joblib')

def draw_tile(box):
    fig = Figure(dpi=80)
    ax = fig.add_subplot(111)
    ax.imshow(np.random.rand(256, 256), interpolation='nearest')
    ax.axis('off')
    ax.axis('tight')
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    return png_output.getvalue()


cachedDraw = mem.cache(draw_tile)

@app.route('/', methods=['GET'])
def hello_world():
    coords = request.args['bbox'].split(',')
    return cachedDraw(coords)


if __name__ == '__main__':
    app.run(debug=True)   