import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import register_handlers  # Підключаємо наші обробники команд

# Токен бота
TOKEN = "RAILWAY_TOKEN"

# Ініціалізація бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Головна функція
async def main():
    logging.basicConfig(level=logging.INFO)
    register_handlers(dp)  # Реєструємо обробники команд
    await dp.start_polling()

# Запускаємо бота
if __name__ == "__main__":
    asyncio.run(main())
