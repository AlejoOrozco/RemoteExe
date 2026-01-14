#!/bin/bash
# BUILD_LISTENER.SH - Build Windows Executable (Mac/Linux)
# =========================================================
# This script uses PyInstaller to create a standalone .exe file
# that doesn't require Python to be installed on the target PC.
#
# HOW TO USE:
# 1. Make sure PyInstaller is installed: pip3 install pyinstaller
# 2. Make this script executable: chmod +x build_listener.sh
# 3. Run this script: ./build_listener.sh
# 4. The .exe will be created in the 'dist' folder

echo "========================================"
echo "RemoteExe Listener - Build Script"
echo "========================================"
echo ""

# Check if PyInstaller is installed
if ! python3 -m pip show pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    python3 -m pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "Failed to install PyInstaller."
        exit 1
    fi
fi

echo ""
echo "Building Windows executable..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Build the executable
# --onefile: Creates a single .exe file
# --name: Name of the output file
# --noconsole: Run without console window (for background service)
# --add-data: Include config.json with the executable
# --hidden-import: Ensure all modules are included
# --target-arch: Specify Windows target (if cross-compiling)

python3 -m PyInstaller --onefile \
    --name listener \
    --noconsole \
    --add-data "config.json:." \
    --hidden-import json \
    --hidden-import socket \
    --hidden-import subprocess \
    --hidden-import logging \
    --hidden-import threading \
    listener.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Build failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "Build successful!"
echo "========================================"
echo ""
echo "The executable is located at: dist/listener.exe"
echo ""
echo "Next steps:"
echo "1. Copy dist/listener.exe and config.json to the target Windows PC"
echo "2. Run install_listener.py (or compile it) to set up auto-start"
echo ""
