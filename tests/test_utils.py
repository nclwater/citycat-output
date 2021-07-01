from citycatio import utils
import geopandas as gpd
from shapely.geometry import Polygon
from unittest import TestCase
import os
from click.testing import CliRunner

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

    def test_geom2ccat(self):
        runner = CliRunner()
        in_path = 'test_geom.gpkg'
        out_path = 'tets_geom.txt'
        gpd.GeoDataFrame(geometry=geoseries).to_file(in_path, driver='GPKG')
        result = runner.invoke(utils.geom2ccat, f'--in_path {in_path} --out_path {out_path}')
        assert result.exit_code == 0
        os.remove(in_path)
        os.remove(out_path)
