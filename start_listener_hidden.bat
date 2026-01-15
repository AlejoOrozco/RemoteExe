@echo off
REM START_LISTENER_HIDDEN.BAT - Start Listener Completely Hidden (Windows)
REM ======================================================================
REM This script starts the listener with NO visible window at all.
REM It runs completely in the background using pythonw.exe
REM
REM HOW TO USE:
REM 1. Double-click this file
REM 2. The listener will start with no window visible
REM 3. Check listener.log to see if it's running

echo Starting RemoteExe Listener (hidden mode)...

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if listener.py exists
if not exist "listener.py" (
    echo ERROR: listener.py not found in current directory
    pause
    exit /b 1
)

REM Use pythonw.exe instead of python.exe
REM pythonw.exe runs Python scripts without showing a console window
start /B pythonw listener.py

echo.
echo Listener started in hidden mode (no window visible)!
echo.
echo To verify it's running:
echo 1. Check listener.log file
echo 2. Or use: tasklist | findstr python
echo.
echo To stop: Use stop_listener.bat or Task Manager
echo.
timeout /t 3 >nul
