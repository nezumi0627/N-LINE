"""バージョン番号の一貫性をチェックするスクリプト"""
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def get_version_from_pyproject() -> str:
    """pyproject.tomlからバージョンを取得"""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    if not pyproject_path.exists():
        return None
    
    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'version = "([^"]+)"', content)
    if match:
        return match.group(1)
    return None


def get_version_from_init() -> str:
    """__init__.pyからバージョンを取得"""
    init_path = PROJECT_ROOT / "src" / "n_line" / "__init__.py"
    if not init_path.exists():
        return None
    
    content = init_path.read_text(encoding="utf-8")
    match = re.search(r'__version__ = "([^"]+)"', content)
    if match:
        return match.group(1)
    return None


def get_version_from_changelog() -> str:
    """CHANGELOG.mdから最新バージョンを取得"""
    changelog_path = PROJECT_ROOT / "CHANGELOG.md"
    if not changelog_path.exists():
        return None
    
    content = changelog_path.read_text(encoding="utf-8")
    # 最初の [x.y.z] 形式のバージョンを探す
    match = re.search(r'^## \[([0-9]+\.[0-9]+\.[0-9]+)\]', content, re.MULTILINE)
    if match:
        return match.group(1)
    return None


def main():
    """メイン関数"""
    pyproject_version = get_version_from_pyproject()
    init_version = get_version_from_init()
    changelog_version = get_version_from_changelog()
    
    versions = {
        "pyproject.toml": pyproject_version,
        "__init__.py": init_version,
        "CHANGELOG.md": changelog_version,
    }
    
    # Noneを除外したバージョンのセット
    valid_versions = {v for v in versions.values() if v is not None}
    
    if len(valid_versions) == 0:
        print("警告: バージョンが見つかりませんでした")
        sys.exit(1)
    
    if len(valid_versions) > 1:
        print("エラー: バージョン番号が一致しません")
        for file, version in versions.items():
            if version:
                print(f"  {file}: {version}")
        sys.exit(1)
    
    version = valid_versions.pop()
    print(f"✓ バージョン番号は一貫しています: {version}")
    sys.exit(0)


if __name__ == "__main__":
    main()

