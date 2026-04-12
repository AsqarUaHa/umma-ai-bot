import mysql.connector
from mysql.connector import pooling
from urllib.parse import urlparse

from core.config import config
from core.logger import setup_logger

logger = setup_logger(__name__)


class Database:
    """Класс для работы с MySQL"""

    _pool = None

    @classmethod
    def _parse_mysql_url(cls, url: str) -> dict:
        """Парсинг MySQL URL"""
        parsed = urlparse(url)
        return {
            "host": parsed.hostname,
            "port": parsed.port or 3306,
            "user": parsed.username,
            "password": parsed.password,
            "database": parsed.path.lstrip("/")
        }

    @classmethod
    def get_pool(cls):
        """Получение connection pool"""
        if cls._pool is None:
            db_config = cls._parse_mysql_url(config.MYSQL_URL)
            cls._pool = pooling.MySQLConnectionPool(
                pool_name="umma_pool",
                pool_size=5,
                **db_config
            )
        return cls._pool

    @classmethod
    def get_connection(cls):
        """Получение соединения из пула"""
        return cls.get_pool().get_connection()


async def init_db():
    """Инициализация базы данных"""
    try:
        conn = Database.get_connection()
        cursor = conn.cursor()

        # Создание таблицы messages
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id BIGINT NOT NULL,
                role VARCHAR(20) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_user_created (user_id, created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)

        conn.commit()
        cursor.close()
        conn.close()

        logger.info("База данных успешно инициализирована")

    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")
        raise
