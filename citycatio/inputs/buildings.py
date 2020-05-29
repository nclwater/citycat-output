import geopandas as gpd


def validate(buildings: gpd.GeoDataFrame):
    assert type(buildings) == gpd.GeoDataFrame
    return buildings


def write(buildings: gpd.GeoDataFrame):
    pass
