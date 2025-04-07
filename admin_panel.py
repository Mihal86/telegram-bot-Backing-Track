import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

TOKEN = os.getenv("RAILWAY_TOKEN")
ADMIN_ID = 6266469974  # Заміни на твоє ID адміністратора

app = Application.builder().token(TOKEN).build()

# Меню для адміністратора
admin_keyboard = ReplyKeyboardMarkup(
    [["Додати трек", "Редагувати трек"]],
    resize_keyboard=True
)

# Обробник команди /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привіт! Я твій бот!")

# Обробник команди /admin
async def admin(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text("Адмін-панель:", reply_markup=admin_keyboard)
    else:
        await update.message.reply_text("У вас немає прав доступу.")

# Обробник для виведення ID користувача
async def get_user_id(update: Update, context: CallbackContext):
    await update.message.reply_text(f"Твій ID: {update.message.from_user.id}")

# Додаємо обробники команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("myid", get_user_id))

if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
