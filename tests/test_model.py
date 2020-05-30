from citycatio import Model, read_postgis
import pandas as pd
import unittest
import rasterio as rio
import numpy as np
from rasterio.transform import Affine
import geopandas as gpd
import psycopg2
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

        Model(dem=dem_file, rainfall=pd.DataFrame([0]), rainfall_polygons=gpd.GeoDataFrame(),
              buildings=gpd.GeoDataFrame(), green_areas=gpd.GeoDataFrame(), configuration={},
              friction=gpd.GeoDataFrame(), boundaries=gpd.GeoDataFrame())

    def test_write_model(self):
        Model(dem=dem_file, rainfall=pd.DataFrame([0])).write('tests/test_model')


class TestReadPostgis(unittest.TestCase):
    def test_read_postgis(self):
        con = psycopg2.connect(database='postgres', user='postgres', password='password', host='localhost')
        dem_file.seek(0)
        with con.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis_raster")
            cursor.execute("SET postgis.gdal_enabled_drivers TO 'GTiff'")

            cursor.execute("DROP TABLE IF EXISTS domain")
            cursor.execute("CREATE TABLE domain (gid serial PRIMARY KEY, geom geometry)")
            cursor.execute("INSERT INTO domain(geom) VALUES (ST_GeomFromText('{}'))".format(
                Polygon([[x_min, y_min], [x_min, y_max], [x_max/2, y_max/2], [x_max, y_min], [x_min, y_min]])))

            cursor.execute("DROP TABLE IF EXISTS dem")
            cursor.execute("CREATE TABLE dem (rast raster)")
            cursor.execute("INSERT INTO dem(rast) VALUES (ST_FromGDALRaster({}))".format(psycopg2.Binary(dem_file.read())))

            cursor.execute("DROP TABLE IF EXISTS rainfall")

        model = read_postgis(con)
        model.write('tests/test_model_postgis')
