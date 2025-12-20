# Core Dashboard Functions

## Overview
This document explains the functions of the dashboard (main screen) displayed immediately after starting N-LINE. 
It consists of basic tools for monitoring, controlling, and maintaining processes.

## Status
- **Last Updated**: 2025-12-14
- **Version**: v0.1.0
- **State**: Stable

## Feature Details

### 1. Status Monitor
- **Description**: Constantly monitors whether LINE is running or stopped.
- **Display**:
    - 🟢 **APP RUNNING**: Running
    - 🔴 **STOPPED**: Stopped

### 2. Kill LINE Process
- **Description**: Forcefully terminates all LINE processes (`LINE.exe`, `LineLauncher.exe`, etc.).
- **Purpose**: Recovery from freezes or when you want a complete restart.

### 3. Clear Cache
- **Description**: Deletes LINE's temporary files to make it run smoother.
- **Target**: Files under `%USERPROFILE%\AppData\Local\LINE\Data\Cache`.
- **Note**: This cannot be executed while LINE is running (due to file locking).

### 4. Launch LINE
- **Description**: Launches the installed version of LINE.
- **Supported Paths**: Automatically searches standard installation locations (`AppData\Local\LINE\bin`).

### 5. Open Install Folder
- **Description**: Opens the LINE installation directory in Explorer.
- **Purpose**: Convenient for manual file checking or placing mods.

## Changelog

| Version | Date | Description |
|:---|:---|:---|
| v0.1.0 | 2025-12-11 | Product release. Implementation of basic features. |
