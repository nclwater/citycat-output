from citycatio import utils
import geopandas as gpd
from shapely.geometry import Polygon
from unittest import TestCase

geoseries = gpd.GeoSeries(
                [
                    Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]),
                    Polygon([(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)])
                ],
                index=[3, 4])


class TestUtils(TestCase):
    def test_geoseries_to_string_with_index(self):
        self.assertMultiLineEqual(
            utils.geoseries_to_string(geoseries, index=True),
            '2\n'
            '3 5 0.0 0.0 1.0 1.0 0.0 0.0 1.0 1.0 0.0 0.0\n' 
            '4 5 1.0 1.0 2.0 2.0 1.0 1.0 2.0 2.0 1.0 1.0\n')

    def test_geoseries_to_string(self):
        self.assertMultiLineEqual(
            utils.geoseries_to_string(geoseries),
            '2\n'
            '5 0.0 0.0 1.0 1.0 0.0 0.0 1.0 1.0 0.0 0.0\n' 
            '5 1.0 1.0 2.0 2.0 1.0 1.0 2.0 2.0 1.0 1.0\n')
