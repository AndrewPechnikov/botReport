import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import pytz
from datetime import datetime

# Завантаження змінних середовища
load_dotenv()

# Базові налаштування
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Встановлюємо часовий пояс
TIMEZONE = pytz.timezone('Europe/Kiev')

# Налаштування логування
def setup_logging():
    """Налаштування системи логування"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOGS_DIR / "bot.log"),
            logging.StreamHandler()
        ]
    )
    
    # Створюємо логер для бота
    logger = logging.getLogger("bot")
    return logger

def get_current_time():
    """Отримати поточний час в київському часовому поясі"""
    return datetime.now(TIMEZONE)

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Не знайдено токен бота в змінних середовища")

# Налаштування для Vercel
IS_VERCEL = os.getenv("VERCEL", False)
WEBHOOK_PATH = "/api/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL", f"https://{os.getenv('VERCEL_URL', '')}{WEBHOOK_PATH}")

# Шлях до файлу з даними
PRICE_FILE = BASE_DIR / "data/НОВИЙ прайс для ІНЖЕНЕРІВ 06.2024.xlsx" 