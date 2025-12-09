import os
import asyncio
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update, context):
    await update.message.reply_text("Assalomu alaykum! Men ChatGPT botman. Savolingizni yozing 😊")

async def handle_message(update, context):
    user_text = update.message.text
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_text}
        ]
    )

    reply = completion.choices[0].message["content"]
    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
