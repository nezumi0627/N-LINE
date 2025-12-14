# N-LINE Usage Guide

## Installation & Setup

### Prerequisites
- Windows 10 or 11
- Python 3.11 or higher
- LINE Desktop Application installed

### First Time Setup
1. Clone the repository or download the source code.
2. Run `run.bat` to automatically set up the virtual environment (`venv`) and install dependencies (`requirements.txt`).
   ```powershell
   ./run.bat
   ```

## Running the Application

Double-click `run.bat` in the project root directory. This will:
1. Activate the Python virtual environment.
2. Launch the `N-LINE` GUI.

## Using the Interface

### Main Dashboard
- **Monitor**: Check the top-left indicator for status.
- **Actions**: Click buttons to Kill Process, Clear Cache, or Launch LINE.
- **Logs**: View the operation history in the bottom text area.

### Debug & Mods
1. Click **"Open Debug Tools"** at the bottom of the main window.
2. **Process Info**: Click "Refresh" to see current memory/CPU usage.
3. **UI Inspector**: 
   - "Scan Top Windows" for a quick overview.
   - "Deep Scan" for a detailed tree of all UI elements (takes a few seconds).
4. **Window Mods**:
   - First, click **"Find Main Window"** to lock onto the running LINE process.
   - Use the slider to change Opacity.
   - Toggle "Always on Top" switch.
   - Enter text and click "Set Title" to rename the window.
5. **Automation**:
   - Ensure a chat room is open in LINE.
   - Type text in the input box and click "Type Text".
   - Click "Send 'Enter' Key" to send the message.
