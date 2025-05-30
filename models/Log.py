from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base, created_at_f, updated_at_f
from sqlalchemy.dialects.postgresql import JSON
import enum

class LogAction(enum.Enum):
    kick = "kick"
    ban = "ban"
    post = "post"
    mute = "mute"
    warn = "warn"
    del_post = "del_post"
    edit_post = "edit_post"
    add_admin = "add_admin"
    del_admin = "del_admin"
    call_cmd = "call_cmd"

class LogModel(Base):

    __tablename__ = "log"

    id: Mapped[int] = mapped_column(primary_key=True)
    moder_id: Mapped[int] = mapped_column(ForeignKey("moders.id"))
    action: Mapped[LogAction]
    payload: Mapped[dict] = mapped_column(JSON)
    banlist_id: Mapped[int | None] = mapped_column(ForeignKey("banlist.id"))
    created_at: Mapped[created_at_f]
    updated_at: Mapped[updated_at_f]
