"""Git履歴からCHANGELOGを生成するスクリプト"""

import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).parent.parent

# WindowsでUTF-8出力を保証するための設定
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def get_git_tags() -> List[str]:
    """Gitタグのリストを取得"""
    try:
        result = subprocess.run(
            ["git", "tag", "--sort=-version:refname"],
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )
        return [tag.strip() for tag in result.stdout.strip().split("\n") if tag.strip()]
    except subprocess.CalledProcessError:
        return []


def get_commits_since_tag(tag: str) -> List[Tuple[str, str, str]]:
    """指定されたタグ以降のコミットを取得"""
    try:
        if tag:
            cmd = ["git", "log", f"{tag}..HEAD", "--pretty=format:%h|%s|%an|%ad", "--date=short"]
        else:
            cmd = ["git", "log", "--pretty=format:%h|%s|%an|%ad", "--date=short"]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8")

        commits = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 4:
                commits.append((parts[0], parts[1], parts[2], parts[3]))
        return commits
    except subprocess.CalledProcessError:
        return []


def categorize_commit(message: str) -> str:
    """コミットメッセージをカテゴリに分類"""
    message_lower = message.lower()

    if message.startswith("feat"):
        return "追加"
    elif message.startswith("fix"):
        return "修正"
    elif message.startswith("docs"):
        return "ドキュメント"
    elif message.startswith("style"):
        return "スタイル"
    elif message.startswith("refactor"):
        return "リファクタリング"
    elif message.startswith("perf"):
        return "パフォーマンス"
    elif message.startswith("test"):
        return "テスト"
    elif message.startswith("chore"):
        return "その他"
    else:
        return "その他"


def format_changelog_entry(
    commits: List[Tuple[str, str, str, str]], version: str, date: str
) -> str:
    """CHANGELOGエントリをフォーマット"""
    if not commits:
        return ""

    categories = {
        "追加": [],
        "修正": [],
        "ドキュメント": [],
        "スタイル": [],
        "リファクタリング": [],
        "パフォーマンス": [],
        "テスト": [],
        "その他": [],
    }

    for commit in commits:
        _, message, author, _ = commit
        category = categorize_commit(message)
        categories[category].append(f"- {message} ({author})")

    lines = [f"## [{version}] - {date}", ""]

    for category, items in categories.items():
        if items:
            lines.append(f"### {category}")
            lines.extend(items)
            lines.append("")

    return "\n".join(lines)


def main():
    """メイン関数"""
    tags = get_git_tags()

    if not tags:
        print("警告: Gitタグが見つかりませんでした")
        sys.exit(1)

    latest_tag = tags[0]
    commits = get_commits_since_tag(latest_tag)

    if not commits:
        print("新しいコミットが見つかりませんでした")
        sys.exit(0)

    # バージョン番号を抽出
    version_match = re.search(r"v?([0-9]+\.[0-9]+\.[0-9]+)", latest_tag)
    if version_match:
        version = version_match.group(1)
    else:
        version = latest_tag

    # 最新コミットの日付を使用
    date = commits[0][3] if commits else ""

    entry = format_changelog_entry(commits, version, date)
    print(entry)


if __name__ == "__main__":
    main()
