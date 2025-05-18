from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models import ModerModel, Level

def _get_moder_emoji(moder: ModerModel):
    if not moder.active:
        return "🔴"
    match moder.level:
        case Level.junior:
            return "🟢"
        case Level.middle:
            return "🟡"
        case Level.senior:
            return "🟣"
        case Level.admin:
            return "⚪"

def moderlist(moders: list[ModerModel]):
    buttons = []
    for moder in moders:
        buttons.append([InlineKeyboardButton(text=f"{_get_moder_emoji(moder)} {moder.name if moder.name else moder.tg_id}", callback_data=f"view:{moder.id}")])
    
    buttons.append([InlineKeyboardButton(text="📌 Добавить", callback_data="add:")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def edit_moder(moder: ModerModel):
    prom_dem = InlineKeyboardButton(text="❌ Снять с поста", callback_data="act:demote") if moder.active else InlineKeyboardButton(text="✅ Вернуть на пост", callback_data="act:promote")
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔧 Изменить роль", callback_data="act:role")],
        [InlineKeyboardButton(text="✏️ Изменить ник", callback_data="act:nick")],
        [prom_dem],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="act:back")]
    ])

def change_role(roles: dict):
    btns = []
    for role in roles:
        btns.append([InlineKeyboardButton(text=role, callback_data=f"role:{role}")])
    btns.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="role:back")])
    return InlineKeyboardMarkup(inline_keyboard=btns)