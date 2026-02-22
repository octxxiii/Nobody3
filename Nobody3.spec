# -*- mode: python ; coding: utf-8 -*-
# Nobody 3 - PyInstaller spec: single exe (onefile) for Windows.
# Build: python -m PyInstaller --noconfirm Nobody3.spec
# Output: dist/Nobody3.exe (one file, ready for GitHub release)
# Put icon.ico in project root for exe + window icon.

import os

block_cipher = None

project_root = '.'
# Bundle icon.ico so app and exe can use it (extracted to _MEIPASS at runtime)
icon_datas = [('icon.ico', '.')] if os.path.isfile(os.path.join(project_root, 'icon.ico')) else []

a = Analysis(
    ['Nobody3.py'],
    pathex=[project_root],
    binaries=[],
    datas=icon_datas,
    hiddenimports=[
        'resources_rc',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngineCore',
        'PyQt5.QtWebChannel',
        'PyQt5.QtWebEngine',
        'yt_dlp',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['pyi_rth_qtwebengine.py'],
    excludes=[
        'tkinter', 'matplotlib', 'numpy', 'pandas', 'PIL', 'scipy', 'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Nobody3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_root, 'icon.ico') if icon_datas else None,
)
