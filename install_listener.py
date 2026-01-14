#!/usr/bin/env python3
"""
INSTALL_LISTENER.PY - Windows Auto-Start Installation Script
============================================================
This script sets up the listener to start automatically on Windows boot.
It creates a Windows Task Scheduler task that runs the listener on startup.

HOW TO USE:
1. Run this script as Administrator on the Windows PC
2. It will create a scheduled task that starts the listener on boot
3. The listener will run in the background automatically

REQUIREMENTS:
- Run as Administrator (right-click -> Run as Administrator)
- Python must be installed (or use the compiled .exe version)
"""

import os
import sys
import subprocess
import json

def is_admin():
    """
    Checks if the script is running with administrator privileges.
    Returns True if running as admin, False otherwise.
    """
    try:
        # On Windows, try to create a file in a protected directory
        # If we can't, we're not admin
        return os.getuid() == 0 if sys.platform != 'win32' else subprocess.run(
            ['net', 'session'], 
            capture_output=True, 
            check=False
        ).returncode == 0
    except:
        return False

def get_script_path():
    """
    Gets the path to the listener executable or script.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_dir = os.path.dirname(sys.executable)
        listener_path = sys.executable
    else:
        # Running as Python script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        listener_path = os.path.join(base_dir, 'listener.py')
    
    return listener_path, base_dir

def create_scheduled_task(listener_path):
    """
    Creates a Windows Task Scheduler task to run the listener on startup.
    
    Args:
        listener_path (str): Full path to listener.exe or listener.py
    """
    # Task name
    task_name = "RemoteExeListener"
    
    # Check if task already exists
    check_task = subprocess.run(
        ['schtasks', '/query', '/tn', task_name],
        capture_output=True,
        check=False
    )
    
    if check_task.returncode == 0:
        print(f"Task '{task_name}' already exists.")
        choice = input("Delete and recreate? (y/n): ").strip().lower()
        if choice == 'y':
            subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'], check=False)
        else:
            print("Keeping existing task.")
            return
    
    # Create the task
    # /tn = task name
    # /tr = task to run (the listener)
    # /sc = schedule (onstart = when computer starts)
    # /ru = run as (SYSTEM = runs as system service)
    # /rl = run level (HIGHEST = administrator privileges)
    # /f = force (overwrite if exists)
    
    if listener_path.endswith('.py'):
        # If it's a Python script, run it with python
        python_exe = sys.executable
        command = f'"{python_exe}" "{listener_path}"'
    else:
        # If it's an executable, run it directly
        command = f'"{listener_path}"'
    
    # Create the scheduled task
    create_cmd = [
        'schtasks', '/create',
        '/tn', task_name,
        '/tr', command,
        '/sc', 'onstart',
        '/ru', 'SYSTEM',
        '/rl', 'HIGHEST',
        '/f'
    ]
    
    print(f"Creating scheduled task '{task_name}'...")
    print(f"Command: {command}")
    
    result = subprocess.run(create_cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Task created successfully!")
        print(f"  The listener will start automatically on boot.")
        print(f"  Task name: {task_name}")
    else:
        print("✗ Failed to create task:")
        print(result.stderr)
        return False
    
    return True

def main():
    """
    Main installation function.
    """
    print("="*60)
    print("RemoteExe Listener - Auto-Start Installation")
    print("="*60)
    print()
    
    # Check if running as admin
    if not is_admin():
        print("WARNING: Not running as Administrator!")
        print("You need administrator privileges to create scheduled tasks.")
        print("Please right-click and select 'Run as Administrator'")
        input("\nPress Enter to continue anyway (may fail)...")
    
    # Get paths
    listener_path, base_dir = get_script_path()
    
    # Check if listener exists
    if not os.path.exists(listener_path):
        print(f"ERROR: Listener not found at: {listener_path}")
        print("Make sure listener.py or listener.exe is in the same folder.")
        sys.exit(1)
    
    # Check if config.json exists
    config_path = os.path.join(base_dir, 'config.json')
    if not os.path.exists(config_path):
        print(f"WARNING: config.json not found at: {config_path}")
        print("The listener may not work without configuration.")
        choice = input("Continue anyway? (y/n): ").strip().lower()
        if choice != 'y':
            sys.exit(1)
    
    print(f"Listener path: {listener_path}")
    print(f"Config path: {config_path}")
    print()
    
    # Create scheduled task
    if create_scheduled_task(listener_path):
        print()
        print("="*60)
        print("Installation complete!")
        print("="*60)
        print()
        print("The listener will now start automatically when Windows boots.")
        print("You can test it by restarting your computer.")
        print()
        print("To remove auto-start later, run:")
        print(f"  schtasks /delete /tn RemoteExeListener /f")
    else:
        print()
        print("Installation failed. Please check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
