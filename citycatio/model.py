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
            friction: Optional[gpd.GeoDataFrame] = None,
            boundaries: Optional[gpd.GeoDataFrame] = None,
            **kwargs
    ):
        self.dem = inputs.Dem(dem)
        self.rainfall = inputs.Rainfall(rainfall)

        self.configuration = inputs.Configuration(
            **{**dict(duration=rainfall.index[-1], rainfall_zones=len(rainfall.columns)), **kwargs})

        self.rainfall_polygons = inputs.RainfallPolygons(rainfall_polygons) if rainfall_polygons is not None else None
        self.buildings = inputs.Buildings(buildings) if buildings is not None else None
        self.green_areas = inputs.GreenAreas(green_areas) if green_areas is not None else None
        self.friction = inputs.Friction(friction) if friction is not None else None
        self.boundaries = inputs.Boundaries(boundaries) if boundaries is not None else None
        self.output: Optional[Output] = None

    def write(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        self.dem.write(path)
        self.rainfall.write(path)
        self.configuration.write(path)
        if self.boundaries is not None:
            self.boundaries.write(path)
