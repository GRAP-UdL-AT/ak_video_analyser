# -*- mode: python ; coding: utf-8 -*-
block_cipher = None
#todo: change automatically the user path
PATH = 'C:/Users/Usuari/development/ak_video_analyser/'

PROJECT_NAME='ak_video_analyser'
PROJECT_NAME_OUT = 'ak_video_analyser_f'
SRC_FOLDER='src'
CONF_FOLDER='conf'
GUI_ASSETS='gui_ext'
ASSETS_FOLDER='assets'

EXECUTABLE_NAME = 'ak_video_analyser_ex'
EXECUTABLE_VERSION_NUMBER = '_0.0.1'

a = Analysis(
    [ PATH+'/'+SRC_FOLDER+'/'+PROJECT_NAME+'/'+'__main__.py' ],
    pathex=[
        PATH+SRC_FOLDER,
        PATH+SRC_FOLDER+'/'+PROJECT_NAME+'/',
        PATH+SRC_FOLDER+PROJECT_NAME+'/'+CONF_FOLDER+'/',
        PATH+SRC_FOLDER+'/'+GUI_ASSETS+'/',
        PATH+SRC_FOLDER+'/'+GUI_ASSETS+'/'+ASSETS_FOLDER
        ],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=EXECUTABLE_NAME+EXECUTABLE_VERSION_NUMBER,  # YOUR EXECUTABLE NAME HERE
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=PATH+SRC_FOLDER+'/'+GUI_ASSETS+'/'+ASSETS_FOLDER+'/'+'icon_app.png'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=PROJECT_NAME_OUT, # YOUR EXECUTABLE FOLDER HERE
)
