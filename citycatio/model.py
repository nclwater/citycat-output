from . import inputs
from .output import Output
import rasterio as rio
import geopandas as gpd
import pandas as pd
from typing import Optional


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
        self.rainfall = inputs.Rainfall(rainfall),
        self.rainfall_polygons = inputs.RainfallPolygons(rainfall_polygons),
        self.buildings = inputs.Buildings(buildings),
        self.green_areas = inputs.GreenAreas(green_areas),
        self.configuration = inputs.Configuration(configuration),
        self.friction = inputs.Friction(friction),
        self.boundaries = inputs.Boundaries(boundaries),
        self.output: Optional[Output] = None
