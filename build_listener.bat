@echo off
REM BUILD_LISTENER.BAT - Build Windows Executable
REM ==============================================
REM This script uses PyInstaller to create a standalone .exe file
REM that doesn't require Python to be installed on the target PC.
REM
REM HOW TO USE:
REM 1. Make sure PyInstaller is installed: pip install pyinstaller
REM 2. Run this script: build_listener.bat
REM 3. The .exe will be created in the 'dist' folder

echo ========================================
echo RemoteExe Listener - Build Script
echo ========================================
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller.
        pause
        exit /b 1
    )
)

echo.
echo Building Windows executable...
echo.

REM Build the executable
REM --onefile: Creates a single .exe file
REM --name: Name of the output file
REM --noconsole: Run without console window (for background service)
REM --add-data: Include config.json with the executable
REM --hidden-import: Ensure all modules are included

pyinstaller --onefile ^
    --name listener ^
    --noconsole ^
    --add-data "config.json;." ^
    --hidden-import json ^
    --hidden-import socket ^
    --hidden-import subprocess ^
    --hidden-import logging ^
    --hidden-import threading ^
    listener.py

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build successful!
echo ========================================
echo.
echo The executable is located at: dist\listener.exe
echo.
echo Next steps:
echo 1. Copy dist\listener.exe and config.json to the target PC
echo 2. Run install_listener.py (or the compiled version) to set up auto-start
echo.
pause
