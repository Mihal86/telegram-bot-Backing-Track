import logging
import asyncio
import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from config import RAILWAY_TOKEN, DATABASE_URL, ADMIN_ID

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=RAILWAY_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Функція підключення до бази даних
async def create_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

db_pool = None

# Ініціалізація БД
async def init_db():
    async with db_pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                language TEXT CHECK (language IN ('uk', 'en')) NOT NULL,
                file_url TEXT NOT NULL
            );
        ''')

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привіт! Вітаємо у музичному магазині. Використовуйте /search <літера> для пошуку треків.")

@dp.message(Command("search"))
async def search_tracks(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Будь ласка, введіть літеру для пошуку.")
        return
    letter = args[1].lower()
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT title, artist, file_url FROM tracks
            WHERE LOWER(title) LIKE $1 OR LOWER(artist) LIKE $1
        """, letter + '%')
    
    if rows:
        response = "Знайдені треки:\n" + "\n".join(f"{row['title']} - {row['artist']} ({row['file_url']})" for row in rows)
    else:
        response = "Треки не знайдено."
    
    await message.answer(response)

@dp.message(Command("add_track"))
async def add_track(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас немає прав для додавання треків.")
        return
    
    args = message.text.split("|", maxsplit=3)
    if len(args) < 4:
        await message.answer("Формат команди: /add_track Назва | Виконавець | Мова (uk/en) | Посилання")
        return
    
    title, artist, language, file_url = map(str.strip, args[1:])
    if language not in ("uk", "en"):
        await message.answer("Мова має бути 'uk' або 'en'.")
        return
    
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO tracks (title, artist, language, file_url)
            VALUES ($1, $2, $3, $4)
        """, title, artist, language, file_url)
    
    await message.answer(f"Трек '{title}' успішно додано!")

async def main():
    global db_pool
    db_pool = await create_db_pool()
    await init_db()
    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
