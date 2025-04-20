from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from config import settings

from database import db_session
from models import LogMessage

router = Router()

class BanStage(StatesGroup):
    author_id = State()
    punish_select = State()
    term = State()
    reason = State()

@router.message(F.chat.id == settings.TG_CHAT_ID, F.chat.type == ChatType.SUPERGROUP)
async def any_group_message(message: Message):
    async with db_session() as session:
        record = LogMessage(user_id=message.from_user.id, message=message.text)
        session.add(record)
        await session.commit()
