# RemoteExe - Remote Command Execution System

A simple, secure system to remotely execute commands on computers in your local network. Perfect for managing multiple PCs from a central location.

## 📋 What is RemoteExe?

RemoteExe allows you to:
- **Send commands** from your Mac to Windows PCs on your network
- **Execute commands** remotely (like `taskkill`, `shutdown`, custom scripts, etc.)
- **Automatically discover** listeners on your network
- **Run listeners** as background services that start on boot

## 🏗️ Architecture

```
Your Mac (Broadcaster)          Windows PC (Listener)
     │                                │
     │ 1. UDP Discovery               │
     ├───────────────────────────────>│
     │                                │
     │ 2. TCP Connect                 │
     ├───────────────────────────────>│
     │                                │
     │ 3. Authenticate                │
     ├───────────────────────────────>│
     │                                │
     │ 4. Send Command                │
     ├───────────────────────────────>│
     │                                │ Executes command
     │                                │
     │ 5. Receive Results             │
     │<───────────────────────────────┤
```

## 📁 Project Structure

```
RemoteExe/
├── broadcaster.py          # Controller (runs on your Mac)
├── listener.py             # Agent (runs on Windows PCs)
├── config.json             # Configuration file
├── install_listener.py     # Auto-start installer for Windows
├── build_listener.bat      # Script to build Windows .exe
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start Guide

### Step 1: Setup on Your Mac (Broadcaster)

1. **Make sure Python 3 is installed**
   ```bash
   python3 --version
   ```

2. **Navigate to the project folder**
   ```bash
   cd "/Users/alejandrogomezorozco/Documents/Dev/Software Apps/RemoteExe"
   ```

3. **Edit the password in config.json**
   ```bash
   # Open config.json and change the password
   # Use a strong password for security!
   ```

4. **Run the broadcaster**
   ```bash
   python3 broadcaster.py
   ```

### Step 2: Setup on Windows PC (Listener)

#### Option A: Using Python Script (Requires Python on Windows)

1. **Copy these files to the Windows PC:**
   - `listener.py`
   - `config.json` (with the same password!)

2. **Install Python 3** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)

3. **Run the listener:**
   ```cmd
   python listener.py
   ```

4. **Set up auto-start:**
   - Right-click `install_listener.py`
   - Select "Run as Administrator"
   - This will make the listener start on boot

#### Option B: Using Standalone Executable (No Python Required)

1. **On your Mac, build the Windows executable:**
   ```bash
   # First, install PyInstaller
   pip3 install pyinstaller
   
   # Then run the build script (you'll need to adapt it for Mac)
   # Or manually run:
   pyinstaller --onefile --name listener --noconsole --add-data "config.json;." listener.py
   ```

2. **Copy to Windows PC:**
   - Copy `dist/listener.exe` from the build
   - Copy `config.json` (same password!)

3. **Run the listener:**
   - Double-click `listener.exe`
   - Or run from command prompt

4. **Set up auto-start:**
   - Create a compiled version of `install_listener.py` or run it with Python
   - Run as Administrator to set up auto-start

## 🔧 Configuration

Edit `config.json` to customize settings:

```json
{
  "port": 8888,                    // TCP port for commands
  "password": "your_password",     // Authentication password
  "discovery_port": 8889,          // UDP port for discovery
  "timeout": 30,                   // Connection timeout (seconds)
  "max_connections": 5             // Max simultaneous connections
}
```

**Important:** Make sure the password in `config.json` matches on both broadcaster and listener!

## 📖 How to Use

### Using the Broadcaster

1. **Start the broadcaster:**
   ```bash
   python3 broadcaster.py
   ```

2. **Discovery:**
   - The broadcaster will automatically search for listeners on your network
   - If found, it will list them
   - If not found, you can enter an IP address manually

3. **Select a listener:**
   - If multiple listeners found, choose one
   - If only one, it's selected automatically

4. **Send commands:**
   ```
   RemoteExe> taskkill /F /IM notepad.exe
   RemoteExe> shutdown /s /t 60
   RemoteExe> echo Hello from remote PC
   RemoteExe> exit
   ```

5. **View results:**
   - Command output is displayed immediately
   - Shows success/failure, output, errors, and exit codes

### Example Commands

**Windows Commands:**
```bash
# Kill a process
taskkill /F /IM notepad.exe

# Shutdown in 60 seconds
shutdown /s /t 60

# Cancel shutdown
shutdown /a

# List running processes
tasklist

# Send a message (if enabled)
msg * "Hello from remote!"

# Run a program
start notepad.exe
```

## 🔒 Security Considerations

1. **Password Protection:**
   - Always use a strong password in `config.json`
   - Change the default password immediately

2. **Network Security:**
   - This is designed for **trusted local networks only**
   - Don't expose the listener to the internet
   - Consider using a firewall to restrict access

3. **Command Validation:**
   - The listener executes commands as the user running it
   - Be careful with commands that could damage the system
   - Consider adding command whitelisting for production use

## 🐛 Troubleshooting

### Broadcaster can't find listeners

1. **Check network:**
   - Make sure both computers are on the same network
   - Check firewall settings (port 8888 and 8889 should be open)

2. **Check listener:**
   - Make sure listener is running on Windows PC
   - Check if it's listening: `netstat -an | findstr 8888`

3. **Manual connection:**
   - Use the manual IP entry option in broadcaster
   - Find Windows PC IP: `ipconfig` (Windows) or check router

### Listener won't start

1. **Check Python:**
   - Make sure Python 3 is installed
   - Try: `python --version`

2. **Check config.json:**
   - Make sure it exists in the same folder
   - Check JSON syntax is valid

3. **Check port:**
   - Make sure port 8888 is not in use
   - Try changing port in config.json

### Auto-start not working

1. **Check permissions:**
   - Make sure you ran `install_listener.py` as Administrator

2. **Check task:**
   - Open Task Scheduler
   - Look for "RemoteExeListener" task
   - Check if it's enabled

3. **Test manually:**
   - Try running the listener manually first
   - If it works manually, the auto-start setup might be the issue

## 📝 Understanding the Code

### Listener.py - How It Works

1. **Configuration Loading:**
   - Reads `config.json` for settings
   - Handles both script and executable modes

2. **Discovery Server:**
   - Runs in a separate thread
   - Listens for UDP broadcast messages
   - Responds with listener information

3. **Command Server:**
   - Main TCP server on port 8888
   - Accepts connections from broadcaster
   - Authenticates using password
   - Executes commands using `subprocess`
   - Returns results as JSON

4. **Command Execution:**
   - Uses `subprocess.run()` for safe execution
   - Captures stdout, stderr, and exit codes
   - Has timeout protection (30 seconds)

### Broadcaster.py - How It Works

1. **Discovery:**
   - Sends UDP broadcast to find listeners
   - Collects responses
   - Lists available listeners

2. **Connection:**
   - Connects to selected listener via TCP
   - Authenticates with password
   - Maintains connection for multiple commands

3. **Command Sending:**
   - Sends commands as JSON
   - Receives results
   - Displays formatted output

## 🔄 Future Enhancements

Possible improvements you could add:

- [ ] Command history
- [ ] Multiple simultaneous connections
- [ ] File transfer capabilities
- [ ] Encrypted communication
- [ ] Web interface
- [ ] Command whitelisting/blacklisting
- [ ] System information gathering
- [ ] Remote desktop viewing

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Feel free to modify and improve this code for your needs!

## ⚠️ Disclaimer

This tool is for use on your own network and computers only. Use responsibly and ensure you have permission before executing commands on remote systems.
