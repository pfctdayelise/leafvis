"""
Basic datastore built ontop of pytables using a simple mapping object
"""
import os
import uuid
import tables
import collections
import numpy as np

GRID_LOCATION = '/tmp/leafvis_grids'

BLOSC = tables.Filters(complib='blosc', complevel=5)

GridSample = collections.namedtuple('GridSample', 'name lats lons values')

################################################################################
# TODO: 
#    1. Cache of png data?
#    2. GridSample representation?
################################################################################

def create_wms_layer(name, lats, lons, values):
    """ Create a wms layer """
    table = tables.openFile('{}/{}.hdf5'.format(GRID_LOCATION, name), 'w')
    
    # Form a unique grid entry
    root = table.createGroup("/", 'grids', 'grid data')

    grid_id = uuid.uuid4()
    grid_root = table.createGroup(root, str(grid_id), "grid_id")

    # For each entry form the table data.
    for label, data in (('lats', lats), ('lons', lons), ('values', values)):
        entry = table.createCArray(
            grid_root, 
            label, 
            tables.Atom.from_dtype(data.dtype),
            data.shape, 
            filters=BLOSC)
        entry[:] = data
    table.close()

    return str(grid_id)


class DataStore(object):
    """ Container class for layers """

    def __init__(self):
        # Define the cache for {layer-name : table handles}
        self.cache = {}

    def __del__(self):
        for _name, table in self.cache.items():
            table.close()

    def update(self):
        """ Refresh the table cache """
        # Close all file handles.
        for key, value in self.cache.items():
            value.close()

        # Loop through all files in the GRID_LOCATION
        for filename in glob.glob('{}/*.hdf5'):
            table = tables.openFile(filename, 'a')
            self.cache[name] = table

    def get_layer(self, grid_id):
        """
        Retrieve a grid from the grid database
        """
        table = self.cache.get(grid_id)
        if table is not None:
            node = table.getNode('/grids/{}'.format(grid_id))
        except tables.NoSuchNodeError as error:
            return None

        return GridSample(node.name, node.lats[:,:], node.lons[:,:], node.values[:,:])

    # FIXME: Caching png data?
    def get_png(self, grid_id, bounding_box):
        pass

################################################################################
# FIXME: Delete code below
################################################################################

# Data store for raw grids 
table = tables.openFile('/tmp/grids.hdf5', 'a')

def store_grid(lats, lons, values):
    """ Stores a grid in a pytables datastore """

    try:
        root = table.getNode('/grids')
    except Exception as error:
        root = table.createGroup("/", 'grids', 'grid data')

    grid_id = uuid.uuid4()
    grid_root = table.createGroup(root, str(grid_id), "grid_id")
    
    for label, data in (('lats', lats), ('lons', lons), ('values', values)):
        entry = table.createCArray(
            grid_root, 
            label, 
            tables.Atom.from_dtype(data.dtype),
            data.shape, 
            filters=BLOSC)

        entry[:] = data
    return grid_id


def retrieve_grid(grid_id):
    """ Retrieve a grid from the grid database """
    try:
        node = table.getNode('/grids/{}'.format(grid_id))
    except tables.NoSuchNodeError as error:
        return None
    return (node.lats[:,:], node.lons[:,:], node.values[:,:])
