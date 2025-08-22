from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from db_services.Banlist import BanlistService
from middlewares.admin import CheckModerAccessMiddleware
from models import Level
from .keyboards import banlog_actions, banlog_view

router = Router()
router.message.middleware(CheckModerAccessMiddleware(Level.middle))
router.callback_query.middleware(CheckModerAccessMiddleware(Level.middle))

class Navigation(StatesGroup):
    view_log_list = State()
    view_current_log = State()

async def show_banlog_page(page=0, *, callback: CallbackQuery = None, message: Message = None):
    offset = page*10
    count = await BanlistService.get_count()
    records = await BanlistService.get_all(offset=offset, limit=10)
    has_next_page = page == 0 and count > 10
    has_prev_page = page > 0
    kb = banlog_actions(records, is_first=not has_prev_page, is_last=not has_next_page)
    if callback:
        await callback.message.edit_text(f"Страница {page+1}", reply_markup=kb)
    else:
        await message.reply("Страница 1", reply_markup=kb)

@router.message(Command("banlog"))
async def _banlog(message: Message, state: FSMContext):
    await state.set_state(Navigation.view_log_list)
    await state.update_data(page=0)
    await show_banlog_page(message=message)

@router.callback_query(Navigation.view_log_list)
async def _view_banlog(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    match callback.data:
        case "cancel":
            await state.clear()
            await callback.message.delete()
            await callback.answer("Отменено")
            return
        case "next":
            await callback.answer()
            new_page = state_data['page']+1
            await state.update_data(page=new_page)
            await show_banlog_page(page=new_page, callback=callback)
            return
        case "prev":
            await callback.answer()
            prev_page = state_data['page']-1
            await state.update_data(page=prev_page)
            await show_banlog_page(page=prev_page, callback=callback)
            return
    
    await callback.answer("Загрузка...")
    log = await BanlistService.get_one(int(callback.data))
    if not log:
        return await callback.message.edit_text("Ошибка. Попробуйте снова или обратитесь ко мне (@almaz_suleymanov2010)")

    log_text = f"Модератор: <code>{log.moder.name}</code>\nПользователь (ID): <code>{log.user_id}</code>\nДата выдачи наказания: <code>{log.created_at}</code>\nСрок: <code>{log.term}</code>"
    log_text += "\n\n<i>В будущем будет возможность снять/продлить бан, пока через управление->разрешения</i>"
    await state.set_state(Navigation.view_current_log)
    await callback.message.edit_text(log_text, parse_mode="HTML", reply_markup=banlog_view())

@router.callback_query(Navigation.view_current_log)
async def _view_current_banlog(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    if callback.data == "back":
        await state.set_state(Navigation.view_log_list)
        await show_banlog_page(state_data['page'], callback=callback)
    else:
        await state.clear()
        await callback.message.edit_text("Ошибка определния кнопки. Обратитесь ко мне (@almaz_suleymanov2010)")