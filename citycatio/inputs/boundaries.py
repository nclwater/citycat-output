import geopandas as gpd


def validate(boundaries: gpd.GeoDataFrame):
    assert type(boundaries) == gpd.GeoDataFrame
    return boundaries


def write(boundaries: gpd.GeoDataFrame):
    pass
