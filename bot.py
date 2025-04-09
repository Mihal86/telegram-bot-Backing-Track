import os
import json
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Отримуємо токен з Railway
TOKEN = os.getenv("RAILWAY_TOKEN")
ADMIN_ID = 6266469974  # ID адміністратора

# Створюємо об'єкт Application
app = Application.builder().token(TOKEN).build()

# Завантажуємо базу треків із JSON
def load_tracks():
    try:
        with open("tracks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

tracks_db = load_tracks()

# Головне меню
main_keyboard = ReplyKeyboardMarkup(
    [["Search Backing Track"]],
    resize_keyboard=True
)

# Меню для адміністратора
admin_keyboard = ReplyKeyboardMarkup(
    [["Додати трек", "Редагувати трек"]],
    resize_keyboard=True
)

# Обробник команди /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привіт! Я твій бот. Обери дію:", reply_markup=main_keyboard)

# Обробник команди /admin
async def admin(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text("Адмін-панель:", reply_markup=admin_keyboard)
    else:
        await update.message.reply_text("У вас немає прав доступу.")

# Функція для клавіатури алфавіту
def get_alphabet_keyboard():
    alphabet_rows = [
        ["А", "Б", "В", "Г", "Д", "Е", "Є", "Ж", "З", "И", "І", "Ї"],
        ["Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф"],
        ["Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ю", "Я"],
        ["A", "B", "C", "D", "E", "F", "G"],
        ["H", "I", "J", "K", "L", "M", "N", "O", "P"],
        ["Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    ]
    return ReplyKeyboardMarkup(alphabet_rows, resize_keyboard=True)

# Обробник натискання "Search Backing Track"
async def show_alphabet(update: Update, context: CallbackContext):
    await update.message.reply_text("Виберіть літеру:", reply_markup=get_alphabet_keyboard())

# Обробник вибору літери та показу треків
async def letter_selected(update: Update, context: CallbackContext):
    letter = update.message.text
    tracks = tracks_db.get(letter, [])

    if tracks:
        keyboard = [
            [InlineKeyboardButton(f"🎵 {track['name']}", callback_data=f"play_{letter}_{idx}")]
            for idx, track in enumerate(tracks)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Ось доступні треки для літери '{letter}':", reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"Немає доступних треків для літери '{letter}'.")

# Обробник натискання кнопки прослухати трек
async def play_track(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split("_")
    letter, track_idx = data[1], int(data[2])
    track = tracks_db[letter][track_idx]

    # Відправляємо обкладинку (якщо є)
    if "cover" in track:
        media = InputMediaPhoto(media=track["cover"], caption=f"🎵 {track['name']}")
        await query.message.reply_media_group([media])

    # Відправляємо аудіофайл
    await query.message.reply_audio(audio=track["url"], caption="🎶 Ваш трек для прослуховування.")

    # Відправляємо PDF (якщо є)
    if "pdf" in track:
        await query.message.reply_document(document=track["pdf"], caption="📄 Ноти")

# Додаємо обробники команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.Text("Search Backing Track"), show_alphabet))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, letter_selected))
app.add_handler(CallbackQueryHandler(play_track, pattern="^play_"))

# Запускаємо бота
if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
