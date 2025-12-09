import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from openai import OpenAI

TELEGRAM_TOKEN = ("TELEGRAM_TOKEN")
OPENAI_API_KEY = ("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_message(update, context):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_text}]
    )

    bot_reply = response.choices[0].message["content"]
    await update.message.reply_text(bot_reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
