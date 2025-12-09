import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Assalomu alaykum, {user.first_name}! 😊\n"
        "Savolingizni yuboring yoki rasm uchun: /image matn"
    )

# /image komandasi orqali rasm yaratish
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Rasm yaratish uchun matn kiriting.\nMasalan: /image chiroyli BMW mashinasi")
        return
    
    prompt = " ".join(context.args)

    try:
        await update.message.reply_text("⏳ Rasm yaratilmoqda, biroz kuting...")

        # OPENAI IMAGE GENERATION
        img = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_url = img.data[0].url

        await update.message.reply_photo(photo=image_url, caption="Mana siz so‘ragan rasm! 😊")

    except Exception as e:
        print("Xatolik:", e)
        await update.message.reply_text("Rasm yaratishda xatolik yuz berdi, keyinroq urinib ko‘ring.")

# Oddiy matnlar — chatGPT javobi
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen o‘zbek tilida yordam beradigan chatbotsan."},
                {"role": "user", "content": user_msg}
            ]
        )

        answer = response.choices[0].message["content"]
        await update.message.reply_text(answer)

    except Exception as e:
        print("Xatolik:", e)
        await update.message.reply_text("Xatolik yuz berdi, keyinroq urinib ko‘ring.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", generate_image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()
