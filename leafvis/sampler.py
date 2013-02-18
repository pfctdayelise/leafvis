"""
Resampling functions that map grids to tiles.
"""
import numpy as np
from pyresample import geometry, image

def resample((lats, lons, values), tl, br, samples=256):
    """
    Returns a grid, which is resampled.
    """

    data_grid = geometry.GridDefinition(lats=lats, lons=lons)
    
    # Form the coordinates for resampling
    rlons = np.linspace(tl[0], br[0], 256)
    rlats = np.linspace(tl[1], br[1], 256)

    resample_grid = geometry.GridDefinition(
        lats=np.tile(rlats, (rlons.size, 1)).T, 
        lons=np.tile(rlons, (rlats.size, 1))
        )

    # Build a resampler.
    resampler = image.ImageContainerNearest(
        values, 
        data_grid, 
        radius_of_influence=50000, 
        reduce_data=True
        )

    # Form the appropriate grid.
    grid = np.flipud(resampler.resample(resample_grid).image_data)
    grid[grid == 0] = np.nan

    return grid