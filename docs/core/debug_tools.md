# DebugTools モジュール

デバッグ用のユーティリティを提供するモジュールです。

## 概要

`DebugTools`は、システム情報やプロセス情報の取得、ディレクトリスキャンなどのデバッグ機能を提供するための静的メソッドのみを提供するユーティリティクラスです。

## クラス

### `DebugTools`

静的メソッドのみを提供するクラスです。インスタンス化は不要です。

## メソッド

### `get_system_info() -> Dict[str, str]`

システム情報を取得します。

**戻り値:**
- `Dict[str, str]`: システム情報を含む辞書

**戻り値の例:**
```python
{
    "OS": "nt",
    "Platform": "win32",
    "Python Version": "3.11.0",
    "User Profile": "C:\\Users\\username"
}
```

**使用例:**
```python
from n_line.core.debug_tools import DebugTools

info = DebugTools.get_system_info()
for key, value in info.items():
    print(f"{key}: {value}")
```

### `get_line_process_details() -> List[Dict[str, Any]]`

LINEプロセスの詳細情報を取得します。

**戻り値:**
- `List[Dict[str, Any]]`: プロセス詳細情報のリスト

**戻り値の例:**
```python
[
    {
        "pid": 12345,
        "name": "LINE.exe",
        "cpu_percent": 2.5,
        "memory_info": psutil._pswindows.svmem(rss=123456789, ...),
        "cmdline": ["LINE.exe", "--arg1", "--arg2"],
        "create_time": 1234567890.0
    }
]
```

**使用例:**
```python
details = DebugTools.get_line_process_details()
for proc in details:
    print(f"PID: {proc['pid']}, Memory: {proc['memory_info'].rss / 1024 / 1024:.2f} MB")
```

### `scan_line_directories() -> Dict[str, List[str]]`

LINE関連のディレクトリをスキャンしてファイル一覧を取得します。

**戻り値:**
- `Dict[str, List[str]]`: ディレクトリ名をキー、ファイル名のリストを値とする辞書

**戻り値の例:**
```python
{
    "Install Dir": ["LINE.exe", "LineLauncher.exe", "..."],
    "Data Dir": ["Cache", "Local Storage", "..."]
}
```

**使用例:**
```python
paths = DebugTools.scan_line_directories()
for name, files in paths.items():
    print(f"[{name}]")
    for file in files:
        print(f"  - {file}")
```

## 実装の詳細

### システム情報の取得

- `os.name`: OS名
- `sys.platform`: プラットフォーム名
- `sys.version`: Pythonバージョン
- `os.environ.get("USERPROFILE")`: ユーザープロファイルパス

### プロセス情報の取得

`psutil`を使用してプロセス情報を取得します。以下の情報を取得:
- PID
- プロセス名
- CPU使用率
- メモリ使用量
- コマンドライン引数
- 作成時刻

### ディレクトリスキャン

- インストールディレクトリ: `LineManager.get_install_path()`から取得
- データディレクトリ: `%LOCALAPPDATA%\LINE`から取得

## エラーハンドリング

すべてのメソッドは適切なエラーハンドリングを実装しており、例外が発生した場合は安全に処理されます。

## 関連モジュール

- `psutil`: プロセス管理
- `os`: ファイルシステム操作
- `sys`: システム情報
- `n_line.core.line_manager`: LINEプロセス管理

