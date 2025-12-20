# WindowManipulator モジュール

Win32 APIを使用してウィンドウの検索、操作を行うモジュールです。

## 概要

`WindowManipulator`は、Win32 APIを使用してウィンドウハンドルを取得し、ウィンドウのプロパティを変更するための静的メソッドのみを提供するユーティリティクラスです。

## クラス

### `WindowManipulator`

静的メソッドのみを提供するクラスです。インスタンス化は不要です。

## メソッド

### `find_process_window(pid: int) -> int`

指定されたPIDのメインウィンドウを検索します。

PIDに属する可視ウィンドウを列挙し、最大のウィンドウを返します。Qtアプリケーション（LINEなど）の場合は、`QWindowIcon`クラス名を優先的に検索します。

**パラメータ:**
- `pid: int`: プロセスID

**戻り値:**
- `int`: 見つかったウィンドウハンドル。見つからない場合は`0`

**使用例:**
```python
from n_line.core.window_manipulator import WindowManipulator

hwnd = WindowManipulator.find_process_window(12345)
if hwnd:
    print(f"Found window: {hwnd}")
```

### `find_main_window() -> int`

タイトルからLINEのメインウィンドウを検索します（レガシー）。

ウィンドウタイトルが「LINE」で、Qtウィンドウクラス名を持つウィンドウを検索します。

**戻り値:**
- `int`: 見つかったウィンドウハンドル。見つからない場合は`0`

**使用例:**
```python
hwnd = WindowManipulator.find_main_window()
if hwnd:
    print(f"Found LINE window: {hwnd}")
```

### `set_always_on_top(hwnd: int, enable: bool) -> None`

ウィンドウを常に最前面に表示する設定を変更します。

**パラメータ:**
- `hwnd: int`: ウィンドウハンドル
- `enable: bool`: `True`の場合は最前面に、`False`の場合は通常表示に

**使用例:**
```python
WindowManipulator.set_always_on_top(hwnd, True)
```

### `set_opacity(hwnd: int, alpha: int) -> None`

ウィンドウの透明度を設定します。

**パラメータ:**
- `hwnd: int`: ウィンドウハンドル
- `alpha: int`: 透明度（0=完全に透明、255=完全不透明）

**使用例:**
```python
# 50%の透明度に設定
WindowManipulator.set_opacity(hwnd, 128)
```

### `scale_window(hwnd: int, width: int, height: int) -> None`

ウィンドウのサイズを変更します（位置は保持）。

**パラメータ:**
- `hwnd: int`: ウィンドウハンドル
- `width: int`: 新しい幅
- `height: int`: 新しい高さ

**使用例:**
```python
WindowManipulator.scale_window(hwnd, 800, 600)
```

### `set_title(hwnd: int, text: str) -> None`

ウィンドウのタイトルを変更します。

**パラメータ:**
- `hwnd: int`: ウィンドウハンドル
- `text: str`: 新しいタイトルテキスト

**使用例:**
```python
WindowManipulator.set_title(hwnd, "Custom Title")
```

## 実装の詳細

### ウィンドウ検索

`win32gui.EnumWindows()`を使用してウィンドウを列挙し、条件に一致するウィンドウを検索します。

### 最前面表示

`win32gui.SetWindowPos()`を使用して`HWND_TOPMOST`または`HWND_NOTOPMOST`を設定します。

### 透明度設定

1. `WS_EX_LAYERED`スタイルを設定
2. `SetLayeredWindowAttributes()`で透明度を設定

## エラーハンドリング

すべてのメソッドは適切なエラーハンドリングを実装していますが、無効なハンドルが渡された場合の動作は未定義です。

## 関連モジュール

- `win32gui`: Win32 GUI API
- `win32con`: Win32定数
- `win32process`: プロセス情報

