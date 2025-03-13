import asyncio
import os
from aiogram import Bot, Dispatcher
from background import keep_alive

from handlers import router


async def main():
    bot_token = os.environ.get('BOT_TOKEN')
    if not bot_token:
        print('Помилка: BOT_TOKEN не налаштований у змінних середовища')
        return
        
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


keep_alive()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнений!')
