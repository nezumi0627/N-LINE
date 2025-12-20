"""ビルド前のテストスクリプト

実行ファイルを作成する前に、必要なモジュールが正しくインポートできるか
テストします。
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

# WindowsでUTF-8出力を保証するための設定
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def test_imports():
    """必要なモジュールがインポートできるかテスト"""
    print("必要なモジュールのインポートをテスト中...\n")

    modules = [
        "customtkinter",
        "PIL",
        "psutil",
        "win32gui",
        "win32con",
        "win32process",
        "uiautomation",
        "keyboard",
        "tkinter",
    ]

    failed = []

    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            failed.append(module)

    print()

    if failed:
        print(f"エラー: {len(failed)}個のモジュールがインポートできませんでした:")
        for module in failed:
            print(f"  - {module}")
        print("\n以下のコマンドで依存関係をインストールしてください:")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("✓ すべてのモジュールが正常にインポートできました")
        return True


def test_customtkinter_assets():
    """customtkinterのアセットファイルが存在するかテスト"""
    print("\ncustomtkinterのアセットファイルを確認中...\n")

    try:
        import customtkinter

        customtkinter_path = Path(customtkinter.__file__).parent
        assets_path = customtkinter_path / "assets"

        if assets_path.exists():
            print(f"✓ アセットディレクトリが見つかりました: {assets_path}")
            asset_files = list(assets_path.rglob("*"))
            print(f"  ファイル数: {len([f for f in asset_files if f.is_file()])}")
            return True
        else:
            print(f"✗ アセットディレクトリが見つかりません: {assets_path}")
            return False
    except ImportError:
        print("✗ customtkinterがインポートできません")
        return False


def main():
    """メイン関数"""
    print("=" * 60)
    print("N-LINE ビルド前テスト")
    print("=" * 60)
    print()

    # パスを追加
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

    # テスト実行
    imports_ok = test_imports()
    assets_ok = test_customtkinter_assets()

    print()
    print("=" * 60)

    if imports_ok and assets_ok:
        print("✓ すべてのテストが成功しました")
        print("実行ファイルの作成を続行できます")
        return 0
    else:
        print("✗ テストが失敗しました")
        print("問題を解決してから再試行してください")
        return 1


if __name__ == "__main__":
    sys.exit(main())
