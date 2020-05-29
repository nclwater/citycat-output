import netCDF4 as nc
import pandas as pd
import os
import numpy as np
from gdal import osr
from datetime import datetime
import rasterio as rio
from rasterio.mask import mask
from shapely.geometry import box, mapping


datatype = "f4"
fill_value = nc.default_fillvals[datatype]


class Output:
    def __init__(self, path, read_dem=True, start_time=datetime(1, 1, 1)):
        self.folder_path = path
        self.read_dem = read_dem
        self.start_time = start_time
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
        self.max_depth = None
        self.times = None
        self.steps = None
        self.ds = None

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

        self.y_index = self.y_size - self.y_index - 1
        self.y = self.y[::-1]

    def create_arrays(self):
        assert self.locations is not None, 'Locations must be read in first'
        self.depth = np.full((self.y_size, self.x_size), fill_value)
        self.x_velocity = np.full((self.y_size, self.x_size), fill_value)
        self.y_velocity = np.full((self.y_size, self.x_size), fill_value)
        self.max_depth = np.full((self.y_size, self.x_size), fill_value)
        self.max_depth[self.y_index, self.x_index] = 0

    def set_array_values(self):
        assert self.depth is not None, 'Arrays must be created first'

        self.depth[self.y_index, self.x_index] = self.variables.Depth.values
        self.x_velocity[self.y_index, self.x_index] = self.variables.Vx.values
        self.y_velocity[self.y_index, self.x_index] = self.variables.Vy.values
        self.max_depth = np.max([self.max_depth, self.depth], axis=0)

    def read_file_paths(self):

        self.file_paths = [os.path.join(self.folder_path, rsl) for rsl in os.listdir(self.folder_path)
                           if rsl.lower().endswith('.rsl')]

        self.file_paths.sort(key=path_to_step)
        
    def read_dem_values(self):
        dem = rio.open(os.path.join(os.path.dirname(self.folder_path), 'Domain_DEM.ASC'))
        bbox = box(min(self.x), min(self.y), max(self.x), max(self.y))
        band, transform = mask(dem, shapes=[mapping(bbox)], crop=True, all_touched=True)
        band.astype(float)[band == dem.nodata] = fill_value
        dem_var = self.ds.createVariable('dem', datatype, dimensions=('y', 'x'))
        dem_var[:] = band
        return dem_var

    def to_netcdf(self, path: str = None, srid: int = None, attributes: dict = None):
        """Converts CityCAT results to a netCDF file

            :param path: path to store netCDF
            :param srid: EPSG Spatial Reference System Identifier of results files
            :param attributes: Dictionary of key-value pairs to store as netCDF attributes
                Keys must begin with an alphabetic character and be alphanumeric, underscore is allowed
        """

        if attributes is not None:
            for key in attributes.keys():
                assert type(key) == str, 'Attribute names must be strings, {} is a {}'.format(key, type(key))
                assert key[0].isalpha(), '{} must begin with an alphabetic character'.format(key)
                assert all(char == '_' or char.isdigit() or char.isalpha() for char in key), \
                    '{} is not alphanumeric (including underscore)'.format(key)
                val = attributes[key]
                allowed_attribute_types = [float, int,  str]
                try:
                    assert all(type(item) in allowed_attribute_types for item in val), \
                        'Attribute value types must be one of {}'.format(allowed_attribute_types)
                except TypeError:
                    assert type(val) in allowed_attribute_types, \
                        '{} type must be one of {}'.format(key, allowed_attribute_types)

        if path is None:
            path = os.path.join(os.path.dirname(self.folder_path), os.path.basename(self.folder_path) + '.nc')

        if os.path.exists(path):
            os.remove(path)

        self.ds = nc.Dataset(path, "w", format="NETCDF4")

        self.read_locations()
        self.create_arrays()

        self.ds.createDimension("time", None)
        self.ds.createDimension("x", self.x_size)
        self.ds.createDimension("y", self.y_size)

        dem = self.read_dem_values() if self.read_dem else None

        depth = self.ds.createVariable("depth", datatype, ("time", "y", "x",), zlib=True, least_significant_digit=3)
        x_vel = self.ds.createVariable("x_vel", datatype, ("time", "y", "x",), zlib=True, least_significant_digit=3)
        y_vel = self.ds.createVariable("y_vel", datatype, ("time", "y", "x",), zlib=True, least_significant_digit=3)
        max_depth = self.ds.createVariable("max_depth", datatype, ("y", "x",), zlib=True, least_significant_digit=3)
        x_variable = self.ds.createVariable("x", datatype, ("x",), zlib=True)
        y_variable = self.ds.createVariable("y", datatype, ("y",), zlib=True)
        times = self.ds.createVariable("time", "f8", ("time",), zlib=True)

        depth.units = 'm'
        x_vel.units = 'm/s'
        y_vel.units = 'm/s'
        max_depth.units = 'm'
        x_variable.units = 'm'
        y_variable.units = 'm'

        times.units = "minutes since {:%Y-%m-%d}".format(self.start_time).replace("-0", "-")
        times.calendar = "gregorian"
        times.long_name = "Time in minutes since {:%Y-%m-%d}".format(self.start_time).replace("-0", "-")

        for i in range(len(self.file_paths)):

            self.read_variables(i)
            self.set_array_values()

            depth[self.steps[i], :, :] = self.depth
            x_vel[self.steps[i], :, :] = self.x_velocity
            y_vel[self.steps[i], :, :] = self.y_velocity

        max_depth[:] = self.max_depth

        times[:] = self.times
        x_variable[:] = self.x
        y_variable[:] = self.y

        if srid is not None:
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(srid)
            depth.grid_mapping = 'crs'
            x_vel.grid_mapping = 'crs'
            y_vel.grid_mapping = 'crs'
            max_depth.grid_mapping = 'crs'
            if dem is not None:
                dem.grid_mapping = 'crs'

            crs = self.ds.createVariable('crs', 'i4')
            crs.spatial_ref = srs.ExportToWkt()
            crs.grid_mapping_name = srs.GetAttrValue('projection').lower()
            crs.scale_factor_at_central_meridian = srs.GetProjParm('scale_factor')
            crs.longitude_of_central_meridian = srs.GetProjParm('central_meridian')
            crs.latitude_of_projection_origin = srs.GetProjParm('latitude_of_origin')
            crs.false_easting = srs.GetProjParm('false_easting')
            crs.false_northing = srs.GetProjParm('false_northing')

        self.ds.Conventions = 'CF-1.6'
        self.ds.institution = 'Newcastle University'
        self.ds.source = 'CityCAT Model Results'
        self.ds.references = 'Glenis, V., Kutija, V. & Kilsby, C.G. (2018) '\
                        'A fully hydrodynamic urban flood modelling system '\
                        'representing buildings, green space and interventions. '\
                        'Environmental Modelling and Software. 109 (August), 272–292'

        self.ds.title = 'CityCAT Model Results'
        self.ds.history = 'Created {}'.format(datetime.now())

        if attributes is not None:
            for key in attributes.keys():
                self.ds.setncattr(key, attributes[key])

        self.ds.close()


def path_to_step(path):
    return int(os.path.basename(path).split('min')[0].split('_')[2][1:])


def path_to_time(path):
    return int(os.path.basename(path).split('min')[0].split('_')[-1].split('.')[0])