# Installer Creation Guide

This guide explains how to create a Windows installer for N-LINE.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Creating the Installer](#creating-the-installer)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

1. **Python 3.8 or higher**
   - Required to run the project.

2. **PyInstaller**
   - Packages Python applications into executables.
   - Installation: `pip install pyinstaller`

3. **Inno Setup**
   - A tool for creating Windows installers.
   - Download: https://jrsoftware.org/isdl.php
   - Recommended version: Inno Setup 6

### Installing Dependencies

```bash
# Install project dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller
```

## Installation Methods

### Method 1: Using the Automated Script (Recommended)

```bash
# Create both the executable and the installer
python scripts/build_installer.py

# Create only the executable
python scripts/build_installer.py --exe-only

# Create only the installer (if the executable already exists)
python scripts/build_installer.py --installer-only

# Clean up build files
python scripts/build_installer.py --clean
```

### Method 2: Manual Creation

#### Step 1: Creating the Executable

```bash
# Create the executable using PyInstaller
pyinstaller --clean n-line.spec
```

The executable will be created at `dist/N-LINE.exe`.

#### Step 2: Creating the Installer

1. Launch Inno Setup Compiler.
2. Open `installer.iss`.
3. Go to "Build" -> "Compile".

Or, from the command line:

```bash
# Specify the path to Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

The installer will be created at `installer/N-LINE-Setup-0.2.0.exe`.

## Creating the Installer

### Configuration Files

#### `n-line.spec` (PyInstaller Configuration)

Defines the packaging settings for the executable.

Key settings:
- `hiddenimports`: Modules that PyInstaller cannot detect.
- `datas`: Data files.
- `console`: Set to `False` as this is a GUI application.

#### `installer.iss` (Inno Setup Configuration)

Defines the installer settings.

Key settings:
- `AppName`: Application name.
- `AppVersion`: Version number.
- `DefaultDirName`: Default installation path.
- `OutputBaseFilename`: Installer file name.

### Customization

#### Adding an Icon

1. Prepare an icon file (`.ico`).
2. Update the `icon` parameter in `n-line.spec`:
   ```python
   icon='path/to/icon.ico',
   ```
3. Update `SetupIconFile` in `installer.iss`:
   ```iss
   SetupIconFile=path/to/icon.ico
   ```

#### Adding a License File

1. Prepare a license file (`.txt`).
2. Update `LicenseFile` in `installer.iss`:
   ```iss
   LicenseFile=LICENSE.txt
   ```

#### Installing Additional Files

Add them to the `[Files]` section of `installer.iss`:

```iss
[Files]
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs
```

## Troubleshooting

### PyInstaller Related

#### Module Not Found
**Problem**: `ModuleNotFoundError` occurs.
**Solution**:
1. Add the module to `hiddenimports` in `n-line.spec`.
2. Rebuild: `pyinstaller --clean n-line.spec`.

#### Executable is Too Large
**Problem**: The executable size is very large.
**Solution**:
1. Add unnecessary modules to `excludes` in `n-line.spec`.
2. Use UPX compression (`upx=True`).

#### Detected as Malware
**Problem**: The executable is detected as a virus by antivirus software.
**Solution**:
1. Use a code signing certificate.
2. Add an exception to the antivirus software.
3. Use the latest version of PyInstaller.

### Inno Setup Related

#### Inno Setup Not Found
**Problem**: The `iscc` command is not found.
**Solution**:
1. Verify Inno Setup is installed.
2. Add the path to your environment variables.
3. Check the path in `scripts/build_installer.py`.

#### Installer Not Created
**Problem**: A compilation error occurs.
**Solution**:
1. Check the syntax in `installer.iss`.
2. Open directly in Inno Setup Compiler to see errors.
3. Check the log files.

### Miscellaneous

#### Executable Does Not Start
**Problem**: Nothing happens when double-clicking the executable.
**Solution**:
1. Run from the command prompt to see error messages.
2. Verify all dependencies are included correctly.
3. Check if antivirus software is blocking it.

#### Poor Performance
**Problem**: The executable takes a long time to start.
**Solution**:
1. Use "folder mode" instead of "one-file mode."
2. Exclude unnecessary modules.
3. Optimize imports at startup.

## Distribution

### Distributing the Installer
You can distribute the created installer (`installer/N-LINE-Setup-0.2.0.exe`).

### Signing (Optional)
Signing the installer with a code signing certificate can avoid security warnings.

```bash
# Example of signing (replace with actual certificate path)
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com installer/N-LINE-Setup-0.2.0.exe
```

## References

- [PyInstaller Official Documentation](https://pyinstaller.org/)
- [Inno Setup Official Documentation](https://jrsoftware.org/ishelp/)
- [Distributing Python Applications](https://docs.python.org/3/distributing/index.html)
