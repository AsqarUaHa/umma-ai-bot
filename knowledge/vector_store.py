import os
import pickle
from typing import List, Dict
import numpy as np
import faiss

from core.config import config
from core.logger import setup_logger
from knowledge.loader import KnowledgeLoader
from services.embedding_service import EmbeddingService

logger = setup_logger(__name__)


class VectorStore:
    """Векторное хранилище с FAISS"""

    def __init__(self):
        self.index = None
        self.chunks = []
        self.embedding_service = EmbeddingService()
        self.dimension = 1536  # Размерность для text-embedding-3-small

    async def initialize(self):
        """Инициализация векторного хранилища"""
        # Проверяем наличие кеша
        if self._load_from_cache():
            logger.info("Векторное хранилище загружено из кеша")
            return

        # Создаем новый индекс
        logger.info("Создание нового векторного индекса...")
        await self._build_index()
        self._save_to_cache()
        logger.info("Векторный индекс создан и сохранен")

    async def _build_index(self):
        """Построение FAISS индекса"""
        # Загрузка документов
        documents = KnowledgeLoader.load_documents()
        if not documents:
            raise ValueError("Нет документов для индексации")

        # Создание чанков
        self.chunks = KnowledgeLoader.prepare_chunks(documents)

        # Создание embeddings
        texts = [chunk["text"] for chunk in self.chunks]
        logger.info(f"Создание embeddings для {len(texts)} чанков...")

        embeddings = []
        batch_size = 100
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = await self.embedding_service.create_embeddings_batch(batch)
            embeddings.extend(batch_embeddings)
            logger.info(f"Обработано {min(i + batch_size, len(texts))}/{len(texts)} чанков")

        # Создание FAISS индекса
        embeddings_array = np.array(embeddings, dtype=np.float32)

        # Используем IndexFlatIP для cosine similarity
        self.index = faiss.IndexFlatIP(self.dimension)

        # Нормализуем векторы для cosine similarity
        faiss.normalize_L2(embeddings_array)
        self.index.add(embeddings_array)

        logger.info(f"FAISS индекс создан с {self.index.ntotal} векторами")

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, any]]:
        """
        Поиск похожих чанков

        Args:
            query_embedding: Embedding запроса
            top_k: Количество результатов

        Returns:
            List[Dict]: Найденные чанки с scores
        """
        if self.index is None or not self.chunks:
            logger.warning("Векторное хранилище не инициализировано")
            return []

        # Нормализуем query embedding
        query_array = np.array([query_embedding], dtype=np.float32)
        faiss.normalize_L2(query_array)

        # Поиск
        scores, indices = self.index.search(query_array, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx].copy()
                chunk["score"] = float(score)
                results.append(chunk)

        return results

    def _save_to_cache(self):
        """Сохранение в кеш"""
        try:
            os.makedirs("data", exist_ok=True)

            # Сохраняем FAISS индекс
            faiss.write_index(self.index, config.FAISS_INDEX_PATH)

            # Сохраняем chunks
            with open(config.VECTOR_CACHE_PATH, "wb") as f:
                pickle.dump(self.chunks, f)

            logger.info("Векторное хранилище сохранено в кеш")

        except Exception as e:
            logger.error(f"Ошибка сохранения кеша: {e}")

    def _load_from_cache(self) -> bool:
        """Загрузка из кеша"""
        try:
            if not os.path.exists(config.FAISS_INDEX_PATH) or \
               not os.path.exists(config.VECTOR_CACHE_PATH):
                return False

            # Загружаем FAISS индекс
            self.index = faiss.read_index(config.FAISS_INDEX_PATH)

            # Загружаем chunks
            with open(config.VECTOR_CACHE_PATH, "rb") as f:
                self.chunks = pickle.load(f)

            return True

        except Exception as e:
            logger.error(f"Ошибка загрузки кеша: {e}")
            return False
