"""バージョン管理モジュール

アプリケーション、インストーラー、アップデーター間で一貫した
バージョン管理を提供するモジュールです。
"""
import re
from pathlib import Path
from typing import Optional


class VersionManager:
    """バージョン管理クラス

    バージョン番号の読み取り、更新、検証を行います。
    """

    @staticmethod
    def get_version_from_pyproject() -> Optional[str]:
        """pyproject.tomlからバージョンを取得

        Returns:
            バージョン番号。見つからない場合はNone
        """
        pyproject_path = Path(__file__).parent.parent.parent.parent / "pyproject.toml"
        if not pyproject_path.exists():
            return None

        content = pyproject_path.read_text(encoding="utf-8")
        match = re.search(r'version = "([^"]+)"', content)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def get_version_from_init() -> Optional[str]:
        """__init__.pyからバージョンを取得

        Returns:
            バージョン番号。見つからない場合はNone
        """
        try:
            from n_line import __version__

            return __version__
        except ImportError:
            return None

    @staticmethod
    def get_version_from_installer() -> Optional[str]:
        """installer.issからバージョンを取得

        Returns:
            バージョン番号。見つからない場合はNone
        """
        installer_path = Path(__file__).parent.parent.parent.parent / "installer.iss"
        if not installer_path.exists():
            return None

        content = installer_path.read_text(encoding="utf-8")
        match = re.search(r'#define AppVersion "([^"]+)"', content)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def verify_version_consistency() -> tuple[bool, dict[str, Optional[str]]]:
        """すべてのファイルでバージョンが一致しているか確認

        Returns:
            (一致しているか, バージョン情報の辞書)
        """
        versions = {
            "pyproject.toml": VersionManager.get_version_from_pyproject(),
            "__init__.py": VersionManager.get_version_from_init(),
            "installer.iss": VersionManager.get_version_from_installer(),
        }

        # Noneを除外したバージョンのセット
        valid_versions = {v for v in versions.values() if v is not None}

        if len(valid_versions) == 0:
            return False, versions

        if len(valid_versions) > 1:
            return False, versions

        return True, versions

    @staticmethod
    def update_all_versions(new_version: str) -> dict[str, bool]:
        """すべてのファイルのバージョンを更新

        Args:
            new_version: 新しいバージョン番号

        Returns:
            更新結果の辞書（ファイル名: 成功したか）
        """
        results = {}

        # pyproject.tomlを更新
        pyproject_path = Path(__file__).parent.parent.parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text(encoding="utf-8")
            new_content = re.sub(
                r'version = "([^"]+)"', f'version = "{new_version}"', content
            )
            pyproject_path.write_text(new_content, encoding="utf-8")
            results["pyproject.toml"] = True
        else:
            results["pyproject.toml"] = False

        # __init__.pyを更新
        init_path = Path(__file__).parent.parent / "__init__.py"
        if init_path.exists():
            content = init_path.read_text(encoding="utf-8")
            new_content = re.sub(
                r'__version__ = "([^"]+)"',
                f'__version__ = "{new_version}"',
                content,
            )
            init_path.write_text(new_content, encoding="utf-8")
            results["__init__.py"] = True
        else:
            results["__init__.py"] = False

        # installer.issを更新
        installer_path = Path(__file__).parent.parent.parent.parent / "installer.iss"
        if installer_path.exists():
            content = installer_path.read_text(encoding="utf-8")
            new_content = re.sub(
                r'#define AppVersion "([^"]+)"',
                f'#define AppVersion "{new_version}"',
                content,
            )
            installer_path.write_text(new_content, encoding="utf-8")
            results["installer.iss"] = True
        else:
            results["installer.iss"] = False

        return results

