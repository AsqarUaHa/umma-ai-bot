# UMMA AI Bot - Telegram Bot с RAG

Production-ready Telegram бот для UMMA Тендер Академия с использованием RAG (Retrieval-Augmented Generation).

## 🚀 Возможности

- ✅ **RAG с FAISS** - настоящий vector search (не keyword)
- ✅ **OpenAI GPT-4o-mini** - быстрые и точные ответы
- ✅ **Кеширование embeddings** - не пересчитываются при каждом запуске
- ✅ **MySQL** - хранение истории диалогов
- ✅ **Только казахский язык** - строгий system prompt
- ✅ **Fallback к куратору** - если нет информации в базе знаний

## 📁 Структура

```
umma-ai-bot/
├── bot/main.py              # Точка входа
├── core/
│   ├── config.py            # Конфигурация
│   └── logger.py            # Логирование
├── services/
│   ├── embedding_service.py # OpenAI embeddings
│   ├── rag_service.py       # RAG pipeline
│   └── llm_service.py       # LLM генерация
├── database/
│   ├── db.py                # MySQL pool
│   ├── queries.py           # SQL запросы
│   └── models.py            # Схемы
├── knowledge/
│   ├── loader.py            # Загрузка документов
│   ├── vector_store.py      # FAISS индекс
│   └── base_knowledge.txt   # База знаний
├── handlers/
│   └── user.py              # Telegram handlers
└── requirements.txt
```

## 🛠 Установка и локальный запуск

### Локальный запуск с SQLite

```bash
cd umma-ai-bot
pip install -r requirements.txt
cp .env.example .env
```

Отредактируйте `.env`:
```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Локальная SQLite база
USE_DATABASE=true
DB_TYPE=sqlite
SQLITE_PATH=data/umma_bot.db

MAX_HISTORY=20
```

Запустите бота:
```bash
python main.py
```

База данных SQLite будет автоматически создана в `data/umma_bot.db`.

## 🌐 Деплой на Render

### 1. Создайте MySQL сервис на Render

1. Зайдите на [render.com](https://render.com)
2. New → PostgreSQL (или используйте внешний MySQL)
3. Скопируйте connection string

### 2. Создайте Web Service

1. Render → New → Web Service
2. Подключите GitHub репозиторий `umma-ai-bot`
3. Настройки:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

4. Добавьте переменные окружения:
   - `BOT_TOKEN` - ваш Telegram bot token
   - `OPENAI_API_KEY` - ваш OpenAI API key
   - `OPENAI_MODEL` - gpt-4o-mini
   - `EMBEDDING_MODEL` - text-embedding-3-small
   - `USE_DATABASE` - true
   - `DB_TYPE` - mysql
   - `MYSQL_URL` - ваш MySQL connection string
   - `MAX_HISTORY` - 20

5. Deploy автоматически запустится

## 📊 Как работает RAG

**Индексация** (при старте):
```
knowledge/*.txt → chunks (800 chars) → embeddings → FAISS → cache
```

**Поиск** (при запросе):
```
user query → embedding → cosine similarity → top-3 chunks
```

**Генерация**:
```
chunks + history → LLM → response (казахский)
```

## 📝 База знаний

Добавьте `.txt` файлы в `knowledge/`:
- `base_knowledge.txt` - основная база знаний
- Можно добавить другие файлы

## 🔧 Настройка

`.env` для локального запуска (SQLite):
```env
BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

USE_DATABASE=true
DB_TYPE=sqlite
SQLITE_PATH=data/umma_bot.db

MAX_HISTORY=20
```

`.env` для продакшена (MySQL):
```env
BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

USE_DATABASE=true
DB_TYPE=mysql
MYSQL_URL=mysql://user:pass@host:3306/db

MAX_HISTORY=20
```

## 📈 Мониторинг

Логи в stdout:
```
2026-04-13 10:00:00 - bot.main - INFO - Запуск бота...
2026-04-13 10:00:01 - database.db - INFO - База данных инициализирована
2026-04-13 10:00:05 - knowledge.vector_store - INFO - Векторное хранилище загружено из кеша
```

## 🐛 Troubleshooting

**MySQL ошибка:**
- Проверьте формат `MYSQL_URL`: `mysql://user:password@host:port/database`

**Embeddings не кешируются:**
- Убедитесь, что директория `data/` доступна для записи

**Бот не отвечает:**
- Проверьте логи
- Убедитесь, что `BOT_TOKEN` корректный

## 📄 Лицензия

MIT
