# N-LINE Features Documentation

## 1. Core Features (Dashboard)

### Status Monitor
- **Description**: Real-time display of LINE's running status.
- **Indicator**: Shows "APP RUNNING" in green or "STOPPED" in red.
- **Mechanism**: Polls the process list every 2 seconds via a background thread using `psutil`.

### Process Killer
- **Description**: Forcefully terminates the LINE application and its associated processes.
- **Use Case**: Useful when LINE freezes, becomes unresponsive, or needs a hard restart.

### Cache Cleaner
- **Description**: Safely removes temporary cache files to free up disk space and resolve loading issues.
- **Constraint**: Only works when LINE is not running (prevents file lock errors).
- **Target**: Clears contents of `%USERPROFILE%\AppData\Local\LINE\Data\Cache`.

### Launch LINE
- **Description**: Starts the LINE application if it is currently stopped.
- **Smart Detection**: automatically searches for the executable in standard installation paths (`LineLauncher.exe`, `LINE.exe`).

### Open Install Folder
- **Description**: Opens the LINE installation directory in Windows Explorer for manual inspection.

## 2. Backup & Tools

### User Data Backup
- **Description**: Creates a backup of the user's LINE data (chats, settings, etc.) excluding the heavy cache folder.
- **Destination**: Backup is saved to `backups/line_backup_YYYYMMDD_HHMMSS`.

## 3. Debug Tools & Engineering
*Accessible via the "Open Debug Tools" button.*

### Process Info
- **Details**: Displays system information (OS, Python version) and detailed metrics for the LINE process (PID, Memory Usage, CPU Usage, Command Line Arguments).

### File Structure
- **Details**: Lists files in the LINE installation directory and the local data folder. Useful for understanding the file layout.

### UI Inspector
- **Standard Scan**: Lists top-level windows belonging to the LINE process using Win32 API. Shows Class Name, Window Title, Visibility, and Size.
- **Deep Scan (UIA)**: Uses Microsoft UI Automation to crawl the entire UI tree. Can identify internal buttons, input fields, pane controls, and their internal IDs (`AutomationId`). This is critical for developing advanced mods or automation scripts.

### Window Mods (Experimental)
- **Opacity Control**: Adjust the transparency of the LINE main window in real-time.
- **Always on Top**: Toggles the "Topmost" state, keeping LINE above all other windows.
- **Title Hijack**: Changes the window title text (e.g., from "LINE" to "N-LINE").
- **Targeting**: Uses Process ID (PID) targeting to ensure the correct window is manipulated even if the title changes.

### Automation (Experimental)
- **Type Text**: Injects text directly into the chat input area (`AutoSuggestTextArea`) without using the clipboard.
- **Send Enter**: Simulates pressing the Enter key to send messages programmatically.
