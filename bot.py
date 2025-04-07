import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

# Завантажуємо токен бота з змінних середовища
TOKEN = os.getenv("RAILWAY_TOKEN")

# Ініціалізуємо бота та диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Налаштовуємо логування
logging.basicConfig(level=logging.INFO)

# Обробник команди /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.reply("Привіт, я твій бот!")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
