import pickle
import store
import sampler
import render
import socket
from functools import wraps

from flask import Flask, request, render_template, current_app, jsonify
from pyproj import Proj

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)

datastore = store.DataStore()

TILECOLORS = {}


# https://gist.github.com/1094140
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


def _drawLayerTile(name, tl, br):

    png = datastore.get_png(name, tl, br)

    cmap, vmin, vmax = TILECOLORS.get(name, ('elevation', 0, 1200))

    if png is None:
        layer = datastore.get_layer(name)
        if layer is None:
            return ''
        grid = sampler.resample(layer, tl, br, samples=256)
        png = render.draw_tile(grid, cmap, vmin, vmax)
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
        print "Refreshing"
        datastore.update()


@app.route('/map/<layer>/<cmap>/<vmin>/<vmax>')
def draw(layer, cmap, vmin, vmax):
    TILECOLORS[layer] = (cmap, float(vmin), float(vmax))
    return render_template('leaflet.html', host=socket.gethostname(), layer=layer)


@app.route('/sample/<layer>/<lat>/<lon>')
@support_jsonp
def sample(layer, lat, lon):
    data  = datastore.get_layer(layer)
    val = sampler.sample_latlon(data, float(lat), float(lon))
    return jsonify(sample=val)


def main():
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
