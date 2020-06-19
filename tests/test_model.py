from citycatio import Model
import pandas as pd
import unittest
import rasterio as rio
import numpy as np
from rasterio.transform import Affine
import geopandas as gpd

dem_file = rio.MemoryFile()
x_min, y_max = 100, 500
res = 5
height, width = 100, 200
x_max = x_min + width * res
y_min = y_max - height * res
array = np.round(np.random.random((height, width)), 3)
transform = Affine.translation(x_min, y_max) * Affine.scale(res, -res)

with rio.open(
        dem_file,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=array.dtype,
        transform=transform,
        nodata=-9999
) as dst:
    dst.write(array, 1)


class TestModel(unittest.TestCase):

    def test_model(self):

        Model(dem=dem_file, rainfall=pd.DataFrame([0]), rainfall_polygons=gpd.GeoDataFrame(),
              buildings=gpd.GeoDataFrame(), green_areas=gpd.GeoDataFrame(),
              friction=gpd.GeoDataFrame(), boundaries=gpd.GeoDataFrame())

    def test_write_model(self):
        Model(dem=dem_file, rainfall=pd.DataFrame([0])).write('tests/test_model')
