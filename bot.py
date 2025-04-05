import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = os.getenv("RAILWAY_TOKEN")  # Отримуємо токен з Railway

# Створюємо об'єкт Application (замість старого Updater)
app = Application.builder().token(TOKEN).build()

# Обробник команди /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привіт! Я твій бот!")

# Додаємо команду /start у хендлер
app.add_handler(CommandHandler("start", start))

# Запускаємо бота
if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
