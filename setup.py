from setuptools import setup

setup(name='citycat_output',
      version='0.1.0',
      description='Convert CityCAT hydrodynamic model outputs',
      url='https://github.com/fmcclean/citycat_output',
      author='Fergus McClean',
      author_email='fergus.mcclean@ncl.ac.uk',
      license='MIT',
      packages=['citycat_output'],
      zip_safe=False,
      install_requires=['netCDF4',
                        'pandas',
                        'gdal'])
