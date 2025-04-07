from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

ADMIN_ID = 6266469974  # ID адміністратора

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

# Функція, яка додається в основний файл бота
def add_admin_handlers(dp):
    dp.add_handler(CommandHandler("admin", admin))

