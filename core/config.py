import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Конфигурация приложения"""

    # Telegram
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Database (optional)
    MYSQL_URL: str = os.getenv("MYSQL_URL", "")
    USE_DATABASE: bool = os.getenv("USE_DATABASE", "false").lower() == "true"
    DB_TYPE: str = os.getenv("DB_TYPE", "sqlite")  # sqlite или mysql
    SQLITE_PATH: str = os.getenv("SQLITE_PATH", "data/umma_bot.db")

    # RAG
    MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "20"))
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100
    TOP_K_CHUNKS: int = 3

    # Paths
    KNOWLEDGE_DIR: str = "knowledge"
    VECTOR_CACHE_PATH: str = "data/vector_cache.pkl"
    FAISS_INDEX_PATH: str = "data/faiss_index.bin"

    def validate(self):
        """Валидация конфигурации"""
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не установлен")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY не установлен")
        # Валидация БД
        if self.USE_DATABASE:
            if self.DB_TYPE == "mysql" and not self.MYSQL_URL:
                raise ValueError("MYSQL_URL не установлен (DB_TYPE=mysql)")
            elif self.DB_TYPE not in ["sqlite", "mysql"]:
                raise ValueError("DB_TYPE должен быть 'sqlite' или 'mysql'")


config = Config()
config.validate()
