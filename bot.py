import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

TOKEN = os.getenv("RAILWAY_TOKEN")
ADMIN_ID = 6266469974  # ID адміністратора

app = Application.builder().token(TOKEN).build()

# Меню для адміністратора
admin_keyboard = ReplyKeyboardMarkup(
    [["Додати трек", "Редагувати трек"]],
    resize_keyboard=True
)

# Обробник команди /admin
async def admin(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text("Адмін-панель:", reply_markup=admin_keyboard)
    else:
        await update.message.reply_text("У вас немає прав доступу.")

app.add_handler(CommandHandler("admin", admin))

if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
