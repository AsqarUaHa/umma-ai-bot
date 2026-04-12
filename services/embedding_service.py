from typing import List
from openai import AsyncOpenAI

from core.config import config
from core.logger import setup_logger

logger = setup_logger(__name__)


class EmbeddingService:
    """Сервис для работы с embeddings"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.EMBEDDING_MODEL

    async def create_embedding(self, text: str) -> List[float]:
        """Создание embedding для текста"""
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Ошибка создания embedding: {e}")
            raise

    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Создание embeddings для списка текстов"""
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Ошибка создания batch embeddings: {e}")
            raise
