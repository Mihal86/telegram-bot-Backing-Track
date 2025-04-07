from telegram.ext import CallbackQueryHandler

# Обробка натискання кнопки
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()  # Відповідаємо на запит
    callback_data = query.data  # Отримуємо callback_data

    if callback_data == "add_track":
        await query.edit_message_text("Ти обрав додавання треку.")
        # Додати код для додавання треку
    elif callback_data == "edit_track":
        await query.edit_message_text("Ти обрав редагування треку.")
        # Додати код для редагування треку
    elif callback_data == "delete_track":
        await query.edit_message_text("Ти обрав видалення треку.")
        # Додати код для видалення треку

# Реєстрація обробника натискання кнопок
def main():
    # Токен бота
    TOKEN = "your-telegram-bot-token"
    
    # Створення об'єкта Application
    application = Application.builder().token(TOKEN).build()

    # Додаємо хендлери
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
