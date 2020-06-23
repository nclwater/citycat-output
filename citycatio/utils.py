import geopandas as gpd


def geoseries_to_string(geoseries: gpd.GeoSeries, index=False):
    """GeoSeries to CityCAT string representation"""
    assert (geoseries.geom_type == 'Polygon').all(), 'Geometries must be of type Polygon'

    s = '{}\n'.format(len(geoseries))

    for idx, geometry in geoseries.items():
        x, y = geometry.exterior.coords.xy
        if index:
            s += '{} '.format(idx)
        s += '{}'.format(len(geometry.exterior.coords))
        for x_val in x:
            s += ' {}'.format(x_val)
        for y_val in y:
            s += ' {}'.format(y_val)
        s += '\n'

    return s
