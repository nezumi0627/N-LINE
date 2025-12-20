"""CHANGELOG.mdが更新されているかチェックするスクリプト"""
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def get_changed_files() -> list[str]:
    """変更されたファイルのリストを取得"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD", "origin/main"],
            capture_output=True,
            text=True,
            check=False,
        )
        files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        
        # マージベースがない場合、HEADと比較
        if not files:
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
                capture_output=True,
                text=True,
                check=False,
            )
            files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
        
        return files
    except subprocess.CalledProcessError:
        return []


def has_code_changes() -> bool:
    """コードに変更があるかチェック"""
    changed_files = get_changed_files()
    
    # コードファイルのパターン
    code_patterns = [
        r"\.py$",
        r"\.toml$",
        r"\.txt$",
    ]
    
    for file in changed_files:
        for pattern in code_patterns:
            if re.search(pattern, file):
                # CHANGELOG.mdやドキュメントの変更は除外
                if "CHANGELOG.md" not in file and "docs/" not in file:
                    return True
    
    return False


def changelog_updated() -> bool:
    """CHANGELOG.mdが更新されているかチェック"""
    changed_files = get_changed_files()
    return "CHANGELOG.md" in changed_files


def main():
    """メイン関数"""
    if not has_code_changes():
        print("コードに変更がないため、CHANGELOGのチェックをスキップします")
        sys.exit(0)
    
    if changelog_updated():
        print("✓ CHANGELOG.mdが更新されています")
        sys.exit(0)
    else:
        print("警告: CHANGELOG.mdが更新されていません")
        print("コードに変更がある場合、CHANGELOG.mdを更新してください")
        sys.exit(1)


if __name__ == "__main__":
    main()

