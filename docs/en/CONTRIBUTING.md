# Contributing Guide

Thank you for contributing to the N-LINE project! Please follow this guide to ensure a smooth contribution process.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Coding Conventions](#coding-conventions)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)

## Code of Conduct

Everyone contributing to this project is expected to follow the code of conduct to maintain an open and welcoming environment.

## How to Contribute

### Reporting Bugs

1. Check existing bug reports on [Issues](https://github.com/nezumi0627/n-line/issues).
2. Create a new issue.
3. Include the following information:
   - Description of the problem
   - Reproduction steps
   - Expected behavior
   - Actual behavior
   - Environmental info (OS, Python version, etc.)
   - Error messages or screenshots

### Feature Requests

1. Check existing requests on [Issues](https://github.com/nezumi0627/n-line/issues).
2. Create a new issue.
3. Include the following information:
   - Description of the feature
   - Use cases
   - Implementation proposals (optional)

### Code Contributions

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/amazing-feature`.
3. Commit your changes: `git commit -m 'feat: Add amazing feature'`.
4. Push the branch: `git push origin feature/amazing-feature`.
5. Create a pull request.

## Development Process

### 1. Clone the Repository

```bash
git clone https://github.com/nezumi0627/n-line.git
cd n-line
```

### 2. Set Up the Development Environment

See the [Developer Guide](DEVELOPMENT.md) for details.

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Implement Changes

- Follow coding conventions.
- Add type hints and docstrings.
- Add tests as necessary.

### 5. Check Code

```bash
# Using Rye
rye run fmt
rye run check

# Using Make
make fmt
make check
```

### 6. Commit

```bash
git add .
git commit -m "feat: description of the feature"
```

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

## Commit Messages

Commit messages should follow [Conventional Commits](https://www.conventionalcommits.org/).

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes only
- `style`: Changes that do not affect the meaning of the code (formatting, etc.)
- `refactor`: Code changes that neither fix a bug nor add a feature
- `test`: Adding or correcting tests
- `chore`: Changes to the build process or auxiliary tools

### Example

```
feat(core): Add process monitoring feature

Add real-time process monitoring to LineManager class.
This allows users to track LINE process status.

Closes #123
```

## Pull Requests

### Checklist

- [ ] Code follows coding conventions.
- [ ] Type hints and docstrings have been added.
- [ ] Tests have been added (if applicable).
- [ ] Documentation has been updated (if applicable).
- [ ] Commit message follows Conventional Commits.
- [ ] All existing tests pass.

### Pull Request Description

Include the following information:

1. **Summary of changes**: What was changed.
2. **Reason for changes**: Why this change is necessary.
3. **Test method**: How you tested it.
4. **Screenshots**: If there are UI changes.

## Review Process

1. Once a pull request is created, it is automatically added to the review queue.
2. A maintainer will perform a review.
3. Respond to any feedback provided.
4. Once approved, it will be merged.

## Questions?

If you have any questions or uncertainties, please ask via [Issues](https://github.com/nezumi0627/n-line/issues).

## License

By contributing code, you agree that your contribution will be licensed under the project's license (MIT).
