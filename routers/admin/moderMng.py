from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from middlewares.admin import CheckModerAccessMiddleware
from config import settings
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.exc import IntegrityError

from models import Level, ModerModel
from database import db_session

from .keyboards import moderlist, edit_moder, change_role

router = Router()
router.message.outer_middleware(CheckModerAccessMiddleware(Level.admin))

moder_rules = {
    Level.junior: {
        "can_delete_messages": True,
        "can_post_messages": True,
        "can_edit_messages": True,
        "can_pin_messages": True,
        "can_manage_topics": True
    },
    Level.middle: {
        "can_delete_messages": True,
        "can_restrict_members": True,
        "can_invite_users": True,
        "can_post_messages": True,
        "can_edit_messages": True,
        "can_pin_messages": True
    },
    Level.senior: {
        "is_anonymous": True,
        "can_manage_chat": True,
        "can_delete_messages": True,
        "can_manage_video_chats": True,
        "can_restrict_members": True,
        "can_promote_members": True,
        "can_change_info": True,
        "can_invite_users": True,
        "can_post_stories": True,
        "can_edit_stories": True,
        "can_delete_stories": True,
        "can_post_messages": True,
        "can_edit_messages": True,
        "can_pin_messages": True,
        "can_manage_topics": True
    }

}

class Navigation(StatesGroup):
    listmoders = State()

class Editmoder(StatesGroup):
    select = State()
    edit_name = State()
    change_level = State()

class NewAdmin(StatesGroup):
    name = State()
    tg_id = State()

async def display_moder_info(message: Message, state: FSMContext, moder: ModerModel):
    info = f"Информация по модератору\nTelegram ID: {moder.tg_id}\nЗаписан как: {moder.name if moder.name else ''}\nУровень: {moder.level}\nСнят: {'Нет' if moder.active else 'Да'}\nДата назначения: {moder.created_at.strftime('%d.%m.%Y %H:%M:%S')}\nПоследние изменения: {moder.updated_at.strftime('%d.%m.%Y %H:%M:%S')}"
    await state.set_state(Editmoder.select)
    await state.update_data(moder=moder)
    await message.edit_text(info, reply_markup=edit_moder(moder))

@router.message(Command("moders"))
async def moders_cmd(message: Message, state: FSMContext):
    async with db_session() as session:
        result = await session.execute(select(ModerModel).filter(ModerModel.tg_id != message.from_user.id))
        moders = result.scalars().all()
        await state.clear()
        await state.set_state(Navigation.listmoders)
        await message.reply("Список модераторов:", reply_markup=moderlist(moders))

@router.callback_query(Navigation.listmoders)
async def moders_list_cb(callback: CallbackQuery, moder_caller: ModerModel, state: FSMContext):
    action, payload = callback.data.split(":")
    if action == "add":
        await callback.answer()
        await callback.message.edit_text("Укажите ID или username пользователя")
        await state.set_state(NewAdmin.tg_id)
    elif action == "view":
        await callback.message.edit_text("Загружаю информацию...")
        async with db_session() as session:
            result = await session.execute(select(ModerModel).filter(ModerModel.id == int(payload)))
            moder = result.scalar_one_or_none()
            if not moder:
                return await callback.answer("Не удалось найти модера")
            if moder.level.value > moder_caller.level.value:
                await callback.answer()
                await display_moder_info(callback.message, state, moder)
            else:
                await callback.answer("Недостаточно прав")

@router.callback_query(Editmoder.select)
async def edit_moder_cb(callback: CallbackQuery, moder_caller: ModerModel, state: FSMContext):
    data = await state.get_data()
    хуйня, action = callback.data.split(":")
    moder: ModerModel = data['moder']
    print(moder_caller, moder)
    match action:
        case "role":
            roles_list = list(moder_rules.keys())
            roles_list.remove(moder.level)
            await state.set_state(Editmoder.change_level)
            await callback.message.edit_reply_markup(reply_markup=change_role(roles_list))
        case "demote":
            if moder_caller.level.value >= Level.senior.value:
                async with db_session() as session:
                    moder.active = False
                    session.add(moder)
                    await session.commit()
                    await callback.answer("Успешно")
                await display_moder_info(callback.message, state, moder)
            else:
                await callback.answer("Недостаточно прав")
        case "promote":
            if moder_caller.level.value >= Level.senior.value:
                async with db_session() as session:
                    moder.active = True
                    session.add(moder)
                    await session.commit()
                    await callback.answer("Успешно")
                await display_moder_info(callback.message, state, moder)
            else:
                await callback.answer("Недостаточно прав")
        case _:
            await callback.message.reply("Функция не готова")

@router.callback_query(Editmoder.change_level)
async def edit_moder_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Ожидайте...")
    хуйня, newrole = callback.data.split(":")
    roles_list = list(moder_rules.keys())
    data = await state.get_data()
    moder: ModerModel = data['moder']
    for role in roles_list:
        if str(role) == newrole:
            async with db_session() as session:
                moder.level = role
                try:
                    session.add(moder)
                    session.commit()
                    await callback.bot.promote_chat_member(settings.TG_CHAT_ID, moder.tg_id, **moder_rules[role])
                    await state.clear()
                    await state.set_state(Navigation.listmoders)
                    await callback.answer("Успешно")
                    await display_moder_info(callback.message, state, moder)
                except Exception:
                    await callback.message.edit_text("Возникла ошибка.")
            break
    

@router.message(NewAdmin.tg_id)
async def name_input(message: Message, state: FSMContext):
    if message.text == '/cancel':
        await state.clear()
        await message.reply("Отменено.")
        return
    try:
        r = await message.bot.get_chat_member(settings.TG_CHAT_ID, message.text)
        if r.status == 'left':
            return await message.reply("Пользователь с указанным ID вышел из чата")
    except TelegramBadRequest:
        return await message.reply("Пользователь с указанным ID никогда не состоял в чате")

    async with db_session() as session:
        result = await session.execute(select(ModerModel).filter(ModerModel.tg_id == int(message.text)))
        moder = result.scalar_one_or_none()
        if moder:
            await message.reply("Пользователь с указанным ID ранее был модератором. Используйте функционал восстановления")
    
    await state.update_data(tg_id=message.text)
    await state.set_state(NewAdmin.name)
    await message.reply("Укажите ник или заметку по модератору для идентификации")
    
@router.message(NewAdmin.name)
async def name_input(message: Message, state: FSMContext):
    if message.text == '/cancel':
        await state.clear()
        await message.reply("Отменено.")
        return
    msg = await message.reply("Ожидайте...")
    data = await state.get_data()
    tg_id = int(data['tg_id'])
    async with db_session() as session:
        new = ModerModel(tg_id=tg_id, name=message.text)
        session.add(new)
        try:
            await session.commit()
            await message.bot.promote_chat_member(settings.TG_CHAT_ID, tg_id, **moder_rules[Level.junior])
        except IntegrityError:
            return await msg.edit_text("Пользователь с таким ID уже присутствует в базе")
    await msg.edit_text("Модератор успешно добавлен. Уровнь: Level.junior")

    
