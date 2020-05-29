import geopandas as gpd


def validate(green_areas: gpd.GeoDataFrame):
    assert type(green_areas) == gpd.GeoDataFrame
    return green_areas


def write(green_areas: gpd.GeoDataFrame):
    pass
