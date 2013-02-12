from flask import Flask, request

import numpy as np
import StringIO

from pyproj import Proj
from joblib import Memory

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import mpl_toolkits.basemap

# FIXME: Look at PyResample!


app = Flask(__name__)

mem = Memory(cachedir='/tmp/joblib')

import matplotlib.pyplot as plt

fig, ax0 = plt.subplots(1, 1, figsize=(10, 10))

proj = Proj(init='epsg:3857')

def draw_tile(box):
    fig = Figure(dpi=80, edgecolor='none')
    fig.patch.set_alpha(0.5)
    ax = fig.add_subplot(111)
    ax.imshow(np.random.rand(256, 256), interpolation='nearest')
    ax.axis('off')
    ax.axis('tight')
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output, transparent=True)
    
    return png_output.getvalue()


cachedDraw = mem.cache(draw_tile)

@app.route('/', methods=['GET'])
def wms():
 
    coords = [float(x) for x in request.args['bbox'].split(',')]
    tl = proj(coords[0], coords[1], inverse=True)
    br = proj(coords[1], coords[2], inverse=True)

    print '{0}\ntl={1},br={2}\n{0}'.format('*'*80, tl, br)

    return draw_tile(coords)

if __name__ == '__main__': 
    plt.ioff()
    app.run(debug=True)   