from http.server import HTTPServer
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update
import json

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

async def handler(request):
    """
    Головний обробник вебхуків для Vercel
    """
    try:
        # Отримуємо тіло запиту
        body = await request.read()
        
        # Логуємо отримання запиту
        logger.info("Отримано webhook запит")
        
        # Перевіряємо наявність даних
        if not body:
            logger.error("Отримано порожній запит")
            return web.Response(status=400, text="Empty request")

        # Конвертуємо bytes в словник
        update_dict = json.loads(body)
        
        # Створюємо об'єкт Update
        update = Update(**update_dict)
        
        # Обробляємо оновлення
        await dp.feed_update(bot=bot, update=update)
        
        # Повертаємо успішну відповідь
        return web.Response(status=200, text="OK")
        
    except Exception as e:
        # Логуємо помилку
        logger.error(f"Помилка при обробці webhook: {e}")
        return web.Response(status=500, text=str(e))

# Створюємо застосунок
app = web.Application()

# Додаємо маршрут
app.router.add_post("/api/webhook", handler)

# Точка входу для Vercel
async def handle(request):
    """
    Vercel Function Handler
    """
    return await handler(request) 