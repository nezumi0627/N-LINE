"""ウィンドウ操作モジュール

Win32 APIを使用してウィンドウの検索、操作（透明度、最前面表示、タイトル変更など）
を行うモジュールです。
"""
from typing import Optional

import win32con
import win32gui
import win32process


class WindowManipulator:
    """ウィンドウの検索と操作を行うクラス

    このクラスは静的メソッドのみを提供し、Win32 APIを使用して
    ウィンドウハンドルを取得し、ウィンドウのプロパティを変更します。
    """

    @staticmethod
    def find_process_window(pid: int) -> int:
        """指定されたPIDのメインウィンドウを検索

        PIDに属する可視ウィンドウを列挙し、最大のウィンドウを返します。
        Qtアプリケーション（LINEなど）の場合は、QWindowIconクラス名を
        優先的に検索します。

        Args:
            pid: プロセスID

        Returns:
            見つかったウィンドウハンドル。見つからない場合は0
        """
        found_hwnd = 0
        max_area = 0

        def enum_handler(hwnd, _):
            nonlocal found_hwnd, max_area
            if not win32gui.IsWindowVisible(hwnd):
                return

            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid != pid:
                return

            # ウィンドウサイズを取得
            rect = win32gui.GetWindowRect(hwnd)
            w = rect[2] - rect[0]
            h = rect[3] - rect[1]
            area = w * h

            class_name = win32gui.GetClassName(hwnd)

            # LINEのメインウィンドウ構造を優先的に検出
            if "QWindowIcon" in class_name and w > 100:
                found_hwnd = hwnd

            # 最大のウィンドウを記録
            if area > max_area:
                max_area = area
                found_hwnd = hwnd

        win32gui.EnumWindows(enum_handler, None)
        return found_hwnd

    @staticmethod
    def find_main_window() -> int:
        """タイトルからLINEのメインウィンドウを検索（レガシー）

        ウィンドウタイトルが「LINE」で、Qtウィンドウクラス名を持つ
        ウィンドウを検索します。

        Returns:
            見つかったウィンドウハンドル。見つからない場合は0
        """
        found_hwnd = 0

        def enum_handler(hwnd, _):
            nonlocal found_hwnd
            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)

            # 条件: タイトルが「LINE」でQtウィンドウ
            if (
                title == "LINE"
                and class_name.startswith("Qt")
                and "QWindowIcon" in class_name
            ):
                # 1x1のダミーウィンドウを避けるためサイズを確認
                rect = win32gui.GetWindowRect(hwnd)
                w = rect[2] - rect[0]
                h = rect[3] - rect[1]
                if w > 100 and h > 100:
                    found_hwnd = hwnd
                    return

        win32gui.EnumWindows(enum_handler, None)
        return found_hwnd

    @staticmethod
    def set_always_on_top(hwnd: int, enable: bool) -> None:
        """ウィンドウを常に最前面に表示する設定を変更

        Args:
            hwnd: ウィンドウハンドル
            enable: Trueの場合は最前面に、Falseの場合は通常表示に
        """
        hwnd_insert_after = (
            win32con.HWND_TOPMOST if enable else win32con.HWND_NOTOPMOST
        )
        win32gui.SetWindowPos(
            hwnd,
            hwnd_insert_after,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )

    @staticmethod
    def set_opacity(hwnd: int, alpha: int) -> None:
        """ウィンドウの透明度を設定

        Args:
            hwnd: ウィンドウハンドル
            alpha: 透明度（0=完全に透明、255=完全不透明）
        """
        # WS_EX_LAYEREDスタイルが設定されていることを確認
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if not (ex_style & win32con.WS_EX_LAYERED):
            win32gui.SetWindowLong(
                hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED
            )

        win32gui.SetLayeredWindowAttributes(hwnd, 0, alpha, win32con.LWA_ALPHA)

    @staticmethod
    def scale_window(hwnd: int, width: int, height: int) -> None:
        """ウィンドウのサイズを変更（位置は保持）

        Args:
            hwnd: ウィンドウハンドル
            width: 新しい幅
            height: 新しい高さ
        """
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        win32gui.MoveWindow(hwnd, x, y, width, height, True)

    @staticmethod
    def set_title(hwnd: int, text: str) -> None:
        """ウィンドウのタイトルを変更

        Args:
            hwnd: ウィンドウハンドル
            text: 新しいタイトルテキスト
        """
        win32gui.SetWindowText(hwnd, text)
