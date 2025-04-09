import os
import psycopg2
from urllib.parse import urlparse
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Завантаження змінних середовища (якщо тестуєте локально)
from dotenv import load_dotenv
load_dotenv()  # Завантажуємо змінні з .env файлу

# Токен бота
TOKEN = os.getenv("RAILWAY_TOKEN")
ADMIN_ID = 6266469974  # ID адміністратора

# Отримуємо URL для підключення до бази даних
DATABASE_URL = os.getenv("DATABASE_PUBLIC_URL")

# Підключення до бази даних
def get_db_connection():
    try:
        result = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            dbname=result.path[1:],  # Витягуємо ім'я бази даних з URL
            user=result.username,     # Витягуємо користувача
            password=result.password, # Витягуємо пароль
            host=result.hostname,     # Витягуємо хост
            port=result.port          # Витягуємо порт
        )
        return conn
    except Exception as e:
        print(f"Помилка при підключенні до бази даних: {e}")
        return None

# Створення таблиці в базі даних (якщо вона ще не існує)
def create_table():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            artist VARCHAR(255),
            genre VARCHAR(100),
            path VARCHAR(255) NOT NULL
        )
        """)
        conn.commit()
        cur.close()
        conn.close()

# Ініціалізація таблиці при старті бота
create_table()

# Створення клавіатури для адміністратора
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

# Обробник команди "Додати трек"
async def add_track_handler(update: Update, context: CallbackContext):
    # Тільки для адміністратора
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text("Будь ласка, надайте назву треку.")

# Обробник команди "Редагувати трек"
async def edit_track_handler(update: Update, context: CallbackContext):
    # Тільки для адміністратора
    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text("Виберіть трек для редагування.")

# Додавання обробників команд
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))

# Додавання обробника для кнопки "Додати трек"
app.add_handler(MessageHandler(filters.Text("Додати трек"), add_track_handler))

# Додавання обробника для кнопки "Редагувати трек"
app.add_handler(MessageHandler(filters.Text("Редагувати трек"), edit_track_handler))

if __name__ == "__main__":
    print("Бот запущено...")
    app.run_polling()
