from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.logger import setup_logger
from services.rag_service import RAGService
from services.llm_service import LLMService
from database.queries import MessageQueries

logger = setup_logger(__name__)
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "Сәлеметсіз бе! 👋\n\n"
        "Мен Ержан - UMMA Тендер Академиясының AI көмекшісімін.\n\n"
        "Тендерлер туралы сұрақтарыңызға жауап беремін. "
        "Сұрағыңызды жазыңыз!"
    )


@router.message(F.text)
async def handle_message(message: Message, vector_store):
    """Обработчик текстовых сообщений"""
    user_id = message.from_user.id
    user_message = message.text

    try:
        # Сохраняем сообщение пользователя
        await MessageQueries.save_message(user_id, "user", user_message)

        # Показываем индикатор печати
        await message.bot.send_chat_action(message.chat.id, "typing")

        # RAG: поиск релевантных чанков
        rag_service = RAGService(vector_store)
        chunks = await rag_service.search_relevant_chunks(user_message, top_k=3)

        # Форматируем контекст
        context = rag_service.format_context(chunks)

        # Получаем историю
        history = await MessageQueries.get_user_history(user_id, limit=10)

        # Генерация ответа
        llm_service = LLMService()
        response = await llm_service.generate_response(
            user_message=user_message,
            context=context,
            history=history
        )

        # Сохраняем ответ
        await MessageQueries.save_message(user_id, "assistant", response)

        # Отправляем ответ
        await message.answer(response)

        logger.info(f"Обработано сообщение от пользователя {user_id}")

    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await message.answer(
            "Кешіріңіз, қате орын алды. Кейінірек қайталап көріңіз немесе "
            "кураторға жазыңыз: @umma_curator"
        )
