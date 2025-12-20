# Updater Feature

This document explains the updater feature integrated into the N-LINE application.

## Overview
This feature allows users to check for the latest version from within the application and download/install updates directly.

## Features

### Version Check
- Retrieves the latest version from the GitHub Releases API.
- Compares it with the currently installed version.
- Notifies the user if an update is available.

### Downloading
- Downloads the installer for the latest version.
- Displays download progress with a progress bar.
- Saves the file to a temporary directory.

### Installation
- Automatically runs the downloaded installer.
- Executes in silent installation mode.
- Automatically closes the application during the update.

## Usage

### Within the Application
1. Click the "Check for Updates" button in the footer of the main window.
2. The Update dialog will open.
3. Click "Check" to look for the latest version.
4. If an update is available, click the "Download" button.
5. Once the download is complete, click "Install" to begin the installation.

### Automatic Checks (Future Implementation)
The ability to automatically check for updates on startup will be added in a future release.

## Configuration

### Version Info URL
You can change the source of version information by modifying `VERSION_URL` in `src/n_line/core/updater.py`.

```python
# Using GitHub Releases API
VERSION_URL = "https://api.github.com/repos/yourusername/n-line/releases/latest"

# Using a custom API endpoint
VERSION_URL = "https://your-domain.com/api/version"
```

### Custom API Endpoint
If using a custom endpoint, the response must be in the following JSON format:

```json
{
  "tag_name": "v0.3.0",
  "assets": [
    {
      "name": "N-LINE-Setup-0.3.0.exe",
      "browser_download_url": "https://example.com/downloads/N-LINE-Setup-0.3.0.exe"
    }
  ]
}
```

## Version Management

### Bumping the Version
Ensure consistent version numbering across all files:

```bash
# Update version
python scripts/bump_version.py patch  # 0.2.0 -> 0.2.1
python scripts/bump_version.py minor  # 0.2.0 -> 0.3.0
python scripts/bump_version.py major  # 0.2.0 -> 1.0.0

# Specify specific version
python scripts/bump_version.py 0.3.0
```

### Updated Files
- `pyproject.toml` - Project metadata.
- `src/n_line/__init__.py` - Package version.
- `installer.iss` - Installer version.

### Verifying Versions
```bash
# Check version consistency
python scripts/check_version.py
```

## Troubleshooting

### Network Error
- Check your internet connection.
- Verify firewall settings.
- Check proxy settings.

### Download Error
- Check for sufficient disk space in the temporary directory.
- Ensure antivirus software is not blocking the download.
- Download and install manually.

### Installation Error
- Administrator privileges may be required.
- Try uninstalling the existing version before reinstalling.

## Security
- Always use HTTPS for download URLs.
- (Future) Verify installer signatures.
- (Future) Verify checksums.

## Future Improvements
- Automatic update checks on startup.
- Background downloading.
- Delta updates.
- Rollback functionality.
