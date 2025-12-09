import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from openai import OpenAI

# -------------------------------------------------------
# ❗ TOKENS — BU YERGA TOKENLARINGIZNI YOZING
# -------------------------------------------------------

TELEGRAM_TOKEN = "TELEGRAM_TOKEN"
OPENAI_API_KEY = "OPENAI_API_KEY"

# OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User histories
user_histories = {}

# System prompt (bot faqat o‘zbekcha gapiradi)
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Siz o'zbek tilida gapiradigan ChatGPT yordamchisiz. "
        "Javoblar sodda, tushunarli va aniq bo'lishi kerak."
    )
}

# -------------------------------------------------------
# /start
# -------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"Assalomu alaykum, {user.first_name or 'doʻst'}!\n\n"
        "Men ChatGPT (GPT-4o-mini) bilan bog‘langan Telegram botman.\n"
        "Savolingizni yozing — o‘zbek tilida javob yuboraman.\n\n"
        "/help — yordam bo‘limi."
    )
    await update.message.reply_text(text)

# -------------------------------------------------------
# /help
# -------------------------------------------------------
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Bot imkoniyatlari:\n"
        "- Savollarga javob berish\n"
        "- Ma'lumot topish\n"
        "- Tushuntirish, tavsiya berish\n"
        "- Matn tuzish yoki tahrirlash\n\n"
        "/reset — suhbat tarixini tozalaydi."
    )
    await update.message.reply_text(text)

# -------------------------------------------------------
# /reset
# -------------------------------------------------------
async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    user_histories.pop(uid, None)
    await update.message.reply_text("Suhbat tarixi tozalandi.")

# -------------------------------------------------------
# Message handler
# -------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    user_text = update.message.text

    history = user_histories.get(uid, [])
    messages = [SYSTEM_PROMPT] + history + [{"role": "user", "content": user_text}]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,
            temperature=0.6
        )

        bot_reply = response.choices[0].message.content

    except Exception as e:
        logger.error(f"OpenAI xatosi: {e}")
        await update.message.reply_text("Kechirasiz, serverda xatolik yuz berdi.")
        return

    await update.message.reply_text(bot_reply)

    # History storage
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": bot_reply})

    if len(history) > 20:
        history = history[-20:]

    user_histories[uid] = history

# -------------------------------------------------------
# MAIN — botni ishga tushurish
# -------------------------------------------------------
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("reset", reset_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
