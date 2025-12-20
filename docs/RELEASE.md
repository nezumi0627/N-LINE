# リリース手順

N-LINEプロジェクトのリリース手順を説明します。

## 📋 目次

- [バージョン管理](#バージョン管理)
- [リリース前の準備](#リリース前の準備)
- [リリース手順](#リリース手順)
- [リリース後の作業](#リリース後の作業)

## バージョン管理

### Semantic Versioning

このプロジェクトは [Semantic Versioning](https://semver.org/lang/ja/) に準拠しています。

形式: `MAJOR.MINOR.PATCH`

- **MAJOR**: 後方互換性のない変更
- **MINOR**: 後方互換性を保った機能追加
- **PATCH**: 後方互換性を保ったバグ修正

### バージョン番号の場所

バージョン番号は以下のファイルで管理されています：

- `pyproject.toml` - プロジェクトメタデータ
- `src/n_line/__init__.py` - パッケージバージョン
- `CHANGELOG.md` - 変更履歴

## リリース前の準備

### 1. コードの確認

```bash
# コードフォーマット
rye run fmt
# または
make fmt

# Lintチェック
rye run check
# または
make check

# 型チェック
rye run type-check
# または
mypy src/n_line
```

### 2. テストの実行

```bash
# テストを実行
rye run test
# または
pytest
```

### 3. ドキュメントの更新

- `CHANGELOG.md` を更新
- 必要に応じて `README.md` を更新
- ドキュメントの整合性を確認

### 4. バージョン番号の更新

```bash
# バージョンを更新（例: patch）
python scripts/bump_version.py patch

# または、直接バージョンを指定
python scripts/bump_version.py 0.3.0
```

### 5. バージョン一貫性の確認

```bash
python scripts/check_version.py
```

## リリース手順

### 1. 変更をコミット

```bash
git add .
git commit -m "chore(release): bump version to v0.3.0"
```

### 2. タグの作成

```bash
# タグを作成
git tag -a v0.3.0 -m "Release v0.3.0"

# タグをプッシュ
git push origin v0.3.0
```

### 3. GitHub Actionsによる自動リリース

タグをプッシュすると、GitHub Actionsが自動的に：

1. バージョン番号を確認
2. CHANGELOGを生成
3. GitHub Releaseを作成

### 4. 手動リリース（必要に応じて）

GitHub Actionsが使用できない場合：

```bash
# CHANGELOGを生成
python scripts/generate_changelog.py > CHANGELOG_TEMP.md

# GitHub Releaseを手動で作成
# https://github.com/nezumi0627/n-line/releases/new
```

## リリース後の作業

### 1. リリースノートの確認

GitHub Releaseページでリリースノートが正しく生成されているか確認します。

### 2. ドキュメントの更新

必要に応じて、以下のドキュメントを更新：

- `README.md` - バージョン番号の更新
- `docs/` - 機能ドキュメントの更新

### 3. コミュニティへの通知

- リリースをコミュニティに通知
- 重要な変更があれば、詳細を説明

## バージョン更新の例

### Patch リリース（バグ修正）

```bash
# 現在のバージョン: 0.2.0
python scripts/bump_version.py patch
# 新しいバージョン: 0.2.1

git add .
git commit -m "chore(release): bump version to v0.2.1"
git tag -a v0.2.1 -m "Release v0.2.1"
git push origin v0.2.1
```

### Minor リリース（新機能）

```bash
# 現在のバージョン: 0.2.0
python scripts/bump_version.py minor
# 新しいバージョン: 0.3.0

git add .
git commit -m "chore(release): bump version to v0.3.0"
git tag -a v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0
```

### Major リリース（破壊的変更）

```bash
# 現在のバージョン: 0.2.0
python scripts/bump_version.py major
# 新しいバージョン: 1.0.0

git add .
git commit -m "chore(release): bump version to v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## CHANGELOGの更新

### 形式

CHANGELOGは [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) 形式に従います。

```markdown
## [0.3.0] - 2024-12-15

### 追加
- 新機能の説明

### 変更
- 変更内容の説明

### 修正
- バグ修正の説明

### 削除
- 削除された機能の説明
```

### カテゴリ

- **追加**: 新機能
- **変更**: 既存機能の変更
- **修正**: バグ修正
- **削除**: 削除された機能
- **セキュリティ**: セキュリティ関連の変更

## トラブルシューティング

### バージョン番号が一致しない

```bash
# バージョンを確認
python scripts/check_version.py

# 手動で修正
# pyproject.toml と __init__.py のバージョンを一致させる
```

### CHANGELOGが更新されていない

```bash
# CHANGELOGをチェック
python scripts/check_changelog.py

# 手動で更新
# CHANGELOG.md を編集
```

### タグが作成できない

```bash
# 既存のタグを確認
git tag

# タグを削除（必要に応じて）
git tag -d v0.3.0
git push origin :refs/tags/v0.3.0

# 再度タグを作成
git tag -a v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0
```

## 参考資料

- [Semantic Versioning](https://semver.org/lang/ja/)
- [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/)
- [Conventional Commits](https://www.conventionalcommits.org/)

