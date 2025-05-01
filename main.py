from config import settings
from aiogram import Bot, Dispatcher
import asyncio, logging
import sys

from allRouters import routers
from routers.user.message_logger import router

from aiogram.enums import UpdateType

bot = Bot(token=settings.TG_TOKEN)
dp = Dispatcher()

async def run():
    dp.include_router(router)
    # for router in routers:
    #     dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=[UpdateType.MESSAGE_REACTION, UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY])

def main():
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("EXITED")

if __name__ == "__main__":
    if "-dev" in sys.argv:
        import py_hot_reload
        py_hot_reload.run_with_reloader(main)
    else:
        main()