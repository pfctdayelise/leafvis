""" Test the datastore """

import numpy as np

from leafvis import store

def test_store_retrieve():
    """ Assert that a grid stored can be retrieved """
    
    lats, lons, values = (
        np.ones((5, 5)),
        np.ones((5, 5)),
        np.ones((5, 5))
        )

    grid_id = store.store_grid(lats, lons, values)

    (rlats, rlons, rvalues) = store.retrieve_grid(grid_id)

    assert np.allclose(lats, rlats)
    assert np.allclose(lons, rlons)
    assert np.allclose(values, rvalues)


def test_datastore():

    lats, lons, values = (
        np.ones((5, 5)),
        np.ones((5, 5)),
        np.ones((5, 5))
        )

    # form a layer datastore.
    dstore = store.DataStore()

    for i in range(10):
        store.create_wms_layer(
            'test-{:02}'.format(i), 
            lats+i, 
            lons+i, 
            values+i
            )

    # Update the data-store cache.
    dstore.update()

    for i in range(10):
        layer = dstore.get_layer('test-{:02}'.format(i)) 
        assert np.allclose(lats+i, layer.lats)
        assert np.allclose(lons+i, layer.lons)
        assert np.allclose(values+i, layer.values)

