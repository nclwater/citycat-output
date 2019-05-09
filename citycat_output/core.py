import netCDF4 as nc
import pandas as pd
import os
import numpy as np


class Run:
    def __init__(self, path):
        self.folder_path = path
        self.file_paths = None
        self.variables = None
        self.locations = None
        self.x = None
        self.y = None
        self.x_size = None
        self.y_size = None
        self.x_index = None
        self.y_index = None
        self.depth = None
        self.x_velocity = None
        self.y_velocity = None
        self.times = None
        self.steps = None

        self.read_file_paths()
        self.get_steps()
        self.get_times()

    def get_times(self):
        self.times = [path_to_time(path) for path in self.file_paths]

    def get_steps(self):
        self.steps = [path_to_step(path) for path in self.file_paths]

    def read_variables(self, i):
        self.variables = pd.read_csv(self.file_paths[i], usecols=['Depth', 'Vx', 'Vy'], delimiter=' ')

    def read_locations(self):
        self.locations = pd.read_csv(self.file_paths[0], usecols=['XCen', 'YCen'], delimiter=' ')
        self.get_unique_coordinates()

    def get_unique_coordinates(self):
        assert self.locations is not None, 'Locations must be read in first'

        self.x, self.x_index = np.unique(self.locations['XCen'].values, return_inverse=True)
        self.y, self.y_index = np.unique(self.locations['YCen'].values, return_inverse=True)

        self.x_size = len(self.x)
        self.y_size = len(self.y)

    def create_arrays(self):
        assert self.locations is not None, 'Locations must be read in first'

        self.depth = np.full((self.y_size, self.x_size), float('NaN'))
        self.x_velocity = np.full((self.y_size, self.x_size), float('NaN'))
        self.y_velocity = np.full((self.y_size, self.x_size), float('NaN'))

    def set_array_values(self):
        assert self.depth is not None, 'Arrays must be created first'

        self.depth[self.y_index, self.x_index] = self.variables.Depth.values
        self.x_velocity[self.y_index, self.x_index] = self.variables.Vx.values
        self.y_velocity[self.y_index, self.x_index] = self.variables.Vy.values

    def read_file_paths(self):

        self.file_paths = [os.path.join(self.folder_path, rsl) for rsl in os.listdir(self.folder_path)
                           if rsl.lower().endswith('.rsl')]

        self.file_paths.sort(key=path_to_step)

    def to_netcdf(self, path=None, srid=None):

        if self.file_paths is None:
            self.read_file_paths()

        if path is None:
            path = os.path.join(os.path.dirname(self.folder_path), os.path.basename(self.folder_path) + '.nc')

        if os.path.exists(path):
            os.remove(path)

        group = nc.Dataset(path, "w", format="NETCDF4")

        self.read_locations()
        self.create_arrays()

        group.createDimension("time", None)
        group.createDimension("x", self.x_size)
        group.createDimension("y", self.y_size)

        depth = group.createVariable("depth", "f4", ("time", "y", "x",), zlib=True, least_significant_digit=3)
        x_vel = group.createVariable("x_vel", "f4", ("time", "y", "x",), zlib=True, least_significant_digit=3)
        y_vel = group.createVariable("y_vel", "f4", ("time", "y", "x",), zlib=True, least_significant_digit=3)
        x_variable = group.createVariable("x", "f4", ("x",), zlib=True)
        y_variable = group.createVariable("y", "f4", ("y",), zlib=True)
        times = group.createVariable("time", "f8", ("time",), zlib=True)

        for i in range(len(self.file_paths)):

            self.read_variables(i)
            self.set_array_values()

            depth[self.steps[i], :, :] = self.depth
            x_vel[self.steps[i], :, :] = self.x_velocity
            y_vel[self.steps[i], :, :] = self.y_velocity

        times[:] = self.times
        x_variable[:] = self.x
        y_variable[:] = self.y

        if srid is not None:
            import osr
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(srid)
            depth.setncattr('grid_mapping', 'spatial_ref')
            x_vel.setncattr('grid_mapping', 'spatial_ref')
            y_vel.setncattr('grid_mapping', 'spatial_ref')

            crs = group.createVariable('spatial_ref', 'i4')
            crs.spatial_ref = srs.ExportToWkt()

        group.close()


def path_to_step(path):
    return int(os.path.basename(path).split('min')[0].split('_')[2][1:])


def path_to_time(path):
    return int(os.path.basename(path).split('min')[0].split('_')[-1].split('.')[0])
