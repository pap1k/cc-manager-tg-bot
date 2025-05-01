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
    print(message.chat.id, settings.TG_CHAT_ID, message.chat.type, ChatType.SUPERGROUP)
    print(message.from_user.id, message.text)
    if message.message_thread_id == settings.CHAT_THREAD_ID:
        async with db_session() as session:
            record = LogMessagesModel(user_id=message.from_user.id, message=message.text)
            session.add(record)
            await session.commit()
