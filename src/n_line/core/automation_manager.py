"""UI自動化モジュール

UI Automationを使用してLINEアプリケーションのUI要素を操作する
モジュールです。チャット入力欄へのテキスト入力や送信操作を提供します。
"""
from typing import Optional

import uiautomation as auto
import win32gui


class AutomationManager:
    """UI Automationを使用したLINEアプリケーションの自動操作クラス

    このクラスは静的メソッドのみを提供し、UI Automation APIを使用して
    LINEアプリケーションのUI要素を検索・操作します。
    """

    @staticmethod
    def _get_line_window() -> Optional[auto.WindowControl]:
        """LINEのメインウィンドウを取得

        Returns:
            見つかったWindowControlオブジェクト。見つからない場合はNone
        """
        window = auto.WindowControl(searchDepth=1, Name="LINE")
        if window.Exists(0, 0):
            return window
        return None

    @staticmethod
    def type_in_chat(text: str) -> str:
        """チャット入力欄にテキストを入力

        Args:
            text: 入力するテキスト

        Returns:
            処理結果を示すメッセージ
        """
        window = AutomationManager._get_line_window()
        if not window:
            return "Error: LINE window not found."

        # ウィンドウを前面に表示
        try:
            if window.NativeWindowHandle:
                if win32gui.IsIconic(window.NativeWindowHandle):
                    win32gui.ShowWindow(window.NativeWindowHandle, 9)  # SW_RESTORE
            window.SetFocus()
        except Exception as e:
            return f"Error focusing window: {e}"

        # チャット入力欄を検索（AutoSuggestTextAreaクラス）
        edit_control = window.EditControl(
            ClassName="AutoSuggestTextArea", searchDepth=15
        )

        if not edit_control.Exists(0, 1):
            return (
                "Error: Chat input field (AutoSuggestTextArea) not found. "
                "Open a chat first."
            )

        try:
            edit_control.Click()
            edit_control.SendKeys(text)
            return "Success: Type text command sent."
        except Exception as e:
            return f"Error controlling UI: {e}"

    @staticmethod
    def press_send() -> str:
        """チャット送信キー（Enter）を送信

        入力欄にフォーカスを当ててEnterキーを送信します。
        これは「送信」ボタンを探すよりも信頼性が高い方法です。

        Returns:
            処理結果を示すメッセージ
        """
        window = AutomationManager._get_line_window()
        if not window:
            return "Error: LINE window not found."

        edit_control = window.EditControl(
            ClassName="AutoSuggestTextArea", searchDepth=15
        )
        if not edit_control.Exists(0, 1):
            return "Error: Chat input field not found."

        try:
            edit_control.Click()
            edit_control.SendKeys("{Enter}")
            return "Success: Enter key sent."
        except Exception as e:
            return f"Error sending key: {e}"
