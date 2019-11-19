# -*- mode: python -*-
import subprocess

block_cipher = None

version = subprocess.check_output("git describe").strip().decode()

a = Analysis(['ui.py', 'ui.spec'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=['cftime'],
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
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
