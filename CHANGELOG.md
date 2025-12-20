# Changelog

このファイルには、プロジェクトのすべての重要な変更が記録されます。

形式は [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) に基づいており、
このプロジェクトは [Semantic Versioning](https://semver.org/lang/ja/) に準拠しています。

## [Unreleased]

### 追加
- 包括的なドキュメント構造の追加
- 開発者向けガイドの追加
- GitHub Actionsワークフローの追加
- PR/Issueテンプレートの追加
- バージョン管理システムの実装

### 変更
- コードのリファクタリング（型ヒント、docstring追加）
- pyproject.tomlの改善（Rye/pip両対応）
- requirements.txtにバージョン指定を追加

### 削除
- "Apply Dark N-LINE Theme"ボタンの削除

## [0.2.0] - 2024-12-14

### 追加
- ModsTab: リアルタイムLINEウィンドウ操作機能
  - 透明度調整
  - 最前面表示
  - ウィンドウタイトル変更
  - 引数インジェクション機能
- QSS編集機能の改善
- UI Inspector: ポイントインスペクト機能（Ctrl+Shift）
- スパイモード機能

### 変更
- QSSスタイリングの改善
- UI Inspectorの機能強化

## [0.1.2] - 2024-12-14

### 追加
- 自動化ツールの追加
- ドキュメントの追加
- 日本語READMEの追加

## [0.1.1] - 2024-12-14

### 変更
- バージョン検証の改善

## [0.1.0] - 2024-12-14

### 追加
- 初回リリース
- LINEプロセス管理機能
  - LINEの起動
  - LINEプロセスの終了
  - キャッシュクリア
  - インストールパスの取得
- UI Inspector機能
  - ウィンドウ構造のスキャン
  - UI要素の詳細情報取得
  - スタイルクラスの抽出
- デバッグツール
  - プロセス情報表示
  - ファイル構造表示
- ウィンドウ操作機能
  - ウィンドウ検索
  - 透明度設定
  - 最前面表示
  - サイズ変更
  - タイトル変更
- QSS編集機能
  - QSSファイルの編集
  - LINEへの適用
- UI自動化機能
  - チャット入力の自動化
  - 送信操作の自動化

[Unreleased]: https://github.com/nezumi0627/n-line/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/nezumi0627/n-line/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/nezumi0627/n-line/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/nezumi0627/n-line/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/nezumi0627/n-line/releases/tag/v0.1.0

