from config import settings
from aiogram import Bot, Dispatcher
import asyncio, logging

from allRouters import routers

from aiogram.enums import UpdateType

bot = Bot(token=settings.TG_TOKEN)
dp = Dispatcher()

async def run():

    for router in routers:
        dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=[UpdateType.MESSAGE_REACTION, UpdateType.MESSAGE])

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("EXITED")