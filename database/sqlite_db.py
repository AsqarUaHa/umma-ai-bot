import sqlite3
import os
from contextlib import contextmanager

from core.logger import setup_logger

logger = setup_logger(__name__)


class SQLiteDatabase:
    """Класс для работы с SQLite"""

    def __init__(self, db_path: str = "data/umma_bot.db"):
        self.db_path = db_path
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для соединения"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()


async def init_db(db_path: str = "data/umma_bot.db"):
    """Инициализация базы данных SQLite"""
    try:
        db = SQLiteDatabase(db_path)

        with db.get_connection() as conn:
            cursor = conn.cursor()

            # Создание таблицы messages
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Создание индекса
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_created
                ON messages(user_id, created_at)
            """)

        logger.info(f"SQLite база данных успешно инициализирована: {db_path}")

    except Exception as e:
        logger.error(f"Ошибка инициализации SQLite БД: {e}")
        raise
