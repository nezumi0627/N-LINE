# UIInspector Module

This module is used to search for and analyze application UI elements using UI Automation.

## Overview

`UIInspector` is a utility class providing only static methods to search for and analyze UI elements via the UI Automation API.

## Class

### `UIInspector`

A class with only static methods. No instantiation is required.

## Methods

### `get_element_at_cursor() -> Optional[auto.Control]`

Retrieves the UI element at the current mouse cursor position.

**Returns:**
- `Optional[auto.Control]`: The found Control object, or `None` if not found.

**Example:**
```python
from n_line.core.ui_inspector import UIInspector

element = UIInspector.get_element_at_cursor()
if element:
    print(f"Element: {element.Name}")
```

### `highlight_element(element: auto.Control, duration: float = 1.0) -> None`

Temporarily displays a red rectangle around the element.

Uses a transparent overlay window to show a red frame around the specified element.

**Parameters:**
- `element: auto.Control`: The UI element to highlight.
- `duration: float`: Display duration in seconds. Defaults to 1.0 seconds.

**Example:**
```python
UIInspector.highlight_element(element, duration=2.0)
```

### `get_detailed_info(element: auto.Control) -> Dict[str, Any]`

Retrieves detailed information about a UI element.

Returns information such as the element's name, type, class name, patterns, and ancestors in a dictionary format.

**Parameters:**
- `element: auto.Control`: The UI element to inspect.

**Returns:**
- `Dict[str, Any]`: A dictionary containing detailed element information.

**Example Return Value:**
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

### `get_unique_style_classes(pid: int) -> List[str]`

Scans the entire UI tree to retrieve a list of unique class names.

Useful for identifying QSS selectors.

**Parameters:**
- `pid: int`: Process ID.

**Returns:**
- `List[str]`: A list of discovered class names.

### `get_extensive_ui_tree(pid: int) -> str`

Scans the entire UI tree of the application with the specified PID.

Traverses the entire control tree using UI Automation and returns a formatted string representation.

**Parameters:**
- `pid: int`: Process ID.

**Returns:**
- `str`: Formatted string representation of the UI tree.

### `get_window_structure(target_pid: int) -> List[Dict[str, Any]]`

Retrieves the window structure (hierarchy) using the Win32 API (legacy).

**Parameters:**
- `target_pid: int`: Target process ID.

**Returns:**
- `List[Dict[str, Any]]`: A list of window information dictionaries.

## Implementation Details

### UI Automation Usage
Uses the `uiautomation` library to access UI elements.

### Element Searching
- `ControlFromPoint()`: Gets the element at the cursor position.
- `GetRootControl()`: Gets the root control.
- `GetChildren()`: Gets child elements.

### Highlighting
Uses a Tkinter transparent window to show a red frame. Executed in a separate thread to avoid blocking.

### LegacyIAccessiblePattern
For Qt applications, `LegacyIAccessiblePattern` is used to retrieve detailed information.

## Error Handling
All methods implement proper error handling and safely process any exceptions.

## Related Modules
- `uiautomation`: UI Automation API
- `win32gui`: Win32 GUI API
- `win32process`: Process information
