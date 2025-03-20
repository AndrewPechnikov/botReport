import asyncio
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Імпортуємо конфігурацію та логування
from bot.config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH, IS_VERCEL, setup_logging
# Імпортуємо роутери
from bot.handlers import router as report_router
from bot.equipment_handlers import equipment_router
from bot.report_handlers import report_router as save_report_router

# Налаштовуємо логування
logger = setup_logging()

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Реєструємо роутери
dp.include_router(report_router)
dp.include_router(equipment_router)
dp.include_router(save_report_router)

async def on_startup(bot: Bot, base_url: str):
    """
    Налаштування вебхука при старті бота
    """
    logger.info("Налаштування вебхука...")
    await bot.set_webhook(f"{base_url}{WEBHOOK_PATH}")
    logger.info(f"Вебхук встановлено на {base_url}{WEBHOOK_PATH}")

async def on_shutdown(bot: Bot):
    """
    Очищення при зупинці бота
    """
    logger.info("Видалення вебхука...")
    await bot.delete_webhook()
    logger.info("Вебхук видалено")

def create_app():
    """
    Створення веб-застосунку для роботи з вебхуками
    """
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    return app

async def start_polling():
    """
    Запуск бота в режимі polling
    """
    logger.info("Запуск бота в режимі polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    if IS_VERCEL:
        # Запуск на Vercel
        logger.info("Запуск на Vercel...")
        app = create_app()
        
        # Додаємо обробник startup
        async def _startup():
            await on_startup(bot, WEBHOOK_URL)
        dp.startup.register(_startup)
        
        # Додаємо обробник shutdown
        async def _shutdown():
            await on_shutdown(bot)
        dp.shutdown.register(_shutdown)
        
        # Запускаємо веб-сервер
        web.run_app(app, host="0.0.0.0", port=8000)
    else:
        # Локальний запуск
        logger.info("Локальний запуск бота...")
        asyncio.run(start_polling())
