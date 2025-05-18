from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def punishment_list():
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