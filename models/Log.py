from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base, created_at_f, updated_at_f
import enum

class Action(enum.Enum):
    kick = "kick"
    ban = "ban"
    post = "post"
    mute = "mute"
    del_post = "del_post"
    edit_post = "edit_post"
    add_admin = "add_admin"
    del_admin = "del_admin"
    call_cmd = "call_cmd"

class LogModel(Base):

    __tablename__ = "log"

    id: Mapped[int] = mapped_column(primary_key=True)
    moder_id: Mapped[int] = mapped_column(ForeignKey("moders.id"))
    action: Mapped[Action]
    payload: Mapped[dict]
    banlist_id: Mapped[int | None] = mapped_column(ForeignKey("banlist.id"))
    created_at: Mapped[created_at_f]
    updated_at: Mapped[updated_at_f]
