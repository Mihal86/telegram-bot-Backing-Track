import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Отримуємо токен з Railway
TOKEN = os.getenv("RAILWAY_TOKEN")

# Створюємо об'єкт Application
app = Application.builder().token(TOKEN).build()

# База даних треків (назва + посилання)
tracks_db = {
    "А": [
        {"name": "Альфа - Пісня 1", "url": "https://example.com/track1.mp3"},
        {"name": "Альфа - Пісня 2", "url": "https://example.com/track2.mp3"},
    ],
    "C": [
        {"name": "Coldplay - Yellow", "url": "https://example.com/yellow.mp3"},
        {"name": "Coldplay - Fix You", "url": "https://example.com/fixyou.mp3"},
    ],
    # Додай більше треків за необхідності
}

# Обробник команди /start
async def start(update: Update, context: CallbackContext):
    keyboard = [["Search Backing Track"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Привіт! Я твій бот. Обери дію:", reply_markup=reply_markup)

# Функція для створення клавіатури з алфавітом
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
    tracks = tracks_db.get(letter, [])

    if tracks:
        keyboard = [[InlineKeyboardButton(f"🎵 {track['name']}", callback_data=f"play_{track['url']}")] for track in tracks]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Ось доступні треки для літери '{letter}':", reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"Немає доступних треків для літери '{letter}'.")

# Обробник натискання кнопки прослухати трек
async def play_track(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    track_url = query.data.split("_", 1)[1]  # Отримуємо URL треку
    await query.message.reply_audio(audio=track_url, caption="🎶 Ваш трек для прослуховування.")

# Додаємо обробники команд
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Text("Search Backing Track"), show_alphabet))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, letter_selected))
app.add_handler(CallbackQueryHandler(play_track, pattern="^play_"))

# Запускаємо бота
if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
