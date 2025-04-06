from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

RAILWAY_TOKEN = os.getenv("RAILWAY_TOKEN")  # Токен для бота
DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")  # URL для бази даних

bot = Bot(token=RAILWAY_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Використовуй /search <літера> для пошуку треків.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
