import os
import json
from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardMarkup,
    InlineKeyboardButton, InputMediaPhoto
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackContext, CallbackQueryHandler
)


# Отримання змінної середовища з Railway
DATABASE_URL = os.getenv("DATABASE_URL")
TOKEN = os.getenv("RAILWAY_TOKEN")  # обов'язково вкажи в Railway

# Функція підключення до бази
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        logging.info("✅ Успішне підключення до бази даних")
        return conn
    except Exception as e:
        logging.error(f"❌ Помилка підключення до бази: {e}")
        return None

# Простий хендлер /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Це музичний бот 🎵")

# Основна асинхронна функція
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Хендлери
    app.add_handler(CommandHandler("start", start))

    # Перевірка БД під час запуску
    get_db_connection()

    # Запуск бота
    await app.run_polling()

# Запуск програми
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
