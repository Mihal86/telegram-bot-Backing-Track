# Фейкова база даних
tracks_db = {
    "A": ["Aerosmith - Dream On", "AC/DC - Back in Black"],
    "Б": ["Бумбокс - Вахтерам", "Без Обмежень - Без неї"],
    "C": ["Coldplay - Yellow", "The Cranberries - Zombie"],
    "К": ["Кино - Группа крови", "Квітка Цісик - Два кольори"],
}

def get_tracks_by_letter(letter):
    return tracks_db.get(letter, [])
