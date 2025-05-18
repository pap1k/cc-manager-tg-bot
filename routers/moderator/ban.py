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
router.message.middleware(CheckModerAccessMiddleware(Level.middle))
router.message_reaction.middleware(CheckModerAccessMiddleware(Level.middle))
router.callback_query.middleware(CheckModerAccessMiddleware(Level.middle))

class BanStage(StatesGroup):
    author_id = State()
    punish_select = State()
    term = State()
    reason = State()

class CustomState:
    def __init__(self, step: State = None, data: dict = {}):
        self.step = step
        self.data = data
    
    def update_data(self, **new_data):
        for k in new_data:
            self.data[k] = new_data[k]

custom_states : dict[int, CustomState] = {} #id: CustomState

@router.message_reaction(F.chat.id == settings.TG_CHAT_ID, F.new_reaction[0].emoji == "🖕")
async def handle_reaction(event: MessageReactionUpdated, state: FSMContext):
    """Пересылает сообщение, пытается определить автора. Если автор определен, сообщение удаляется. Если не опреден, то запрашивается ID автора и удаляется позже"""
    fwd_msg = await event.bot.forward_message(event.user.id, settings.TG_CHAT_ID, event.message_id)
    
    custom_states[event.user.id] = CustomState()
    my_state = custom_states[event.user.id]
    is_hidden = fwd_msg.forward_origin.type == "hidden_user"
    my_state.update_data(message_id=event.message_id)

    if not is_hidden:
        my_state.update_data(ban_user=fwd_msg.forward_origin.sender_user.id)
        my_state.step = BanStage.punish_select
        await event.bot.send_message(event.user.id, f"Выберите наказание для пользователя <code>{fwd_msg.forward_origin.sender_user.first_name} {fwd_msg.forward_origin.sender_user.last_name}</code>", parse_mode="HTML", reply_markup=punishment_list())
        await event.bot.delete_message(settings.TG_CHAT_ID, event.message_id)
    else:
        # await state.set_state(BanStage.author_id)
        my_state.step = BanStage.author_id
        await event.bot.send_message(event.user.id, f"Автор сообщения скрыл свой профиль. Укажите его ID:")


@router.message()
async def input_id(message: Message, state: FSMContext):
    if(message.from_user.id not in custom_states):
        return
    my_state = custom_states[message.from_user.id]
    if my_state.step != BanStage.author_id:
        return
    if message.text == '/cancel':
        del custom_states[message.from_user.id]
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
    
    await message.bot.delete_message(settings.TG_CHAT_ID, my_state.data['message_id'])
    
    my_state.update_data(ban_user=member.user.id)
    my_state.step = BanStage.punish_select
    await message.reply(f"Выберите наказание для пользователя <code>{member.user.full_name}</code>", parse_mode="HTML", reply_markup=punishment_list())

@router.callback_query()
async def apply_punish(callback: CallbackQuery, state: FSMContext):
    if(callback.from_user.id not in custom_states):
        return
    my_state = custom_states[callback.from_user.id]
    if my_state.step != BanStage.punish_select:
        return
    await callback.answer()
    if callback.data == "kick":
        ...
    elif callback.data == "ban":
        ...
    elif callback.data == "mute":
        ...
    elif callback.data == "warn":
        ...
    elif callback.data == "cancel":
        del custom_states[callback.from_user.id]
        await callback.message.edit_text("Отменено")
    else:
        logging.warning(f"Не получилось определить тип наказания. Data: {callback.data}; User: {callback.from_user.id}")        

