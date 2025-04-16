import os
import asyncio
import psycopg2
from psycopg2 import OperationalError
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Функція для підключення до бази даних
def connect_to_database():
    try:
        db_url = os.environ.get("DATABASE_URL")  # Зчитуємо змінну середовища
        if not db_url:
            raise ValueError("❌ DATABASE_URL не встановлено!")
        conn = psycopg2.connect(db_url)
        print("✅ Підключено до бази даних успішно!")
        conn.close()
    except (Exception, OperationalError) as e:
        print(f"❌ Помилка підключення до бази: {e}")

# Стартова команда бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я музичний бот 🤖")

# Головна асинхронна функція
async def main():
    connect_to_database()

    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN не встановлено!")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🚀 Бот запущено!")
    await app.run_polling()

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
