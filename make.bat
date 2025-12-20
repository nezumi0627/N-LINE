@echo off

if "%1"=="" goto help

if "%1"=="install" goto install
if "%1"=="start" goto start
if "%1"=="fmt" goto fmt
if "%1"=="check" goto check
if "%1"=="fix" goto fix
if "%1"=="clean" goto clean
if "%1"=="build-installer" goto build-installer

:help
echo Usage: make.bat [target]
echo.
echo Targets:
echo   install         Install dependencies using rye
echo   start           Run the application
echo   fmt             Format code using rye
echo   check           Lint code
echo   fix             Fix lint errors
echo   clean           Clean temporary files
echo   build-installer Build installer
goto :eof

:install
echo Installing dependencies...
rye sync
goto :eof

:start
echo Starting N-LINE...
rye run python -m n_line
goto :eof

:fmt
echo Formatting code...
rye fmt
goto :eof

:check
echo Checking code...
rye check
goto :eof

:fix
echo Fixing lint errors...
rye check --fix
goto :eof

:clean
echo Cleaning cache...
if exist .ruff_cache rmdir /s /q .ruff_cache
if exist __pycache__ rmdir /s /q __pycache__
if exist src\n_line\__pycache__ rmdir /s /q src\n_line\__pycache__
python scripts\build_installer.py --clean
echo Done.
goto :eof

:build-installer
echo Building installer...
python scripts\build_installer.py
goto :eof
