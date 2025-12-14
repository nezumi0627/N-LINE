# N-LINE Project

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-v0.2.0-orange.svg)

> [Japanese Version Here](README.md)

## 💻 Development

This project uses `rye` for dependency management and `makefile` for task automation.

### Commands

| Command | Description |
|:---|:---|
| `make install` | Install dependencies |
| `make start` | Run the application |
| `make fmt` | Format code (ruff) |
| `make check` | Lint check (ruff) |
| `make fix` | Auto-fix lint errors |

For Windows users without `make`, use `make.bat` (e.g., `.\make start`).

**N-LINE** is a powerful Python-based utility for managing, debugging, and modifying the LINE Desktop application on Windows. It provides a modern GUI dashboard for task management (process killing, cache cleaning) and advanced engineering tools for checking internal UI structures and automating interactions.

---

## 📚 Documentation Index

This project contains comprehensive documentation. Please refer to the specific sections below:

| Section | Description | Link |
| :--- | :--- | :--- |
| **✨ Features** | Detailed breakdown of all tools, including Modding and Automation capability. | [View Features](docs/features.md) |
| **🛠️ Specifications** | Technical architecture, directory structure, libraries, and design principles. | [View Specs](docs/specifications.md) |
| **🚀 Usage Guide** | How to install, run, and operate the application. | [View Usage](docs/usage.md) |

---

## 🔥 Quick Start

1. **Install**: Ensure Python 3.11+ is installed.
2. **Run**: Double-click `run.bat`.
3. **Enjoy**: The app handles dependencies (`customtkinter`, `psutil`, `pywin32`, etc.) automatically.

## ⚠️ Disclaimer
This tool is for educational and debugging purposes only. Use it responsibly.
