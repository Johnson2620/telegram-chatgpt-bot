import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! Matn yuboring yoki /rasm bilan rasm yarating."
    )


async def rasm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("❗ Misol: /rasm samolyotda uchayotgan mushuk")
        return

    await update.message.reply_text("⏳ Rasm yaratilmoqda...")

    try:
        img = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )
        url = img.data[0].url
        await update.message.reply_photo(photo=url)

    except Exception as e:
        print("Xatolik:", e)
        await update.message.reply_text("❗ Rasm yaratishda xatolik yuz berdi.")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Siz foydalanuvchiga o‘zbek tilida yordam berasiz."},
                {"role": "user", "content": user_msg},
            ]
        )

        answer = res.choices[0].message["content"]
        await update.message.reply_text(answer)

    except Exception as e:
        print("Xatolik:", e)
        await update.message.reply_text("Xatolik yuz berdi.")


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rasm", rasm))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()


if __name__ == "__main__":
    main()
