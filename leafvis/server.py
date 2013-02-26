import pickle
import store
import sampler
import render

from flask import Flask, request, render_template
from pyproj import Proj

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)

datastore = store.DataStore()

def _drawLayerTile(name, tl, br):
    
    png = datastore.get_png(name, tl, br)

    if png is None:
        layer = datastore.get_layer(name)
        if layer is None:
            return ''
        grid = sampler.resample(layer, tl, br, samples=256)       
        png = render.draw_tile(grid)
        datastore.store_png(name, tl, br, png)
    return png


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
  
    return _drawLayerTile(layer, tl, br)  

@app.route('/grids/<state>')
def refresh(state):
    if 'refresh' in state:
        datastore.update()

@app.route('/map/<layer>')
def draw(layer):
    return render_template('leaflet.html', layer=layer)

if __name__ == '__main__': 
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
