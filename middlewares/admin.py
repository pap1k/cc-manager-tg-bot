from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Awaitable, Dict, Any, Callable
import logging
from config import settings

class CheckAdminAccessMiddleware(BaseMiddleware):
    async def __call__(self, 
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any]) -> Any:

        if int(data['event_from_user'].id) in settings.ADMIN_LIST:
            return await handler(event, data)
        else:
            logging.info(f"Unregistreg admin called command")
                