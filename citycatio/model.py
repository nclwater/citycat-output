from . import inputs
from .output import Output
import rasterio as rio
import geopandas as gpd
import pandas as pd
from typing import Optional
import os
import shutil


class Model:
    def __init__(
            self,
            dem: rio.MemoryFile,
            rainfall: pd.DataFrame,
            rainfall_polygons: Optional[gpd.GeoDataFrame] = None,
            buildings: Optional[gpd.GeoDataFrame] = None,
            green_areas: Optional[gpd.GeoDataFrame] = None,
            configuration: Optional[dict] = None,
            friction: Optional[gpd.GeoDataFrame] = None,
            boundaries: Optional[gpd.GeoDataFrame] = None,
    ):
        self.dem = inputs.Dem(dem)
        self.rainfall = inputs.Rainfall(rainfall)
        self.rainfall_polygons = inputs.RainfallPolygons(rainfall_polygons) if rainfall_polygons is not None else None,
        self.buildings = inputs.Buildings(buildings) if buildings is not None else None,
        self.green_areas = inputs.GreenAreas(green_areas) if green_areas is not None else None,
        self.configuration = inputs.Configuration(configuration) if configuration is not None else None,
        self.friction = inputs.Friction(friction) if friction is not None else None,
        self.boundaries = inputs.Boundaries(boundaries) if boundaries is not None else None,
        self.output: Optional[Output] = None

    def write(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        self.dem.write(path)
        self.rainfall.write(path)


def read_postgis(con, domain_table='domain', domain_id=1, rainfall_table='rainfall', dem_table='dem'):
    with con.cursor() as cursor:
        cursor.execute("""
        SELECT ST_AsGDALRaster(ST_Union(ST_Clip(rast, geom)), 'GTiff') 
        FROM {}, {} WHERE ST_Intersects(rast, geom) and gid={}
        """.format(dem_table, domain_table, domain_id))

        dem = rio.MemoryFile(cursor.fetchone()[0].tobytes())

    return Model(dem=dem, rainfall=pd.DataFrame([0]))
