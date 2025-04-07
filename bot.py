import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Отримуємо токен з Railway
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

# Функція для створення клавіатури з алфавітом
def get_alphabet_keyboard():
    alphabet_rows = [
        "АБВГДЕЄЖЗИІЇ",
        "ЙКЛМНОПРСТУФ",
        "ХЦЧШЩЬЮЯ",
        "ABCDEFG",
        "HIJKLMNOP",
        "QRSTUVWXYZ"
    ]
    
    keyboard = [[InlineKeyboardButton(letter, callback_data=f"letter_{letter}") for letter in row] for row in alphabet_rows]
    
    return InlineKeyboardMarkup(keyboard)

# Обробник кнопки "Search Backing Track" → показує алфавіт
async def show_alphabet(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Виберіть літеру:", reply_markup=get_alphabet_keyboard())

# Обробник вибору літери
async def letter_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    letter = query.data.split("_")[1]  # Отримуємо вибрану літеру
    await query.answer()
    await query.message.reply_text(f"Ви вибрали літеру: {letter}\n(Тут буде список треків)")

# Додаємо обробники команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(show_alphabet, pattern="^music_menu$"))
app.add_handler(CallbackQueryHandler(letter_selected, pattern="^letter_"))

# Запускаємо бота
if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
