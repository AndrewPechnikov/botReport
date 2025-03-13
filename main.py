import asyncio
from aiogram import Bot, Dispatcher
from background import keep_alive

from handlers import router


async def main():
    bot = Bot(token='7597075440:AAFGbuJH5W8-t02xRsdWWbLxhwLS5Kh0grU')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


keep_alive()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнений!')
