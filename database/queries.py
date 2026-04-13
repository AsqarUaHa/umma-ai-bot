from typing import List, Dict
from datetime import datetime

from core.logger import setup_logger
from core.config import config

logger = setup_logger(__name__)


def get_db_adapter():
    """Получение адаптера БД в зависимости от конфигурации"""
    if not config.USE_DATABASE:
        return None

    if config.DB_TYPE == "sqlite":
        from database.sqlite_db import SQLiteDatabase
        return SQLiteDatabase(config.SQLITE_PATH)
    else:
        from database.db import Database
        return Database


class MessageQueries:
    """Запросы для работы с сообщениями"""

    @staticmethod
    async def save_message(user_id: int, role: str, content: str):
        """
        Сохранение сообщения в БД

        Args:
            user_id: ID пользователя
            role: Роль (user/assistant)
            content: Содержимое сообщения
        """
        if not config.USE_DATABASE:
            logger.debug("База данных отключена, сообщение не сохранено")
            return

        try:
            db = get_db_adapter()

            if config.DB_TYPE == "sqlite":
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
                        (user_id, role, content)
                    )
            else:
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO messages (user_id, role, content) VALUES (%s, %s, %s)",
                    (user_id, role, content)
                )
                conn.commit()
                cursor.close()
                conn.close()

        except Exception as e:
            logger.error(f"Ошибка сохранения сообщения: {e}")

    @staticmethod
    async def get_user_history(user_id: int, limit: int = None) -> List[Dict[str, str]]:
        """
        Получение истории сообщений пользователя

        Args:
            user_id: ID пользователя
            limit: Максимальное количество сообщений

        Returns:
            List[Dict]: История сообщений
        """
        if not config.USE_DATABASE:
            logger.debug("База данных отключена, история пуста")
            return []

        try:
            db = get_db_adapter()

            if limit is None:
                limit = config.MAX_HISTORY

            if config.DB_TYPE == "sqlite":
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        SELECT role, content, created_at
                        FROM messages
                        WHERE user_id = ?
                        ORDER BY created_at DESC
                        LIMIT ?
                        """,
                        (user_id, limit)
                    )
                    messages = cursor.fetchall()

                    return [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in reversed(messages)
                    ]
            else:
                conn = db.get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute(
                    """
                    SELECT role, content, created_at
                    FROM messages
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (user_id, limit)
                )
                messages = cursor.fetchall()
                cursor.close()
                conn.close()

                return [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in reversed(messages)
                ]

        except Exception as e:
            logger.error(f"Ошибка получения истории: {e}")
            return []
