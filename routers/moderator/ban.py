import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, MessageReactionUpdated, CallbackQuery
from aiogram.enums import ChatType
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from middlewares.admin import CheckModerAccessMiddleware
from config import settings
from sqlalchemy.exc import IntegrityError

from .keyboards import punishment_list

from database import db_session
from models import ModerModel, Level

router = Router()
router.message.outer_middleware(CheckModerAccessMiddleware(Level.middle))

class BanStage(StatesGroup):
    author_id = State()
    punish_select = State()
    term = State()
    reason = State()

@router.message_reaction(F.chat.id == settings.TG_CHAT_ID, F.new_reaction.contains("🖕"))
async def handle_reaction(event: MessageReactionUpdated, state: FSMContext):
    """Пересылает сообщение, пытается определить автора. Если автор определен, сообщение удаляется. Если не опреден, то запрашивается ID автора и удаляется позже"""
    fwd_msg = await event.bot.forward_message(event.user.id, settings.TG_CHAT_ID, event.message_id)
    author = fwd_msg.forward_from.full_name if fwd_msg.forward_from else "Скрыт пользователем"

    if author:
        await state.update_data(ban_user=fwd_msg.forward_from.id, message_id=event.message_id)
        await event.bot.send_message(event.user.id, f"Выберите наказание для пользователя <code>{author}</code>", parse_mode="HTML", reply_markup=punishment_list())
        await state.set_state(BanStage.punish_select)
        # await event.bot.delete_message(settings.TG_CHAT_ID, event.message_id)
    else:
        await state.set_state(BanStage.author_id)
        await event.bot.send_message(event.user.id, f"Автор сообщения скрыл свой профиль. Укажите его ID:")


@router.message(BanStage.author_id)
async def input_id(message: Message, state: FSMContext):
    if message.text == '/cancel':
        await state.clear()
        await message.reply("Отменено.")
        return
    author_id = message.text
    if not author_id.isdigit():
        await message.reply("ID должен состояить из цифр")
        return
    member = await message.bot.get_chat_member(settings.TG_CHAT_ID, int(author_id))
    if not member:
        await message.reply("Пользователь с указанным ID не найден в группе. Проверьте ID на корректность.")
        return
    
    await state.update_data(ban_id=member.user.id)
    await state.set_state(BanStage.punish_select)
    await message.reply(f"Выберите наказание для пользователя <code>{member.user.full_name}</code>", parse_mode="HTML", reply_markup=punishment_list())

@router.callback_query(BanStage.punish_select)
async def apply_punish(callback: CallbackQuery, state: FSMContext):
    if callback.data == "kick":
        ...
    elif callback.data == "ban":
        ...
    elif callback.data == "mute":
        ...
    elif callback.data == "warn":
        ...
    else:
        logging.warn(f"Не получилось определить тип наказания. Data: {callback.data}; User: {callback.from_user.id}")        

