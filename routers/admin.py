from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from middlewares.admin import CheckAdminAccessMiddleware
from config import settings

router = Router()
router.message.outer_middleware(CheckAdminAccessMiddleware())


@router.message(Command("anon"))
async def anon(message: Message):
    r = await message.bot.get_chat_member(settings.TG_CHAT_ID, message.from_user.id)
    if r.status != 'administrator':
        await message.reply("Вы не администратор")
        return
    if r.is_anonymous == True:
        print("disable")
        await message.bot.promote_chat_member(
                        settings.TG_CHAT_ID,
                        message.from_user.id,
                        is_anonymous=False,
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
                        can_manage_topics= True)
        await message.reply("🔴Анонимка выключена")
    elif r.is_anonymous == False:
        print("enable")
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
                        can_manage_topics= True)
        await message.reply("🟢Анонимка включена")
    else:
        await message.reply("Не удалось определить статус анонимки")

@router.message(Command("admin"))
async def makeadmin(message: Message):
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