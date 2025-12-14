# N-LINE Technical Specifications

## Technology Stack
- **Language**: Python 3.11+
- **GUI Framework**: CustomTkinter (Modern UI wrapper for Tkinter)
- **Process Management**: `psutil` (Cross-platform process and system monitoring)
- **Windows Integration**: 
  - `pywin32` (Win32 API access for low-level window manipulation)
  - `uiautomation` (Microsoft UI Automation for deep UI inspection and control)
- **Image Processing**: `Pillow` (PIL Fork)

## Architecture

### Directory Structure
```
N-LINE/
├── core/                   # Core business logic
│   ├── line_manager.py     # Main logic for LINE process/file interaction
│   ├── backup_manager.py   # Backup functionality
│   ├── debug_tools.py      # System info and file scanning
│   ├── ui_inspector.py     # Win32 & UIA window inspection logic
│   ├── window_manipulator.py # Window manipulation (opacity, topmost, title)
│   └── automation_manager.py # Automated interaction (typing, keys)
├── gui/                    # Graphical User Interface
│   ├── app.py              # Main application window & tabs
│   └── debug_tools.py      # Debug Tools sub-window logic
├── docs/                   # Documentation
├── venv/                   # Virtual Environment
├── main.py                 # Application Entry Point
├── run.bat                 # Execution script
├── requirements.txt        # Dependency list
└── README.md               # Project Overview
```

### Core Design Principles
1.  **Separation of Concerns**: UI logic (`gui/`) is separated from business logic (`core/`). The GUI classes call static methods or instances of Core classes.
2.  **Thread Safety**: Monitoring tasks (like checking if LINE is running) run in separate threads (`threading.Thread`) to prevent freezing the main GUI thread.
3.  **Robust Error Handling**: File and process operations are wrapped in try-except blocks to handle permissions issues or missing files gracefully.
4.  **Extensibility**: The project is structured to easily add new modules (e.g., `window_manipulator`, `automation_manager`) without rewriting existing code.

## Key Modules

### LineManager (`core.line_manager`)
- **Responsibility**: Manages the LINE process lifecycle.
- **Key Methods**: 
  - `is_line_running()`: Checks active processes.
  - `kill_line()`: Terminates LINE.exe and related processes.
  - `clear_cache()`: Removes temporary files from the local AppData directory.

### UIInspector (`core.ui_inspector`)
- **Responsibility**: Analyzes the window structure of running processes.
- **Technology**: Uses `win32gui` for standard window enumeration and `uiautomation` for deep tree traversal of generic UI elements (buttons, inputs).

### AutomationManager (`core.automation_manager`)
- **Responsibility**: Handles programmatic interaction with the LINE client.
- **Capabilities**: Sends keystrokes and injects text into specific discovered control elements (e.g., `AutoSuggestTextArea`).
