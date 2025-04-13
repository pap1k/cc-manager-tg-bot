from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from middlewares.admin import CheckAdminAccessMiddleware
from config import settings
import aiohttp
from sqlalchemy.exc import IntegrityError

from database import db_session
from models import ModerModel, Level

router = Router()
router.message.outer_middleware(CheckAdminAccessMiddleware())

@router.message(Command("test"))
async def test(message: Message):
    async with db_session() as session:
        moder = ModerModel(tg_id=message.from_user.id)
        session.add(moder)
        try:
            await session.commit()
            await message.reply("ok")
        except IntegrityError:
            await message.reply("Пользователь с таким ID уже присутствует в базе")
        except Exception:
            await message.reply("Произошла ошибка")

@router.message(Command("cat"))
async def cat(message: Message):
    msg = await message.reply("Ищу котика для вас...")
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get("https://aleatori.cat/random.json")
            if response.status == 200:
                data = await response.json()
                if 'url' in data:
                    await message.reply_photo(data['url'])
                    await msg.delete()
                    return
        except Exception:
            await message.edit_text("Произошла ошибка при получении котика :(")
    await msg.edit_text("Не получилось ничего найти :(\nПопробуйте позже")

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