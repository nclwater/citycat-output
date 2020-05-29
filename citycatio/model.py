from . import inputs
from .output import Output
import rasterio as rio
import geopandas as gpd
import pandas as pd
from typing import Optional


class Model:
    def __init__(
            self,
            dem: rio.DatasetReader,
            rainfall: pd.DataFrame,
            rainfall_polygons: Optional[gpd.GeoDataFrame] = None,
            buildings: Optional[gpd.GeoDataFrame] = None,
            green_areas: Optional[gpd.GeoDataFrame] = None,
            configuration: Optional[dict] = None,
            friction: Optional[gpd.GeoDataFrame] = None,
            boundaries: Optional[gpd.GeoDataFrame] = None,
    ):
        self.dem = inputs.dem.validate(dem)
        self.rainfall = inputs.rainfall.validate(rainfall),
        self.rainfall_polygons = inputs.rainfall_polygons.validate(rainfall_polygons),
        self.buildings = inputs.buildings.validate(buildings),
        self.green_areas = inputs.green_areas.validate(green_areas),
        self.configuration = inputs.configuration.validate(configuration),
        self.friction = inputs.friction.validate(friction),
        self.boundaries = inputs.boundaries.validate(boundaries),
        self.output: Optional[Output] = None
