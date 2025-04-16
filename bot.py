import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Отримуємо токен з змінних середовища Railway
TOKEN = os.getenv("BOT_TOKEN")

# Створюємо об'єкт Application
app = Application.builder().token(TOKEN).build()

# Обробник команди /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привіт! Я твій бот!")

# Додаємо обробник команди /start
app.add_handler(CommandHandler("start", start))

# Запускаємо бота
if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
