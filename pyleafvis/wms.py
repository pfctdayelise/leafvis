from flask import Flask, request
from flask import Flask, request, json, jsonify, current_app, render_template
from functools import wraps

import numpy as np
import StringIO

from pyproj import Proj
from joblib import Memory

from pyresample import geometry, image

import sys
sys.path.append('/Users/nfaggian/Desktop/development/metex')

from metex import data


from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import mpl_toolkits.basemap

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs).data) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function


# FIXME: Look at PyResample!
app = Flask(__name__)

mem = Memory(cachedir='/tmp/joblib')

import matplotlib.pyplot as plt

lats, lons = data.coords()
topo = data.topo()

proj = Proj(init='epsg:3857')

def resample(tl, br):
    
   
    model_grid = geometry.GridDefinition(lats=lats, lons=lons)
    
    alons = np.linspace(tl[0], br[0], 256)
    alats = np.linspace(tl[1], br[1], 256)
    Alats = np.tile(alats, (alons.size, 1)).T
    Alons = np.tile(alons, (alats.size, 1))

    analysis_grid = geometry.GridDefinition(lats=Alats, lons=Alons)
    resampler = image.ImageContainerNearest(
        topo, 
        model_grid, 
        radius_of_influence=50000, 
        reduce_data=True
        )

    grid = np.flipud(resampler.resample(analysis_grid).image_data)

    grid[grid == 0] = np.nan

    return grid

def draw_tile(tl, br):

    grid = resample(tl, br)

    fig = Figure(dpi=80, edgecolor='none')
    fig.patch.set_alpha(0.1)
    ax = fig.add_axes((0,0,1,1))
    ax.matshow(grid, interpolation='nearest', alpha=0.5, vmin=0, vmax=2500)
    ax.contour(grid, level=[500])
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
    br = proj(coords[2], coords[3], inverse=True)

    print '{0}\ntl={1},br={2}\n{0}'.format('*'*80, tl, br)

    return cachedDraw(tl, br)


@app.route('/sample/<location>')
@support_jsonp
def SAMPLER(location):
    """
    """
    return jsonify(value='bah')

from flask import render_template

@app.route('/map')
def hello():
    return render_template('leaflet.html')

if __name__ == '__main__': 
    plt.ioff()
    app.run(debug=True)   