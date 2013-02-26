"""
Basic datastore built ontop of pytables using a simple mapping object
"""

import glob
import os
import uuid
import tables
import collections
import numpy as np

# Form the leafvis cache.
GRID_LOCATION = '/tmp/leafvis_grids'
try:
    os.mkdir(GRID_LOCATION)
except OSError:
    pass


Layer = collections.namedtuple('Layer', 'name lats lons values')

def create_layer(layer):
    """ Create a wms layer """

    with tables.openFile('{}/{}.hdf5'.format(GRID_LOCATION, layer.name), 'w') as table:
    
        # Form a unique grid entry
        _ = table.createGroup("/", 'png_cache', 'graphic cache')
        root = table.createGroup("/", 'grids', 'grid data')

        grid_root = table.createGroup(root, layer.name, "grid_id")

        # For each entry form the table data.
        for label, data in (('lats', layer.lats), ('lons', layer.lons), ('values', layer.values)):
            entry = table.createCArray(
                grid_root, 
                label, 
                tables.Atom.from_dtype(data.dtype),
                data.shape, 
                filters=tables.Filters(complib='blosc', complevel=5)
                )
            entry[:] = data

        grid_root._v_attrs.name = layer.name 


class DataStore(object):
    """ Container class for layers """

    def __init__(self):
        # Define the cache for {grid_id : table}
        self.cache = {}

    def __del__(self):
        
        # Close all open files.
        for _name, table in self.cache.items():
            table.close()

        # Delete temporary files.
        for filename in glob.glob('{}/*.hdf5'.format(GRID_LOCATION)):
            os.unlink(filename)

    def update(self):
        """ Refresh the table cache """
        # Close all file handles.
        for key, value in self.cache.items():
            value.close()

        # Loop through all files in the GRID_LOCATION
        for filename in glob.glob('{}/*.hdf5'.format(GRID_LOCATION)):
            # Open a file handle
            table = tables.openFile(filename, 'a')

            # Populate the cache
            name = table.listNodes('/grids')[0]._v_attrs.name
            
            self.cache[name] = table
            
    def get_layer(self, name):
        """
        Retrieve a grid from the grid database
        """

        table = self.cache.get(name)

        if table is not None:
            try:
               node = table.getNode('/grids/{}'.format(name))
            except tables.NoSuchNodeError as error:
                return None
            return Layer(
                node._v_attrs.name, 
                node.lats.read(), 
                node.lons.read(), 
                node.values.read()
                )

    ###########################################################################

    def get_png(self, name, tl, br):
        """
        Retrieve a grid from the grid database
        """
        img_id = 'img{}'.format(hash((tl, br))).replace('-','_')

        table = self.cache.get(name)
        if table is not None:
            try:
               node = table.getNode('/png_cache/{}'.format(img_id))
            except tables.NoSuchNodeError as error:
                return None
            return node.png.read()

    def store_png(self, name, tl, br, image_buffer):
        """ 
        Form an image cache.
        """
        img_id = 'img{}'.format(hash((tl, br))).replace('-','_')
        table = self.cache.get(name)
        root = table.getNode("/png_cache")
        grid_root = table.createGroup(root, img_id, "png_id")
        table.createArray(grid_root, 'png', image_buffer, "image")

