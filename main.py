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
@bot.message_handler(commands=['postindex'])
def postindex_cmd(message):

    txt = """
<b>━━━━━━━━━━ ⚜ TSD MASTER LIBRARY ⚜ ━━━━━━━━━━</b>

<b>📚 INSTITUTE / APPS</b>

• <a href='https://t.me/c/2498151175/7873'>P Ladder RR Hinglish</a>
• <a href='https://t.me/c/2498151175/2596'>P Ladder RR English</a>
• <a href='https://t.me/c/2498151175/11035'>P Ladder X Hinglish</a>
• <a href='https://t.me/c/2498151175/9823'>P Ladder X English</a>
• <a href='https://t.me/c/2498151175/2516'>Doc Tutorials</a>
• <a href='https://t.me/c/2498151175/10'>MIST Old</a>
• <a href='https://t.me/c/2498151175/2946'>BTR 2.0</a>
• <a href='https://t.me/c/2498151175/12396'>Core BTR</a>
• <a href='https://t.me/c/2498151175/2453'>Cerebellum</a>
• <a href='https://t.me/c/2498151175/12773'>Clinical Guruji</a>

<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>

<b>👨‍⚕️ TEACHERS — SUBJECT WISE</b>

• <a href='https://t.me/c/2498151175/6866'>Dr Deepak Marwah — Medicine</a>
• <a href='https://t.me/c/2498151175/8185'>Dr Priyansh Jain — Medicine</a>
• <a href='https://t.me/c/2498151175/8317'>Dr Priyansh Jain — Biochemistry</a>
• <a href='https://t.me/c/2498151175/12526'>QRP Biochemistry — Priyansh Jain</a>
• <a href='https://t.me/c/2498151175/8394'>Dr Azam — Biochemistry</a>
• <a href='https://t.me/c/2498151175/7516'>Dr Rajiv Dhawan — ENT</a>
• <a href='https://t.me/c/2498151175/2421'>Dr GRG — Pharmacology</a>
• <a href='https://t.me/c/2498151175/2454'>Dr Zainab — Radiology</a>
• <a href='https://t.me/c/2498151175/1068'>Salman Sir — Pharma & Micro</a>
• <a href='https://t.me/c/2498151175/6765'>Dr Deepti Bahl — OBGY DFX</a>
• <a href='https://t.me/c/2498151175/3664'>Deepti Bahl — OBGYN DAMS</a>
• <a href='https://t.me/c/2498151175/3529'>Dr Sudha — Ophthalmology</a>

<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>

<b>📝 GENERAL RESOURCE HUBS</b>

• <a href='https://t.me/c/2498151175/6850'>Notes</a>

<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>

<i>⚠ More Topics & Mega Subject Archives Will Be Added Continuously.</i>
"""

    bot.send_message(message.chat.id, txt, disable_web_page_preview=True)

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
