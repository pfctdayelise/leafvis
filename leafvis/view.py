""" Defines a leafvis view """

import requests
import pickle

def upload_data((lats, lons, values), host="http://localhost:5000/"):
    """ Uploads the layer data onto the WMS datastore """
    data = pickle.dumps((lats, lons, values))
    payload = {'data': data}
    r = requests.put(host, params=payload)
    return r.content

#import numpy as np
#foo = np.zeros((100,100))
#upload_data((foo, foo, foo))