import rasterio as rio


def validate(dem: rio.DatasetReader):
    assert type(dem) == rio.DatasetReader
    return dem


def write(dem: rio.DatasetReader):
    pass
