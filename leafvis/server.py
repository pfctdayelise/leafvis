
import pickle
import store
import sampler
import render

from flask import Flask, request, render_template
from pyproj import Proj
from joblib import Memory

memory = Memory(cachedir='/tmp/joblib', verbose=False)

app = Flask(__name__)


@memory.cache
def __drawLayerTile(layer_data, tl, br):
    grid = sampler.resample(layer_data, tl, br, samples=256)
    return render.draw_tile(grid)


@app.route('/', methods=['GET'])
def wms():
    """ A *basic* web mapping service """

    # Retrieve the source projection.
    srs = request.args['srs']
    
    # Form a projection function and compute the tile coordinates.
    proj = Proj(init=srs)
    coords = [float(x) for x in request.args['bbox'].split(',')]
    tl = proj(coords[0], coords[1], inverse=True)
    br = proj(coords[2], coords[3], inverse=True)

    # Retrieve the layer of interest.
    layer = request.args['layers']
    layer_data = store.retrieve_grid(layer)

    if layer_data is None:
        return ''

    return __drawLayerTile(layer_data, tl, br)  

@app.route('/', methods=['PUT'])
def upload():
    layer_data = request.args['data']
    layer = pickle.loads(layer_data)
    layer_id = store.store_grid(*layer)
    return str(layer_id)

@app.route('/map/<layer>')
def draw(layer):
    return render_template('leaflet.html', layer=layer)

if __name__ == '__main__': 
      app.run(debug=False)   