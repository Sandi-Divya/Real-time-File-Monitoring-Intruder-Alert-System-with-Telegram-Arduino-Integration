import time
import psutil ##give access to get infomation about running procesess
import telebot

# -----------------------------
# Telegram setup
bot_token = ##"ADD YOUR BOT TOKEN"  # Replace with your bot token
user_id = ##ACCOUNT ID          # Replace with your Telegram user ID
bot = telebot.TeleBot(bot_token)

# -----------------------------
# App to monitor
app_name = "WhatsApp.exe"  # Exact process name from Task Manager
app_running = False

# -----------------------------
print(f"🔍 Monitoring {app_name}...")

while True:
    # Check if the process is running
    running = any(proc.name() == app_name for proc in psutil.process_iter())
    
    if running and not app_running:
        # App just opened
        print(f"⚠️ {app_name} opened!")
        bot.send_message(user_id, f"⚠️ {app_name} was opened!")
        app_running = True
        
    elif not running and app_running:
        # App just closed
        print(f"ℹ️ {app_name} closed!")
        bot.send_message(user_id, f"ℹ️ {app_name} was closed!")
        app_running = False
    
    time.sleep(2)  # Check every 2 seconds
