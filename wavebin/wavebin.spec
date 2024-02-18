# -*- mode: python ; coding: utf-8 -*-

arch = 'x86_64'
ver = 3.0
name = f'wavebin-{ver}.{arch}'

a = Analysis(
    ['__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('interface/assets', 'wavebin/interface/assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=arch,
    codesign_identity=None,
    entitlements_file=None,
    icon='interface/assets/icon-multi.ico',
    version='wavebin.rc'
)

app = BUNDLE(
    exe,
    name='wavebin.app',
    icon='interface/assets/icon-multi.ico',
    bundle_identifier=None
)
