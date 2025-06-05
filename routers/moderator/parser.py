import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, MessageReactionUpdated, CallbackQuery
from aiogram.enums import ChatType
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from middlewares.admin import CheckModerAccessMiddleware

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from config import settings

from .keyboards import tag_settings, tag_edit

from database import db_session
from models import ModerModel, Level, TagSettingsModel

router = Router()
router.message.middleware(CheckModerAccessMiddleware(Level.senior))
router.message_reaction.middleware(CheckModerAccessMiddleware(Level.senior))
router.callback_query.middleware(CheckModerAccessMiddleware(Level.senior))


class Navigation(StatesGroup):
    tag_select = State()
    tag_add_name = State()
    tag_add_id = State()
    tag_edit = State()

@router.message(Command("parser"))
async def parser_cmd(message: Message, state: FSMContext, moder_caller: ModerModel):
    async with db_session() as session:
        result = await session.execute(select(TagSettingsModel))
        current_tag_settings = result.scalars().all()
        
    await state.set_state(Navigation.tag_select)
    await message.reply("Текущие настройки парсера:", reply_markup=tag_settings(current_tag_settings))

@router.callback_query(Navigation.tag_select)
async def tag_select_cb(callback: CallbackQuery, state: FSMContext, moder_caller: ModerModel):
    match callback.data:
        case "add":
            await callback.answer()
            await state.set_state(Navigation.tag_add_name)
            await callback.message.edit_text("Введите тег <b>БЕЗ</b> <code>#</code>:", parse_mode="HTML")
        case _:
            async with db_session() as session:
                result = await session.execute(select(TagSettingsModel).filter(TagSettingsModel.id == int(callback.data)))
                tag = result.scalar_one_or_none()
                if not tag:
                    return await callback.answer("Произошла ошибка поиска настройки для выбранного тега")
                await callback.answer()
                await state.update_data(view_tag=tag)
                await state.set_state(Navigation.tag_edit)
                await callback.message.edit_text(f"Посты с тегом <code>#{tag.tag}</code> публикуются в канал <code>{tag.channel}</code>", parse_mode="HTML", reply_markup=tag_edit())
                    
        


@router.message(Navigation.tag_add_name)
async def tag_add_name_msg(message: Message, state: FSMContext):
    await message.delete()

    result_tag = "#"+message.text
    if message.text.startswith("#"):
        await message.bot.send_message(message.chat.id, "Обратите внимание, что вы ввели тег с <code>#</code>! Редактирование доступно из списка настроек", parse_mode="HTML")

    await state.update_data(tag=result_tag)
    await state.set_state(Navigation.tag_add_id)

    await message.bot.send_message(message.chat.id, f"Тег сохранен. Парсер будет искать тег равный <code>{result_tag}</code>.\nТеперь введите thread_id, куда будут выкладываться сообщения.\n\nУзнать ID топика можно скопировав ссылку на сообщение. Формат ссылки такой:<pre>https://t.me/c/ID_КАНАЛА/ID_ТОПИКА/ID_СООБЩЕНИЯ</pre>", parse_mode="HTML")
    
@router.message(Navigation.tag_add_id)
async def tag_add_id_msg(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("ID должен был числом!")
    await message.delete()
    data = await state.get_data()
    new_tag = TagSettingsModel(tag=data.get("tag"), channel=message.text)

    async with db_session() as session:
        session.add(new_tag)
        try:
            await session.commit()
        except IntegrityError:
            await state.clear()
            return await message.bot.send_message(message.chat.id, "Произошла ошибка сохранения информации в БД. Скорее всего, настройка для такого тега уже существует. Используйте функционал редактирования.")

    await message.bot.send_message(message.chat.id, "Настройка успешно сохранена")


