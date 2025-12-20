# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller設定ファイル（フォルダモード）
N-LINEアプリケーションをフォルダモードでパッケージ化
フォルダモードの方がcustomtkinterなどの問題が少ない
"""

import sys
import os
from pathlib import Path

# WindowsでUTF-8出力を保証するための設定
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

block_cipher = None

# プロジェクトルート（specファイルのディレクトリ）
# SPECPATHはPyInstallerが提供する変数
try:
    # PyInstallerがSPECPATHを提供している場合
    if 'SPECPATH' in globals():
        spec_file_path = os.path.abspath(SPECPATH)
        project_root = Path(os.path.dirname(spec_file_path))
    else:
        # フォールバック: 現在の作業ディレクトリからN-LINEプロジェクトを探す
        # build_installer.pyがC:\projects\N-LINEから実行されることを前提とする
        cwd = Path(os.getcwd())
        # N-LINEプロジェクトの特徴的なファイル/フォルダを探す
        if (cwd / 'src' / 'n_line').exists():
            project_root = cwd
        elif (cwd / 'N-LINE' / 'src' / 'n_line').exists():
            project_root = cwd / 'N-LINE'
        elif (cwd.parent / 'src' / 'n_line').exists():
            project_root = cwd.parent
        else:
            # 環境変数から取得（build_installer.pyが設定）
            project_root_env = os.environ.get('PROJECT_ROOT')
            if project_root_env:
                project_root = Path(project_root_env)
            else:
                project_root = cwd
except Exception as e:
    # 最後の手段: 現在の作業ディレクトリを使用
    project_root = Path(os.getcwd())
    print(f"警告: project_rootの解決に失敗しました: {e}")

# 絶対パスに変換
project_root = project_root.resolve()
print(f"デバッグ: project_root = {project_root}")

# データファイルとhiddenimportsを初期化
datas = []
hiddenimports = []

# customtkinterを確実に含める
# 仮想環境のsite-packagesパスを直接指定（--add-data相当）
customtkinter_path = None
customtkinter_site_packages = None

# 方法1: 直接インポートしてパスを取得（最も確実）
# PyInstallerが実行される時点で、仮想環境がアクティブでない可能性があるため、
# まずインポートを試みる
try:
    import customtkinter
    customtkinter_path = Path(customtkinter.__file__).parent.resolve()
    customtkinter_site_packages = str(customtkinter_path.parent.resolve())
    print(f"✓ customtkinterをインポートから見つけました: {customtkinter_path}")
except ImportError:
    # 方法2: プロジェクト内のvenvを直接指定
    # 環境変数からプロジェクトルートを取得
    project_root_from_env = os.environ.get('PROJECT_ROOT')
    if project_root_from_env:
        project_root_actual = Path(project_root_from_env).resolve()
    else:
        # 現在の作業ディレクトリからN-LINEプロジェクトを探す
        cwd = Path(os.getcwd())
        if (cwd / 'src' / 'n_line').exists():
            project_root_actual = cwd
        elif (cwd.parent / 'src' / 'n_line').exists():
            project_root_actual = cwd.parent
        else:
            project_root_actual = project_root
    
    # venvと.venvの両方を確認
    for venv_dir in ['venv', '.venv']:
        venv_customtkinter = project_root_actual / venv_dir / 'Lib' / 'site-packages' / 'customtkinter'
        if venv_customtkinter.exists() and (venv_customtkinter / '__init__.py').exists():
            customtkinter_path = venv_customtkinter.resolve()
            customtkinter_site_packages = str(customtkinter_path.parent.resolve())
            print(f"✓ customtkinterを{venv_dir}パスから見つけました: {customtkinter_path}")
            break
    
    if customtkinter_path is None:
        # 方法3: site-packagesから探す
        import site
        for site_packages in site.getsitepackages():
            potential_path = Path(site_packages).resolve() / 'customtkinter'
            if potential_path.exists() and (potential_path / '__init__.py').exists():
                customtkinter_path = potential_path.resolve()
                customtkinter_site_packages = str(potential_path.parent.resolve())
                print(f"✓ customtkinterをsite-packagesから見つけました: {customtkinter_path}")
                break

if customtkinter_path is None:
    print("警告: customtkinterが見つかりません！")
    print("仮想環境をアクティブにして、customtkinterがインストールされているか確認してください。")
    print("ビルドを続行しますが、customtkinterが含まれない可能性があります。")
else:
    # customtkinterパッケージ全体を_internalに配置（重要！）
    # PyInstallerの--add-data相当: ("パス", "customtkinter")
    # これにより、.json、.otfなどのデータファイルも含まれる
    # Windowsではセミコロン区切りだが、specファイルではタプル形式
    datas.append((str(customtkinter_path), 'customtkinter'))
    print(f"  datasに追加: {customtkinter_path} -> customtkinter")
    
    # PyInstallerのユーティリティを使用してサブモジュールを収集
    try:
        from PyInstaller.utils.hooks import collect_submodules, collect_data_files
        
        # すべてのサブモジュールを収集
        submodules = collect_submodules('customtkinter')
        hiddenimports.extend(submodules)
        
        # データファイルも収集（重複を避ける）
        try:
            data_files = collect_data_files('customtkinter', includes=['**/*'])
            # 既に追加したパッケージ全体と重複しないようにフィルタリング
            for df in data_files:
                if df not in datas:
                    datas.append(df)
        except Exception:
            pass
        
    except ImportError:
        # PyInstallerのユーティリティが使えない場合、手動で収集
        import pkgutil
        try:
            for importer, modname, ispkg in pkgutil.walk_packages(
                path=[str(customtkinter_path)],
                prefix='customtkinter.'
            ):
                if modname not in hiddenimports:
                    hiddenimports.append(modname)
        except Exception as e:
            print(f"警告: サブモジュールの収集中にエラー: {e}")
    
    print(f"  サブモジュール数: {len([m for m in hiddenimports if m.startswith('customtkinter')])}")

# customtkinterをhiddenimportsに確実に追加
if 'customtkinter' not in hiddenimports:
    hiddenimports.insert(0, 'customtkinter')

# 基本的なモジュールを追加
# 実際に使用しているモジュールのみを追加
basic_imports = [
    'PIL',
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageTk',
    'psutil',
    # pywin32のモジュール（実際に使用しているもののみ）
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

# pywin32のモジュールを確実に含める
# win32gui, win32con, win32processは.pydファイルなので、確実に含める必要がある
binaries = []

# 方法1: 直接インポートを試みる
win32_path = None
win32_site_packages = None
try:
    # win32パッケージ自体は__file__がNoneになる場合があるため、win32guiなどを使用
    import win32gui
    win32_path = Path(win32gui.__file__).parent.resolve()
    win32_site_packages = str(win32_path.parent.resolve())
    print(f"✓ win32パッケージをインポートから見つけました: {win32_path}")
except (ImportError, AttributeError):
    try:
        import win32api
        win32_path = Path(win32api.__file__).parent.resolve()
        win32_site_packages = str(win32_path.parent.resolve())
        print(f"✓ win32パッケージをwin32apiから見つけました: {win32_path}")
    except (ImportError, AttributeError):
        # 方法2: プロジェクト内のvenvから探す
        project_root_from_env = os.environ.get('PROJECT_ROOT')
        if project_root_from_env:
            project_root_actual = Path(project_root_from_env).resolve()
        else:
            cwd = Path(os.getcwd())
            if (cwd / 'src' / 'n_line').exists():
                project_root_actual = cwd
            elif (cwd.parent / 'src' / 'n_line').exists():
                project_root_actual = cwd.parent
            else:
                project_root_actual = project_root
        
        # venvと.venvの両方を確認
        for venv_dir in ['venv', '.venv']:
            venv_win32 = project_root_actual / venv_dir / 'Lib' / 'site-packages' / 'win32'
            if venv_win32.exists():
                win32_path = venv_win32.resolve()
                win32_site_packages = str(win32_path.parent.resolve())
                print(f"✓ win32パッケージを{venv_dir}パスから見つけました: {win32_path}")
                break
        
        if win32_path is None:
            # 方法3: site-packagesから探す
            import site
            for site_packages in site.getsitepackages():
                potential_win32 = Path(site_packages).resolve() / 'win32'
                if potential_win32.exists():
                    win32_path = potential_win32.resolve()
                    win32_site_packages = str(potential_win32.parent.resolve())
                    print(f"✓ win32パッケージをsite-packagesから見つけました: {win32_path}")
                    break

if win32_path:
    # win32パッケージ全体をdatasに追加（.pydファイル、.pyファイルも含まれる）
    # win32conはwin32\lib\win32con.pyにあるため、win32パッケージ全体を含める必要がある
    datas.append((str(win32_path), 'win32'))
    print(f"  datasに追加: {win32_path} -> win32")
    
    # pywin32_system32も追加（DLLファイルが含まれる）
    pywin32_system32_path = win32_path.parent / 'pywin32_system32'
    if pywin32_system32_path.exists():
        datas.append((str(pywin32_system32_path), 'pywin32_system32'))
        print(f"  pywin32_system32も追加: {pywin32_system32_path}")
    
    # win32comとpythoncomは使用していないため、追加しない
else:
    print("警告: win32パッケージが見つかりません！")
    print("pywin32がインストールされているか確認してください。")

# pathexにcustomtkinterとwin32のsite-packagesを追加
pathex_list = [str(project_root), str(project_root / 'src')]
if customtkinter_site_packages and customtkinter_site_packages not in pathex_list:
    pathex_list.append(customtkinter_site_packages)
if win32_site_packages and win32_site_packages not in pathex_list:
    pathex_list.append(win32_site_packages)

a = Analysis(
    ['src/n_line/__main__.py'],
    pathex=pathex_list,
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[str(project_root)],  # hookファイルを使用
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
    icon=None,
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
