#!/usr/bin/env python3
"""
INSTALL_LISTENER.PY - Complete Installation Script
===================================================
This is the ONLY file you need to install RemoteExe listener.
It configures everything automatically:
- Auto-start on Windows boot
- Run in background (no visible window)
- Works with Python script or compiled .exe

HOW TO USE:
1. Copy listener.py, config.json, and install_listener.py to Windows PC
2. Run as Administrator: python install_listener.py
3. Done! The listener will start automatically on boot in background.

You can also run this remotely via RemoteExe once you have initial access.
"""

import os
import sys
import subprocess
import json
import shutil

def is_admin():
    """Check if running with administrator privileges."""
    try:
        if sys.platform != 'win32':
            return os.getuid() == 0
        # On Windows, check admin privileges
        return subprocess.run(
            ['net', 'session'], 
            capture_output=True, 
            check=False
        ).returncode == 0
    except:
        return False

def get_script_path():
    """Get paths to listener and base directory."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_dir = os.path.dirname(sys.executable)
        listener_path = sys.executable
    else:
        # Running as Python script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        listener_path = os.path.join(base_dir, 'listener.py')
    
    return listener_path, base_dir

def find_pythonw():
    """Find pythonw.exe (runs Python without console window)."""
    # Try to find pythonw.exe in the same directory as python.exe
    python_exe = sys.executable  # e.g., C:\Python39\python.exe
    python_dir = os.path.dirname(python_exe)
    pythonw_exe = os.path.join(python_dir, 'pythonw.exe')
    
    if os.path.exists(pythonw_exe):
        return pythonw_exe
    
    # If not found, try common locations
    common_paths = [
        os.path.join(os.path.dirname(python_exe), 'pythonw.exe'),
        r'C:\Python39\pythonw.exe',
        r'C:\Python310\pythonw.exe',
        r'C:\Python311\pythonw.exe',
        r'C:\Python312\pythonw.exe',
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # Fallback: use python.exe (will show window, but works)
    print("WARNING: pythonw.exe not found, using python.exe (window will be visible)")
    return python_exe

def create_scheduled_task(listener_path, base_dir):
    """
    Creates Windows Task Scheduler task with proper settings:
    - Runs on startup
    - Runs in background (no window)
    - Runs even if user not logged in
    - Highest privileges
    """
    task_name = "RemoteExeListener"
    
    # Check if task already exists
    check_task = subprocess.run(
        ['schtasks', '/query', '/tn', task_name],
        capture_output=True,
        check=False
    )
    
    if check_task.returncode == 0:
        print(f"⚠ Task '{task_name}' already exists.")
        print("Deleting existing task...")
        subprocess.run(['schtasks', '/delete', '/tn', task_name, '/f'], 
                      capture_output=True, check=False)
    
    # Determine how to run the listener
    if listener_path.endswith('.py'):
        # Python script: use pythonw.exe for no window
        pythonw_exe = find_pythonw()
        program = pythonw_exe
        arguments = f'"{listener_path}"'
        start_in = base_dir
    else:
        # Compiled .exe: run directly
        program = listener_path
        arguments = ""
        start_in = base_dir
    
    # Create task using XML for better control (follows image guidelines)
    # This matches the Task Scheduler GUI settings from the image
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>RemoteExe Listener - Remote Command Execution Service</Description>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Enabled>true</Enabled>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <RunLevel>HighestAvailable</RunLevel>
      <UserId>S-1-5-18</UserId>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{program}</Command>
      <Arguments>{arguments}</Arguments>
      <WorkingDirectory>{start_in}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>'''
    
    # Save XML to temp file
    temp_xml = os.path.join(base_dir, 'task_temp.xml')
    try:
        with open(temp_xml, 'w', encoding='utf-16') as f:
            f.write(xml_content)
        
        # Create task from XML
        create_cmd = [
            'schtasks', '/create',
            '/tn', task_name,
            '/xml', temp_xml,
            '/f'
        ]
        
        print(f"Creating scheduled task '{task_name}'...")
        print(f"Program: {program}")
        if arguments:
            print(f"Arguments: {arguments}")
        print(f"Working Directory: {start_in}")
        print()
        
        result = subprocess.run(create_cmd, capture_output=True, text=True)
        
        # Clean up temp file
        if os.path.exists(temp_xml):
            os.remove(temp_xml)
        
        if result.returncode == 0:
            print("✓ Task created successfully!")
            print(f"  ✓ Auto-start on boot: Enabled")
            print(f"  ✓ Background mode: Enabled (no window)")
            print(f"  ✓ Run with highest privileges: Enabled")
            print(f"  ✓ Run even if user not logged in: Enabled")
            return True
        else:
            print("✗ Failed to create task:")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)
            return False
    
    except Exception as e:
        print(f"✗ Error creating task: {str(e)}")
        if os.path.exists(temp_xml):
            os.remove(temp_xml)
        return False

def test_listener_running():
    """Check if listener is currently running."""
    try:
        # Check if port 8888 is in use
        result = subprocess.run(
            ['netstat', '-an'],
            capture_output=True,
            text=True,
            check=False
        )
        if '8888' in result.stdout and 'LISTENING' in result.stdout:
            return True
    except:
        pass
    return False

def main():
    """Main installation function - does everything automatically."""
    print("="*70)
    print("RemoteExe Listener - Complete Installation")
    print("="*70)
    print()
    print("This script will configure:")
    print("  ✓ Auto-start on Windows boot")
    print("  ✓ Run in background (no visible window)")
    print("  ✓ Run with highest privileges")
    print()
    
    # Check if running as admin
    if not is_admin():
        print("⚠ WARNING: Not running as Administrator!")
        print("You need administrator privileges to create scheduled tasks.")
        print()
        print("Please:")
        print("  1. Right-click on this file")
        print("  2. Select 'Run as Administrator'")
        print()
        input("Press Enter to continue anyway (will likely fail)...")
        print()
    
    # Get paths
    listener_path, base_dir = get_script_path()
    
    # Check if listener exists
    if not os.path.exists(listener_path):
        print(f"✗ ERROR: Listener not found at: {listener_path}")
        print("Make sure listener.py or listener.exe is in the same folder.")
        sys.exit(1)
    
    # Check if config.json exists
    config_path = os.path.join(base_dir, 'config.json')
    if not os.path.exists(config_path):
        print(f"⚠ WARNING: config.json not found at: {config_path}")
        print("The listener may not work without configuration.")
        choice = input("Continue anyway? (y/n): ").strip().lower()
        if choice != 'y':
            sys.exit(1)
        print()
    
    print("Files found:")
    print(f"  ✓ Listener: {listener_path}")
    print(f"  ✓ Config: {config_path}")
    print()
    
    # Create scheduled task
    print("Installing...")
    print("-" * 70)
    if create_scheduled_task(listener_path, base_dir):
        print("-" * 70)
        print()
        print("="*70)
        print("✓ INSTALLATION COMPLETE!")
        print("="*70)
        print()
        print("The listener is now configured to:")
        print("  • Start automatically when Windows boots")
        print("  • Run in background (no window visible)")
        print("  • Continue running even after closing terminal")
        print()
        print("To test immediately, you can:")
        print("  1. Restart your computer, OR")
        print("  2. Manually start the task:")
        print("     schtasks /run /tn RemoteExeListener")
        print()
        print("To uninstall later, run:")
        print("  schtasks /delete /tn RemoteExeListener /f")
        print()
        
        # Offer to start now
        if test_listener_running():
            print("ℹ Listener is already running.")
        else:
            start_now = input("Start the listener now? (y/n): ").strip().lower()
            if start_now == 'y':
                print("Starting listener...")
                subprocess.run(['schtasks', '/run', '/tn', 'RemoteExeListener'], 
                             capture_output=True, check=False)
                print("Listener started! Check listener.log to verify.")
    else:
        print("-" * 70)
        print()
        print("✗ INSTALLATION FAILED")
        print()
        print("Possible solutions:")
        print("  1. Make sure you're running as Administrator")
        print("  2. Check if Task Scheduler service is running")
        print("  3. Try running from Command Prompt as Administrator")
        print()
        sys.exit(1)

if __name__ == '__main__':
    main()
