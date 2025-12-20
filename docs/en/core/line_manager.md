# LineManager Module

This module manages LINE processes and installation paths.

## Overview

`LineManager` is a utility class providing only static methods to manage the LINE application process.

## Class

### `LineManager`

A class with only static methods. No instantiation is required.

## Methods

### `get_line_processes() -> List[psutil.Process]`

Retrieves a list of currently running LINE processes.

**Returns:**
- `List[psutil.Process]`: A list of LINE processes, or an empty list if none are found.

**Example:**
```python
from n_line.core.line_manager import LineManager

processes = LineManager.get_line_processes()
for proc in processes:
    print(f"PID: {proc.pid}, Name: {proc.name()}")
```

### `is_line_running() -> bool`

Checks if LINE is currently running.

**Returns:**
- `bool`: `True` if LINE is running, `False` otherwise.

### `kill_line() -> bool`

Terminates all LINE processes.

**Returns:**
- `bool`: `True` if processes were found and termination was attempted, `False` if no processes were found.

### `get_install_path() -> Optional[str]`

Retrieves the installation path for LINE.

Tries to obtain it from currently running processes; if it fails, it checks standard paths like `%LOCALAPPDATA%\LINE\bin`.

**Returns:**
- `Optional[str]`: The installation path, or `None` if not found.

### `clear_cache() -> str`

Clears the LINE cache directory.

**Returns:**
- `str`: A message indicating the result of the process.

### `launch_line() -> str`

Launches LINE.

Checks executable candidates in order of priority:
1. `LineLauncher.exe`
2. `current/LINE.exe`
3. `LINE.exe`

**Returns:**
- `str`: A message indicating the result of the process.

### `relaunch_with_params(args: List[str]) -> str`

Terminates LINE and restarts it with the specified arguments.

**Parameters:**
- `args: List[str]`: A list of command-line arguments to pass at startup.

**Returns:**
- `str`: A message indicating the result of the process.

## Implementation Details

### Process Searching
Uses `psutil.process_iter()` to enumerate processes and filters for those named `LINE.exe`.

### Installation Path Discovery
1. Gets the executable file path from a running process.
2. If it fails, checks standard paths such as `%LOCALAPPDATA%\LINE\bin`.

### Cache Clearing
Deletes the contents of `%LOCALAPPDATA%\LINE\Cache`. For safety, it deletes only the contents and not the folder itself.

## Error Handling
All methods implement proper error handling and safely process any exceptions.

## Related Modules
- `psutil`: Process management
- `os`: File system operations
- `subprocess`: Process launching
