import os
import json
import telebot
from flask import Flask, request
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
app = Flask(__name__)

ANCHOR_FILE = "anchors.json"

# =========================================
# LOAD SAVE
# =========================================
def load_anchors():
    if not os.path.exists(ANCHOR_FILE):
        with open(ANCHOR_FILE, "w") as f:
            json.dump({}, f)
    with open(ANCHOR_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_anchors(data):
    with open(ANCHOR_FILE, "w") as f:
        json.dump(data, f, indent=2)

anchors = load_anchors()

# =========================================
# START
# =========================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(
        message,
        "✅ <b>TSD LIBRARY DIRECTORY BUILDER ACTIVE</b>\n\n/anchor Name = save topic link\n/panel = generate clickable menus"
    )

# =========================================
# SAVE ANCHOR
# =========================================
@bot.message_handler(commands=['anchor'])
def anchor_cmd(message):
    global anchors

    if not message.message_thread_id:
        bot.reply_to(message, "❌ Use inside a forum topic.")
        return

    args = message.text.split(maxsplit=1)
    custom_name = args[1] if len(args) > 1 else "UNNAMED"

    chat_id = message.chat.id
    msg_id = message.message_id

    link = f"https://t.me/c/{str(chat_id)[4:]}/{msg_id}"

    anchors[custom_name.upper()] = link
    save_anchors(anchors)

    txt = f"""✅ <b>ANCHOR SAVED</b>

🏷 <b>{custom_name}</b>
🔗 <code>{link}</code>"""

    bot.reply_to(message, txt)
