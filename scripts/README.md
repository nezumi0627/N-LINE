# スクリプト一覧

このディレクトリには、開発とリリースに使用するユーティリティスクリプトが含まれています。

## スクリプト

### `bump_version.py`

バージョン番号を更新します。

**使用方法:**

```bash
# Patch リリース（0.2.0 -> 0.2.1）
python scripts/bump_version.py patch

# Minor リリース（0.2.0 -> 0.3.0）
python scripts/bump_version.py minor

# Major リリース（0.2.0 -> 1.0.0）
python scripts/bump_version.py major

# 直接バージョンを指定
python scripts/bump_version.py 0.3.0
```

**更新されるファイル:**
- `pyproject.toml`
- `src/n_line/__init__.py`

### `check_version.py`

バージョン番号の一貫性をチェックします。

**使用方法:**

```bash
python scripts/check_version.py
```

**チェック内容:**
- `pyproject.toml` のバージョン
- `__init__.py` のバージョン
- `CHANGELOG.md` の最新バージョン

すべてのバージョンが一致している必要があります。

### `check_changelog.py`

CHANGELOG.mdが更新されているかチェックします。

**使用方法:**

```bash
python scripts/check_changelog.py
```

**チェック内容:**
- コードに変更がある場合、CHANGELOG.mdが更新されているか

### `generate_changelog.py`

Git履歴からCHANGELOGを生成します。

**使用方法:**

```bash
python scripts/generate_changelog.py
```

**出力:**
- 最新タグ以降のコミットからCHANGELOGエントリを生成

**注意:** このスクリプトはリリース時に自動的に実行されます。

## 開発ワークフローでの使用

### リリース前

```bash
# 1. バージョンを更新
python scripts/bump_version.py patch

# 2. バージョンの一貫性を確認
python scripts/check_version.py

# 3. CHANGELOGを更新（手動）
# CHANGELOG.md を編集

# 4. CHANGELOGの更新を確認
python scripts/check_changelog.py
```

### CI/CDでの使用

これらのスクリプトは、GitHub Actionsワークフローで自動的に実行されます：

- `check_version.py` - PRチェック時
- `check_changelog.py` - PRチェック時
- `generate_changelog.py` - リリース時

## トラブルシューティング

### スクリプトが実行できない

```bash
# Pythonパスを確認
python --version

# スクリプトの実行権限を確認
ls -l scripts/*.py
```

### バージョンが更新されない

```bash
# ファイルの権限を確認
# 書き込み権限があることを確認

# 手動で確認
python scripts/check_version.py
```

