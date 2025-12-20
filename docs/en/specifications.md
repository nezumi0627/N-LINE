# N-LINE Technical Specifications

## Tech Stack
- **Language**: Python 3.11+
- **GUI Framework**: CustomTkinter (a modern UI wrapper for Tkinter)
- **Process Management**: `psutil` (cross-platform process and system monitoring)
- **Windows Integration**: 
  - `pywin32` (low-level Win32 API access for window manipulation)
  - `uiautomation` (Microsoft UI Automation for deep UI inspection and control)
- **Image Processing**: `Pillow` (PIL Fork)

## Architecture

### Directory Structure
```
N-LINE/
├── core/                   # Core business logic
│   ├── line_manager.py     # Main logic for LINE process/file operations
│   ├── backup_manager.py   # Backup functionality
│   ├── debug_tools.py      # System info and file scanning
│   ├── ui_inspector.py     # Win32 & UIA window inspection logic
│   ├── window_manipulator.py # Window operations (opacity, topmost, title)
│   └── automation_manager.py # Automated interaction (input, key sending)
├── gui/                    # Graphical User Interface
│   ├── app.py              # Main application window and tabs
│   └── debug_tools.py      # Debugging tool sub-window logic
├── docs/                   # Documentation (Japanese)
│   └── en/                 # English Documents
├── venv/                   # Virtual environment
├── main.py                 # Application entry point
├── run.bat                 # Execution script
├── requirements.txt        # Dependency list
└── README.md               # Project overview
```

### Core Design Principles
1.  **Separation of Concerns**: UI logic (`gui/`) is separated from business logic (`core/`). GUI classes call static methods or instances of core classes.
2.  **Thread Safety**: Monitoring tasks (such as checking if LINE is running) are executed in separate threads (`threading.Thread`) to prevent the main GUI thread from freezing.
3.  **Robust Error Handling**: File and process operations are wrapped in try-except blocks to appropriately handle permission issues or missing files.
4.  **Extensibility**: The project is structured so that new modules (e.g., `window_manipulator`, `automation_manager`) can be easily added without rewriting existing code.

## Key Modules

### LineManager (`core.line_manager`)
- **Role**: Manages the lifecycle of the LINE process.
- **Key Methods**: 
  - `is_line_running()`: Checks for active processes.
  - `kill_line()`: Forcibly terminates LINE.exe and associated processes.
  - `clear_cache()`: Deletes temporary files from the local AppData directory.

### UIInspector (`core.ui_inspector`)
- **Role**: Analyzes the window structure of running processes.
- **Tech**: Uses `win32gui` for standard window enumeration and `uiautomation` for deep tree traversal of common UI elements (buttons, input fields).

### AutomationManager (`core.automation_manager`)
- **Role**: Handles programmatic interaction with the LINE client.
- **Functionality**: Sends keystrokes or injects text into specific discovered control elements (e.g., `AutoSuggestTextArea`).
