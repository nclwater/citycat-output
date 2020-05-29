import geopandas as gpd


def validate(rainfall_polygons: gpd.GeoDataFrame):
    assert type(rainfall_polygons) == gpd.GeoDataFrame
    return rainfall_polygons


def write(rainfall_polygons: gpd.GeoDataFrame):
    pass
