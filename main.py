import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, CallbackContext, filters
)
from openai import OpenAI
from flask import Flask, request

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

# Flask route (Telegram webhook shu yerga xabar yuboradi)
@app.route("/", methods=["POST"])
def webhook():
    from telegram import Update
    update = Update.de_json(request.get_json(), bot)
    application.create_task(handle_update(update))
    return "ok", 200

# Telegram bot obyektini yaratish
application = ApplicationBuilder().token(TOKEN).build()
bot = application.bot

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Savolingizni yuboring.")

# Chat javobi
async def chat(update: Update, context: CallbackContext):
    msg = update.message.text
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen o'zbekcha gapiradigan chatbotsan."},
                {"role": "user", "content": msg},
            ]
        )

        answer = response.choices[0].message["content"]
        await update.message.reply_text(answer)

    except Exception as e:
        print("Xatolik:", e)
        await update.message.reply_text("Xatolik yuz berdi.")

# Handlerlarni qo‘shish
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# Webhook URL (Render sizga beradi)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Webhook o‘rnatish
@app.before_first_request
def set_webhook():
    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
