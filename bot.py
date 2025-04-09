import os
import psycopg2

# Отримуємо URI з середовища
DATABASE_URL = os.getenv("DATABASE_PUBLIC_URL")

# Підключення до PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Перевірка з'єднання
def test_db_connection():
    try:
        conn = get_db_connection()
        print("Підключення до бази даних успішне!")
        conn.close()
    except Exception as e:
        print(f"Помилка при підключенні до бази даних: {e}")

# Викликаємо тестову функцію, щоб перевірити підключення
test_db_connection()
