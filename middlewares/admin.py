from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Awaitable, Dict, Any, Callable

from sqlalchemy import select, and_
from models import Level, ModerModel
from database import db_session

class CheckModerAccessMiddleware(BaseMiddleware):
    def __init__(self, level: Level = Level.junior):
        super().__init__()
        self.level = level

    async def __call__(self, 
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any]) -> Any:
        async with db_session() as session:
            result = await session.execute(
                select(ModerModel).where(
                    and_(
                        ModerModel.tg_id == int(data['event_from_user'].id),
                        ModerModel.active == True
                    )
                )
            )
            moder = result.scalar_one_or_none()
            if moder:
                if moder.level.value >= self.level.value:
                    data['moder_caller'] = moder
                    return await handler(event, data)
                