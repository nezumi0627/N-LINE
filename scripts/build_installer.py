"""インストーラー作成スクリプト"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def check_pyinstaller() -> bool:
    """PyInstallerがインストールされているかチェック"""
    try:
        subprocess.run(
            ["pyinstaller", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_inno_setup() -> tuple[bool, str | None]:
    """Inno Setupがインストールされているかチェック"""
    # Inno Setupの一般的なインストールパス
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    for path in inno_paths:
        if Path(path).exists():
            return True, path
    
    # PATHから検索
    try:
        result = subprocess.run(
            ["where", "iscc"],
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout.strip():
            return True, result.stdout.strip()
    except subprocess.CalledProcessError:
        pass
    
    return False, None


def build_executable() -> bool:
    """PyInstallerで実行ファイルを作成"""
    print("PyInstallerで実行ファイルを作成中...")
    
    # ビルド前テストを実行
    print("\nビルド前テストを実行中...")
    test_result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "test_build.py")],
        cwd=PROJECT_ROOT,
    )
    if test_result.returncode != 0:
        print("\n⚠ 警告: ビルド前テストが失敗しましたが、続行します...\n")
    
    # フォルダモードのspecファイルを優先的に使用
    spec_file = PROJECT_ROOT / "n-line-onedir.spec"
    if not spec_file.exists():
        # フォールバック: 通常のspecファイル
        spec_file = PROJECT_ROOT / "n-line.spec"
        if not spec_file.exists():
            print(f"エラー: specファイルが見つかりません")
            return False
    
    try:
        # PyInstallerを実行（詳細な出力を有効化）
        # pyinstallerコマンドを使用（仮想環境内でインストールされている必要がある）
        env = os.environ.copy()
        # プロジェクトルートを環境変数として設定（specファイルから読み取れるように）
        env['PROJECT_ROOT'] = str(PROJECT_ROOT.resolve())
        
        result = subprocess.run(
            ["pyinstaller", "--clean", "-y", "--log-level=INFO", str(spec_file)],
            check=True,
            cwd=PROJECT_ROOT,
            capture_output=False,  # 出力を表示
            env=env,  # 環境変数を継承（仮想環境のPATHを含む）
        )
        print("✓ 実行ファイルの作成が完了しました")
        
        # 実行ファイルが作成されたか確認（フォルダモードまたはワンファイルモード）
        exe_path_single = PROJECT_ROOT / "dist" / "N-LINE.exe"  # ワンファイルモード
        exe_path_folder = PROJECT_ROOT / "dist" / "N-LINE" / "N-LINE.exe"  # フォルダモード
        
        if exe_path_single.exists():
            print(f"✓ 実行ファイル（ワンファイル）: {exe_path_single}")
            return True
        elif exe_path_folder.exists():
            print(f"✓ 実行ファイル（フォルダモード）: {exe_path_folder}")
            print(f"  フォルダ: {exe_path_folder.parent}")
            return True
        else:
            print("⚠ 警告: 実行ファイルが見つかりません")
            print(f"  確認したパス:")
            print(f"    - {exe_path_single}")
            print(f"    - {exe_path_folder}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"エラー: 実行ファイルの作成に失敗しました: {e}")
        print("\nトラブルシューティング:")
        print("1. 仮想環境がアクティブか確認")
        print("2. すべての依存関係がインストールされているか確認")
        print("3. docs/TROUBLESHOOTING_INSTALLER.md を参照")
        return False


def build_installer() -> bool:
    """Inno Setupでインストーラーを作成"""
    print("Inno Setupでインストーラーを作成中...")
    
    is_installed, iscc_path = check_inno_setup()
    if not is_installed:
        print("警告: Inno Setupが見つかりません")
        print("Inno Setupをインストールしてください: https://jrsoftware.org/isdl.php")
        print("または、実行ファイルのみを使用してください: python scripts/build_installer.py --exe-only")
        print("\n実行ファイルは dist/N-LINE.exe に作成されました")
        return False
    
    iss_file = PROJECT_ROOT / "installer.iss"
    if not iss_file.exists():
        print(f"エラー: {iss_file} が見つかりません")
        return False
    
    try:
        # 出力ディレクトリを作成
        output_dir = PROJECT_ROOT / "installer"
        output_dir.mkdir(exist_ok=True)
        
        result = subprocess.run(
            [iscc_path, str(iss_file)],
            check=True,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        
        # 出力を表示
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        # インストーラーファイルが作成されたか確認
        installer_files = list(output_dir.glob("*.exe"))
        if installer_files:
            print(f"✓ インストーラーの作成が完了しました")
            for installer_file in installer_files:
                print(f"  → {installer_file}")
            return True
        else:
            print("⚠ 警告: インストーラーファイルが見つかりません")
            print(f"  出力ディレクトリ: {output_dir}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"エラー: インストーラーの作成に失敗しました: {e}")
        if e.stdout:
            print(f"標準出力: {e.stdout}")
        if e.stderr:
            print(f"標準エラー: {e.stderr}")
        return False


def clean_build_files() -> None:
    """ビルドファイルをクリーンアップ"""
    print("ビルドファイルをクリーンアップ中...")
    
    dirs_to_remove = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_remove:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  削除: {dir_name}/")
    
    # .specファイルから生成されたファイルを削除
    for spec_file in PROJECT_ROOT.glob("*.spec"):
        if spec_file.name != "n-line.spec":
            spec_file.unlink()


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="N-LINEインストーラーを作成")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="ビルドファイルをクリーンアップ",
    )
    parser.add_argument(
        "--exe-only",
        action="store_true",
        help="実行ファイルのみ作成（インストーラーは作成しない）",
    )
    parser.add_argument(
        "--installer-only",
        action="store_true",
        help="インストーラーのみ作成（実行ファイルは既に存在することを前提）",
    )
    
    args = parser.parse_args()
    
    if args.clean:
        clean_build_files()
        return
    
    # PyInstallerのチェック
    if not args.installer_only:
        if not check_pyinstaller():
            print("エラー: PyInstallerがインストールされていません")
            print("インストール: pip install pyinstaller")
            sys.exit(1)
    
    # 実行ファイルの作成
    if not args.installer_only:
        if not build_executable():
            sys.exit(1)
    
    # インストーラーの作成
    if not args.exe_only:
        if not build_installer():
            sys.exit(1)
    
    print("\n✓ インストーラーの作成が完了しました！")
    installer_dir = PROJECT_ROOT / "installer"
    if installer_dir.exists():
        print(f"インストーラーは {installer_dir} にあります")


if __name__ == "__main__":
    main()

