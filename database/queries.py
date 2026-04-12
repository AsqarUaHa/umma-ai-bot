from typing import List, Dict
from datetime import datetime

from database.db import Database
from core.logger import setup_logger
from core.config import config

logger = setup_logger(__name__)


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
        try:
            conn = Database.get_connection()
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
            raise

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
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(dictionary=True)

            if limit is None:
                limit = config.MAX_HISTORY

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

            # Возвращаем в хронологическом порядке
            return [
                {"role": msg["role"], "content": msg["content"]}
                for msg in reversed(messages)
            ]

        except Exception as e:
            logger.error(f"Ошибка получения истории: {e}")
            return []
