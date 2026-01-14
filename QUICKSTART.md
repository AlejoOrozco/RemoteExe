# Quick Start Guide

## 🎯 For Beginners - Step by Step

### Part 1: Setup on Your Mac (5 minutes)

1. **Open Terminal** on your Mac

2. **Navigate to the project folder:**
   ```bash/
   ç
   ```

3. **Change the password** in `config.json`:
   - Open `config.json` in a text editor
   - Change `"change_this_password_123"` to your own password
   - Save the file

4. **Test the broadcaster:**
   ```bash
   python3 broadcaster.py
   ```
   - It will try to discover listeners (won't find any yet, that's OK)
   - Type `exit` to quit

### Part 2: Setup on Windows PC (10 minutes)

#### Option A: Quick Test (Python Required)

1. **Copy these files to your Windows PC:**
   - `listener.py`
   - `config.json` (make sure it has the SAME password!)

2. **On Windows, open Command Prompt** (search for "cmd")

3. **Navigate to where you copied the files:**
   ```cmd
   cd C:\path\to\your\files
   ```

4. **Run the listener:**
   ```cmd
   python listener.py
   ```
   - You should see: "RemoteExe Listener is running on port 8888"
   - Keep this window open

5. **On your Mac, run the broadcaster again:**
   ```bash
   python3 broadcaster.py
   ```
   - It should now find your Windows PC!
   - Try a command like: `echo Hello from Windows!`

#### Option B: Standalone Executable (No Python Needed)

**Note:** Building Windows .exe from Mac requires either:
- A Windows machine/VM, OR
- Wine (for cross-compilation)

**Easiest approach:** Build on the Windows PC itself:

1. **On Windows PC, install Python** (if not installed)

2. **Copy these files to Windows:**
   - `listener.py`
   - `config.json`
   - `build_listener.bat`

3. **Install PyInstaller:**
   ```cmd
   pip install pyinstaller
   ```

4. **Build the executable:**
   ```cmd
   build_listener.bat
   ```

5. **Find the .exe:**
   - Look in the `dist` folder
   - You'll find `listener.exe`

6. **Run the .exe:**
   - Double-click `listener.exe`
   - Or run from command prompt

### Part 3: Auto-Start Setup (5 minutes)

1. **On Windows PC, right-click `install_listener.py`**

2. **Select "Run as Administrator"**

3. **Follow the prompts**

4. **Restart your Windows PC** to test

5. **The listener should start automatically!**

## 🧪 Testing

### Test 1: Basic Connection
```
On Mac: python3 broadcaster.py
Should find: Windows PC
Command: echo Test
Expected: Output showing "Test"
```

### Test 2: Windows Command
```
Command: tasklist | findstr python
Expected: List of Python processes
```

### Test 3: Auto-Start
```
1. Restart Windows PC
2. Wait 30 seconds
3. On Mac: python3 broadcaster.py
4. Should still find the listener (running automatically)
```

## ❓ Common Issues

**"No listeners found"**
- Check both computers are on same Wi-Fi/network
- Check Windows firewall isn't blocking ports 8888, 8889
- Try manual IP entry in broadcaster

**"Connection refused"**
- Make sure listener is running on Windows
- Check the IP address is correct
- Verify password matches in both config.json files

**"Authentication failed"**
- Password in broadcaster's config.json must match listener's config.json
- Check for typos or extra spaces

## 📞 Next Steps

Once it's working:
1. Try different commands
2. Set up auto-start on multiple Windows PCs
3. Customize config.json settings
4. Read the full README.md for advanced features

Happy remote controlling! 🚀
