import os
import random
import threading
import signal
import sys
from datetime import datetime, timedelta
import telebot
from playwright.sync_api import sync_playwright

# --- CONFIG FROM ENVIRONMENT ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_ID = int(os.getenv("TELEGRAM_USER_ID", "0"))
LOGIN_USER = os.getenv("LOGIN_USER")
LOGIN_PASS = os.getenv("LOGIN_PASS")
LOGIN_URL = os.getenv("LOGIN_URL")
ACTION_URL = os.getenv("ACTION_URL")

bot = telebot.TeleBot(TOKEN)

# Saving here: { chat_id: {'end_time': datetime, 'cancel_event': threading.Event} }
active_tasks = {}

# --- SHUTDOWN HANDLER ---
def signal_handler(sig, frame):
    print("Graceful shutdown initiated...")
    try:
        bot.send_message(USER_ID, "⚠️ **System Shutdown**: The Bot is going offline. Any active timers have been cleared.")
    except Exception as e:
        print(f"Could not send shutdown message: {e}")
    sys.exit(0)

# Register signals for Docker stop / Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def perform_web_action(page, chat_id, target_state):
    """
    target_state: 'in' to ensure sign-in, 'out' to ensure sign-out
    """
    icon_selector = "i.o_hr_attendance_sign_in_out_icon"
    
    # 1. Login
    page.goto(LOGIN_URL, wait_until="networkidle")
    page.fill("#login", LOGIN_USER)
    page.fill("#password", LOGIN_PASS)
    page.click("button[type='submit']")
    
    # 2. Navigate to Attendance Action
    page.wait_for_timeout(3000)
    page.goto(ACTION_URL, wait_until="domcontentloaded")
    page.wait_for_selector(icon_selector, state="visible", timeout=60000)
    
    classes = page.get_attribute(icon_selector, "class")
    
    if target_state == 'in':
        if "fa-sign-out" in classes:
            bot.send_message(chat_id, "⚠️ Active session from yesterday detected. Closing it first...")
            page.click(icon_selector) # Close old session
            page.wait_for_timeout(4000)
            page.wait_for_selector("i.fa-sign-in", state="visible", timeout=20000)
            page.click(icon_selector) # Perform new Sign-In
            return "✅ Old session cleared and New Sign-In confirmed."
        else:
            page.click(icon_selector) # Standard Sign-In
            return "✅ Standard Sign-In confirmed."
            
    elif target_state == 'out':
        if "fa-sign-out" in classes:
            page.click(icon_selector) # Sign out
            return "✅ Sign-Out confirmed."
        else:
            return "ℹ️ You were already 'Signed Out'. No action required."

def run_full_shift(chat_id, cancel_event):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        
        try:
            # --- PHASE 1: SMART SIGN-IN ---
            bot.send_message(chat_id, "🚀 Phase 1: Ensuring Sign-In...")
            result_in = perform_web_action(page, chat_id, 'in')
            bot.send_message(chat_id, result_in)
            browser.close()
            
            # PHASE 2: WAIT (Interruptible)
            wait_minutes = random.randint(575, 595) # Random between 9h35m and 9h55m
            wait_seconds = wait_minutes * 60
            end_time = datetime.now() + timedelta(minutes=wait_minutes)
            
            # Update global task with end time
            active_tasks[chat_id]['end_time'] = end_time
            
            bot.send_message(chat_id, f"🕒 Phase 2: Timer started.\nAutomatic Sign-Out scheduled for {end_time.strftime('%H:%M:%S')}.\nUse /cancel to stop.")
            
            # Wait using event.wait() instead of time.sleep()
            # Returns True if the event was set (cancelled), False if timeout reached
            cancelled = cancel_event.wait(timeout=wait_seconds)
            
            if cancelled:
                bot.send_message(chat_id, "🛑 **Countdown Cancelled**. I will not perform the automatic Sign-Out.")
                return
            
            # --- PHASE 3: AUTOMATIC SIGN-OUT ---
            bot.send_message(chat_id, "🚀 Phase 3: Performing Sign-Out...")
            with sync_playwright() as p_out:
                browser_out = p_out.chromium.launch(headless=True)
                page_out = browser_out.new_page()
                result_out = perform_web_action(page_out, chat_id, 'out')
                bot.send_message(chat_id, result_out)
                browser_out.close()

        except Exception as e:
            # Screenshot on error
            try:
                page.screenshot(path="error.png")
                with open("error.png", "rb") as f:
                    bot.send_photo(chat_id, f, caption=f"❌ Error during process: {str(e)}")
            except:
                bot.send_message(chat_id, f"❌ Critical Error: {str(e)}")
        finally:
            active_tasks.pop(chat_id, None)

@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.from_user.id == USER_ID:
        if message.chat.id in active_tasks:
            bot.reply_to(message, "⚠️ A shift is already in progress!")
        else:
            cancel_event = threading.Event()
            active_tasks[message.chat.id] = {'end_time': None, 'cancel_event': cancel_event}
            threading.Thread(target=run_full_shift, args=(message.chat.id,cancel_event)).start()
    else:
        bot.reply_to(message, "🚫 Access denied.")

@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    if message.from_user.id == USER_ID:
        if message.chat.id in active_tasks:
            active_tasks[message.chat.id]['cancel_event'].set()
            bot.reply_to(message, "⚙️ Cancellation signal sent...")
        else:
            bot.reply_to(message, "❌ No active timer to cancel.")

@bot.message_handler(commands=['status'])
def handle_status(message):
    if message.from_user.id == USER_ID:
        task = active_tasks.get(message.chat.id)
        if task and task['end_time']:
            rem = task['end_time'] - datetime.now()
            h, r = divmod(int(rem.total_seconds()), 3600)
            m, s = divmod(r, 60)
            bot.reply_to(message, f"🕒 Time remaining: {h}h {m}m {s}s\nTarget time: {active_tasks[message.chat.id].strftime('%H:%M:%S')}")
        else:
            bot.reply_to(message, "❌ No active shift found.")


if __name__ == "__main__":
    print("Bot is running and waiting for Telegram commands...")
    # Startup
    try:
        bot.send_message(USER_ID, "🤖 Full Workday Agent Online.\nCommands: /start, /status, /cancel")
    except:
        pass

    bot.polling()