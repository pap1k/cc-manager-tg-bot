import logging, asyncio
from typing import Coroutine
from classes.bot import bot
from config import settings

LOG_THREAD_ID = 2

class AsyncRemoteHandler(logging.Handler):
    def __init__(self, async_callback: Coroutine):
        super().__init__()
        self.async_callback = async_callback
        self.setLevel(logging.WARNING)  # Только WARNING и выше

    def emit(self, record):
        if record.levelno >= self.level:  # Проверяем уровень
            log_message = self.format(record)
            asyncio.create_task(self._async_emit(log_message))

    async def _async_emit(self, message: str):
        try:
            await self.async_callback(message)
        except Exception as e:
            print(f"🔴[REMOTE_LOGGER] Async log error: {e}")

async def send_to_remote(log: str):
    await bot.send_message(settings.LOG_CHAT_ID, f"[LOG] {log}",  message_thread_id = LOG_THREAD_ID)
    