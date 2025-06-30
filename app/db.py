import psycopg
from app import app


def get_db_connection():
    """Функция для подключения к базе данных."""
    return psycopg.connect(
        host='localhost',
        port=app.config['DB_PORT'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        dbname=app.config['DB_NAME']
    )