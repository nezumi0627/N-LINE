# LineManager モジュール

LINEプロセスとインストールパスを管理するモジュールです。

## 概要

`LineManager`は、LINEアプリケーションのプロセスを管理するための静的メソッドのみを提供するユーティリティクラスです。

## クラス

### `LineManager`

静的メソッドのみを提供するクラスです。インスタンス化は不要です。

## メソッド

### `get_line_processes() -> List[psutil.Process]`

実行中のLINEプロセスのリストを取得します。

**戻り値:**
- `List[psutil.Process]`: LINEプロセスのリスト。見つからない場合は空リスト

**使用例:**
```python
from n_line.core.line_manager import LineManager

processes = LineManager.get_line_processes()
for proc in processes:
    print(f"PID: {proc.pid}, Name: {proc.name()}")
```

### `is_line_running() -> bool`

LINEが実行中かどうかを確認します。

**戻り値:**
- `bool`: LINEが実行中の場合は`True`、そうでなければ`False`

**使用例:**
```python
if LineManager.is_line_running():
    print("LINE is running")
```

### `kill_line() -> bool`

すべてのLINEプロセスを終了します。

**戻り値:**
- `bool`: プロセスが見つかり終了処理を試みた場合は`True`、プロセスが見つからなかった場合は`False`

**使用例:**
```python
if LineManager.kill_line():
    print("LINE processes terminated")
```

### `get_install_path() -> Optional[str]`

LINEのインストールパスを取得します。

実行中のプロセスから取得を試み、失敗した場合は一般的なパス（`%LOCALAPPDATA%\LINE\bin`）を確認します。

**戻り値:**
- `Optional[str]`: インストールパス。見つからない場合は`None`

**使用例:**
```python
path = LineManager.get_install_path()
if path:
    print(f"LINE installed at: {path}")
```

### `clear_cache() -> str`

LINEのキャッシュディレクトリをクリアします。

**戻り値:**
- `str`: 処理結果を示すメッセージ

**使用例:**
```python
result = LineManager.clear_cache()
print(result)
```

### `launch_line() -> str`

LINEを起動します。

実行ファイルの候補を優先順位順に確認:
1. `LineLauncher.exe`
2. `current/LINE.exe`
3. `LINE.exe`

**戻り値:**
- `str`: 処理結果を示すメッセージ

**使用例:**
```python
result = LineManager.launch_line()
print(result)
```

### `relaunch_with_params(args: List[str]) -> str`

LINEを終了し、指定された引数で再起動します。

**パラメータ:**
- `args: List[str]`: 起動時に渡すコマンドライン引数のリスト

**戻り値:**
- `str`: 処理結果を示すメッセージ

**使用例:**
```python
result = LineManager.relaunch_with_params(["-stylesheet", "style.qss"])
print(result)
```

## 実装の詳細

### プロセス検索

`psutil.process_iter()`を使用してプロセスを列挙し、プロセス名が`LINE.exe`のものをフィルタリングします。

### インストールパスの検索

1. 実行中のプロセスから実行ファイルのパスを取得
2. 失敗した場合、一般的なパス（`%LOCALAPPDATA%\LINE\bin`）を確認

### キャッシュのクリア

`%LOCALAPPDATA%\LINE\Cache`の内容を削除します。フォルダ自体は削除せず、内容のみを削除します（安全のため）。

## エラーハンドリング

すべてのメソッドは適切なエラーハンドリングを実装しており、例外が発生した場合は安全に処理されます。

## 関連モジュール

- `psutil`: プロセス管理
- `os`: ファイルシステム操作
- `subprocess`: プロセス起動

