# 貢献ガイド

N-LINEプロジェクトへの貢献をありがとうございます！このガイドに従って、スムーズに貢献できるようにしましょう。

## 📋 目次

- [行動規範](#行動規範)
- [貢献の方法](#貢献の方法)
- [開発プロセス](#開発プロセス)
- [コーディング規約](#コーディング規約)
- [コミットメッセージ](#コミットメッセージ)
- [プルリクエスト](#プルリクエスト)

## 行動規範

このプロジェクトは、オープンで歓迎的な環境を維持するために、貢献者全員が行動規範に従うことを期待しています。

## 貢献の方法

### バグ報告

1. [Issues](https://github.com/nezumi0627/n-line/issues)で既存のバグ報告を確認
2. 新しいIssueを作成
3. 以下の情報を含める:
   - 問題の説明
   - 再現手順
   - 期待される動作
   - 実際の動作
   - 環境情報（OS、Pythonバージョンなど）
   - エラーメッセージやスクリーンショット

### 機能要望

1. [Issues](https://github.com/nezumi0627/n-line/issues)で既存の要望を確認
2. 新しいIssueを作成
3. 以下の情報を含める:
   - 機能の説明
   - 使用例
   - 実装の提案（任意）

### コード貢献

1. リポジトリをフォーク
2. 機能ブランチを作成: `git checkout -b feature/amazing-feature`
3. 変更をコミット: `git commit -m 'feat: Add amazing feature'`
4. ブランチをプッシュ: `git push origin feature/amazing-feature`
5. プルリクエストを作成

## 開発プロセス

### 1. リポジトリのクローン

```bash
git clone https://github.com/nezumi0627/n-line.git
cd n-line
```

### 2. 開発環境のセットアップ

詳細は [開発者向けガイド](DEVELOPMENT.md) を参照してください。

### 3. ブランチの作成

```bash
git checkout -b feature/your-feature-name
# または
git checkout -b fix/your-bug-fix
```

### 4. 変更の実装

- コーディング規約に従う
- 型ヒントとdocstringを追加
- 必要に応じてテストを追加

### 5. コードのチェック

```bash
# Ryeを使用する場合
rye run fmt
rye run check

# Makeを使用する場合
make fmt
make check
```

### 6. コミット

```bash
git add .
git commit -m "feat: 機能の説明"
```

## コーディング規約

### Pythonスタイルガイド

- **PEP 8** に準拠
- 型ヒントを使用
- docstringを追加（Googleスタイル推奨）

### コード例

```python
"""モジュールの説明"""
from typing import List, Optional

class ExampleClass:
    """クラスの説明"""

    def example_method(self, param: str) -> Optional[List[str]]:
        """メソッドの説明

        Args:
            param: パラメータの説明

        Returns:
            戻り値の説明
        """
        # 実装
        pass
```

### 命名規則

- **クラス名**: `PascalCase` (例: `LineManager`)
- **関数・メソッド名**: `snake_case` (例: `get_line_processes`)
- **定数**: `UPPER_SNAKE_CASE` (例: `PROCESS_NAME`)
- **プライベートメソッド**: `_leading_underscore` (例: `_internal_method`)

## コミットメッセージ

コミットメッセージは [Conventional Commits](https://www.conventionalcommits.org/) に従ってください。

### 形式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### タイプ

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの動作に影響しない変更（フォーマットなど）
- `refactor`: バグ修正や機能追加を伴わないコード変更
- `test`: テストの追加や修正
- `chore`: ビルドプロセスやツールの変更

### 例

```
feat(core): Add process monitoring feature

Add real-time process monitoring to LineManager class.
This allows users to track LINE process status.

Closes #123
```

## プルリクエスト

### チェックリスト

- [ ] コードがコーディング規約に従っている
- [ ] 型ヒントとdocstringが追加されている
- [ ] テストが追加されている（該当する場合）
- [ ] ドキュメントが更新されている（該当する場合）
- [ ] コミットメッセージがConventional Commitsに従っている
- [ ] 既存のテストがすべて通過している

### プルリクエストの説明

以下の情報を含めてください:

1. **変更の概要**: 何を変更したか
2. **変更の理由**: なぜこの変更が必要か
3. **テスト方法**: どのようにテストしたか
4. **スクリーンショット**: UIの変更がある場合

## レビュープロセス

1. プルリクエストが作成されると、自動的にレビューキューに追加されます
2. メンテナーがレビューを行います
3. フィードバックがあれば、対応してください
4. 承認されると、マージされます

## 質問がある場合

質問や不明な点がある場合は、[Issues](https://github.com/nezumi0627/n-line/issues)で質問してください。

## ライセンス

貢献するコードは、プロジェクトのライセンス（MIT）の下で公開されることに同意したものとみなされます。

