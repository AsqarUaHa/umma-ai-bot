from typing import List, Dict
from openai import AsyncOpenAI

from core.config import config
from core.logger import setup_logger

logger = setup_logger(__name__)


class LLMService:
    """Сервис для работы с LLM"""

    SYSTEM_PROMPT = """Сен Ержан - UMMA Тендер Академиясының көмекшісісің.

МАҢЫЗДЫ ЕРЕЖЕЛЕР:
1. Тек қазақ тілінде жауап бер
2. Қысқа және түсінікті жаз
3. ТЕК берілген контекст негізінде жауап бер
4. Егер контекстте жауап жоқ болса, мынаны жаз: "Кешіріңіз, бұл сұрақ бойынша дәл ақпарат жоқ. Кураторға жазыңыз: @umma_curator"
5. ЕШҚАШАН ақпаратты ойдан шығарма
6. Достық және кәсіби стильде сөйле

Сенің міндетің - студенттерге тендер бойынша көмектесу."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL

    async def generate_response(
        self,
        user_message: str,
        context: str,
        history: List[Dict[str, str]] = None
    ) -> str:
        """
        Генерация ответа от LLM

        Args:
            user_message: Сообщение пользователя
            context: Контекст из RAG
            history: История сообщений

        Returns:
            str: Ответ модели
        """
        try:
            messages = [
                {"role": "system", "content": self.SYSTEM_PROMPT}
            ]

            # Добавляем историю (если есть)
            if history:
                for msg in history[-10:]:  # Последние 10 сообщений
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            # Формируем промпт с контекстом
            if context:
                user_prompt = f"""КОНТЕКСТ З БАЗЫ ЗНАНИЙ:
{context}

СҰРАҚ СТУДЕНТТЕН:
{user_message}

Контекст негізінде жауап бер. Егер контекстте жауап жоқ болса, кураторға жібер."""
            else:
                user_prompt = f"""СҰРАҚ СТУДЕНТТЕН:
{user_message}

Контекст табылмады. Кураторға жібер."""

            messages.append({"role": "user", "content": user_prompt})

            # Запрос к OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )

            answer = response.choices[0].message.content
            logger.info(f"LLM ответ сгенерирован (длина: {len(answer)})")

            return answer

        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {e}")
            return "Кешіріңіз, қазір техникалық қиындықтар бар. Кейінірек қайталап көріңіз."
