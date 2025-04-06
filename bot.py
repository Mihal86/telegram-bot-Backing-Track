from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
import asyncpg
import os
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Завантажуємо змінні середовища
DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")  # Використовуємо нову змінну

RAILWAY_TOKEN = os.getenv("RAILWAY_TOKEN")

bot = Bot(token=RAILWAY_TOKEN)
dp = Dispatcher(bot)

class AddTrackStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_artist = State()
    waiting_for_language = State()
    waiting_for_file_url = State()
    waiting_for_image = State()
    waiting_for_pdf = State()

# Підключення до бази даних
async def db_connect():
    return await asyncpg.connect(DATABASE_URL)  # Підключення через змінну середовища

# Перевірка адміністратора
ADMIN_ID = 6266469974

async def add_track_to_db(title, artist, language, file_url, image_url, pdf_url):
    conn = await db_connect()
    await conn.execute('''
    INSERT INTO tracks (title, artist, language, file_url, image_url, pdf_url)
    VALUES ($1, $2, $3, $4, $5, $6)
    ''', title, artist, language, file_url, image_url, pdf_url)
    await conn.close()

# Команда /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Використовуй /search <літера> для пошуку треків.")

# Пошук треків
@dp.message_handler(commands=["search"])
async def cmd_search(message: types.Message):
    search_letter = message.text.split()[1].lower()
    conn = await db_connect()
    tracks = await conn.fetch('''
    SELECT title, artist, file_url FROM tracks
    WHERE LOWER(title) LIKE $1 OR LOWER(artist) LIKE $1
    ''', f'{search_letter}%')
    await conn.close()
    
    if tracks:
        result = "\n".join([f"{track['title']} - {track['artist']}" for track in tracks])
        await message.answer(f"Результати пошуку:\n{result}")
    else:
        await message.answer("Треки не знайдені.")

# Додавання треку (для адміністратора)
@dp.message_handler(commands=["add_track"])
async def cmd_add_track(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас немає доступу до цієї команди.")
        return
    
    # Запитуємо дані для нового треку
    await message.answer("Надішліть назву треку.")
    await dp.current_state(user=message.from_user.id).set_state(AddTrackStates.waiting_for_title)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
