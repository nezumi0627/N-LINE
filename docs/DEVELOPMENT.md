# 開発者向けガイド

N-LINEプロジェクトの開発環境セットアップと開発方法を説明します。

## 📋 目次

- [前提条件](#前提条件)
- [開発環境のセットアップ](#開発環境のセットアップ)
- [プロジェクト構造](#プロジェクト構造)
- [開発ワークフロー](#開発ワークフロー)
- [コーディング規約](#コーディング規約)
- [テスト](#テスト)
- [デバッグ](#デバッグ)

## 前提条件

- Python 3.8以上
- Windows 10/11
- Git
- （推奨）Rye または pip

## 開発環境のセットアップ

### 方法1: Ryeを使用する場合（推奨）

Ryeは、Pythonプロジェクトの依存関係管理とパッケージングを簡素化するツールです。

#### Ryeのインストール

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://rye-up.com/get/ps1).Content | Invoke-Expression

# または、公式サイトからインストール
# https://rye-up.com/guide/installation/
```

#### プロジェクトのセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/nezumi0627/n-line.git
cd n-line

# 依存関係をインストール
rye sync

# アプリケーションを起動
rye run start
```

#### Ryeの便利なコマンド

```bash
# 依存関係の追加
rye add <package-name>

# 開発依存関係の追加
rye add --dev <package-name>

# 依存関係の更新
rye sync --update

# コードフォーマット
rye run fmt

# 静的解析
rye run check
```

### 方法2: pipを使用する場合

#### 仮想環境の作成

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境をアクティベート（Windows）
venv\Scripts\activate

# 仮想環境をアクティベート（Linux/Mac）
source venv/bin/activate
```

#### 依存関係のインストール

```bash
# 依存関係をインストール
pip install -r requirements.txt

# 開発依存関係もインストールする場合
pip install -r requirements-dev.txt  # 存在する場合
```

#### アプリケーションの起動

```bash
python -m n_line
```

## プロジェクト構造

```
n-line/
├── src/
│   └── n_line/              # メインパッケージ
│       ├── __init__.py
│       ├── __main__.py      # エントリーポイント
│       ├── core/            # コア機能モジュール
│       │   ├── line_manager.py
│       │   ├── window_manipulator.py
│       │   ├── ui_inspector.py
│       │   ├── automation_manager.py
│       │   └── debug_tools.py
│       └── gui/             # GUIモジュール
│           ├── app.py
│           ├── debug_window.py
│           └── tabs/        # タブコンポーネント
│               ├── process_tab.py
│               ├── files_tab.py
│               ├── inspector_tab.py
│               ├── mods_tab.py
│               ├── qss_tab.py
│               └── automation_tab.py
├── docs/                    # ドキュメント
├── tests/                   # テスト（将来追加）
├── pyproject.toml          # Rye/pip設定
├── requirements.txt        # pip依存関係
├── Makefile                # Makeタスク
├── make.bat                # Windows用Makeタスク
└── README.md              # プロジェクトREADME
```

## 開発ワークフロー

### 1. ブランチの作成

```bash
git checkout -b feature/your-feature-name
```

### 2. コードの編集

- コーディング規約に従ってコードを記述
- 型ヒントとdocstringを追加
- 必要に応じてテストを追加

### 3. コードのフォーマットとチェック

```bash
# Ryeを使用する場合
rye run fmt
rye run check

# Makeを使用する場合
make fmt
make check
```

### 4. コミットとプッシュ

```bash
git add .
git commit -m "feat: 機能の説明"
git push origin feature/your-feature-name
```

### 5. プルリクエストの作成

GitHubでプルリクエストを作成し、レビューを依頼します。

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

### インポートの順序

1. 標準ライブラリ
2. サードパーティライブラリ
3. ローカルモジュール

```python
import os
from typing import List

import customtkinter
import psutil

from n_line.core.line_manager import LineManager
```

## テスト

### テストの実行

```bash
# pytestを使用する場合（将来追加）
pytest

# 特定のテストを実行
pytest tests/test_line_manager.py
```

### テストの書き方

```python
"""テストモジュール"""
import pytest

from n_line.core.line_manager import LineManager


def test_get_line_processes():
    """LINEプロセスの取得テスト"""
    processes = LineManager.get_line_processes()
    assert isinstance(processes, list)
```

## デバッグ

### ログの確認

アプリケーション内のログテキストボックスでログを確認できます。

### デバッグツールの使用

1. メインウィンドウから「Open Debug Tools」をクリック
2. 各タブでデバッグ情報を確認

### よくある問題

#### LINEプロセスが見つからない

- LINEが実行中か確認
- 管理者権限で実行を試す

#### UI Automationが動作しない

- COMの初期化が必要な場合がある
- `UIAutomationInitializerInThread`を使用

詳細は [トラブルシューティング](TROUBLESHOOTING.md) を参照してください。

## 依存関係の管理

### 新しい依存関係の追加

#### Ryeを使用する場合

```bash
rye add <package-name>
rye sync
```

#### pipを使用する場合

```bash
pip install <package-name>
pip freeze > requirements.txt
```

### 依存関係の更新

#### Ryeを使用する場合

```bash
rye sync --update
```

#### pipを使用する場合

```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

## リリース手順

1. バージョン番号を更新（`pyproject.toml`）
2. CHANGELOGを更新
3. タグを作成
4. GitHubでリリースを作成

## 参考資料

- [Python公式ドキュメント](https://docs.python.org/ja/)
- [Rye公式ドキュメント](https://rye-up.com/)
- [PEP 8](https://pep8-ja.readthedocs.io/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

