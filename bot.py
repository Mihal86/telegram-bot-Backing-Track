import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Отримуємо токен з Railway
TOKEN = os.getenv("RAILWAY_TOKEN")

# Створюємо об'єкт Application
app = Application.builder().token(TOKEN).build()

# База даних треків (поки що просто словник)
tracks_db = {
    "А": ["Альфа - Пісня 1", "Альфа - Пісня 2"],
    "Б": ["Бета - Трек 1"],
    "C": ["Coldplay - Yellow", "Coldplay - Fix You"],
    "D": ["Drake - God's Plan"],
    "E": ["Eminem - Lose Yourself"],
    # Додай більше треків за необхідності
}

# Обробник команди /start
async def start(update: Update, context: CallbackContext):
    keyboard = [["Search Backing Track"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Привіт! Я твій бот. Обери дію:", reply_markup=reply_markup)

# Функція для створення клавіатури з алфавітом (ReplyKeyboardMarkup)
def get_alphabet_keyboard():
    alphabet_rows = [
        ["А", "Б", "В", "Г", "Д", "Е", "Є", "Ж", "З", "И", "І", "Ї"],
        ["Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф"],
        ["Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ю", "Я"],
        ["A", "B", "C", "D", "E", "F", "G"],
        ["H", "I", "J", "K", "L", "M", "N", "O", "P"],
        ["Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    ]
    return ReplyKeyboardMarkup(alphabet_rows, resize_keyboard=True, one_time_keyboard=True)

# Обробник натискання "Search Backing Track" → показує клавіатуру
async def show_alphabet(update: Update, context: CallbackContext):
    await update.message.reply_text("Виберіть літеру:", reply_markup=get_alphabet_keyboard())

# Обробник вибору літери та виведення списку треків
async def letter_selected(update: Update, context: CallbackContext):
    letter = update.message.text  # Отримуємо вибрану літеру
    
    # Отримуємо список треків для цієї літери
    tracks = tracks_db.get(letter, [])  

    if tracks:
        track_list = "\n".join([f"🎵 {track}" for track in tracks])
        await update.message.reply_text(f"Ось доступні треки для літери '{letter}':\n\n{track_list}")
    else:
        await update.message.reply_text(f"Немає доступних треків для літери '{letter}'.")

# Додаємо обробники команд
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Text("Search Backing Track"), show_alphabet))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, letter_selected))  # Обробка вибору літери

# Запускаємо бота
if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
