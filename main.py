import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.start import router
from aiohttp import web

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found!")

# Dummy веб-сервер, чтобы Render не ругался на порт
async def handle(request):
    return web.Response(text="Newey bot is alive!")

async def start_web():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    print("Dummy web server started on port 10000")

# Основной бот
async def start_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    print("Newey bot started polling!")
    await dp.start_polling(bot)

# Запуск всего вместе
async def main():
    # Запускаем веб-сервер и бота параллельно
    await asyncio.gather(
        start_web(),
        start_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())
