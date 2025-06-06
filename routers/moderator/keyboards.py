from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import TagSettingsModel

def punishment_list() -> InlineKeyboardMarkup:
    punish = {
        "kick": "Кик",
        "ban": "Бан",
        "mute": "Мут",
        "warn": "Предупредить",
        "cancel": "< Отменить"
    }
    keyboard = []
    for key in punish:
        keyboard.append([
            InlineKeyboardButton(text=punish[key], callback_data=key)
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

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