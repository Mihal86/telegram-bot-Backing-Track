import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_PUBLIC_URL")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Помилка при підключенні до бази даних: {e}")
        return None
