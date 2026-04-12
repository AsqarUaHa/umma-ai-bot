from typing import List, Dict
import numpy as np

from core.logger import setup_logger
from services.embedding_service import EmbeddingService
from knowledge.vector_store import VectorStore

logger = setup_logger(__name__)


class RAGService:
    """Сервис для RAG (Retrieval-Augmented Generation)"""

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.embedding_service = EmbeddingService()

    async def search_relevant_chunks(self, query: str, top_k: int = 3) -> List[Dict[str, any]]:
        """
        Поиск релевантных чанков для запроса

        Args:
            query: Запрос пользователя
            top_k: Количество возвращаемых чанков

        Returns:
            List[Dict]: Список чанков с текстом и score
        """
        try:
            # Создаем embedding для запроса
            query_embedding = await self.embedding_service.create_embedding(query)

            # Поиск в векторном хранилище
            results = self.vector_store.search(query_embedding, top_k)

            logger.info(f"Найдено {len(results)} релевантных чанков для запроса")

            return results

        except Exception as e:
            logger.error(f"Ошибка поиска релевантных чанков: {e}")
            return []

    def format_context(self, chunks: List[Dict[str, any]]) -> str:
        """
        Форматирование контекста из чанков для промпта

        Args:
            chunks: Список найденных чанков

        Returns:
            str: Отформатированный контекст
        """
        if not chunks:
            return ""

        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(f"[Контекст {i}]\n{chunk['text']}")

        return "\n\n".join(context_parts)
