import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler
import psycopg2

TOKEN = os.getenv("RAILWAY_TOKEN")
ADMIN_ID = 6266469974  # ID адміністратора
DATABASE_URL = os.getenv("postgresql://postgres:WdZTOBcrjZXsXSdxELttDUtSJntpQUWT@yamabiko.proxy.rlwy.net:45245/railway")

app = Application.builder().token(TOKEN).build()

# Підключення до PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Створення таблиці для треків
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            letter CHAR(1) NOT NULL,
            url VARCHAR(255),
            cover VARCHAR(255),
            pdf VARCHAR(255)
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Додавання треку
def add_track(name, letter, url, cover=None, pdf=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tracks (name, letter, url, cover, pdf) 
        VALUES (%s, %s, %s, %s, %s);
    ''', (name, letter, url, cover, pdf))
    conn.commit()
    cursor.close()
    conn.close()

# Пошук треків за літерою
def get_tracks_by_letter(letter):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, url, cover, pdf 
        FROM tracks 
        WHERE letter = %s;
    ''', (letter,))
    tracks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tracks

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
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text("Адмін-панель:", reply_markup=admin_keyboard)
    else:
        await update.message.reply_text("У вас немає прав доступу.")

# Обробник додавання треку
async def add_track_handler(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        track_name = "Новий трек"  # Приклад
        track_letter = "A"  # Приклад
        track_url = "http://example.com/track.mp3"  # Приклад
        # Додаємо трек до бази
        add_track(track_name, track_letter, track_url)
        await update.message.reply_text(f"Трек '{track_name}' додано!")
    else:
        await update.message.reply_text("У вас немає прав доступу.")

# Додавання обробників команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.Text("Додати трек"), add_track_handler))

# Створення таблиці для треків при старті
create_table()

# Запуск бота
if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()


def test_db_connection():
    try:
        conn = get_db_connection()
        print("Підключення до бази даних успішне!")
        conn.close()
    except Exception as e:
        print(f"Помилка при підключенні до бази даних: {e}")
