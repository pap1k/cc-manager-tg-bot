from aiogram import Router, Bot
from aiogram.types import Message
from aiogram import F
import logging

from config import settings
from services.MessageLogger import LogMessageService
from models import LogMessagesModel

router = Router()
router.message.middleware()

async def check_banwords(bot: Bot, text: str, user_id: int) -> bool:
    logger = logging.getLogger()
    for word in settings.BANWORDS:
        if word in text or word.replace('е', 'ё') in text:
            messages_count = len(await LogMessageService.get_all())
            user = await bot.get_chat_member(settings.TG_CHAT_ID, user_id)
            log_text = f"\nОтправлено подозрительное сообщение\nTEXT={text}\nUSER={user.user.id} ({user.user.full_name})"
            if messages_count > 0:
                await bot.send_message(settings.LOG_CHAT_ID, f"[FILTER]"+log_text+f"\nПользователь НЕ заблокирован, так как ранее от него была активность (всего сообщений: {messages_count})", message_thread_id = 2)
                return False
            else:
                await bot.ban_chat_member(settings.TG_CHAT_ID, user_id, revoke_messages=True)
                await bot.send_message(settings.LOG_CHAT_ID, f"[FILTER]"+log_text+"\nПользователь заблокирован", message_thread_id = 2)
                return False
    return True


@router.message(F.chat.id == settings.TG_CHAT_ID)
async def any_group_message(message: Message):
    if message.message_thread_id == settings.CHAT_THREAD_ID:
        text = message.text if message.text else "<Не текст>"
        if await check_banwords(message.bot, text, message.from_user.id):
            record = LogMessagesModel(user_id=message.from_user.id, message=text, link=message.get_url(include_thread_id=True))
            await LogMessageService.create(record)

