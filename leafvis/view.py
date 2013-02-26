""" Defines a leafvis view for IPython """

import requests
import pickle
import store

from IPython.display import HTML


def leaflet(name, lats, lons, data, host="http://localhost:5000"):
    """ Returns a HTML leaflet view """

    _id = store.create_wms_layer(name, lats, lons, data)
    
    # Tell the WMS server to refresh its grid cache.
    r = requests.get('{}/grids/refresh'.format(host), params={})
    
    if r.content is None:
        raise ValueError('Cannot update grids')

    url = ('<iframe '
           ' src={}/map/{}'
           ' width=850'
           ' height=650'
           '</iframe>'
          ).format(host, name)
    
    return HTML(url)
