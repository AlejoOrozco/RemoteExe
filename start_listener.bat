@echo off
REM START_LISTENER.BAT - Start Listener in Background (Windows)
REM ============================================================
REM This script starts the listener in the background so it continues
REM running even after you close the terminal.
REM
REM HOW TO USE:
REM 1. Double-click this file, OR
REM 2. Run from CMD: start_listener.bat

echo Starting RemoteExe Listener in background...

REM Get the directory where this script is located
cd /d "%~dp0"

REM Check if listener.py exists
if not exist "listener.py" (
    echo ERROR: listener.py not found in current directory
    echo Please make sure this script is in the same folder as listener.py
    pause
    exit /b 1
)

REM Start the listener in a new window (minimized)
REM /MIN = Start minimized
REM /B = Don't create new window (runs in background)
start /MIN /B python listener.py

REM Alternative: Start completely hidden (no window at all)
REM start /B pythonw listener.py

echo.
echo Listener started in background!
echo.
echo To stop the listener:
echo 1. Open Task Manager (Ctrl+Shift+Esc)
echo 2. Find "python.exe" or "listener.exe" process
echo 3. End the process
echo.
echo Or use: stop_listener.bat
echo.
timeout /t 3 >nul
