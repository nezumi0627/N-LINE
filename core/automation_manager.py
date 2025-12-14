import uiautomation as auto
import time
from typing import Optional


class AutomationManager:
    @staticmethod
    def _get_line_window() -> Optional[auto.WindowControl]:
        # Try to find the main LINE window
        # Based on logs, Name is 'LINE'
        window = auto.WindowControl(searchDepth=1, Name="LINE")
        if window.Exists(0, 0):
            return window
        return None

    @staticmethod
    def type_in_chat(text: str) -> str:
        window = AutomationManager._get_line_window()
        if not window:
            return "Error: LINE window not found."

        # Bring to front
        try:
            if window.NativeWindowHandle:
                import win32gui

                if win32gui.IsIconic(window.NativeWindowHandle):
                    win32gui.ShowWindow(window.NativeWindowHandle, 9)  # SW_RESTORE
            window.SetFocus()
        except Exception as e:
            return f"Error focusing window: {e}"

        # Find the input text area
        # Based on scan: EditControl Class='AutoSuggestTextArea'
        # It is deeply nested, so we use a recursive search or deep search
        edit_control = window.EditControl(
            ClassName="AutoSuggestTextArea", searchDepth=15
        )

        if not edit_control.Exists(0, 1):  # fast check
            # Try searching regardless of depth if previous failed (though searchDepth 15 is deep enough usually)
            return "Error: Chat input field (AutoSuggestTextArea) not found. Open a chat first."

        try:
            edit_control.Click()
            edit_control.SendKeys(text)
            return "Success: Type text command sent."
        except Exception as e:
            return f"Error controlling UI: {e}"

    @staticmethod
    def press_send() -> str:
        # Focusing the edit control and pressing Enter is the most reliable way
        # as the 'Send' button might be disabled (if empty) or hard to identify uniquely
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
