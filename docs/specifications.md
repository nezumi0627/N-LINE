# N-LINE 技術仕様書

## 技術スタック
- **言語**: Python 3.11+
- **GUI フレームワーク**: CustomTkinter (TkinterのモダンUIラッパー)
- **プロセス管理**: `psutil` (クロスプラットフォームなプロセス・システム監視)
- **Windows 統合**: 
  - `pywin32` (低レベルなウィンドウ操作のためのWin32 APIアクセス)
  - `uiautomation` (深いUI調査と制御のためのMicrosoft UI AUtomation)
- **画像処理**: `Pillow` (PIL Fork)

## アーキテクチャ

### ディレクトリ構造
```
N-LINE/
├── core/                   # コアビジネスロジック
│   ├── line_manager.py     # LINEプロセス/ファイル操作のメインロジック
│   ├── backup_manager.py   # バックアップ機能
│   ├── debug_tools.py      # システム情報とファイルスキャン
│   ├── ui_inspector.py     # Win32 & UIA ウィンドウ調査ロジック
│   ├── window_manipulator.py # ウィンドウ操作 (透明度, 最前面, タイトル)
│   └── automation_manager.py # 自動操作インタラクション (入力, キー送信)
├── gui/                    # グラフィカルユーザーインターフェース
│   ├── app.py              # メインアプリケーションウィンドウとタブ
│   └── debug_tools.py      # デバッグツールサブウィンドウのロジック
├── docs/                   # ドキュメント (日本語)
│   └── en/                 # English Documents
├── venv/                   # 仮想環境
├── main.py                 # アプリケーションエントリーポイント
├── run.bat                 # 実行スクリプト
├── requirements.txt        # 依存関係リスト
└── README.md               # プロジェクト概要
```

### コア設計原則
1.  **関心の分離**: UIロジック (`gui/`) はビジネスロジック (`core/`) から分離されています。GUIクラスはCoreクラスの静的メソッドやインスタンスを呼び出します。
2.  **スレッドセーフ**: 監視タスク（LINEが起動しているかの確認など）は、メインGUIスレッドのフリーズを防ぐために別スレッド (`threading.Thread`) で実行されます。
3.  **堅牢なエラーハンドリング**: ファイルやプロセス操作は、権限の問題やファイルの欠落を適切に処理するために try-except ブロックでラップされています。
4.  **拡張性**: プロジェクトは、既存のコードを書き直すことなく新しいモジュール（例：`window_manipulator`, `automation_manager`）を簡単に追加できるように構造化されています。

## キーモジュール

### LineManager (`core.line_manager`)
- **役割**: LINEプロセスのライフサイクルを管理します。
- **主なメソッド**: 
  - `is_line_running()`: アクティブなプロセスを確認します。
  - `kill_line()`: LINE.exe と関連プロセスを強制終了します。
  - `clear_cache()`: ローカルAppDataディレクトリから一時ファイルを削除します。

### UIInspector (`core.ui_inspector`)
- **役割**: 実行中のプロセスのウィンドウ構造を分析します。
- **技術**: 標準的なウィンドウ列挙には `win32gui` を、一般的なUI要素（ボタン、入力欄）の深いツリー探索には `uiautomation` を使用します。

### AutomationManager (`core.automation_manager`)
- **役割**: LINEクライアントとのプログラムによる対話を処理します。
- **機能**: 特定の発見されたコントロール要素（例：`AutoSuggestTextArea`）に対してキーストロークを送信したりテキストを注入したりします。
