# Troubleshooting

This document summarizes common issues and solutions when using N-LINE.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Runtime Errors](#runtime-errors)
- [Features Not Working](#features-not-working)
- [Performance Issues](#performance-issues)

## Installation Issues

### Python Not Found
**Problem**: The `python` command is not recognized.
**Solution**:
1. Verify if Python is installed.
2. Check if Python is added to the `PATH` environment variable.
3. Ensure Python 3.8 or higher is installed.

### Dependency Installation Fails
**Problem**: `pip install` or `rye sync` fails.
**Solution**:
1. Check your internet connection.
2. Try running as an administrator.
3. Ensure you are using a virtual environment.
4. Clear old caches: `pip cache purge`.

### pywin32 Installation Error
**Problem**: Installation of `pywin32` fails.
**Solution**:
1. Check if Visual C++ Redistributable is installed.
2. Run as administrator: `pip install pywin32`.
3. After manual installation, run `python Scripts/pywin32_postinstall.py -install`.

## Runtime Errors

### LINE Process Not Found
**Problem**: Error stating that the LINE process cannot be found.
**Solution**:
1. Verify if LINE is running.
2. Ensure the process name is `LINE.exe`.
3. Try running as an administrator.
4. Check the Task Manager for LINE processes.

### Module Not Found
**Problem**: `ModuleNotFoundError` occurs.
**Solution**:
1. Verify if dependencies are installed: `pip list`.
2. Check if the virtual environment is active.
3. Reinstall dependencies: `pip install -r requirements.txt`.

### Window Not Found
**Problem**: Window manipulation features cannot find the window.
**Solution**:
1. Verify if LINE is running.
2. Check if the LINE window is visible (not purely a background process).
3. Ensure the window is not minimized.
4. Try using a different Process ID (PID).

## Features Not Working

### UI Automation Not Working
**Problem**: UI Inspector or automation features do not function.
**Solution**:
1. Verify if LINE is running.
2. Check if a chat window is open.
3. Try running as an administrator.
4. COM initialization might be required (using `UIAutomationInitializerInThread` in code).

### Hotkeys Not Working
**Problem**: Point-to-inspect (Ctrl+Shift) does not work.
**Solution**:
1. Try running as an administrator (Windows sometimes requires this for global hotkeys).
2. Check if other applications are using the same hotkeys.
3. Verify if the `keyboard` library is functioning correctly.

### QSS Not Applied
**Problem**: Styles do not change after applying a QSS file.
**Solution**:
1. Verify if LINE was restarted.
2. Ensure the QSS file path is correct.
3. Check the syntax of the QSS file for errors.
4. Verify the class names are correct (use UI Inspector to check).

### Cache Clearing Fails
**Problem**: Clearing the cache fails.
**Solution**:
1. Ensure LINE is completely shut down.
2. Try running as an admin.
3. Manually delete the cache folder at `%LOCALAPPDATA%\LINE\Cache`.

## Performance Issues

### Application is Heavy/Laggy
**Problem**: The application responds slowly.
**Solution**:
1. Check system resources (CPU, Memory).
2. Close other resource-heavy applications.
3. Close debug tool tabs to reduce memory usage.

### UI Inspector is Slow
**Problem**: Scanning the UI tree takes a long time.
**Solution**:
1. Deep scans take time; use standard scans when possible.
2. Avoid other tasks during scanning.
3. Limit the scan range if necessary.

## Miscellaneous Issues

### Logs Not Displayed
**Problem**: Nothing appears in the log text box.
**Solution**:
1. Check if log output is enabled.
2. Restart the application.
3. Check for internal errors in the console/terminal.

### Debug Window Does Not Open
**Problem**: Clicking the debug tool button does nothing.
**Solution**:
1. Check if the window is already open or behind others.
2. Restart the application.
3. Check the error log.

## Support

If the above solutions do not resolve your problem, please seek support via:

1. Reporting the issue on [GitHub Issues](https://github.com/nezumi0627/n-line/issues).
2. Attaching error messages and logs.
3. Describing your environment (OS, Python version, etc.).
