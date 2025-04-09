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
        ["H", "I",
