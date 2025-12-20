# APIリファレンス

N-LINEのAPIリファレンスです。

## コアモジュール

### LineManager

LINEプロセスとインストールパスを管理するモジュール。

- [詳細ドキュメント](../core/line_manager.md)

### WindowManipulator

Win32 APIを使用してウィンドウを操作するモジュール。

- [詳細ドキュメント](../core/window_manipulator.md)

### UIInspector

UI Automationを使用してUI要素を検査・分析するモジュール。

- [詳細ドキュメント](../core/ui_inspector.md)

### AutomationManager

UI Automationを使用してLINEアプリケーションを自動操作するモジュール。

- [詳細ドキュメント](../core/automation.md)

### DebugTools

デバッグ用のユーティリティを提供するモジュール。

- [詳細ドキュメント](../core/debug_tools.md)

## GUIモジュール

### NLineApp

メインアプリケーションクラス。

**場所:** `n_line.gui.app`

**主要メソッド:**
- `launch_line_action()`: LINEを起動
- `kill_line_action()`: LINEプロセスを終了
- `clear_cache_action()`: キャッシュをクリア
- `open_debug_window()`: デバッグウィンドウを開く

### DebugWindow

デバッグツールを提供するウィンドウクラス。

**場所:** `n_line.gui.debug_window`

**タブ:**
- Process Info
- File Structure
- UI Inspector
- Window Mods
- Styles (QSS)
- Automation

## 使用例

### LINEプロセスの管理

```python
from n_line.core.line_manager import LineManager

# LINEが実行中か確認
if LineManager.is_line_running():
    print("LINE is running")

# LINEを起動
result = LineManager.launch_line()
print(result)

# LINEを終了
LineManager.kill_line()
```

### ウィンドウ操作

```python
from n_line.core.window_manipulator import WindowManipulator
from n_line.core.line_manager import LineManager

# LINEプロセスを取得
procs = LineManager.get_line_processes()
if procs:
    # ウィンドウを検索
    hwnd = WindowManipulator.find_process_window(procs[0].pid)
    if hwnd:
        # 透明度を設定
        WindowManipulator.set_opacity(hwnd, 200)
        # 最前面に表示
        WindowManipulator.set_always_on_top(hwnd, True)
```

### UI要素の検査

```python
from n_line.core.ui_inspector import UIInspector
from n_line.core.line_manager import LineManager

# LINEプロセスを取得
procs = LineManager.get_line_processes()
if procs:
    # UIツリーを取得
    tree = UIInspector.get_extensive_ui_tree(procs[0].pid)
    print(tree)
    
    # スタイルクラスを抽出
    classes = UIInspector.get_unique_style_classes(procs[0].pid)
    for cls in classes:
        print(cls)
```

### UI自動化

```python
from n_line.core.automation_manager import AutomationManager

# チャットにテキストを入力
result = AutomationManager.type_in_chat("Hello, World!")
print(result)

# 送信
result = AutomationManager.press_send()
print(result)
```

## 詳細情報

各モジュールの詳細なAPIドキュメントは、[コアモジュールドキュメント](../core/)を参照してください。

