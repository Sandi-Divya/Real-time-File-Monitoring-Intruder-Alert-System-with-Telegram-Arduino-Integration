# Real-time-File-Monitoring-Intruder-Alert-System-with-Telegram-Arduino-Integration

A smart Python script that continuously monitors a folder on computer in real-time and instantly notifies you on Telegram whenever files are created, modified, or deleted. Optionally, it can trigger an Arduino to give physical alerts, like flashing LEDs or sounding buzzers, for real-time intrusion awareness.

## Future Improvements

In the future, this project could be extended to **application or process monitoring**.  
Instead of just watching files and folders, **it could detect when specific applications (like WhatsApp, browsers, or any other program) are opened or closed.**

This would allow real-time alerts not only for file changes but also for **software usage events**, making the system more versatile and powerful for personal security or monitoring purposes.

---
## Why I Built This

I created **SecureFileAlertBot** for several reasons:

1. **Learning experience** – To combine Python, Telegram bots, and Arduino hardware in one practical project.  
2. **Practical security** – To monitor sensitive folders and get instant alerts if anyone accesses them.  
3. **Understanding systems** – To gain insight into file system events, real-time monitoring, and hardware communication.  
4. **Background automation** – To learn how to run scripts invisibly without interfering with my workflow.  

> This is a fully working, real-world security system — perfect for personal or small office use.

---

## Key Features & Learning Opportunities of the project
By exploring or building this project, you can learn:
1. **File system monitoring** – Understand how operating systems track file events and how to efficiently listen for changes.
2. **API integration** – Learn to work with Telegram's bot API, handle authentication, and send real-time alerts.
3. **Hardware communication** – Discover how to connect Python scripts with Arduino boards via serial communication.
4. **Debouncing logic** – Handle rapid file events without spamming notifications.
5. **Background automation** – Run scripts silently in the background on Windows without CMD windows.
6. **Error handling** – Keep your program running smoothly even if optional parts (like Arduino) aren't connected.

---

## Setup

