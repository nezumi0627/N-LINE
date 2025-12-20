# DebugTools Module

A module providing utility functions for debugging.

## Overview

`DebugTools` is a utility class providing only static methods for retrieving system and process information, and scanning directories.

## Class

### `DebugTools`

A class with only static methods; instantiation is not required.

## Methods

### `get_system_info() -> Dict[str, str]`

Retrieves system information.

**Returns:**
- `Dict[str, str]`: A dictionary containing system info.

**Example Return Value:**
```python
{
    "OS": "nt",
    "Platform": "win32",
    "Python Version": "3.11.0",
    "User Profile": "C:\\Users\\username"
}
```

### `get_line_process_details() -> List[Dict[str, Any]]`

Retrieves detailed information about LINE processes.

**Returns:**
- `List[Dict[str, Any]]`: A list of process details.

**Example Return Value:**
```python
[
    {
        "pid": 12345,
        "name": "LINE.exe",
        "cpu_percent": 2.5,
        "memory_info": psutil._pswindows.svmem(rss=123456789, ...),
        "cmdline": ["LINE.exe", "--arg1", "--arg2"],
        "create_time": 1234567890.0
    }
]
```

### `scan_line_directories() -> Dict[str, List[str]]`

Scans LINE-related directories and retrieves lists of files.

**Returns:**
- `Dict[str, List[str]]`: A dictionary mapping directory names to lists of filenames.

**Example Return Value:**
```python
{
    "Install Dir": ["LINE.exe", "LineLauncher.exe", "..."],
    "Data Dir": ["Cache", "Local Storage", "..."]
}
```

## Implementation Details

### System Information Retrieval
- `os.name`: OS name
- `sys.platform`: Platform name
- `sys.version`: Python version
- `os.environ.get("USERPROFILE")`: User profile path

### Process Information Retrieval
Uses `psutil` to retrieve process info including PID, name, CPU usage, memory usage, command-line arguments, and creation time.

### Directory Scanning
- Installation directory: Obtained from `LineManager.get_install_path()`.
- Data directory: Obtained via `%LOCALAPPDATA%\LINE`.

## Error Handling
All methods implement appropriate error handling to safely manage exceptions.

## Related Modules
- `psutil`: Process management
- `os`: File system operations
- `sys`: System information
- `n_line.core.line_manager`: LINE process management
