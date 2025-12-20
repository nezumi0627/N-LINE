# Developer Guide

This guide explains how to set up the development environment and develop for the N-LINE project.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Coding Conventions](#coding-conventions)
- [Testing](#testing)
- [Debugging](#debugging)

## Prerequisites

- Python 3.8 or higher
- Windows 10/11
- Git
- (Recommended) Rye or pip

## Development Environment Setup

### Method 1: Using Rye (Recommended)

Rye is a tool that simplifies dependency management and packaging for Python projects.

#### Installing Rye

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://rye-up.com/get/ps1).Content | Invoke-Expression

# Alternatively, install from the official site:
# https://rye-up.com/guide/installation/
```

#### Project Setup

```bash
# Clone the repository
git clone https://github.com/nezumi0627/n-line.git
cd n-line

# Install dependencies
rye sync

# Start the application
rye run start
```

#### Useful Rye Commands

```bash
# Add a dependency
rye add <package-name>

# Add a dev dependency
rye add --dev <package-name>

# Update dependencies
rye sync --update

# Format code
rye run fmt

# Static analysis
rye run check
```

### Method 2: Using pip

#### Creating a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Activate the virtual environment (Linux/Mac)
source venv/bin/activate
```

#### Installing Dependencies

```bash
# Install dependencies
pip install -r requirements.txt

# Install dev dependencies if they exist
pip install -r requirements-dev.txt
```

#### Starting the Application

```bash
python -m n_line
```

## Project Structure

```
n-line/
├── src/
│   └── n_line/              # Main package
│       ├── __init__.py
│       ├── __main__.py      # Entry point
│       ├── core/            # Core functionality modules
│       │   ├── line_manager.py
│       │   ├── window_manipulator.py
│       │   ├── ui_inspector.py
│       │   ├── automation_manager.py
│       │   └── debug_tools.py
│       └── gui/             # GUI modules
│           ├── app.py
│           ├── debug_window.py
│           └── tabs/        # Tab components
│               ├── process_tab.py
│               ├── files_tab.py
│               ├── inspector_tab.py
│               ├── mods_tab.py
│               ├── qss_tab.py
│               └── automation_tab.py
├── docs/                    # Documentation
├── tests/                   # Tests (to be added)
├── pyproject.toml          # Rye/pip configuration
├── requirements.txt        # pip dependencies
├── Makefile                # Make tasks
├── make.bat                # Windows Make tasks
└── README.md              # Project README
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Edit Code

- Follow coding conventions.
- Add type hints and docstrings.
- Add tests as necessary.

### 3. Format and Check Code

```bash
# Using Rye
rye run fmt
rye run check

# Using Make
make fmt
make check
```

### 4. Commit and Push

```bash
git add .
git commit -m "feat: description of the feature"
git push origin feature/your-feature-name
```

### 5. Create a Pull Request

Create a pull request on GitHub and request a review.

## Coding Conventions

### Python Style Guide

- Conform to **PEP 8**.
- Use type hints.
- Add docstrings (Google style recommended).

### Code Example

```python
"""Module description"""
from typing import List, Optional

class ExampleClass:
    """Class description"""

    def example_method(self, param: str) -> Optional[List[str]]:
        """Method description

        Args:
            param: Parameter description

        Returns:
            Return value description
        """
        # Implementation
        pass
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `LineManager`)
- **Functions/Methods**: `snake_case` (e.g., `get_line_processes`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `PROCESS_NAME`)
- **Private Methods**: `_leading_underscore` (e.g., `_internal_method`)

### Import Order

1. Standard libraries
2. Third-party libraries
3. Local modules

```python
import os
from typing import List

import customtkinter
import psutil

from n_line.core.line_manager import LineManager
```

## Testing

### Running Tests

```bash
# Using pytest (to be added)
pytest

# Run specific tests
pytest tests/test_line_manager.py
```

### Writing Tests

```python
"""Test module"""
import pytest

from n_line.core.line_manager import LineManager


def test_get_line_processes():
    """Test retrieving LINE processes"""
    processes = LineManager.get_line_processes()
    assert isinstance(processes, list)
```

## Debugging

### Checking Logs

Logs can be viewed in the log text box within the application.

### Using Debug Tools

1. Click "Open Debug Tools" from the main window.
2. Check debug information in each tab.

### Common Issues

#### LINE Process Not Found
- Ensure LINE is running.
- Try running with administrator privileges.

#### UI Automation Not Working
- COM initialization may be required.
- Use `UIAutomationInitializerInThread`.

See [Troubleshooting](TROUBLESHOOTING.md) for more details.

## Dependency Management

### Adding New Dependencies

#### Using Rye
```bash
rye add <package-name>
rye sync
```

#### Using pip
```bash
pip install <package-name>
pip freeze > requirements.txt
```

### Updating Dependencies

#### Using Rye
```bash
rye sync --update
```

#### Using pip
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

## Release Procedure

1. Update the version number (`pyproject.toml`).
2. Update the CHANGELOG.
3. Create a tag.
4. Create a release on GitHub.

## References

- [Official Python Documentation](https://docs.python.org/3/)
- [Official Rye Documentation](https://rye-up.com/)
- [PEP 8](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
