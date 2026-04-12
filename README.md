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

## 🛠 Установка

```bash
cd umma-ai-bot
pip install -r requirements.txt
cp .env.example .env
# Заполните .env
python bot/main.py
```

## 🌐 Деплой на Railway

### 1. Создайте MySQL сервис

1. Зайдите на [railway.app](https://railway.app)
2. New Project → Add MySQL
3. Скопируйте `MYSQL_URL` из переменных

### 2. Создайте GitHub репозиторий

```bash
cd umma-ai-bot
git init
git add .
git commit -m "Initial commit"
gh repo create umma-ai-bot --public --source=. --push
```

### 3. Подключите к Railway

1. Railway → New → GitHub Repo
2. Выберите `umma-ai-bot`
3. Добавьте переменные окружения:
   - `BOT_TOKEN` - ваш Telegram bot token
   - `OPENAI_API_KEY` - ваш OpenAI API key
   - `OPENAI_MODEL` - gpt-4o-mini
   - `EMBEDDING_MODEL` - text-embedding-3-small
   - `MYSQL_URL` - из MySQL сервиса
   - `MAX_HISTORY` - 20

4. Deploy автоматически запустится

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

`.env`:
```env
BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
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
