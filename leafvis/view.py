""" Defines a leafvis view for IPython """

import requests
import pickle
from IPython.display import HTML


def upload_data((lats, lons, values), host="http://localhost:5000/"):
    """ Uploads the layer data onto the WMS datastore """
    data = pickle.dumps((lats, lons, values))
    payload = {'data': data}
    r = requests.put(host, params=payload)
    return r.content


def leaflet(lats, lons, data):
    """ Returns a HTML leaflet view """

    mapID = upload_data((lats, lons, data))

    url = ('<iframe '
           ' src=http://localhost:5000/map/{}'
           ' width=850'
           ' height=650'
           '</iframe>'
          ).format(mapID)
    
    return HTML(url)
