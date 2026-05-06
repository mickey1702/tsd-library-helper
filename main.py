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

# =========================================
# SHOW SAVED ANCHORS
# =========================================
@bot.message_handler(commands=['showanchors'])
def showanchors_cmd(message):
    global anchors

    if not anchors:
        bot.reply_to(message, "No anchors saved.")
        return

    txt = "<b>📚 SAVED ANCHORS</b>\n\n"
    for k, v in anchors.items():
        txt += f"• {k}\n{v}\n\n"

    bot.reply_to(message, txt)

# =========================================
# ID COMMAND
# =========================================
@bot.message_handler(commands=['id'])
def id_cmd(message):
    bot.reply_to(
        message,
        f"💬 CHAT ID: <code>{message.chat.id}</code>\n🧵 TOPIC ID: <code>{getattr(message,'message_thread_id',None)}</code>"
    )

# =========================================
# PANEL GENERATOR
# =========================================
@bot.message_handler(commands=['panel'])
def panel_cmd(message):
    global anchors

    # SUBJECTS PANEL
    subject_markup = InlineKeyboardMarkup(row_width=2)
    for name in [
        "NOTES", "CLINICAL GURUJI", "MIST"
    ]:
        if name in anchors:
            subject_markup.add(InlineKeyboardButton(name.title(), url=anchors[name]))

    bot.send_message(
        message.chat.id,
        "📚 <b>BROWSE CORE RESOURCES</b>",
        reply_markup=subject_markup
    )

    # FACULTY PANEL
    faculty_markup = InlineKeyboardMarkup(row_width=2)
    for name in [
        "DR PRIYANSH JAIN MEDICINE",
        "SALMAN SIR'S PHARMA & MICRO",
        "DR AZAM BIOCHEMISTRY",
        "RADIOLOGY BY DR ZAINAB VORA"
    ]:
        if name in anchors:
            faculty_markup.add(InlineKeyboardButton(name[:25], url=anchors[name]))

    bot.send_message(
        message.chat.id,
        "👨‍🏫 <b>BROWSE BY FACULTY</b>",
        reply_markup=faculty_markup
    )

    # INSTITUTE PANEL
    inst_markup = InlineKeyboardMarkup(row_width=2)
    for name in [
        "CORE BTR",
        "BTR 2.0",
        "CEREBELLUM"
    ]:
        if name in anchors:
            inst_markup.add(InlineKeyboardButton(name, url=anchors[name]))

    bot.send_message(
        message.chat.id,
        "🏢 <b>BROWSE BY INSTITUTE</b>",
        reply_markup=inst_markup
    )

    # REVISION PANEL
    rev_markup = InlineKeyboardMarkup(row_width=2)
    for name in [
        "PREP RR HINGLISH",
        "PREP RR ENGLISH",
        "PREP X HINGLISH",
        "PREP X ENGLISH",
        "QRP BIOCHEMISTRY PRIYANSH JAIN"
    ]:
        if name in anchors:
            rev_markup.add(InlineKeyboardButton(name[:20], url=anchors[name]))

    bot.send_message(
        message.chat.id,
        "🎯 <b>RAPID REVISION PROGRAMS</b>",
        reply_markup=rev_markup
    )

# =========================================
# WEBHOOK
# =========================================
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def home():
    return "TSD Library Directory Builder Running"

# =========================================
# MAIN
# =========================================
if __name__ == "__main__":
    bot.remove_webhook()

    RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
    if RENDER_URL:
        bot.set_webhook(url=f"{RENDER_URL}/{BOT_TOKEN}")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
