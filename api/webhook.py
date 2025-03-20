from http.server import HTTPServer
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from main import bot, dp, on_startup, on_shutdown

async def handle_webhook(request):
    """
    Обробник вебхуків для Vercel
    """
    try:
        # Отримуємо дані від Telegram
        update = await request.json()
        
        # Обробляємо оновлення
        await dp.feed_webhook_update(bot, update)
        
        return web.Response(status=200)
    except Exception as e:
        return web.Response(status=500, text=str(e))

app = web.Application()
app.router.add_post("/api/webhook", handle_webhook)

# Додаємо обробники startup/shutdown
app.on_startup.append(lambda app: on_startup(bot, str(request.url)))
app.on_shutdown.append(lambda app: on_shutdown(bot))

# Точка входу для Vercel
handler = app._make_handler() 