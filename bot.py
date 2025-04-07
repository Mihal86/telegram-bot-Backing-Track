import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram import F
import asyncio

# Завантажуємо токен бота з змінних середовища
TOKEN = os.getenv("RAILWAY_TOKEN")

# Ініціалізуємо бота та диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO)

# Обробник команди /start
@dp.message(commands=['start'])
async def send_welcome(message: Message):
    await message.answer("Привіт, я твій бот!")

async def main():
    dp.include_router(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
