@echo off
REM STOP_LISTENER.BAT - Stop Running Listener (Windows)
REM ===================================================
REM This script stops the running listener process.

echo Stopping RemoteExe Listener...

REM Kill Python processes running listener.py
taskkill /F /FI "WINDOWTITLE eq listener.py*" /IM python.exe >nul 2>&1
taskkill /F /FI "COMMANDLINE eq *listener.py*" /IM python.exe >nul 2>&1

REM Also try to kill by process name if it's a compiled .exe
taskkill /F /IM listener.exe >nul 2>&1

REM More aggressive: kill all python processes with "listener" in command line
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /I "PID"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /I "listener" >nul
    if not errorlevel 1 (
        taskkill /F /PID %%a >nul 2>&1
    )
)

echo.
echo Listener stopped (if it was running).
echo.
pause
