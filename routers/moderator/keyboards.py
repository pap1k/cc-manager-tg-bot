from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import TagSettingsModel

def punishment_list() -> InlineKeyboardMarkup:
    punish = {
        # "kick": "Кик",
        "ban": "Пермач",
        "tempban": "Временный бан",
        "mute": "Временный мут",
        # "warn": "Предупредить",
        # "cancel": "< Отменить"
    }
    keyboard = []
    for key in punish:
        keyboard.append([
            InlineKeyboardButton(text=punish[key], callback_data=key)
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def punish_term_select() -> InlineKeyboardMarkup:
    terms = {
        "1h": "1 час",
        "24h": "24 часа",
        "7d": "1 неделя",
        "1m": "1 месяц (30 дней)",
        "cancel": "Отменить"
    }
    kb = []
    for key in terms:
        kb.append([
            InlineKeyboardButton(text=terms[key], callback_data=key)
        ])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def tag_settings(settings: list[TagSettingsModel]) -> InlineKeyboardMarkup:
    btns = []
    for setting in settings:
        btns.append([
            InlineKeyboardButton(text=f"{setting.tag} ---> {setting.channel}", callback_data=f"{setting.id}")
        ])
    btns.append([InlineKeyboardButton(text=f"Добавить", callback_data="add")])
    return InlineKeyboardMarkup(inline_keyboard=btns)

def tag_edit() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редактировать тег", callback_data="edit_tag")],
        [InlineKeyboardButton(text="🔧 Изменить канал", callback_data="edit_thread")],
        [InlineKeyboardButton(text="❌ Удалить", callback_data="delete")],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
    ])