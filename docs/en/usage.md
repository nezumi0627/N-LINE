# N-LINE Usage Guide

## Installation and Setup

### Prerequisites
- Windows 10 or 11
- Python 3.11 or higher
- LINE Desktop application must be installed

### Quick Start
1. Double-click `run.bat` to launch.
   - On the first run, a virtual environment (`venv`) will be created automatically, and the necessary libraries (`uiautomation`, `customtkinter`, etc.) will be installed.

---

## 🚀 Advanced Usage

### 1. How to use UI Inspector Mode (Spy Mode)
This feature allows you to investigate LINE's internal structure (button IDs and hierarchy).

1. Open **Debug Tools** and select the **"UI Inspector"** tab.
2. Toggle the **"Inspector Mode (Ctrl+Shift to Spy)"** switch to **ON**.
3. Move your mouse cursor over the LINE window.
4. Press both **`Ctrl`** and **`Shift`** simultaneously on your keyboard.
5. The element you are pointing at will be momentarily highlighted with a **red frame**, and detailed information will appear in the Debug window.

### 2. UI Customization via Arg Injection (Revolution)
This feature allows you to forcefully change LINE's appearance using CSS (Qt Stylesheet / .qss).

#### Preparation
Create a `.qss` file that describes the design you want to apply.
(A sample file named `test_style.qss` is generated at the project root.)

It is recommended to copy this file to one of the following folders that LINE can access:
- `%USERPROFILE%\AppData\Local\LINE\bin\current\`

#### Execution Steps
1. Open **Debug Tools** and select the **"Window Mods"** tab.
2. Locate the **"Arg Injection (Relaunch)"** section at the bottom.
3. Enter arguments in the input field.
   - Example: `-stylesheet test_style.qss`
   - Full path example: `-stylesheet "C:\Path\To\Your\style.qss"`
4. Click the **"Relaunch with Args"** button.
5. LINE will restart, and the specified style will be applied.

---

## Basic Operations

### Main Dashboard
- **Kill Process**: Forcefully terminates LINE.
- **Clear Cache**: Deletes the cache (images and temporary files) to improve performance.
- **Launch LINE**: Starts LINE.

### Debug & Mods
- **Opacity / Topmost**: Adjust window transparency or fix it to the front.
- **Automation**: Test text sending while a chat screen is open.