### Step 1: Get Your Telegram Bot Ready

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Copy your bot token (it looks like `123456789:ABCdef...`)
4. Now talk to [@userinfobot](https://t.me/userinfobot) to get your user ID (it's just a number)
5. Put both in the code:
   ```python
   bot_token = "your_token_here"
   user_id = your_id_here
   ```

The user ID ensures alerts only go to your Telegram account, not anyone else who might find your bot.

### Step 2: Choose Your Folder to Monitor

Change this line to whatever folder you want to watch:
```python
folder_to_monitor = r"C:\Users\YourName\Desktop\YourFolder"
```

Make sure to use the `r` before the quotes — it tells Python to read the path correctly on Windows.

### Step 3: Arduino Setup (Skip if You Don't Have One)

If you want physical alerts, upload this simple sketch to your Arduino:

```cpp
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();
    if (signal == '1') {
      // Flash LED 3 times
      for(int i = 0; i < 3; i++) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(200);
        digitalWrite(LED_BUILTIN, LOW);
        delay(200);
      }
    }
  }
}
```

Then:
1. Check which COM port your Arduino is on: Arduino IDE → Tools → Port
2. Update the port in the script:
   ```python
   arduino_port = "COM6"  # Change to your port
   ```
3. Make sure the baud rate matches:
   ```python
   baud_rate = 9600
   ```

If you don't have an Arduino or don't want to use it, the script handles this automatically. It'll try to connect, and if it can't find the Arduino, it just skips that part and still works fine for Telegram alerts.

---

## Running It

### 1) First Time - Testing Mode

First, I tested the script the normal way using CMD (Command Prompt) to make sure everything worked:

```bash
python secure_file_alert.py
```

This lets you see all the messages in the terminal as files are created, modified, or deleted. It's useful for testing and debugging.

<img width="1148" height="152" alt="bot3" src="https://github.com/user-attachments/assets/a82b3e21-b613-452f-9e94-59f1b2277af4" />


### 2) Running Silently in Background

After confirming it works, I wanted the script to run silently in the background without keeping a terminal window open. To do that:

I used `pythonw` instead of `python`:

```bash
pythonw secure_file_alert.py
```

`pythonw` runs the script without opening a CMD window.

### Creating a Desktop Shortcut

To make it easier, I created a shortcut on my desktop:

1. Right-click on Desktop → New → Shortcut
2. For location, enter:
   ```
   C:\Users\YourName\AppData\Local\Programs\Python\Python3X\pythonw.exe "C:\path\to\secure_file_alert.py"
   ```
   (Adjust the paths to match your Python installation and script location)
3. Click Next, give it a name like "File Monitor"
4. Click Finish

Now, whenever I click the shortcut, the script starts running in the background automatically — monitoring my folder, sending Telegram alerts, and triggering Arduino (if connected) — without showing any terminal window.

<img width="422" height="206" alt="bot" src="https://github.com/user-attachments/assets/418476be-4b41-4276-8238-7edca4f574f1" />

This way, I can leave the script running all the time without it interfering with anything else I'm doing.

### 3) Set the Script to **Autorun on Startup** (Task Scheduler)

1. Open **Task Scheduler**  
- Press `Win + S` → type `Task Scheduler` → Enter
2. Click **Create Task**
3. **General Tab**  
- Name: `SecureFileAlert`  
- Check: **Run whether user is logged on or not**  
- Optional: **Run with highest privileges**
4. **Triggers Tab**  
- Click **New…** → Begin the task: **At log on** → OK
5. **Actions Tab**  
- Click **New…** → Action: **Start a program**  
- Program/script: `pythonw.exe` path  
- Add arguments: `"C:\path\to\secure_file_alert.py"` → OK
6. **Conditions Tab**  
- Uncheck: **Start the task only if the computer is on AC power**
7. **Settings Tab**  
- Check: **Allow task to be run on demand**  
- Optional: Restart on failure
8. Click **OK** and enter your Windows password if prompted

The script will now run automatically in the background every time you start your computer.

### Stopping It

- **If running in CMD:** Press `Ctrl + C`
- **If running in background:** Open Task Manager → Find `pythonw.exe` → End Task

---

## How It Actually Works

### The File Monitoring System

The script uses Python's `watchdog` library to monitor the folder. Instead of constantly checking if files changed (which would waste CPU resources), it uses an Observer pattern:

```python
observer = Observer()
observer.schedule(Watcher(), folder_to_monitor, recursive=True)
observer.start()
```

This watches the folder in real-time and only triggers when something actually happens. The `recursive=True` means it also watches all subfolders inside your main folder.

### Understanding the Watcher Class

The `Watcher` class handles three types of events:

1. **on_created** - When a new file appears
2. **on_modified** - When an existing file changes
3. **on_deleted** - When a file is removed

Each event triggers the same process: check if we should alert, then send Telegram message, then signal Arduino (if connected).

### The Debounce Logic (Preventing Alert Spam)

Here's a problem I ran into: when you save a file in Windows, it sometimes triggers multiple events really fast. Like if you save a Word document, Windows might trigger "modified" 5 times in one second.

To fix this, I added debounce logic. It works like this:

```python
last_created_deleted = {}
last_modified = {}
DEBOUNCE_SECONDS = 2.5
```

The script keeps track of when it last sent an alert for each file. If another event for the same file happens within 2.5 seconds, it ignores it. This way you get one clean alert instead of 10 spam messages.

I use two separate timers:
- `last_created_deleted` - for new and deleted files
- `last_modified` - for changes to existing files

This prevents spam while still letting you know about legitimate changes.

### Files That Get Ignored

Windows creates some system files automatically that nobody cares about:

```python
IGNORE_FILES = ["desktop.ini", "Thumbs.db"]
```

- `desktop.ini` - Windows uses this to remember folder settings
- `Thumbs.db` - Windows stores thumbnail previews here

These get filtered out before any alert is sent. You can add more files to this list if you want.

### Telegram Communication

The bot uses the `telebot` library to send messages:

```python
bot = telebot.TeleBot(bot_token)
bot.send_message(user_id, f"📁 New File Created: {filename}")
```

It's straightforward — when an event happens, format a message and send it to your user ID. The bot token authenticates with Telegram's servers.

### Arduino Communication

If Arduino is connected, the script sends a simple signal:

```python
arduino.write(b'1')
```

This sends the byte `'1'` over the serial port. The Arduino is constantly listening for this signal, and when it receives it, it runs whatever code you programmed (like flashing an LED).

The `try-except` block handles the connection:
```python
try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Give Arduino time to initialize
    print("[Serial] Connected to Arduino!")
except Exception as e:
    arduino = None
    print(f"[Serial] Could not connect to Arduino: {e}")
```

If the connection fails, `arduino` is set to `None`, and the script just skips the Arduino parts later.

### The Main Loop

```python
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

This keeps the script running forever. The `time.sleep(1)` prevents the loop from wasting CPU — it just waits and lets the Observer do its thing. When you press Ctrl+C, it catches the interrupt and stops cleanly.

---

## Customizing the Script

### Change the Debounce Time

If you're getting too many alerts or not enough, adjust this:
```python
DEBOUNCE_SECONDS = 2.5  # Make it longer or shorter
```

### Ignore More Files

Add any files or patterns you don't want alerts for:
```python
IGNORE_FILES = ["desktop.ini", "Thumbs.db", ".tmp", "~$"]
```

The `~$` catches temporary Microsoft Office files.

### Change Alert Messages

Edit these lines to customize what the alerts say:
```python
bot.send_message(user_id, f"📁 New File Created: {filename}")
bot.send_message(user_id, f"⚠️ File Modified: {filename}")
bot.send_message(user_id, f"❌ File Deleted: {filename}")
```

You can add timestamps, file paths, or whatever else you want.

### Monitor Multiple Folders

If you want to watch more than one folder, you can schedule multiple watchers:
```python
observer.schedule(Watcher(), r"C:\Folder1", recursive=True)
observer.schedule(Watcher(), r"C:\Folder2", recursive=True)
observer.schedule(Watcher(), r"C:\Folder3", recursive=True)
```

### Turn Off Subfolder Monitoring

If you only want to watch the main folder and not subfolders:
```python
observer.schedule(Watcher(), folder_to_monitor, recursive=False)
```

---

## Troubleshooting

### Telegram Not Working

**Problem:** Not getting any Telegram messages

**Solutions:**
- Make sure you've started a chat with your bot first (send it `/start`)
- Double-check your bot token and user ID are typed correctly
- Verify you have an internet connection
- Try sending a test message directly using the bot token to make sure it works

### Arduino Issues

**Problem:** Arduino not responding to alerts

**Solutions:**
- Check the COM port in Device Manager (Windows key + X → Device Manager → Ports)
- Make sure the Arduino IDE isn't open (it locks the COM port)
- Verify the baud rate matches in both Python and Arduino code (9600)
- Try unplugging and plugging the Arduino back in
- Upload the Arduino sketch again to make sure it's there

### Getting Too Many Alerts

**Problem:** Telegram is spamming me with messages

**Solutions:**
- Increase `DEBOUNCE_SECONDS` to something like 5 or 10
- Add more files to `IGNORE_FILES` list
- Check if an antivirus or backup program is constantly modifying files
- Consider using `recursive=False` if subfolders are causing noise

### Script Crashes or Won't Start

**Problem:** Error messages or script immediately stops

**Solutions:**
- Check that your folder path is correct and the folder exists
- Make sure all libraries are installed (`pip install pyserial pyTelegramBotAPI watchdog`)
- Read the error message — it usually tells you exactly what's wrong
- Try running with `python` instead of `pythonw` to see error messages
- Verify you have permission to access the folder you're monitoring

### Can't Find pythonw.exe

**Problem:** Windows says it can't find pythonw.exe

**Solution:**
Find your Python installation folder, usually something like:
- `C:\Python3X\pythonw.exe`
- `C:\Users\YourName\AppData\Local\Programs\Python\Python3X\pythonw.exe`

Or just search for "pythonw.exe" in Windows Explorer.

---

## Files in This Project

```
SecureFileAlertBot/
├── secure_file_alert.py    # Main script
├── arduino_sketch.ino       # Arduino code (optional)
└── README.md                # This file
```

That's basically it. It's a straightforward script that monitors a folder and keeps you informed. Nothing fancy, just reliable monitoring that actually works.
