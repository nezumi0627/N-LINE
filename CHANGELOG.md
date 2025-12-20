# Changelog

すべての重要な変更が記録されます。
形式は [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) に基づいており、
このプロジェクトは [Semantic Versioning](https://semver.org/lang/ja/) に準拠しています。

## [0.2.0] - 2025-12-20

### 追加
- **ModsTab**: リアルタイムLINEウィンドウ操作機能
  - 透明度調整、最前面表示、ウィンドウタイトル変更
  - 引数インジェクション機能（`--remote-debugging-port`等）
- **UI Inspector**: CTRL+SHIFTによるポイントインスペクト機能
- **スパイモード**: ウィンドウ要素のリアルタイム追跡
- **自動化**: チャット送信の自動化機能
- **開発ツール**: ビルド自動化スクリプト、チャンジログ生成スクリプト

### 修正
- PyInstallerでのビルドエラー（win32パッケージのパス解決）を修正
- 仮想環境（`.venv` / `venv`）の自動検出ロジックの改善
- GitHub Actionsでのエンコーディングエラー（UnicodeEncodeError）の修正

### 変更
- ドキュメント構造の刷新（日本語・英語のマルチリンガル化対応中）
- QSSスタイリング機能の強化

## [0.1.2] - 2025-12-14

### 追加
- 自動化ツールの初期実装
- 詳細なドキュメントの追加

## [0.1.1] - 2025-12-14

### 修正
- バージョン検証ロジックの改善
- パス検出の不具合修正

## [0.1.0] - 2025-12-14

### 追加
- 初回リリース
- LINEプロセス管理（プロセス一覧、停止、キャッシュクリア）
- 基本的なQSSインジェクション機能

[0.2.0]: https://github.com/nezumi0627/n-line/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/nezumi0627/n-line/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/nezumi0627/n-line/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/nezumi0627/n-line/releases/tag/v0.1.0
