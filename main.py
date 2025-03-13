
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from utils.background import keep_alive
from bot.handlers import router
from bot.equipment_handlers import equipment_router
from bot.report_handlers import report_router

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

async def main():
    """
    Головна асинхронна функція, яка запускає бота
    """
    # Отримуємо токен з змінних середовища
    bot_token = os.environ.get('BOT_TOKEN')
    if not bot_token:
        print('Помилка: BOT_TOKEN не налаштований у змінних середовища')
        return
        
    # Створюємо екземпляр бота та диспетчера
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    
    # Підключаємо маршрутизатори з обробниками повідомлень
    dp.include_router(router)
    dp.include_router(equipment_router)
    dp.include_router(report_router)
    
    # Запускаємо бота
    print('Бот запущений!')
    await dp.start_polling(bot)


# Запускаємо фоновий сервер для підтримки бота
keep_alive()

if __name__ == '__main__':
    try:
        # Запускаємо головну функцію
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнений!')
