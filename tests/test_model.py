from citycatio import Model
import pandas as pd
import unittest
import rasterio as rio
import numpy as np
from rasterio.transform import Affine
import geopandas as gpd
from shapely.geometry import Polygon

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

        Model(dem=dem_file, rainfall=pd.DataFrame([0, 0]),
              buildings=gpd.GeoDataFrame(), green_areas=gpd.GeoDataFrame(),
              friction=gpd.GeoDataFrame(), open_boundaries=gpd.GeoDataFrame())

    def test_write_model(self):
        Model(dem=dem_file,
              rainfall=pd.DataFrame({0: [0, 0], 1: [0, 0]}),
              open_boundaries=gpd.GeoDataFrame(
                  geometry=[Polygon([(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min), (x_min, y_min)])]),
              buildings=gpd.GeoDataFrame(
                  geometry=[Polygon([(x_min, y_min), (x_min, y_min+res), (x_min+res, y_min+res),
                                     (x_min+res, y_min), (x_min, y_min)])]),
              friction=gpd.GeoDataFrame(
                  geometry=[Polygon([(x_max-res, y_max-res), (x_max, y_max-res), (x_max, y_max),
                                     (x_max, y_max-res), (x_max-res, y_max-res)])],
                  index=[0.03]
              ),
              green_areas=gpd.GeoDataFrame(
                  geometry=[Polygon([(x_max-res, y_max-res), (x_max, y_max-res), (x_max, y_max),
                                     (x_max, y_max-res), (x_max-res, y_max-res)])],
                  index=[1]
              ),
              rainfall_polygons=gpd.GeoSeries([
                      Polygon([(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min), (x_min, y_min)]),
                      Polygon([(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min), (x_min, y_min)]),
                  ])

              ).write('tests/test_model')
