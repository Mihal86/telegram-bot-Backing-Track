import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def test_db_connection():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Успішно підключено до бази")
        await conn.close()
    except Exception as e:
        print("❌ Помилка підключення до бази:", e)
