# Release Procedure

This document explains the release procedures for the N-LINE project.

## 📋 Table of Contents

- [Versioning](#versioning)
- [Pre-release Preparation](#pre-release-preparation)
- [Release Procedure](#release-procedure)
- [Post-release Tasks](#post-release-tasks)

## Versioning

### Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/).

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes.
- **MINOR**: Add functionality in a backwards compatible manner.
- **PATCH**: Backwards compatible bug fixes.

### Version Locations

The version number is managed in the following files:

- `pyproject.toml` - Project metadata.
- `src/n_line/__init__.py` - Package version.
- `CHANGELOG.md` - Change history.

## Pre-release Preparation

### 1. Verification

```bash
# Format code
rye run fmt
# or
make fmt

# Lint check
rye run check
# or
make check

# Type check
rye run type-check
# or
mypy src/n_line
```

### 2. Run Tests

```bash
# Run tests
rye run test
# or
pytest
```

### 3. Update Documentation

- Update `CHANGELOG.md`.
- Update `README.md` as necessary.
- Verify documentation consistency.

### 4. Bump Version

```bash
# Bump version (e.g., patch)
python scripts/bump_version.py patch

# Or specify a specific version
python scripts/bump_version.py 0.3.0
```

### 5. Verify Version Consistency

```bash
python scripts/check_version.py
```

## Release Procedure

### 1. Commit Changes

```bash
git add .
git commit -m "chore(release): bump version to v0.3.0"
```

### 2. Create Tag

```bash
# Create tag
git tag -a v0.3.0 -m "Release v0.3.0"

# Push tag
git push origin v0.3.0
```

### 3. Automated Release via GitHub Actions

Pushing a tag automatically triggers GitHub Actions to:
1. Verify the version number.
2. Generate a CHANGELOG.
3. Create a GitHub Release.

### 4. Manual Release (if necessary)

If GitHub Actions is unavailable:
```bash
# Generate CHANGELOG
python scripts/generate_changelog.py > CHANGELOG_TEMP.md

# Manually create a GitHub Release
# https://github.com/nezumi0627/n-line/releases/new
```

## Post-release Tasks

### 1. Verify Release Notes
Check the GitHub Release page to ensure release notes are generated correctly.

### 2. Update Documentation
Update the following documents as needed:
- `README.md` - Update the version number.
- `docs/` - Update feature documentation.

### 3. Notify the Community
- Announce the release to the community.
- Explain any significant changes.

## Version Bump Examples

### Patch Release (Bug Fixes)
```bash
# Current version: 0.2.0
python scripts/bump_version.py patch
# New version: 0.2.1

git add .
git commit -m "chore(release): bump version to v0.2.1"
git tag -a v0.2.1 -m "Release v0.2.1"
git push origin v0.2.1
```

### Minor Release (New Features)
```bash
# Current version: 0.2.0
python scripts/bump_version.py minor
# New version: 0.3.0

git add .
git commit -m "chore(release): bump version to v0.3.0"
git tag -a v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0
```

### Major Release (Breaking Changes)
```bash
# Current version: 0.2.0
python scripts/bump_version.py major
# New version: 1.0.0

git add .
git commit -m "chore(release): bump version to v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## CHANGELOG Updates

### Format
The CHANGELOG follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

```markdown
## [0.3.0] - 2024-12-15

### Added
- Description of new features.

### Changed
- Description of changes.

### Fixed
- Description of bug fixes.

### Removed
- Description of removed features.
```

## Troubleshooting

### Version Mismatch
```bash
# Verify version
python scripts/check_version.py

# Manually fix
# Ensure pyproject.toml and __init__.py versions match.
```

### Tag Creation Fails
```bash
# Check existing tags
git tag

# Delete tag (if necessary)
git tag -d v0.3.0
git push origin :refs/tags/v0.3.0

# Re-create tag
git tag -a v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0
```

## References
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- [Conventional Commits](https://www.conventionalcommits.org/)
