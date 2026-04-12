import os
from typing import List, Dict
from pathlib import Path

from core.config import config
from core.logger import setup_logger

logger = setup_logger(__name__)


class KnowledgeLoader:
    """Загрузчик базы знаний"""

    @staticmethod
    def load_documents() -> List[Dict[str, str]]:
        """
        Загрузка всех документов из knowledge/

        Returns:
            List[Dict]: Список документов с метаданными
        """
        documents = []
        knowledge_path = Path(config.KNOWLEDGE_DIR)

        if not knowledge_path.exists():
            logger.warning(f"Директория {config.KNOWLEDGE_DIR} не найдена")
            return documents

        for file_path in knowledge_path.glob("*.txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()

                if content:
                    documents.append({
                        "filename": file_path.name,
                        "content": content
                    })
                    logger.info(f"Загружен документ: {file_path.name}")

            except Exception as e:
                logger.error(f"Ошибка загрузки {file_path.name}: {e}")

        logger.info(f"Всего загружено документов: {len(documents)}")
        return documents

    @staticmethod
    def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """
        Разбиение текста на чанки

        Args:
            text: Исходный текст
            chunk_size: Размер чанка
            overlap: Перекрытие между чанками

        Returns:
            List[str]: Список чанков
        """
        if chunk_size is None:
            chunk_size = config.CHUNK_SIZE
        if overlap is None:
            overlap = config.CHUNK_OVERLAP

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]

            # Пытаемся разбить по предложениям
            if end < text_length:
                last_period = chunk.rfind(".")
                last_newline = chunk.rfind("\n")
                split_point = max(last_period, last_newline)

                if split_point > chunk_size // 2:
                    chunk = chunk[:split_point + 1]
                    end = start + split_point + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return [c for c in chunks if len(c) > 50]  # Фильтруем слишком короткие

    @staticmethod
    def prepare_chunks(documents: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """
        Подготовка чанков из документов

        Args:
            documents: Список документов

        Returns:
            List[Dict]: Список чанков с метаданными
        """
        all_chunks = []

        for doc in documents:
            chunks = KnowledgeLoader.chunk_text(doc["content"])

            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "text": chunk,
                    "source": doc["filename"],
                    "chunk_id": i
                })

        logger.info(f"Создано чанков: {len(all_chunks)}")
        return all_chunks
