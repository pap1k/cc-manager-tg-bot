from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from middlewares.admin import CheckModerAccessMiddleware
from config import settings
import aiohttp
from sqlalchemy.exc import IntegrityError

from database import db_session
from models import ModerModel, Level

from db_services.Moder import ModerService
from .rules import moder_rules

router = Router()
router.message.middleware(CheckModerAccessMiddleware())

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
async def anon(message: Message, moder_caller: ModerModel):
    r = await message.bot.get_chat_member(settings.TG_CHAT_ID, message.from_user.id)
    if r.status != 'administrator':
        await message.reply("Вы не администратор")
        return
    if r.is_anonymous == True:
        await message.bot.promote_chat_member(
                        settings.TG_CHAT_ID,
                        message.from_user.id,
                        is_anonymous=False,
                        **moder_rules[moder_caller.level])
        await message.reply("🔴Анонимка выключена")
    elif r.is_anonymous == False:
        await message.bot.promote_chat_member(
                        settings.TG_CHAT_ID,  
                        message.from_user.id,
                        is_anonymous= True,
                        **moder_rules[moder_caller.level])
        await message.reply("🟢Анонимка включена")
    else:
        await message.reply("Не удалось определить статус анонимки")
