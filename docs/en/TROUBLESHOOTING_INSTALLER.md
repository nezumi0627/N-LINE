# Installer Creation Troubleshooting

## customtkinter Not Found Error

### Problem
When running the executable, the following error occurs:
```
ModuleNotFoundError: No module named 'customtkinter'
```

### Solutions

#### 1. Build within a Virtual Environment
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create executable
pyinstaller --clean n-line.spec
```

#### 2. Verify customtkinter is installed correctly
```bash
python -c "import customtkinter; print(customtkinter.__file__)"
```

#### 3. Update PyInstaller
```bash
pip install --upgrade pyinstaller
```

#### 4. Try Folder Mode instead of One-file Mode
Modify the `exe` and `coll` sections in `n-line.spec`:

```python
exe = EXE(
    pyz,
    a.scripts,
    [],  # Empty list
    exclude_binaries=True,  # Exclude binaries
    name='N-LINE',
    # ...
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    # ...
    name='N-LINE',
)
```
This will create all files in the `dist/N-LINE/` folder.

#### 5. Build in Debug Mode
In `n-line.spec`:
```python
console=True,  # Show console
debug=True,   # Output debug information
```
This will provide more detailed error messages.

## Other Issues

### Asset Files Not Found
If customtkinter asset files are missing:
1. Check the `datas` section in `n-line.spec`.
2. Verify the path to customtkinter is correct.
3. Manually add the asset files.

### Executable is Too Large
- Set `upx=False` in `n-line.spec`.
- Add unnecessary modules to the `excludes` list.

### Slow Startup
- One-file mode is naturally slower to start.
- Consider using Folder Mode for faster startup.
