# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller設定ファイル
N-LINEアプリケーションを実行ファイルにパッケージ化
"""

import sys
import os
from pathlib import Path

block_cipher = None

# プロジェクトルート（specファイルのディレクトリ）
project_root = Path(os.path.dirname(os.path.abspath(SPECPATH)))

# 仮想環境のsite-packagesを検出
import site
venv_site_packages = None
for site_pkg in site.getsitepackages():
    # 仮想環境のsite-packagesを優先的に使用
    if 'venv' in str(site_pkg) or 'virtualenv' in str(site_pkg):
        venv_site_packages = site_pkg
        break
# 見つからない場合は最初のsite-packagesを使用
if venv_site_packages is None and site.getsitepackages():
    venv_site_packages = site.getsitepackages()[0]

# データファイル（必要に応じて追加）
# customtkinterのアセットファイルを含める
datas = []
hiddenimports = []

# customtkinterを明示的に含める
# PyInstallerがcustomtkinterを検出できない場合があるため、明示的に指定
# インポートせずにパスから直接探す（PyInstallerの実行環境でcustomtkinterが見つからない場合があるため）
customtkinter_pathex = None
customtkinter_path = None

# 仮想環境のsite-packagesを優先して探す
search_paths = []
if venv_site_packages:
    search_paths.append(Path(venv_site_packages))
# プロジェクト内のvenvも確認
venv_path = project_root / 'venv' / 'Lib' / 'site-packages'
if venv_path.exists():
    search_paths.append(venv_path)
# システムのsite-packagesも確認
for site_pkg in site.getsitepackages():
    search_paths.append(Path(site_pkg))

# customtkinterを探す
for site_packages in search_paths:
    if site_packages is None or not site_packages.exists():
        continue
    potential_path = site_packages / 'customtkinter'
    if potential_path.exists() and (potential_path / '__init__.py').exists():
        customtkinter_path = potential_path
        customtkinter_pathex = str(site_packages)
        # パッケージ全体を_internalに配置（customtkinterフォルダとして）
        datas.append((str(customtkinter_path), 'customtkinter'))
        print(f"✓ customtkinterを見つけました: {customtkinter_path}")
        break

if customtkinter_path is None:
    print("警告: customtkinterが見つかりません")
else:
    # すべてのサブモジュールを収集（パスから直接）
    import pkgutil
    try:
        # customtkinterパッケージ内のすべてのモジュールを収集
        for item in customtkinter_path.rglob('*.py'):
            if item.name == '__init__.py':
                continue
            rel_path = item.relative_to(customtkinter_path)
            module_name = 'customtkinter.' + '.'.join(rel_path.parts[:-1] + (rel_path.stem,))
            if module_name not in hiddenimports:
                hiddenimports.append(module_name)
    except Exception as e:
        print(f"警告: サブモジュールの収集中にエラー: {e}")

# 基本的なモジュールを追加（重複を避ける）
basic_imports = [
    'customtkinter',
    'PIL',
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageTk',
    'psutil',
    'win32gui',
    'win32con',
    'win32process',
    'uiautomation',
    'keyboard',
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'threading',
    'datetime',
    'shlex',
    'urllib',
    'urllib.request',
    'urllib.error',
    'json',
]

# 重複を避けて追加
for imp in basic_imports:
    if imp not in hiddenimports:
        hiddenimports.append(imp)

# customtkinterを確実に含めるため、hiddenimportsに追加（重要！）
if 'customtkinter' not in hiddenimports:
    hiddenimports.insert(0, 'customtkinter')

# pathexにcustomtkinterのパスを追加（重要！）
pathex_list = [str(project_root), str(project_root / 'src')]
if customtkinter_pathex and customtkinter_pathex not in pathex_list:
    pathex_list.append(customtkinter_pathex)

a = Analysis(
    ['src/n_line/__main__.py'],
    pathex=pathex_list,  # customtkinterのパスを含める
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[str(project_root)],  # プロジェクトルートのhookを使用
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# フォルダモード（ワンファイルモードより確実）
exe = EXE(
    pyz,
    a.scripts,
    [],  # 空のリストでバイナリを除外
    exclude_binaries=True,  # バイナリを除外してフォルダモードに
    name='N-LINE',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUIアプリケーションなのでコンソールを非表示
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # アイコンファイルがある場合は指定
)

# フォルダモード用のCOLLECT
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='N-LINE',
)

