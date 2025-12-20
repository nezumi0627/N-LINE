# WindowManipulator Module

This module is used to search for and manipulate windows via the Win32 API.

## Overview

`WindowManipulator` is a utility class containing only static methods. It uses the Win32 API to obtain window handles and modify window properties.

## Class

### `WindowManipulator`

A class providing only static methods. No instantiation is required.

## Methods

### `find_process_window(pid: int) -> int`

Searches for the main window associated with a given PID.

Enumerates visible windows belonging to the PID and returns the largest window. For Qt applications like LINE, it prioritizes searching for the `QWindowIcon` class name.

**Parameters:**
- `pid: int`: Process ID.

**Returns:**
- `int`: The found window handle, or `0` if not found.

**Example:**
```python
from n_line.core.window_manipulator import WindowManipulator

hwnd = WindowManipulator.find_process_window(12345)
if hwnd:
    print(f"Found window: {hwnd}")
```

### `find_main_window() -> int`

Searches for the LINE main window based on its title (legacy).

Searches for a window with the title "LINE" and a Qt window class name.

**Returns:**
- `int`: The found window handle, or `0` if not found.

### `set_always_on_top(hwnd: int, enable: bool) -> None`

Toggles whether a window stays on top of others.

**Parameters:**
- `hwnd: int`: Window handle.
- `enable: bool`: `True` for topmost, `False` for normal display.

### `set_opacity(hwnd: int, alpha: int) -> None`

Sets the transparency of a window.

**Parameters:**
- `hwnd: int`: Window handle.
- `alpha: int`: Opacity (0 = completely transparent, 255 = completely opaque).

**Example:**
```python
# Set to 50% transparency
WindowManipulator.set_opacity(hwnd, 128)
```

### `scale_window(hwnd: int, width: int, height: int) -> None`

Resizes the window while keeping its position.

**Parameters:**
- `hwnd: int`: Window handle.
- `width: int`: New width.
- `height: int`: New height.

### `set_title(hwnd: int, text: str) -> None`

Changes the window's title.

**Parameters:**
- `hwnd: int`: Window handle.
- `text: str`: New title text.

## Implementation Details

### Window Searching
Uses `win32gui.EnumWindows()` to enumerate windows and search for matching criteria.

### Topmost Display
Uses `win32gui.SetWindowPos()` with `HWND_TOPMOST` or `HWND_NOTOPMOST`.

### Opacity Settings
1. Sets the `WS_EX_LAYERED` style.
2. Uses `SetLayeredWindowAttributes()` to define the opacity.

## Error Handling
All methods implement proper error handling, but behavior is undefined if an invalid handle is passed.

## Related Modules
- `win32gui`: Win32 GUI API
- `win32con`: Win32 constants
- `win32process`: Process information
