# API Reference

This is the API reference for N-LINE.

## Core Modules

### LineManager
A module for managing LINE processes and installation paths.
- [Detailed Document](../core/line_manager.md)

### WindowManipulator
A module for manipulating windows using the Win32 API.
- [Detailed Document](../core/window_manipulator.md)

### UIInspector
A module for inspecting and analyzing UI elements using UI Automation.
- [Detailed Document](../core/ui_inspector.md)

### AutomationManager
A module for automating the LINE application using UI Automation.
- [Detailed Document](../core/automation.md)

### DebugTools
A module providing utility functions for debugging.
- [Detailed Document](../core/debug_tools.md)

## GUI Modules

### NLineApp
The main application class.
**Location**: `n_line.gui.app`

### DebugWindow
The window class providing debugging tools.
**Location**: `n_line.gui.debug_window`

## Usage Examples

### Managing LINE Processes
```python
from n_line.core.line_manager import LineManager

# Check if LINE is running
if LineManager.is_line_running():
    print("LINE is running")

# Launch LINE
result = LineManager.launch_line()
print(result)

# Kill LINE processes
LineManager.kill_line()
```

### Window Manipulation
```python
from n_line.core.window_manipulator import WindowManipulator
from n_line.core.line_manager import LineManager

# Get LINE processes
procs = LineManager.get_line_processes()
if procs:
    # Find window
    hwnd = WindowManipulator.find_process_window(procs[0].pid)
    if hwnd:
        # Set opacity
        WindowManipulator.set_opacity(hwnd, 200)
        # Always on top
        WindowManipulator.set_always_on_top(hwnd, True)
```

### UI Element Inspection
```python
from n_line.core.ui_inspector import UIInspector
from n_line.core.line_manager import LineManager

# Get LINE processes
procs = LineManager.get_line_processes()
if procs:
    # Get UI tree
    tree = UIInspector.get_extensive_ui_tree(procs[0].pid)
    print(tree)
    
    # Extract style classes
    classes = UIInspector.get_unique_style_classes(procs[0].pid)
    for cls in classes:
        print(cls)
```

### UI Automation
```python
from n_line.core.automation_manager import AutomationManager

# Type text into chat
result = AutomationManager.type_in_chat("Hello, World!")
print(result)

# Send
result = AutomationManager.press_send()
print(result)
```

## Detailed Information
For detailed API documentation of each module, please refer to the [Core Modules Documentation](../core/).
