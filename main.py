from config import settings
from aiogram import Bot, Dispatcher, types
import asyncio, logging

from allRouters import routers

bot = Bot(token=settings.TG_TOKEN)
dp = Dispatcher()
    
async def run():
    for router in routers:
        dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("EXITED")