import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "✅ <b>TSD LIBRARY HELPER BOT ACTIVE</b>\nUse /anchor TopicName inside any forum topic.")

@bot.message_handler(commands=['anchor'])
def anchor_cmd(message):

    if not message.message_thread_id:
        bot.reply_to(message, "❌ Use inside a forum topic.")
        return

    args = message.text.split(maxsplit=1)
    custom_name = args[1] if len(args) > 1 else "UNNAMED"

    chat_id = message.chat.id
    topic_id = message.message_thread_id
    msg_id = message.message_id

    link = f"https://t.me/c/{str(chat_id)[4:]}/{msg_id}"

    txt = f"""✅ <b>ANCHOR SAVED</b>

🏷 <b>{custom_name}</b>
💬 CHAT ID: <code>{chat_id}</code>
🧵 TOPIC ID: <code>{topic_id}</code>
📨 MESSAGE ID: <code>{msg_id}</code>

🔗 <code>{link}</code>"""

    bot.reply_to(message, txt)

@bot.message_handler(commands=['id'])
def id_cmd(message):
    bot.reply_to(
        message,
        f"💬 CHAT ID: <code>{message.chat.id}</code>\n🧵 TOPIC ID: <code>{getattr(message,'message_thread_id',None)}</code>"
    )

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def home():
    return "TSD Library Helper Running"

if __name__ == "__main__":
    bot.remove_webhook()

    RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
    if RENDER_URL:
        bot.set_webhook(url=f"{RENDER_URL}/{BOT_TOKEN}")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
