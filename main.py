import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}!\n"
        "Savolingizni yozing, men yordam beraman."
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "O'zbekcha yordamchi bo‘l."},
                {"role": "user", "content": user_msg},
            ]
        )

        answer = response.choices[0].message["content"]
        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi.")
        print("ERROR:", e)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    await app.run_polling()

import asyncio
asyncio.run(main())
