import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext):
    keyboard = [
        ["ℹ️ Інформація", "📞 Контакти"],
        ["⚙️ Налаштування"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Оберіть дію:", reply_markup=reply_markup)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    import asyncio
    asyncio.run(app.run_polling())
