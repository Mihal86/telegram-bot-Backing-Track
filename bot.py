import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Отримуємо токен з змінних середовища Railway
TOKEN = os.getenv("RAILWAY_TOKEN")

# Створюємо об'єкт Application
app = Application.builder().token(TOKEN).build()

# Обробник команди /start
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Search Backing Track", callback_data="music_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привіт! Я твій бот. Обери дію:", reply_markup=reply_markup)

# Обробник команди /music — показує алфавіт для вибору
async def music(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(letter, callback_data=f"letter_{letter}") for letter in row]
        for row in ["АБВГДЕЄЖЗИІЇ", "ЙКЛМНОПРСТУФ", "ХЦЧШЩЬЮЯ", "ABCDEFG", "HIJKLMNOP", "QRSTUVWXYZ"]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("Виберіть літеру:", reply_markup=reply_markup)
    elif isinstance(update, CallbackContext) and update.callback_query:
        await update.callback_query.message.edit_text("Виберіть літеру:", reply_markup=reply_markup)
        await update.callback_query.answer()

# Обробник вибору літери
async def letter_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    letter = query.data.split("_")[1]  # Отримуємо вибрану літеру
    await query.answer()
    await query.message.edit_text(f"Ви вибрали літеру: {letter}\n(Тут буде список треків)")

# Обробник натискання на кнопку "Search Backing Track"
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "music_menu":
        await music(update.callback_query, context)

# Додаємо обробники команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler, pattern="^music_menu$"))
app.add_handler(CallbackQueryHandler(letter_selected, pattern="^letter_"))

# Запускаємо бота
if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
