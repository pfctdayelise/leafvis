"""
Basic datastore built ontop of pytables using a simple mapping object
"""

import uuid
import tables

import numpy as np

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
    
    filters = tables.Filters(complib='blosc', complevel=5)
    
    for label, data in (('lats', lats), ('lons', lons), ('values', values)):
        entry = table.createCArray(
            grid_root, 
            label, 
            tables.Atom.from_dtype(data.dtype),
            data.shape, 
            filters=filters)

        entry[:] = data
    return grid_id


def retrieve_grid(grid_id):
    """ Retrieve a grid from the grid database """
    try:
        node = table.getNode('/grids/{}'.format(grid_id))
    except tables.NoSuchNodeError as error:
        return None
    return (node.lats, node.lons, node.values)
