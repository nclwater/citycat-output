import geopandas as gpd
from ..utils import geoseries_to_string
import os


class RainfallPolygons:
    def __init__(self, data: gpd.GeoDataFrame):
        assert type(data) == gpd.GeoDataFrame
        self.data = data

    def write(self, path):
        with open(os.path.join(path, 'Rainfall_Polygons.txt'), 'w') as f:
            f.write(geoseries_to_string(self.data.geometry))
