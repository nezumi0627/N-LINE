# UIInspector モジュール

UI Automationを使用してアプリケーションのUI要素を検索、分析するモジュールです。

## 概要

`UIInspector`は、UI Automation APIを使用してアプリケーションのUI要素を検索・分析するための静的メソッドのみを提供するユーティリティクラスです。

## クラス

### `UIInspector`

静的メソッドのみを提供するクラスです。インスタンス化は不要です。

## メソッド

### `get_element_at_cursor() -> Optional[auto.Control]`

マウスカーソル位置のUI要素を取得します。

**戻り値:**
- `Optional[auto.Control]`: 見つかったControlオブジェクト。見つからない場合は`None`

**使用例:**
```python
from n_line.core.ui_inspector import UIInspector

element = UIInspector.get_element_at_cursor()
if element:
    print(f"Element: {element.Name}")
```

### `highlight_element(element: auto.Control, duration: float = 1.0) -> None`

要素の周りに赤い矩形を一時的に表示します。

透明なオーバーレイウィンドウを使用して、指定された要素の周りに赤い枠を表示します。

**パラメータ:**
- `element: auto.Control`: ハイライトするUI要素
- `duration: float`: 表示時間（秒）。デフォルトは1.0秒

**使用例:**
```python
UIInspector.highlight_element(element, duration=2.0)
```

### `get_detailed_info(element: auto.Control) -> Dict[str, Any]`

UI要素の詳細情報を取得します。

要素の名前、型、クラス名、パターン、祖先要素などの詳細情報を辞書形式で返します。

**パラメータ:**
- `element: auto.Control`: 情報を取得するUI要素

**戻り値:**
- `Dict[str, Any]`: 要素の詳細情報を含む辞書

**戻り値の例:**
```python
{
    "Name": "Button",
    "ControlType": "ButtonControl",
    "ClassName": "QPushButton",
    "AutomationId": "",
    "Rect": BoundingRectangle(...),
    "ProcessId": 12345,
    "Value": "",
    "Patterns": ["Invoke (Clickable)"],
    "Ancestors": ["QWidget('MainWindow')", "QMainWindow('LINE')"]
}
```

**使用例:**
```python
info = UIInspector.get_detailed_info(element)
print(f"Name: {info['Name']}")
print(f"Class: {info['ClassName']}")
```

### `get_unique_style_classes(pid: int) -> List[str]`

UIツリー全体をスキャンしてユニークなクラス名のリストを取得します。

QSSセレクタの特定に有用です。

**パラメータ:**
- `pid: int`: プロセスID

**戻り値:**
- `List[str]`: 見つかったクラス名のリスト

**使用例:**
```python
classes = UIInspector.get_unique_style_classes(pid)
for cls in classes:
    print(cls)
```

### `get_extensive_ui_tree(pid: int) -> str`

指定されたPIDのアプリケーションのUIツリー全体をスキャンします。

UI Automationを使用してコントロールツリー全体を走査し、フォーマットされた文字列表現を返します。

**パラメータ:**
- `pid: int`: プロセスID

**戻り値:**
- `str`: UIツリーのフォーマットされた文字列表現

**使用例:**
```python
tree = UIInspector.get_extensive_ui_tree(pid)
print(tree)
```

### `get_window_structure(target_pid: int) -> List[Dict[str, Any]]`

Win32 APIを使用してウィンドウ構造（階層）を取得します（レガシー）。

**パラメータ:**
- `target_pid: int`: 対象プロセスID

**戻り値:**
- `List[Dict[str, Any]]`: ウィンドウ情報のリスト

**使用例:**
```python
windows = UIInspector.get_window_structure(pid)
for win in windows:
    print(f"Title: {win['title']}, Class: {win['class']}")
```

## 実装の詳細

### UI Automationの使用

`uiautomation`ライブラリを使用してUI要素にアクセスします。

### 要素の検索

- `ControlFromPoint()`: カーソル位置の要素を取得
- `GetRootControl()`: ルートコントロールを取得
- `GetChildren()`: 子要素を取得

### ハイライト表示

Tkinterの透明ウィンドウを使用して、要素の周りに赤い枠を表示します。別スレッドで実行してブロックを回避します。

### LegacyIAccessiblePattern

Qtアプリケーションの場合、`LegacyIAccessiblePattern`を使用して詳細情報を取得します。

## エラーハンドリング

すべてのメソッドは適切なエラーハンドリングを実装しており、例外が発生した場合は安全に処理されます。

## 関連モジュール

- `uiautomation`: UI Automation API
- `win32gui`: Win32 GUI API
- `win32process`: プロセス情報

