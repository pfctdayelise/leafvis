"""
Resampling functions that map grids to tiles.
"""

from pyresample import geometry, image

def resample(tl, br):
    
   
    model_grid = geometry.GridDefinition(lats=lats, lons=lons)
    
    alons = np.linspace(tl[0], br[0], 256)
    alats = np.linspace(tl[1], br[1], 256)
    Alats = np.tile(alats, (alons.size, 1)).T
    Alons = np.tile(alons, (alats.size, 1))

    analysis_grid = geometry.GridDefinition(lats=Alats, lons=Alons)
    resampler = image.ImageContainerNearest(
        topo, 
        model_grid, 
        radius_of_influence=50000, 
        reduce_data=True
        )

    grid = np.flipud(resampler.resample(analysis_grid).image_data)

    grid[grid == 0] = np.nan

    return grid