import sys
import os

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем и запускаем бота
from bot.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
