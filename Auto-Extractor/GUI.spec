# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['GUI.py'],
             pathex=['T:\\current\\Users\\Staff\\Jiztom\\Python_Projects\\Image_Extraction_Template\\Multi-OS'],
             binaries=[],
             datas=[('tractor-512.ico', '.'),('parameters.xml', '.'),('hand_icon.ico', '.')],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name = 'RW Auto Extractor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon= 'tractor-512.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='GUI')
