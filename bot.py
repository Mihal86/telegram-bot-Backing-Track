import os
import json
from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardMarkup,
    InlineKeyboardButton, InputMediaPhoto
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackContext, CallbackQueryHandler
)
DATABASE_URL = os.getenv("${{ Postgres-KFcd.DATABASE_URL }}")
TOKEN = os.getenv("RAILWAY_TOKEN")

# Функція підключення до бази
def get_db_connection():
    try:
        conn = psycopg2.connect(${{ Postgres-KFcd.DATABASE_URL }})
        logging.info("✅ Успішне підключення до бази даних")
        return conn
    except Exception as e:
        logging.error(f"❌ Помилка підключення до бази: {e}")
        
        return None
ADMIN_ID = 6266469974
TRACKS_FILE = "tracks.json"


app = Application.builder().token(TOKEN).build()

def load_tracks():
    if not os.path.exists(TRACKS_FILE):
        return {}
    with open(TRACKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tracks(data):
    with open(TRACKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

tracks_db = load_tracks()

async def start(update: Update, context: CallbackContext):
    keyboard = [["Search Backing Track"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Я твій бот. Обери дію:", reply_markup=reply_markup)

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

async def show_alphabet(update: Update, context: CallbackContext):
    await update.message.reply_text("Виберіть літеру:", reply_markup=get_alphabet_keyboard())

async def letter_selected(update: Update, context: CallbackContext):
    if "adding_track" in context.user_data:
        return await receive_letter(update, context)
    
    letter = update.message.text
    tracks = tracks_db.get(letter, [])

    if tracks:
        keyboard = [
            [InlineKeyboardButton(f"?? {track['name']}", callback_data=f"play_{letter}_{idx}")]
            for idx, track in enumerate(tracks)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Ось доступні треки для літери '{letter}':", reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"Немає доступних треків для літери '{letter}'.")

async def play_track(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split("_")
    letter, track_idx = data[1], int(data[2])
    track = tracks_db[letter][track_idx]

    if "cover" in track:
        media = InputMediaPhoto(media=track["cover"], caption=f"?? {track['name']}")
        await query.message.reply_media_group([media])

    await query.message.reply_audio(audio=track["url"], caption="?? Ваш трек для прослуховування.")

    if "pdf" in track:
        await query.message.reply_document(document=track["pdf"], caption="?? Ноти")

admin_keyboard = ReplyKeyboardMarkup(
    [["Додати трек", "Редагувати трек"]],
    resize_keyboard=True
)

async def admin(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text("Адмін-панель:", reply_markup=admin_keyboard)
    else:
        await update.message.reply_text("У вас немає прав доступу.")

async def add_track(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        return

    await update.message.reply_text("Введіть літеру для треку:")
    context.user_data["adding_track"] = True

async def receive_letter(update: Update, context: CallbackContext):
    letter = update.message.text.upper()
    context.user_data["track_letter"] = letter
    await update.message.reply_text("Тепер відправте назву треку:")
    context.user_data["adding_name"] = True

async def receive_name(update: Update, context: CallbackContext):
    context.user_data["track_name"] = update.message.text
    await update.message.reply_text("Тепер відправте аудіофайл:")
    context.user_data["adding_audio"] = True

async def receive_audio(update: Update, context: CallbackContext):
    file_id = update.message.audio.file_id
    letter = context.user_data["track_letter"]
    name = context.user_data["track_name"]

    new_track = {"name": name, "url": file_id}

    if letter not in tracks_db:
        tracks_db[letter] = []
    
    tracks_db[letter].append(new_track)
    save_tracks(tracks_db)

    await update.message.reply_text(f"Трек '{name}' додано до категорії '{letter}'.")
    context.user_data.clear()

async def receive_cover(update: Update, context: CallbackContext):
    if "adding_audio" not in context.user_data:
        return
    
    file_id = update.message.photo[-1].file_id
    tracks_db[context.user_data["track_letter"]][-1]["cover"] = file_id
    save_tracks(tracks_db)
    await update.message.reply_text("Обкладинку збережено.")

async def receive_pdf(update: Update, context: CallbackContext):
    if "adding_audio" not in context.user_data:
        return
    
    file_id = update.message.document.file_id
    tracks_db[context.user_data["track_letter"]][-1]["pdf"] = file_id
    save_tracks(tracks_db)
    await update.message.reply_text("PDF збережено.")

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Text("Search Backing Track"), show_alphabet))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, letter_selected))
app.add_handler(CallbackQueryHandler(play_track, pattern="^play_"))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.Text("Додати трек"), add_track))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_letter))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name))
app.add_handler(MessageHandler(filters.AUDIO, receive_audio))
app.add_handler(MessageHandler(filters.PHOTO, receive_cover))
app.add_handler(MessageHandler(filters.Document.PDF, receive_pdf))

if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
