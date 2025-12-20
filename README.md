# N-LINE

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-v0.2.0-orange.svg)

> [English Version](README_EN.md)

**N-LINE** は、Windows上のLINEデスクトップアプリケーションを管理、デバッグ、および変更するための強力なPythonベースのユーティリティです。

## ✨ 主な機能

- 🔧 **LINEプロセス管理**: 起動、終了、キャッシュクリア
- 🔍 **UI Inspector**: UI要素の検査と分析
- 🎨 **ウィンドウ操作**: 透明度、最前面表示、タイトル変更
- 📝 **QSS編集**: Qt Stylesheetの編集と適用
- 🤖 **UI自動化**: チャット入力の自動化
- 🐛 **デバッグツール**: プロセス情報、ファイル構造の表示

## 🚀 クイックスタート

### 前提条件

- Python 3.8以上
- Windows 10/11
- LINEデスクトップアプリケーション

### インストール方法

#### Ryeを使用する場合（推奨）

```bash
# Ryeをインストール（未インストールの場合）
# https://rye-up.com/guide/installation/

# プロジェクトをクローン
git clone https://github.com/nezumi0627/n-line.git
cd n-line

# 依存関係をインストール
rye sync

# アプリケーションを起動
rye run start
```

#### pipを使用する場合

```bash
# プロジェクトをクローン
git clone https://github.com/nezumi0627/n-line.git
cd n-line

# 仮想環境を作成（推奨）
python -m venv venv
venv\Scripts\activate  # Windows

# 依存関係をインストール
pip install -r requirements.txt

# アプリケーションを起動
python -m n_line
```

#### 簡単な起動方法（Windows）

`run.bat` をダブルクリックするだけです。

## 📖 ドキュメント

詳細なドキュメントは [`docs/`](docs/) ディレクトリを参照してください。

- [📚 ドキュメント目次](docs/README.md) - すべてのドキュメントへのリンク
- [✨ 機能一覧](docs/features.md) - 各機能の詳細説明
- [🛠️ 技術仕様](docs/specifications.md) - アーキテクチャと設計
- [🚀 利用ガイド](docs/usage.md) - 使い方ガイド
- [👨‍💻 開発者向けガイド](docs/DEVELOPMENT.md) - 開発環境のセットアップ

## 🛠️ 開発

### 開発環境のセットアップ

詳細は [開発者向けガイド](docs/DEVELOPMENT.md) を参照してください。

### 開発コマンド

#### Ryeを使用する場合

```bash
rye run start    # アプリケーション起動
rye run fmt      # コードフォーマット
rye run check    # 静的解析・Lint
```

#### Makeを使用する場合

```bash
make install     # 依存関係のインストール
make start       # アプリケーションの起動
make fmt         # コードのフォーマット
make check       # 静的解析・Lint
make fix         # Lintエラーの自動修正
```

Windowsで `make` がない場合は、`make.bat` を使用できます。

## 📁 プロジェクト構造

```
n-line/
├── src/
│   └── n_line/          # メインパッケージ
│       ├── core/       # コア機能モジュール
│       └── gui/        # GUIモジュール
├── docs/               # ドキュメント
├── pyproject.toml      # Rye/pip設定
├── requirements.txt    # pip依存関係
└── README.md           # このファイル
```

## ⚠️ 免責事項

このツールは教育およびデバッグ目的でのみ提供されています。責任を持って使用してください。

## 📄 ライセンス

MIT License

## 🤝 貢献

バグ報告や機能要望は、GitHubのIssuesに投稿してください。プルリクエストも歓迎します。

## 📞 サポート

問題が発生した場合は、[Issues](https://github.com/nezumi0627/n-line/issues) で報告してください。
