from http.server import HTTPServer
from aiogram import Bot, Dispatcher, types
import json
from typing import Dict, Any

# Імпортуємо конфігурацію
from bot.config import BOT_TOKEN, setup_logging

# Налаштовуємо логування
logger = setup_logging()

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Імпортуємо роутери
from bot.handlers import router as report_router
from bot.equipment_handlers import equipment_router
from bot.report_handlers import report_router as save_report_router

# Реєструємо роутери
dp.include_router(report_router)
dp.include_router(equipment_router)
dp.include_router(save_report_router)

async def process_update(update_data: dict) -> bool:
    """
    Обробка оновлення від Telegram
    """
    try:
        logger.info(f"Обробка оновлення: {update_data}")
        update = types.Update(**update_data)
        await dp.feed_update(bot=bot, update=update)
        return True
    except Exception as e:
        logger.error(f"Помилка при обробці оновлення: {e}")
        return False

def format_response(status_code: int, body: str) -> Dict[str, Any]:
    """
    Форматування відповіді для Vercel
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({"message": body})
    }

async def handler(request) -> Dict[str, Any]:
    """
    Обробник для Vercel Serverless Function
    """
    try:
        # Перевіряємо метод запиту
        if request.get("method", "POST") != "POST":
            return format_response(405, "Method not allowed")

        # Отримуємо тіло запиту
        body = request.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)
        
        # Логуємо отримання запиту
        logger.info(f"Отримано webhook запит: {body}")
        
        # Обробляємо оновлення
        success = await process_update(body)
        
        if success:
            return format_response(200, "OK")
        else:
            return format_response(500, "Failed to process update")
            
    except Exception as e:
        logger.error(f"Помилка при обробці webhook: {e}")
        return format_response(500, str(e))

def main(request):
    """
    Точка входу для Vercel
    """
    import asyncio
    return asyncio.run(handler(request)) 