# AutomationManager モジュール

UI Automationを使用してLINEアプリケーションのUI要素を操作するモジュールです。

## 概要

`AutomationManager`は、UI Automation APIを使用してLINEアプリケーションのUI要素を検索・操作するための静的メソッドのみを提供するユーティリティクラスです。

## クラス

### `AutomationManager`

静的メソッドのみを提供するクラスです。インスタンス化は不要です。

## メソッド

### `_get_line_window() -> Optional[auto.WindowControl]`

LINEのメインウィンドウを取得します。

**戻り値:**
- `Optional[auto.WindowControl]`: 見つかったWindowControlオブジェクト。見つからない場合は`None`

**注意:** このメソッドは内部使用を想定しています。

### `type_in_chat(text: str) -> str`

チャット入力欄にテキストを入力します。

**パラメータ:**
- `text: str`: 入力するテキスト

**戻り値:**
- `str`: 処理結果を示すメッセージ

**使用例:**
```python
from n_line.core.automation_manager import AutomationManager

result = AutomationManager.type_in_chat("Hello, World!")
print(result)
```

### `press_send() -> str`

チャット送信キー（Enter）を送信します。

入力欄にフォーカスを当ててEnterキーを送信します。これは「送信」ボタンを探すよりも信頼性が高い方法です。

**戻り値:**
- `str`: 処理結果を示すメッセージ

**使用例:**
```python
result = AutomationManager.press_send()
print(result)
```

## 実装の詳細

### ウィンドウの検索

`auto.WindowControl()`を使用して、名前が「LINE」のウィンドウを検索します。

### チャット入力欄の検索

`AutoSuggestTextArea`クラス名の`EditControl`を検索します。深い階層にある可能性があるため、`searchDepth=15`で検索します。

### テキスト入力

1. ウィンドウを前面に表示
2. 入力欄をクリック
3. `SendKeys()`でテキストを入力

### 送信

1. 入力欄にフォーカスを当てる
2. `{Enter}`キーを送信

## エラーハンドリング

すべてのメソッドは適切なエラーハンドリングを実装しており、例外が発生した場合は安全に処理されます。

## 注意事項

- LINEが実行中である必要があります
- チャットウィンドウが開いている必要があります
- UI Automationが正常に動作する必要があります

## 関連モジュール

- `uiautomation`: UI Automation API
- `win32gui`: Win32 GUI API

