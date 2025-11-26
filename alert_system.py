import time
import serial
import os
import telebot
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler

# -----------------------------
# Telegram setup
bot_token = #"ADD BOT TOKEN"
user_id = #_ADD TELEGRAM ACOUNT ID_#  #Ensures alerts go only to my Telegram account.
bot = telebot.TeleBot(bot_token) #Initializes the bot object, which can send messages.

# Arduino setup
arduino_port = "COM6"  # COM port to communicate with Arduino
baud_rate = 9600 #Communication speed

#If Arduino is not connected, the script still works for Telegram alerts.
try:
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)
    print("[Serial] Connected to Arduino!")
except Exception as e:
    arduino = None
    print(f"[Serial] Could not connect to Arduino: {e}")

# Folder to monitor
folder_to_monitor = r"C:\Users\Sandali\OneDrive\Desktop\SecretFiles"

# Files to ignore
IGNORE_FILES = ["desktop.ini", "Thumbs.db"]

# Debounce setup
last_created_deleted = {}
last_modified = {}
DEBOUNCE_SECONDS = 2.5  # Ignore repeated alerts within 2.5 seconds

def should_alert_create_delete(file_name):
    now = time.time()
    if file_name in last_created_deleted:
        if now - last_created_deleted[file_name] < DEBOUNCE_SECONDS:
            return False
    last_created_deleted[file_name] = now
    return True

def should_alert_modified(file_name):
    now = time.time()
    if file_name in last_modified:
        if now - last_modified[file_name] < DEBOUNCE_SECONDS:
            return False
    last_modified[file_name] = now
    return True

# -----------------------------
class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        filename = os.path.basename(event.src_path)
        if filename in IGNORE_FILES or event.is_directory or not should_alert_create_delete(filename):
            return
        print(f"📁 New File Created: {filename}")
        bot.send_message(user_id, f"📁 New File Created: {filename}")
        if arduino:
            arduino.write(b'1')

    def on_modified(self, event):
        filename = os.path.basename(event.src_path)
        if filename in IGNORE_FILES or event.is_directory or not should_alert_modified(filename):
            return
        print(f"⚠️ File Modified: {filename}")
        bot.send_message(user_id, f"⚠️ File Modified: {filename}")
        if arduino:
            arduino.write(b'1')

    def on_deleted(self, event):
        filename = os.path.basename(event.src_path)
        if filename in IGNORE_FILES or event.is_directory or not should_alert_create_delete(filename):
            return
        print(f"❌ File Deleted: {filename}")
        bot.send_message(user_id, f"❌ File Deleted: {filename}")
        if arduino:
            arduino.write(b'1')

# -----------------------------
observer = Observer() #watches folder in real-time
observer.schedule(Watcher(), folder_to_monitor, recursive=True)
observer.start()
print(f"🔍 Monitoring Folder: {folder_to_monitor}")

try:
    while True:
        time.sleep(1) #avoids CPU overload
except KeyboardInterrupt: #allows you to stop script with Ctrl+C
    observer.stop()
observer.join() #ensures clean exit
