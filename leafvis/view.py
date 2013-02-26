""" Defines a leafvis view for IPython """

import requests
import pickle
import store

from IPython.display import HTML


def leaflet(layer, host="http://localhost:5000"):
    """ Returns a HTML leaflet view """

    _ = store.create_layer(layer)
    
    # Tell the WMS server to refresh its grid cache.
    r = requests.get('{}/grids/refresh'.format(host), params={})
    
    if r.content is None:
        raise ValueError('Cannot update grids')

    url = ('<iframe '
           ' src={}/map/{}'
           ' width=850'
           ' height=650'
           '</iframe>'
          ).format(host, layer.name)
    
    return HTML(url)
