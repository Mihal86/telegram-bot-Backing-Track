import os
import psycopg2
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Отримання змінних середовища
TOKEN = os.getenv("RAILWAY_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Перевірка наявності змінних
if not TOKEN:
    raise ValueError("❌ RAILWAY_TOKEN не встановлено!")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL не встановлено!")

# Функція для перевірки підключення до бази
def check_postgres_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        print("✅ Успішне підключення до PostgreSQL")
    except Exception as e:
        print("❌ Помилка підключення до бази:", e)

# Обробник команди /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привіт! Я твій бот!")

# Основна функція
async def main():
    check_postgres_connection()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🤖 Бот запущено...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
