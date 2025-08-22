from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
 
from models import TagSettingsModel, BanlistModel, BanAction

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

def banlog_actions(records: list[BanlistModel], is_first=False, is_last=False) -> InlineKeyboardMarkup:
    btns = []
    for record in records:
        action = ""
        match record.action:
            case BanAction.ban:
                action = "заблокирован"
            case BanAction.mute:
                action = "замьючен"
            case BanAction.tempban:
                action = "временно заблокирован"
        btns.append([
            InlineKeyboardButton(text=f"{record.user_id} {action} [{record.created_at}]", callback_data=f"{record.id}")
        ])
    
    next_prev = []
    if not is_first:
        next_prev.append(InlineKeyboardButton(text="<< Назад", callback_data=f"prev"))
    if not is_last:
        next_prev.append(InlineKeyboardButton(text="Далее >>", callback_data=f"next"))
    if len(next_prev) > 0:
        btns.append(next_prev)

    btns.append([InlineKeyboardButton(text="Закрыть", callback_data=f"cancel")])

    return InlineKeyboardMarkup(inline_keyboard=btns)

def banlog_view():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]])