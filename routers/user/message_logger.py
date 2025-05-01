from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram import F
from config import settings

from database import db_session
from models import LogMessagesModel

router = Router()

@router.message()
async def any_group_message(message: Message):
    if message.message_thread_id == settings.CHAT_THREAD_ID:
        async with db_session() as session:
            text = message.text if message.text else "<Не текст>"
            record = LogMessagesModel(user_id=message.from_user.id, message=text, link=message.get_url(include_thread_id=True))
            session.add(record)
            await session.commit()
