# -*- mode: python -*-
import subprocess
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

version = subprocess.check_output("git describe").strip().decode()

osgeo_binaries = collect_data_files('osgeo', include_py_files=True)

block_cipher = None

binaries = []
for p, lib in osgeo_binaries:
    if '.pyd' in p:
        binaries.append((p, '.'))

a = Analysis(['ui.py', 'ui.spec'],
             pathex=['.'],
             binaries=binaries,
             datas=[],
             hiddenimports=['cftime', 'rasterio._shim', 'rasterio.control', 'rasterio._io', 'rasterio.sample',
                            'rasterio.vrt'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='CityCAT-Output-Converter-{}'.format(version),
          debug=True,
          strip=False,
          upx=False,
          # upx_exclude=['vcruntime140.dll', 'qwindows.dll'],
          runtime_tmpdir=None,
          console=True )
