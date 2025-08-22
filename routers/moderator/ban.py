import logging, time, datetime

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router
from aiogram.types import Message, MessageReactionUpdated, CallbackQuery, ChatPermissions
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from middlewares.admin import CheckModerAccessMiddleware
from config import settings

from .keyboards import punishment_list, punish_term_select

from models import Level
from db_services.Banlist import BanlistService

router = Router()
router.message.middleware(CheckModerAccessMiddleware(Level.middle))
router.message_reaction.middleware(CheckModerAccessMiddleware(Level.middle))
router.callback_query.middleware(CheckModerAccessMiddleware(Level.middle))

mute_permissions = ChatPermissions(
    can_send_messages=False,
    can_send_photos=False,
    can_send_audios=False,
    can_send_documents=False,
    can_send_other_messages=False,
    can_send_polls=False,
    can_send_video_notes=False,
    can_send_videos=False,
    can_send_voice_notes=False
    )

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

def user_in_custom_states(message: Message | CallbackQuery):
    return message.from_user.id in custom_states

def user_on_correct_step(need_step: State):
    return lambda message: user_in_custom_states(message) and need_step == custom_states[message.from_user.id].step

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
        try:
            await event.bot.delete_message(settings.TG_CHAT_ID, event.message_id)
        except TelegramBadRequest:
            await event.bot.send_message(event.user.id, "Сообщение не может быть удалено")
    else:
        # await state.set_state(BanStage.author_id)
        my_state.step = BanStage.author_id
        await event.bot.send_message(event.user.id, f"Автор сообщения скрыл свой профиль. Укажите его ID:")


@router.message(F.func(user_in_custom_states) and F.func(user_on_correct_step(BanStage.author_id)))
async def input_id(message: Message):
    my_state = custom_states[message.from_user.id]
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
    
    try:
        await message.bot.delete_message(settings.TG_CHAT_ID, my_state.data['message_id'])
    except TelegramBadRequest:
        await message.bot.send_message(message.from_user.id, "Сообщение не может быть удалено")
    
    
    my_state.update_data(ban_user=member.user.id)
    my_state.step = BanStage.punish_select
    await message.reply(f"Выберите наказание для пользователя <code>{member.user.full_name}</code>", parse_mode="HTML", reply_markup=punishment_list())

@router.callback_query(F.func(user_in_custom_states) and F.func(user_on_correct_step(BanStage.punish_select)))
async def apply_punish(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    my_state = custom_states[callback.from_user.id]
    if callback.data == "kick":
        ...
    elif callback.data == "ban":
        await callback.bot.ban_chat_member(settings.TG_CHAT_ID, my_state.data['ban_user'], revoke_messages=True)
        del custom_states[callback.from_user.id]
        await BanlistService.ban(callback.from_user.id, my_state.data['ban_user'], f"[AUTO] Реакцией на сообщение {my_state.data['message_id']}")
        await callback.message.edit_text("Наказание выдано")
    elif callback.data == "tempban":
        my_state.step = BanStage.term
        my_state.update_data(action="tempban")
        await callback.message.edit_text("Выерите срок наказания:", reply_markup=punish_term_select())
    elif callback.data == "mute":
        my_state.step = BanStage.term
        my_state.update_data(action="mute")
        await callback.message.edit_text("Выерите срок наказания:", reply_markup=punish_term_select())
    elif callback.data == "warn":
        ...
    elif callback.data == "cancel":
        del custom_states[callback.from_user.id]
        await callback.message.edit_text("Отменено")
    else:
        logging.warning(f"Не получилось определить тип наказания. Data: {callback.data}; User: {callback.from_user.id}")

@router.callback_query(F.func(user_in_custom_states) and F.func(user_on_correct_step(BanStage.term)))
async def term_select(callback: CallbackQuery, state: FSMContext):
    my_state = custom_states[callback.from_user.id]
    date_plus = 0
    match callback.data:
        case "1h":
            date_plus = 60*60*1
        case "24h":
            date_plus = 60*60*24
        case "7d":
            date_plus = 60*60*25*7
        case "1m":
            date_plus = 60*60*25*30
        case "cancel":
            del custom_states[callback.from_user.id]
            await callback.answer("Отменено")
            await callback.message.edit_text("Наказание отменено")
            return
        case _:
            date_plus = -1
    
    if date_plus == -1:
        await callback.answer("Не удалось определить срок, попробуйте еще раз")
        return await callback.message.edit_text("Выерите срок наказания:", reply_markup=punish_term_select())
    
    await callback.answer()
    ban_term = time.time()+date_plus
    match my_state.data['action']:
        case 'tempban':
            await BanlistService.tempban(callback.from_user.id, my_state.data['ban_user'], callback.data, f"[AUTO] Реакцией на сообщение {my_state.data['message_id']}")
            await callback.bot.ban_chat_member(settings.TG_CHAT_ID, my_state.data['ban_user'], time.time()+date_plus)
        case 'mute':
            await BanlistService.mute(callback.from_user.id, my_state.data['ban_user'], callback.data, f"[AUTO] Реакцией на сообщение {my_state.data['message_id']}")
            await callback.bot.restrict_chat_member(settings.TG_CHAT_ID, my_state.data['ban_user'], mute_permissions, until_date=ban_term)
    del custom_states[callback.from_user.id]
    await callback.message.edit_text("Наказание выдано до "+datetime.datetime.fromtimestamp(ban_term).strftime("%d.%m.%Y в %H:%M"))
    

