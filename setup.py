from setuptools import setup

setup(name='citycatio',
      version='0.5.1',
      description='CityCAT extension to create inputs and convert outputs',
      url='https://github.com/nclwater/citycatio',
      author='Fergus McClean',
      author_email='fergus.mcclean@ncl.ac.uk',
      license='GPL-3.0',
      packages=['citycatio', 'citycatio.inputs'],
      zip_safe=False,
      install_requires=['gdal', 'geopandas', 'rasterio', 'netCDF4', 'pandas', 'numpy'])
