import citycat_output
import unittest
import pandas as pd
import numpy as np
import os
import shutil
import netCDF4 as nc


class TestCore(unittest.TestCase):
    time_interval = 5
    folder = 'R1C1_SurfaceMaps'
    netcdf_path = folder + '.nc'

    @classmethod
    def get_file_name(cls, step):
        return os.path.join(cls.folder, 'R1_C1_T{}_{}min.rsl'.format(step, step * cls.time_interval))

    @classmethod
    def setUpClass(cls):
        print('setup')
        x = [1, 1, 2]
        y = [1, 2, 1]
        os.mkdir(cls.folder)
        for i in range(6):
            pd.DataFrame({
                'XCen': x,
                'YCen': y,
                'Depth': np.random.randint(0, 5000, len(x)) / 1000,
                'Vx': np.random.randint(0, 1000, len(x)) / 1000,
                'Vy': np.random.randint(0, 5000, len(x)) / 1000,
                'T_0.000_sec': [None] * 3}).to_csv(cls.get_file_name(i), sep=' ')

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.folder)
        os.remove(cls.netcdf_path)

    def test_reading_time(self):
        results = citycat_output.Results(self.get_file_name(0))
        self.assertEqual(results.time, 0)

    def test_variables(self):
        results = citycat_output.Results(self.get_file_name(0))
        results.read_variables()
        self.assertIsInstance(results.variables, cls=pd.DataFrame)

    def test_locations(self):
        results = citycat_output.Results(self.get_file_name(0))
        results.read_locations()
        self.assertIsInstance(results.locations, cls=pd.DataFrame)

    def test_create_array(self):
        results = citycat_output.Results(self.get_file_name(0))
        results.read_locations()
        results.read_variables()
        results.create_arrays()
        self.assertIsInstance(results.depth, cls=np.ndarray)

    def test_create_array_with_locations(self):
        results = citycat_output.Results(self.get_file_name(0))
        results.read_variables()
        other_results = citycat_output.Results(self.get_file_name(5))
        other_results.read_locations()
        results.set_locations(other_results.locations)
        results.create_arrays()
        self.assertIsInstance(results.depth, cls=np.ndarray)

    def test_getting_paths(self):
        run = citycat_output.Run(self.folder)
        run.get_results()
        self.assertIsInstance(run.results, list)

    def test_create_netcdf(self):
        run = citycat_output.Run(self.folder)
        run.get_results()
        run.to_netcdf(self.netcdf_path)
        ds = nc.Dataset(self.netcdf_path)
        self.assertIsNotNone(ds)
        ds.close()


if __name__ == '__main__':
    unittest.main()
