"""UI要素検査モジュール

UI Automationを使用してアプリケーションのUI要素を検索、分析する
モジュールです。ウィンドウ構造の取得、要素の詳細情報取得、スタイルクラス
の抽出などの機能を提供します。
"""
import threading
from typing import Any, Dict, List, Optional

import uiautomation as auto
import win32gui
import win32process


class UIInspector:
    """UI要素の検査と分析を行うクラス

    このクラスは静的メソッドのみを提供し、UI Automation APIを使用して
    アプリケーションのUI要素を検索・分析します。
    """

    @staticmethod
    def get_element_at_cursor() -> Optional[auto.Control]:
        """マウスカーソル位置のUI要素を取得

        Returns:
            見つかったControlオブジェクト。見つからない場合はNone
        """
        try:
            x, y = win32gui.GetCursorPos()
            element = auto.ControlFromPoint(x, y)
            return element
        except Exception:
            return None

    @staticmethod
    def highlight_element(element: auto.Control, duration: float = 1.0) -> None:
        """要素の周りに赤い矩形を一時的に表示

        透明なオーバーレイウィンドウを使用して、指定された要素の周りに
        赤い枠を表示します。

        Args:
            element: ハイライトするUI要素
            duration: 表示時間（秒）
        """
        try:
            rect = element.BoundingRectangle
            if rect.right <= rect.left or rect.bottom <= rect.top:
                return

            def show_highlight():
                import tkinter as tk

                root = tk.Tk()

                # Window settings for transparent overlay
                root.overrideredirect(True)
                root.attributes("-topmost", True)
                root.attributes("-alpha", 0.7)  # Semi-transparent
                root.attributes(
                    "-transparentcolor", "white"
                )  # White becomes fully transparent

                # Calculate geometry
                w = rect.right - rect.left
                h = rect.bottom - rect.top
                x = rect.left
                y = rect.top

                root.geometry(f"{w}x{h}+{x}+{y}")

                # Create canvas relative to 0,0 since window is positioned at rect
                canvas = tk.Canvas(
                    root, width=w, height=h, bg="white", highlightthickness=0
                )
                canvas.pack(fill="both", expand=True)

                # Draw red border
                canvas.create_rectangle(0, 0, w - 1, h - 1, outline="red", width=3)

                root.after(int(duration * 1000), root.destroy)
                root.mainloop()

            # Run in a separate thread to not block
            t = threading.Thread(target=show_highlight)
            t.start()

        except Exception:
            pass

    @staticmethod
    def get_detailed_info(element: auto.Control) -> Dict[str, Any]:
        """UI要素の詳細情報を取得

        要素の名前、型、クラス名、パターン、祖先要素などの詳細情報を
        辞書形式で返します。

        Args:
            element: 情報を取得するUI要素

        Returns:
            要素の詳細情報を含む辞書
        """
        if not element:
            return {}

        info = {
            "Name": element.Name,
            "ControlType": element.ControlTypeName,
            "ClassName": element.ClassName,
            "AutomationId": element.AutomationId,
            "Rect": element.BoundingRectangle,
            "ProcessId": element.ProcessId,
            "Value": "",
            "Patterns": [],
        }

        # Check patterns for editing capabilities
        if element.GetPattern(auto.PatternId.ValuePattern):
            info["Patterns"].append("Value")
            try:
                p = element.GetValuePattern()
                if p:
                    info["Value"] = p.Value
            except Exception:
                pass

        if element.GetPattern(auto.PatternId.InvokePattern):
            info["Patterns"].append("Invoke (Clickable)")

        if element.GetPattern(auto.PatternId.TogglePattern):
            info["Patterns"].append("Toggle")

        # --- Advanced: Retrieve LegacyIAccessible (Crucial for Qt Apps) ---
        # Qt often hides real object names in LegacyIAccessible properties
        if element.GetPattern(auto.PatternId.LegacyIAccessiblePattern):
            info["Patterns"].append("LegacyIAccessible")
            try:
                legacy = element.GetLegacyIAccessiblePattern()
                if legacy:
                    info["LegacyName"] = legacy.Name
                    info["LegacyDescription"] = legacy.Description
                    info["LegacyValue"] = legacy.Value
                    info["LegacyRole"] = legacy.Role
                    # Sometimes Description holds the objectName or class info
            except Exception:
                pass

        # --- Hierarchy: Ancestors ---
        # Walk up to find the container context (e.g. ChatPanel -> LcWidget)
        ancestors = []
        try:
            parent = element.GetParentControl()
            depth = 0
            while parent and depth < 5:  # Limit depth
                name = parent.Name if parent.Name else "NoName"
                cls = parent.ClassName if parent.ClassName else "NoClass"
                ancestors.append(f"{cls}('{name}')")

                # Check for PID mismatch (hit desktop)
                if parent.ProcessId != element.ProcessId:
                    break

                parent = parent.GetParentControl()
                depth += 1
        except Exception:
            pass

        info["Ancestors"] = ancestors

        return info

    @staticmethod
    def get_unique_style_classes(pid: int) -> List[str]:
        """UIツリー全体をスキャンしてユニークなクラス名のリストを取得

        QSSセレクタの特定に有用です。

        Args:
            pid: プロセスID

        Returns:
            見つかったクラス名のリスト
        """
        classes = set()

        try:
            root = auto.GetRootControl()
            app_window = None

            # Find window for PID
            for attempt in root.GetChildren():
                if attempt.ProcessId == pid:
                    app_window = attempt
                    classes.add(app_window.ClassName)  # Add root class
                    break

            if not app_window:
                return ["Error: Could not find main window."]

            # Recursive scan
            def walk(control):
                children = control.GetChildren()
                for child in children:
                    if child.ClassName:
                        classes.add(child.ClassName)
                    walk(child)

            walk(app_window)

        except Exception as e:
            return [f"Scan Error: {str(e)}"]

        return sorted(list(classes))

    @staticmethod
    def get_extensive_ui_tree(pid: int) -> str:
        """指定されたPIDのアプリケーションのUIツリー全体をスキャン

        UI Automationを使用してコントロールツリー全体を走査し、
        フォーマットされた文字列表現を返します。

        Args:
            pid: プロセスID

        Returns:
            UIツリーのフォーマットされた文字列表現
        """
        output = []
        try:
            # Find the main window element for the PID
            # We search for the first window element that matches the PID
            root = auto.GetRootControl()
            app_window = None

            # Walk top level windows to find one belonging to our PID
            for attempt in root.GetChildren():
                if attempt.ProcessId == pid:
                    app_window = attempt
                    break

            if not app_window:
                # Try finding by process explicitly if top-level walk failed
                # This is slower but maybe necessary
                # Actually, let's just use a walker if simple loop fails
                pass

            if not app_window:
                return "Could not find a top-level window for this process via UI Automation."

            output.append(
                f"Root Window: {app_window.Name} (ClassName: {app_window.ClassName})"
            )

            # Recursive walker
            def walk(control, depth):
                children = control.GetChildren()
                for child in children:
                    indent = "  " * depth
                    info = f"{indent}- {child.ControlTypeName} "
                    if child.Name:
                        info += f"Name='{child.Name}' "
                    if child.AutomationId:
                        info += f"ID='{child.AutomationId}' "
                    if child.ClassName:
                        info += f"Class='{child.ClassName}' "

                    # Add rect info for more detail
                    r = child.BoundingRectangle
                    info += f"Rect=({r.left}, {r.top}, {r.right}, {r.bottom})"

                    output.append(info)
                    walk(child, depth + 1)

            walk(app_window, 1)

        except Exception as e:
            return f"Error during UI Automation scan: {str(e)}"

        return "\n".join(output)

    @staticmethod
    def get_window_structure(target_pid: int) -> List[Dict[str, Any]]:
        """Win32 APIを使用してウィンドウ構造（階層）を取得（レガシー）

        Args:
            target_pid: 対象プロセスID

        Returns:
            ウィンドウ情報のリスト
        """
        windows = []

        def enum_window_callback(hwnd, _):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid == target_pid:
                # Found a window belonging to the target process
                win_info = UIInspector._get_window_info(hwnd)
                # Get children
                win_info["children"] = UIInspector._get_child_windows(hwnd)
                windows.append(win_info)

        win32gui.EnumWindows(enum_window_callback, None)
        return windows

    @staticmethod
    def _get_child_windows(parent_hwnd) -> List[Dict[str, Any]]:
        children = []

        def enum_child_callback(hwnd, _):
            children.append(UIInspector._get_window_info(hwnd))
            # Note: EnumChildWindows enumerates ALL descendants, so this flat list
            # might contain nested children. For a strict tree, logic needs to be recursive manually
            # checking GetParent. However, for a simple inspection, a flat list or direct children is okay.
            # But EnumChildWindows is recursive. To build a tree, we strictly need check parent.
            return True

        # Custom approach for tree: Just get direct children is hard with simple API.
        # We will use EnumChildWindows and filter by GetParent

        all_descendants = []

        def collect_descendants(hwnd, _):
            all_descendants.append(hwnd)
            return True

        try:
            win32gui.EnumChildWindows(parent_hwnd, collect_descendants, None)
        except Exception:
            pass  # Some windows refuse enumeration

        # Filter only direct children
        direct_children = []
        for hwnd in all_descendants:
            if win32gui.GetParent(hwnd) == parent_hwnd:
                child_info = UIInspector._get_window_info(hwnd)
                # Recursively get valid children from the descendant list?
                # Doing full recursion might be slow, so we limit depth or just show this level.
                # Let's try to get grandchildren too basically.
                child_info["children"] = UIInspector._get_child_windows(hwnd)
                direct_children.append(child_info)

        return direct_children

    @staticmethod
    def _get_window_info(hwnd) -> Dict[str, Any]:
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]

        return {
            "hwnd": hwnd,
            "title": title,
            "class": class_name,
            "rect": rect,
            "size": f"{width}x{height}",
            "visible": win32gui.IsWindowVisible(hwnd),
        }
