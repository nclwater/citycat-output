import netCDF4 as nc
import pandas as pd
import os


class Results:
    def __init__(self, path):
        self.path = path
        self.variables = None
        self.locations = None
        self.df = None
        self.array = None
        self.x = None
        self.y = None
        self.x_size = None
        self.y_size = None
        self.time = int(os.path.basename(path).split('min')[0].split('_')[-1].split('.')[0])
        self.step = int(os.path.basename(path).split('min')[0].split('_')[2][1:])

    def read_variables(self):
        self.variables = pd.read_csv(self.path, usecols=['Depth', 'Vx', 'Vy'], delimiter=' ')
        return self.variables

    def read_locations(self):
        self.locations = pd.read_csv(self.path, usecols=['XCen', 'YCen'], delimiter=' ')
        self._get_xy()
        return self.locations

    def set_locations(self, locations):
        self.locations = locations
        self._get_xy()

    def _get_xy(self):
        assert self.locations is not None, 'Locations must be read in first'

        self.x = sorted(self.locations['XCen'].unique())
        self.y = sorted(self.locations['YCen'].unique())

        self.x_size = len(self.x)
        self.y_size = len(self.y)

    def create_array(self):
        assert self.locations is not None, 'Locations must be read in first'
        assert self.variables is not None, 'Variables must be read in first'

        self.df: pd.DataFrame = pd.concat([self.locations, self.variables], axis=1)
        self.array = self.df.pivot('XCen', 'YCen').values.transpose().reshape(-1, self.x_size, self.y_size)


class Run:
    def __init__(self, path):
        self.path = path
        self.results = None

    def get_results(self):

        self.results = [os.path.join(self.path, rsl) for rsl in os.listdir(self.path)
                        if rsl.lower().endswith('.rsl')]

        def get_step(path):
            return Results(path).step

        self.results.sort(key=get_step)

    def to_netcdf(self, path=None, srid=None):

        if self.results is None:
            self.get_results()

        if path is None:
            path = os.path.join(os.path.dirname(self.path), os.path.basename(self.path) + '.nc')

        if os.path.exists(path):
            os.remove(path)

        group = nc.Dataset(path, "w", format="NETCDF4")

        first_results = Results(self.results[0])
        first_results.read_locations()

        group.createDimension("time", None)
        group.createDimension("x", first_results.x_size)
        group.createDimension("y", first_results.y_size)

        depth = group.createVariable("depth", "f4", ("time", "y", "x",), zlib=True, least_significant_digit=3)
        x_vel = group.createVariable("x_vel", "f4", ("time", "y", "x",), zlib=True, least_significant_digit=3)
        y_vel = group.createVariable("y_vel", "f4", ("time", "y", "x",), zlib=True, least_significant_digit=3)
        x_variable = group.createVariable("x", "f4", ("x",), zlib=True)
        y_variable = group.createVariable("y", "f4", ("y",), zlib=True)
        times = group.createVariable("time", "f8", ("time",), zlib=True)

        for path in self.results:
            rsl = Results(path)
            rsl.read_variables()
            rsl.set_locations(first_results.locations)
            rsl.create_array()

            depth[rsl.step, :, :] = rsl.array[0]
            x_vel[rsl.step, :, :] = rsl.array[1]
            y_vel[rsl.step, :, :] = rsl.array[2]

        times[:] = [Results(path).time for path in self.results]
        x_variable[:] = first_results.x
        y_variable[:] = first_results.y

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
