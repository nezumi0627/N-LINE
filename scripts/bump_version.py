"""バージョン番号を更新するスクリプト"""

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# WindowsでUTF-8出力を保証するための設定
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def get_current_version() -> str:
    """現在のバージョンを取得"""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'version = "([^"]+)"', content)
    if match:
        return match.group(1)
    return None


def update_pyproject(version: str) -> bool:
    """pyproject.tomlのバージョンを更新"""
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    if not pyproject_path.exists():
        return False

    content = pyproject_path.read_text(encoding="utf-8")
    new_content = re.sub(r'version = "([^"]+)"', f'version = "{version}"', content)

    pyproject_path.write_text(new_content, encoding="utf-8")
    return True


def update_init(version: str) -> bool:
    """__init__.pyのバージョンを更新"""
    init_path = PROJECT_ROOT / "src" / "n_line" / "__init__.py"

    if not init_path.exists():
        # __init__.pyが存在しない場合は作成
        content = f'"""N-LINE Package"""\n\n__version__ = "{version}"\n'
    else:
        content = init_path.read_text(encoding="utf-8")
        if "__version__" in content:
            new_content = re.sub(r'__version__ = "([^"]+)"', f'__version__ = "{version}"', content)
        else:
            new_content = content.rstrip() + f'\n\n__version__ = "{version}"\n'
        content = new_content

    init_path.write_text(content, encoding="utf-8")
    return True


def update_installer(version: str) -> bool:
    """installer.issのバージョンを更新"""
    installer_path = PROJECT_ROOT / "installer.iss"
    if not installer_path.exists():
        return False

    content = installer_path.read_text(encoding="utf-8")
    new_content = re.sub(
        r'#define AppVersion "([^"]+)"', f'#define AppVersion "{version}"', content
    )

    installer_path.write_text(new_content, encoding="utf-8")
    return True


def bump_version(current: str, bump_type: str) -> str:
    """バージョン番号を更新"""
    parts = current.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    return f"{major}.{minor}.{patch}"


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="バージョン番号を更新")
    parser.add_argument(
        "version",
        nargs="?",
        help="新しいバージョン番号（例: 0.3.0）または bump type（major, minor, patch）",
    )
    parser.add_argument(
        "--type",
        choices=["major", "minor", "patch"],
        help="バージョンの更新タイプ",
    )

    args = parser.parse_args()

    current_version = get_current_version()
    if not current_version:
        print("エラー: 現在のバージョンを取得できませんでした")
        sys.exit(1)

    if args.version:
        if args.version in ["major", "minor", "patch"]:
            new_version = bump_version(current_version, args.version)
        elif re.match(r"^\d+\.\d+\.\d+$", args.version):
            new_version = args.version
        else:
            print(f"エラー: 無効なバージョン形式: {args.version}")
            sys.exit(1)
    elif args.type:
        new_version = bump_version(current_version, args.type)
    else:
        print("エラー: バージョン番号または更新タイプを指定してください")
        sys.exit(1)

    print(f"バージョンを {current_version} から {new_version} に更新します")

    if update_pyproject(new_version):
        print("✓ pyproject.toml を更新しました")
    else:
        print("✗ pyproject.toml の更新に失敗しました")
        sys.exit(1)

    if update_init(new_version):
        print("✓ __init__.py を更新しました")
    else:
        print("✗ __init__.py の更新に失敗しました")
        sys.exit(1)

    if update_installer(new_version):
        print("✓ installer.iss を更新しました")
    else:
        print("⚠ installer.iss の更新に失敗しました（ファイルが存在しない可能性があります）")

    print(f"\nバージョン更新が完了しました: {new_version}")
    print("次に、CHANGELOG.mdを更新してください")


if __name__ == "__main__":
    main()
