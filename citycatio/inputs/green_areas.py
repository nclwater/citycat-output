import geopandas as gpd


class GreenAreas:
    def __init__(self, data: gpd.GeoDataFrame):
        assert type(data) == gpd.GeoDataFrame
        self.data = data

    def write(self):
        pass
