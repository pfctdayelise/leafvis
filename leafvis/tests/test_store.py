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

