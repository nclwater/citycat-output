import geopandas as gpd


def geoseries_to_string(geoseries: gpd.GeoSeries, index=False, index_first=True):
    """GeoSeries to CityCAT string representation"""
    assert (geoseries.geom_type == 'Polygon').all(), 'Geometries must be of type Polygon'

    s = '{}\n'.format(len(geoseries))

    for idx, geometry in geoseries.items():
        if not index:
            s += '{}'.format(len(geometry.exterior.coords))
        elif index_first:
            s += '{} {}'.format(idx, len(geometry.exterior.coords))
        else:
            s += '{} {}'.format(len(geometry.exterior.coords), idx)
        x, y = geometry.exterior.coords.xy
        for x_val in x:
            s += ' {}'.format(x_val)
        for y_val in y:
            s += ' {}'.format(y_val)
        s += '\n'

    return s
