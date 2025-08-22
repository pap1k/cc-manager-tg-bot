from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import settings
from db_services.Moder import ModerService

from models import Level, ModerModel

router = Router()

@router.message(Command("admin"))
async def makeadmin(message: Message):
    print(12)
    if not settings.IS_TEST:
        return await message.reply("Команда не доступна в продакшен режиме")
    moder = ModerModel(tg_id=message.from_user.id, name="TEST_ADMIN", level=Level.admin)
    await ModerService.create(moder)
    await message.bot.promote_chat_member(
                        settings.TG_CHAT_ID,
                        message.from_user.id,
                        is_anonymous= True,
                        can_manage_chat= True,
                        can_delete_messages= True,
                        can_manage_video_chats= True,
                        can_restrict_members= True,
                        can_promote_members= True,
                        can_change_info= True,
                        can_invite_users= True,
                        can_post_stories= True,
                        can_edit_stories= True,
                        can_delete_stories= True,
                        can_post_messages= True,
                        can_edit_messages= True,
                        can_pin_messages= True,
                        can_manage_topics= True
                        )
    await message.reply("Успешно")