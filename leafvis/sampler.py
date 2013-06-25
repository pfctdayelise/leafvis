"""
Resampling functions that map grids to tiles.
"""

import numpy as np
from pyresample import geometry, image

def resample(layer, tl, br, samples=256):
    """
    Returns a grid, which is resampled.
    """

    data_grid = geometry.GridDefinition(lats=layer.lats, lons=layer.lons)
    
    # Form the coordinates for resampling
    rlons = np.linspace(tl[0], br[0], 256)
    rlats = np.linspace(tl[1], br[1], 256)

    resample_grid = geometry.GridDefinition(
        lats=np.tile(rlats, (rlons.size, 1)).T, 
        lons=np.tile(rlons, (rlats.size, 1))
        )

    # Build a resampler.
    resampler = image.ImageContainerNearest(
        layer.values, 
        data_grid, 
        radius_of_influence=6500, 
        reduce_data=True
        )

    # Form the appropriate grid.
    grid = np.flipud(resampler.resample(resample_grid).image_data)
    grid[grid == 0] = np.nan

    return grid


def sample_latlon(layer, lat, lon):
    """
    Returns a float which is a value grid, which is resampled.
    """

    data_grid = geometry.GridDefinition(lats=layer.lats, lons=layer.lons)
    
    resampler = image.ImageContainerNearest(
        layer.values, 
        data_grid, 
        radius_of_influence=6500, 
        reduce_data=False
        )

    resample_grid = geometry.GridDefinition(
        lats=np.ones((1, 1)) * lat, 
        lons=np.ones((1, 1)) * lon)

    # Form the appropriate grid.
    grid = resampler.resample(resample_grid).image_data
    return float(grid[0][0])

