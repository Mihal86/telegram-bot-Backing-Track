from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
import asyncpg
import os

RAILWAY_TOKEN = "your-telegram-bot-token"
DATABASE_URL = os.getenv("${{ Postgres.DATABASE_URL }}")  # Ваш URL для підключення до PostgreSQL

bot = Bot(token=RAILWAY_TOKEN)
dp = Dispatcher(bot)

# Підключення до бази даних
async def db_connect():
    return await asyncpg.connect(${{ Postgres.DATABASE_URL }})

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
    await dp.current_state(user=message.from_user.id).set_state("waiting_for_title")

@dp.message_handler(state="waiting_for_title")
async def process_title(message: types.Message):
    title = message.text
    await dp.current_state(user=message.from_user.id).set_state("waiting_for_artist")
    await message.answer("Тепер введіть виконавця.")

@dp.message_handler(state="waiting_for_artist")
async def process_artist(message: types.Message):
    artist = message.text
    await dp.current_state(user=message.from_user.id).set_state("waiting_for_language")
    await message.answer("Введіть мову треку (uk/en).")

@dp.message_handler(state="waiting_for_language")
async def process_language(message: types.Message):
    language = message.text
    await dp.current_state(user=message.from_user.id).set_state("waiting_for_file_url")
    await message.answer("Надішліть посилання на файл треку.")

@dp.message_handler(state="waiting_for_file_url")
async def process_file_url(message: types.Message):
    file_url = message.text
    await dp.current_state(user=message.from_user.id).set_state("waiting_for_image")
    await message.answer("Надішліть зображення для треку.")

@dp.message_handler(state="waiting_for_image", content_types=types.ContentType.PHOTO)
async def process_image(message: types.Message):
    image_url = message.photo[-1].file_id
    await dp.current_state(user=message.from_user.id).set_state("waiting_for_pdf")
    await message.answer("Надішліть PDF файл для треку.")

@dp.message_handler(state="waiting_for_pdf", content_types=types.ContentType.DOCUMENT)
async def process_pdf(message: types.Message):
    pdf_url = message.document.file_id
    await dp.current_state(user=message.from_user.id).finish()

    # Додаємо трек до бази даних
    await add_track_to_db(title, artist, language, file_url, image_url, pdf_url)
    
    await message.answer("Трек успішно додано!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
