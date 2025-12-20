"""
PyInstaller hook for customtkinter
This hook ensures that customtkinter and all its dependencies are included
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
from pathlib import Path

# customtkinterのすべてのサブモジュールを収集
try:
    hiddenimports = collect_submodules('customtkinter')
except Exception:
    # collect_submodulesが失敗した場合、手動で収集
    hiddenimports = ['customtkinter']
    try:
        import customtkinter
        import pkgutil
        customtkinter_path = Path(customtkinter.__file__).parent
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=[str(customtkinter_path)],
            prefix='customtkinter.'
        ):
            hiddenimports.append(modname)
    except ImportError:
        pass

# customtkinterのデータファイルを収集
datas = []
try:
    # まずPyInstallerのユーティリティを試す
    datas = collect_data_files('customtkinter', includes=['**/*'])
except Exception:
    # collect_data_filesが失敗した場合、手動で追加
    try:
        import customtkinter
        customtkinter_path = Path(customtkinter.__file__).parent.resolve()
        # パッケージ全体を含める
        datas.append((str(customtkinter_path), 'customtkinter'))
    except ImportError:
        # customtkinterが見つからない場合、site-packagesから探す
        import site
        for site_packages in site.getsitepackages():
            customtkinter_path = Path(site_packages) / 'customtkinter'
            if customtkinter_path.exists():
                datas.append((str(customtkinter_path), 'customtkinter'))
                break

