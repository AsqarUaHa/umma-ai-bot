# Быстрый старт

## Требования

- Python 3.11 или выше
- Telegram Bot Token
- OpenAI API Key

## Установка Python (если не установлен)

1. Скачайте Python с https://www.python.org/downloads/
2. **ВАЖНО**: При установке отметьте "Add Python to PATH"
3. Перезапустите компьютер после установки

## Локальный запуск

### Вариант 1: Через BAT файл
1. Дважды кликните на `run.bat`

### Вариант 2: Через PowerShell
1. Правой кнопкой на `run.ps1` → "Запустить с помощью PowerShell"
2. Если появится ошибка политики выполнения, запустите PowerShell от администратора и выполните:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### Вариант 3: Вручную
```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Запустить бота
python main.py
```

Бот автоматически:
- Создаст виртуальное окружение
- Установит зависимости
- Создаст SQLite базу в `data/umma_bot.db`
- Запустится

## Что нужно настроить

Файл `.env` уже настроен для локального запуска с SQLite.

Проверьте что указаны:
- `BOT_TOKEN` - токен вашего Telegram бота
- `OPENAI_API_KEY` - ключ OpenAI API

## База знаний

Добавьте текстовые файлы в папку `knowledge/` с информацией для бота.

## Деплой на Render

См. инструкции в `README.md`
