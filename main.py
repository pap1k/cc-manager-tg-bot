from config import settings
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import UpdateType
import asyncio, logging
import sys

from allRouters import routers


def create_bot(use_proxy: bool) -> tuple[Bot, Dispatcher]:
    if use_proxy:
        session = AiohttpSession(proxy="socks5://127.0.0.1:8000")
        bot = Bot(token=settings.TG_TOKEN, session=session)
    else:
        bot = Bot(token=settings.TG_TOKEN)
    dp = Dispatcher()
    return bot, dp

async def run(use_proxy: bool):
    bot, dp = create_bot(use_proxy)
    for router in routers:
        dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=[UpdateType.MESSAGE_REACTION, UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY])

def main(use_proxy = False):
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(run(use_proxy))
    except KeyboardInterrupt:
        print("EXITED")

if __name__ == "__main__":
    if "-dev" in sys.argv:
        import py_hot_reload
        py_hot_reload.run_with_reloader(main)

    else:
        main("-p" in sys.argv)
