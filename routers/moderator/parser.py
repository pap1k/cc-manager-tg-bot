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
from sqlalchemy import select, delete, update

from db_services.Tag import TagService

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
    tag_edit_tag = State()
    tag_edit_thread = State()

@router.message(Command("parser"))
async def parser_cmd(message: Message, state: FSMContext, moder_caller: ModerModel):
    current_tag_settings = await TagService.get_all()
        
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
            tag = await TagService.get_one(TagSettingsModel.id, int(callback.data))
            if not tag:
                return await callback.answer("Произошла ошибка поиска настройки для выбранного тега")
            await callback.answer()
            await state.update_data(view_tag=tag)
            await state.set_state(Navigation.tag_edit)
            await callback.message.edit_text(f"Посты с тегом <code>#{tag.tag}</code> публикуются в канал <code>{tag.channel}</code>", parse_mode="HTML", reply_markup=tag_edit())
                    
@router.callback_query(Navigation.tag_edit)
async def tag_edit_cb(callback: CallbackQuery, state: FSMContext, moder_caller: ModerModel):
    match callback.data:
        case "edit_tag":
            await callback.answer()
            await state.set_state(Navigation.tag_edit_tag)
            await callback.message.edit_text("Укажите новый тег:")
        case "edit_thread":
            await callback.answer()
            await state.set_state(Navigation.tag_edit_thread)
            await callback.message.edit_text("Укажите новый ID топика (<code>__skip</code> для игнорирования):", parse_mode="HTML")
        case "delete":
            data = await state.get_data()
            await TagService.delete(data.get("view_tag"))
            await callback.answer("Удалено")
        case "cancel":
            await state.clear()
        case _:
            pass


@router.message(Navigation.tag_edit_tag)
async def tag_edit_tag(message: Message, state: FSMContext):
    data = await state.get_data()
    tag = data.get("view_tag")
    await TagService.update(tag, tag=message.text)
    await state.clear()
    await message.answer(f"Тег успешно обновлен на <code>#{message.text}</code>", parse_mode="HTML")

@router.message(Navigation.tag_edit_thread)
async def tag_edit_thread(message: Message, state: FSMContext):
    data = await state.get_data()
    tag = data.get("view_tag")
    await TagService.update(tag, channel=message.text)
    await state.clear()
    await message.answer(f"Топик успешно обновлен на <code>{message.text}</code>", parse_mode="HTML")

@router.message(Navigation.tag_add_name)
async def tag_add_name_msg(message: Message, state: FSMContext):
    await message.delete()

    result_tag = message.text
    if message.text.startswith("#"):
        await message.bot.send_message(message.chat.id, "Обратите внимание, что вы ввели тег с <code>#</code>! Редактирование доступно из списка настроек", parse_mode="HTML")

    await state.update_data(tag=result_tag)
    await state.set_state(Navigation.tag_add_id)

    await message.bot.send_message(message.chat.id, f"Тег сохранен. Парсер будет искать тег равный <code>#{result_tag}</code>.\nТеперь введите thread_id, куда будут выкладываться сообщения (<code>__skip</code> для игнорирования постов и указанным тегом).\n\nУзнать ID топика можно скопировав ссылку на сообщение. Формат ссылки такой:<pre>https://t.me/c/ID_КАНАЛА/ID_ТОПИКА/ID_СООБЩЕНИЯ</pre>", parse_mode="HTML")
    
@router.message(Navigation.tag_add_id)
async def tag_add_id_msg(message: Message, state: FSMContext):
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


