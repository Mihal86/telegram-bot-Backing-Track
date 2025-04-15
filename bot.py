import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from db import test_db_connection

load_dotenv()
RAILWAY_TOKEN = os.getenv("RAILWAY_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Бот працює ✅")

if __name__ == "__main__":
    asyncio.run(test_db_connection())  # тест БД при старті

    app = ApplicationBuilder().token(RAILWAY_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
