import geopandas as gpd


def validate(friction: gpd.GeoDataFrame):
    assert type(friction) == gpd.GeoDataFrame
    return friction


def write(friction: gpd.GeoDataFrame):
    pass
