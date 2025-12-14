import win32gui
import win32con
import win32api
import win32process


class WindowManipulator:
    @staticmethod
    def find_process_window(pid: int) -> int:
        """
        Finds the main window for a given PID.
        We look for a visible window owned by this PID.
        Prioritizes windows with 'Qt' in class name if possible (for LINE),
        but generic fallback is finding the largest visible window.
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

            # Check bounds
            rect = win32gui.GetWindowRect(hwnd)
            w = rect[2] - rect[0]
            h = rect[3] - rect[1]
            area = w * h

            # Simple heuristic: The largest visible window is likely the main one.
            # Or if we spot the specific Qt class.
            class_name = win32gui.GetClassName(hwnd)

            # If it's definitely the main LINE window structure
            if "QWindowIcon" in class_name and w > 100:
                found_hwnd = hwnd
                # High priority, stop? No, waiting for enum to finish or check others?
                # Actually, EnumWindow order is Z-order.
                # Let's just track the largest one that matches criteria, or just largest visible.

            if area > max_area:
                max_area = area
                found_hwnd = hwnd

        win32gui.EnumWindows(enum_handler, None)
        return found_hwnd

    @staticmethod
    def find_main_window() -> int:
        """
        Legacy: Attempts to find the main LINE window handle by title.
        """
        found_hwnd = 0

        def enum_handler(hwnd, _):
            nonlocal found_hwnd
            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)

            # Condition: Title is 'LINE' and looks like a Qt Window
            if (
                title == "LINE"
                and class_name.startswith("Qt")
                and "QWindowIcon" in class_name
            ):
                # Check bounds to avoid 1x1 dummy windows if any
                rect = win32gui.GetWindowRect(hwnd)
                w = rect[2] - rect[0]
                h = rect[3] - rect[1]
                if w > 100 and h > 100:
                    found_hwnd = hwnd
                    return

        win32gui.EnumWindows(enum_handler, None)
        return found_hwnd

    @staticmethod
    def set_always_on_top(hwnd: int, enable: bool):
        hwnd_insert_after = win32con.HWND_TOPMOST if enable else win32con.HWND_NOTOPMOST
        # SWP_NOMOVE | SWP_NOSIZE
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
    def set_opacity(hwnd: int, alpha: int):
        """
        alpha: 0 (transparent) to 255 (opaque)
        """
        # Ensure WS_EX_LAYERED is set
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if not (ex_style & win32con.WS_EX_LAYERED):
            win32gui.SetWindowLong(
                hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED
            )

        win32gui.SetLayeredWindowAttributes(hwnd, 0, alpha, win32con.LWA_ALPHA)

    @staticmethod
    def scale_window(hwnd: int, width: int, height: int):
        # Preserve position, just change size
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        win32gui.MoveWindow(hwnd, x, y, width, height, True)

    @staticmethod
    def set_title(hwnd: int, text: str):
        win32gui.SetWindowText(hwnd, text)
