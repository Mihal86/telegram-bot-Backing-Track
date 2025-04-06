from aiogram import types, Dispatcher
from database import get_tracks_by_letter  # Підключаємо базу даних

# Команда старт
async def start_command(message: types.Message):
    await message.answer("Привіт! Я допоможу знайти backing track.\nНапиши /search для пошуку.")

# Пошук за алфавітом
async def search_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    letters = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ"
    buttons = [types.KeyboardButton(letter) for letter in letters]
    
    keyboard.add(*buttons)
    await message.answer("Оберіть першу літеру виконавця:", reply_markup=keyboard)

# Вибір пісень за літерою
async def letter_chosen(message: types.Message):
    letter = message.text.upper()
    tracks = get_tracks_by_letter(letter)

    if tracks:
        track_list = "\n".join([f"🎵 {track}" for track in tracks])
        await message.answer(f"Ось треки на {letter}:\n{track_list}")
    else:
        await message.answer("Немає треків на цю літеру. Спробуйте іншу.")

# Реєструємо команди
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(search_command, commands=["search"])
    dp.register_message_handler(letter_chosen, content_types=["text"])
