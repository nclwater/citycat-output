from setuptools import setup

setup(name='citycat_output',
      version='0.1.1',
      description='Convert CityCAT outputs to netCDF',
      url='https://github.com/nclwater/citycat-output',
      author='Fergus McClean',
      author_email='fergus.mcclean@ncl.ac.uk',
      license='GPL-3.0',
      packages=['citycat_output'],
      zip_safe=False,
      install_requires=['netCDF4',
                        'pandas',
                        'gdal'])
