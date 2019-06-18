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
    steps = range(6)

    @classmethod
    def get_file_name(cls, step):
        return os.path.join(cls.folder, 'R1_C1_T{}_{}min.rsl'.format(step, step * cls.time_interval))

    @classmethod
    def setUpClass(cls):
        print('setup')
        x = [1, 1, 2]
        y = [1, 2, 1]
        os.mkdir(cls.folder)
        for i in cls.steps:
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

    def test_get_times(self):
        run = citycat_output.Run(self.folder)
        run.get_times()
        self.assertIsInstance(run.times, cls=list)

    def test_get_steps(self):
        run = citycat_output.Run(self.folder)
        run.get_steps()
        self.assertIsInstance(run.steps, cls=list)

    def test_read_variables(self):
        run = citycat_output.Run(self.folder)
        run.read_variables(0)
        self.assertIsInstance(run.variables, cls=pd.DataFrame)

    def test_get_unique_coordinates(self):
        run = citycat_output.Run(self.folder)
        run.read_locations()
        run.get_unique_coordinates()
        self.assertIsInstance(run.x, np.ndarray)

    def test_read_locations(self):
        results = citycat_output.Run(self.folder)
        results.read_locations()
        self.assertIsInstance(results.locations, cls=pd.DataFrame)

    def test_create_arrays(self):
        results = citycat_output.Run(self.folder)
        results.read_locations()
        results.create_arrays()
        self.assertIsInstance(results.depth, cls=np.ndarray)

    def test_set_array_values(self):
        run = citycat_output.Run(self.folder)
        run.read_variables(0)
        run.read_locations()
        run.create_arrays()
        run.set_array_values()
        self.assertIsNotNone(run.depth.max())

    def test_read_file_paths(self):
        run = citycat_output.Run(self.folder)
        run.read_file_paths()
        self.assertIsInstance(run.file_paths, list)

    def test_to_netcdf(self):
        run = citycat_output.Run(self.folder)
        run.read_file_paths()
        run.to_netcdf(self.netcdf_path)
        ds = nc.Dataset(self.netcdf_path)
        self.assertIsNotNone(ds)
        ds.close()


if __name__ == '__main__':
    unittest.main()