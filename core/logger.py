import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """Настройка логгера"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Форматирование
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Хендлер для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
