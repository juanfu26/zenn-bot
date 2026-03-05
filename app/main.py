import os
import random
import threading
import signal
import sys
import logging
from datetime import datetime, timedelta
import telebot
from playwright.sync_api import sync_playwright

import messages as msg

# --- LOGGING CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

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

def bot_send(chat_id, text):
    """Wrapper to add a timestamp to telegram messages"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    bot.send_message(chat_id, f"[{timestamp}] {text}")

# --- SHUTDOWN HANDLER ---
def signal_handler(sig, frame):
    logger.info(msg.LOG_SHUTDOWN_INIT)
    try:
        bot_send(USER_ID, msg.TG_SHUTDOWN)
    except Exception as e:
        logger.error(msg.LOG_SHUTDOWN_ERR.format(e))
    sys.exit(0)

# Register signals for Docker stop / Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def perform_web_action(page, icon_selector, target_state, chat_id):
    """
    target_state: 'in' to ensure sign-in, 'out' to ensure sign-out
    """
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
            bot_send(chat_id, msg.TG_OLD_SESSION_DETECTED)
            page.click(icon_selector) # Close old session
            page.wait_for_timeout(4000)
            page.wait_for_selector("i.fa-sign-in", state="visible", timeout=20000)
            page.click(icon_selector) # Perform new Sign-In
            return msg.TG_OLD_SESSION_CLEARED
        else:
            page.click(icon_selector) # Standard Sign-In
            return msg.TG_SIGN_IN_CONFIRMED
            
    elif target_state == 'out':
        if "fa-sign-out" in classes:
            page.click(icon_selector) # Sign out
            return msg.TG_SIGN_OUT_CONFIRMED
        else:
            return msg.TG_ALREADY_SIGNED_OUT

def perform_sign_in(chat_id):
    logger.info(msg.LOG_START_SIGN_IN.format(chat_id))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        try:
            bot_send(chat_id, msg.TG_STARTING_SIGN_IN)
            result_in = perform_web_action(page, "i.o_hr_attendance_sign_in_out_icon", 'in', chat_id)
            bot_send(chat_id, result_in)
            logger.info(msg.LOG_SIGN_IN_COMPLETE.format(chat_id, result_in))
        except Exception as e:
            try:
                page.screenshot(path="error.png")
                with open("error.png", "rb") as f:
                    bot.send_photo(chat_id, f, caption=msg.TG_ERROR_SIGN_IN.format(str(e)))
            except:
                pass
            raise e # Re-raise to stop flow
        finally:
            browser.close()

def perform_sign_out(chat_id):
    logger.info(msg.LOG_START_SIGN_OUT.format(chat_id))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        try:
            bot_send(chat_id, msg.TG_STARTING_SIGN_OUT)
            result_out = perform_web_action(page, "i.o_hr_attendance_sign_in_out_icon", 'out', chat_id)
            bot_send(chat_id, result_out)
            
            # Esperar a que se muestre el mensaje de salida
            page.wait_for_timeout(3000)
            try:
                screenshot_path = "exit_screenshot.png"
                page.screenshot(path=screenshot_path)
                with open(screenshot_path, "rb") as f:
                    bot.send_photo(chat_id, f, caption=msg.TG_SCREENSHOT_SIGN_OUT)
            except Exception as img_err:
                logger.error(msg.LOG_SIGN_OUT_SCREENSHOT_ERR.format(chat_id, img_err))
                
            logger.info(msg.LOG_SIGN_OUT_COMPLETE.format(chat_id, result_out))
        except Exception as e:
            try:
                page.screenshot(path="error.png")
                with open("error.png", "rb") as f:
                    bot.send_photo(chat_id, f, caption=msg.TG_ERROR_SIGN_OUT.format(str(e)))
            except:
                pass
            raise e
        finally:
            browser.close()

def execute_workday_cycle(chat_id, cancel_event):
    logger.info(msg.LOG_SHIFT_STARTED.format(chat_id))
    try:
        # --- SIGN IN ---
        perform_sign_in(chat_id)
        
        # --- WAIT ---
        wait_minutes = random.randint(575, 595)
        # For testing, you could comment out above and use: wait_minutes = 1 
        wait_seconds = wait_minutes * 60 + random.randint(2,55)
        end_time = datetime.now() + timedelta(minutes=wait_minutes)
        
        active_tasks[chat_id]['end_time'] = end_time
        
        logger.info(msg.LOG_SLEEPING.format(chat_id, wait_minutes, end_time.strftime('%H:%M:%S')))
        bot_send(chat_id, msg.TG_TIMER_STARTED.format(end_time.strftime('%H:%M:%S')))
        
        # Sleep until timeout or cancelled
        cancelled = cancel_event.wait(timeout=wait_seconds)
        
        if cancelled:
            logger.info(msg.LOG_CANCELLED.format(chat_id))
            bot_send(chat_id, msg.TG_COUNTDOWN_CANCELLED)
            return
        
        # --- SIGN OUT ---
        perform_sign_out(chat_id)

    except Exception as e:
        logger.error(msg.LOG_CRITICAL_ERROR.format(chat_id, e))
        bot_send(chat_id, msg.TG_CRITICAL_ERROR.format(str(e)))
    finally:
        active_tasks.pop(chat_id, None)
        logger.info(msg.LOG_SHIFT_FINISHED.format(chat_id))

@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.from_user.id == USER_ID:
        if message.chat.id in active_tasks:
            bot_send(message.chat.id, msg.TG_SHIFT_IN_PROGRESS)
        else:
            cancel_event = threading.Event()
            active_tasks[message.chat.id] = {'end_time': None, 'cancel_event': cancel_event}
            threading.Thread(target=execute_workday_cycle, args=(message.chat.id, cancel_event)).start()
    else:
        bot.reply_to(message, msg.TG_ACCESS_DENIED)

@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    if message.from_user.id == USER_ID:
        if message.chat.id in active_tasks:
            active_tasks[message.chat.id]['cancel_event'].set()
            bot_send(message.chat.id, msg.TG_CANCELLATION_SENT)
        else:
            bot_send(message.chat.id, msg.TG_NO_TIMER_TO_CANCEL)

@bot.message_handler(commands=['status'])
def handle_status(message):
    if message.from_user.id == USER_ID:
        task = active_tasks.get(message.chat.id)
        if task and task['end_time']:
            rem = task['end_time'] - datetime.now()
            if rem.total_seconds() > 0:
                h, r = divmod(int(rem.total_seconds()), 3600)
                m, s = divmod(r, 60)
                bot_send(message.chat.id, msg.TG_TIMER_ACTIVE.format(h, m, s, task['end_time'].strftime('%H:%M:%S')))
            else:
                bot_send(message.chat.id, msg.TG_TIMER_FINISHING)
        elif task and not task['end_time']:
            bot_send(message.chat.id, msg.TG_SIGN_IN_ACTIVE)
        else:
            bot_send(message.chat.id, msg.TG_NO_SHIFT_FOUND)

if __name__ == "__main__":
    logger.info(msg.LOG_BOT_RUNNING)
    try:
        bot_send(USER_ID, msg.TG_BOT_ONLINE)
    except:
        pass
    bot.polling(non_stop=True)