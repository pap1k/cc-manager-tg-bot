from config import settings
from aiogram import Bot, Dispatcher, types
import asyncio, logging
from routers.admin import router as admin_router
bot = Bot(token=settings.TG_TOKEN)
dp = Dispatcher()
    
async def run():
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("EXITED")