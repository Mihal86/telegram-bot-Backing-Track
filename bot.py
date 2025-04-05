from telegram import Bot
import os
import asyncio

# Отримуємо токен бота з Railway
TOKEN = os.getenv("RAILWAY_TOKEN")

bot = Bot(token=TOKEN)

async def delete_commands():
    await bot.set_my_commands([])  # Видаляємо всі команди

# Запускаємо функцію
asyncio.run(delete_commands())

print("✅ Меню команд успішно очищено!")
