import citycatio
import unittest
import pandas as pd
import numpy as np
import os
import shutil
import netCDF4 as nc
import datetime


class TestOutput(unittest.TestCase):
    time_interval = 5
    folder = 'R1C1_SurfaceMaps'
    netcdf_path = folder + '.nc'
    steps = range(6)
    dem_path = 'Domain_DEM.ASC'

    @classmethod
    def get_file_name(cls, step):
        return os.path.join(cls.folder, 'R1_C1_T{}_{}min.rsl'.format(step, step * cls.time_interval))

    @classmethod
    def setUpClass(cls):
        print('setup')
        x = [5, 5, 15]
        y = [5, 15, 15]
        os.mkdir(cls.folder)
        for i in cls.steps:
            pd.DataFrame({
                'XCen': x,
                'YCen': y,
                'Depth': np.random.randint(0, 5000, len(x)) / 1000,
                'Vx': np.random.randint(0, 1000, len(x)) / 1000,
                'Vy': np.random.randint(0, 5000, len(x)) / 1000,
                'T_0.000_sec': [None] * 3}).to_csv(cls.get_file_name(i), sep=' ')
        with open(cls.dem_path, 'w') as f:
            f.write(
                "ncols        {}\n".format(len(set(x)) + 1) +
                "nrows        {}\n".format(len(set(y))) +
                "xllcorner    0\n"
                "yllcorner    0\n"
                "cellsize     10\n"
                "NODATA_value  -9999\n"
                "5 5 -9999\n"
                "5 5 -9999\n"
            )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.folder)
        os.remove(cls.netcdf_path)
        os.remove(cls.dem_path)

    def test_get_times(self):
        run = citycatio.Output(self.folder)
        run.get_times()
        self.assertIsInstance(run.times, cls=list)

    def test_get_steps(self):
        run = citycatio.Output(self.folder)
        run.get_steps()
        self.assertIsInstance(run.steps, cls=list)

    def test_read_variables(self):
        run = citycatio.Output(self.folder)
        run.read_variables(0)
        self.assertIsInstance(run.variables, cls=pd.DataFrame)

    def test_get_unique_coordinates(self):
        run = citycatio.Output(self.folder)
        run.read_locations()
        run.get_unique_coordinates()
        self.assertIsInstance(run.unique_x, np.ndarray)

    def test_read_locations(self):
        results = citycatio.Output(self.folder)
        results.read_locations()
        self.assertIsInstance(results.locations, cls=pd.DataFrame)

    def test_create_arrays(self):
        results = citycatio.Output(self.folder)
        results.read_locations()
        results.create_arrays()
        self.assertIsInstance(results.depth, cls=np.ndarray)

    def test_set_array_values(self):
        run = citycatio.Output(self.folder)
        run.read_variables(0)
        run.read_locations()
        run.create_arrays()
        run.set_array_values()
        self.assertIsNotNone(run.depth.max())

    def test_read_file_paths(self):
        run = citycatio.Output(self.folder)
        run.read_file_paths()
        self.assertIsInstance(run.file_paths, list)

    def test_to_netcdf(self):
        run = citycatio.Output(self.folder)
        run.to_netcdf(self.netcdf_path, srid=27700, attributes={'key': 'value'})
        ds = nc.Dataset(self.netcdf_path)
        self.assertIsNotNone(ds)
        self.assertIsNotNone(ds.variables['crs'])
        self.assertEqual(ds.key, 'value')
        self.assertTrue(ds.variables['max_depth'][:].max() > 0)
        self.assertTrue('dem' in ds.variables.keys())
        self.assertTrue(ds.variables['dem'][0, 0] == 5)
        ds.close()

    def test_to_netcdf_attribute_names_are_strings(self):
        with self.assertRaises(AssertionError):
            citycatio.Output(self.folder).to_netcdf(self.netcdf_path, attributes={123: 'value'})

    def test_to_netcdf_attribute_names_start_with_letter(self):
        with self.assertRaises(AssertionError):
            citycatio.Output(self.folder).to_netcdf(self.netcdf_path, attributes={'1key': 'value'})

    def test_to_netcdf_attribute_names_are_alphanumeric(self):
        with self.assertRaises(AssertionError):
            citycatio.Output(self.folder).to_netcdf(self.netcdf_path, attributes={'key*': 'value'})

    def test_to_netcdf_attribute_value_type(self):
        with self.assertRaises(AssertionError):
            citycatio.Output(self.folder).to_netcdf(self.netcdf_path, attributes={'key': datetime.datetime.now()})

    def test_to_netcdf_attribute_value_types(self):
        with self.assertRaises(AssertionError):
            citycatio.Output(self.folder).to_netcdf(self.netcdf_path, attributes={'key': [datetime.datetime.now()]})


if __name__ == '__main__':
    unittest.main()
