from sqlalchemy.orm import Mapped, mapped_column, object_session
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey
from database import Base, created_at_f, updated_at_f, tg_id_f
from sqlalchemy.dialects.postgresql import JSON
import enum

from .Moder import ModerModel

class LogAction(enum.Enum):
    banlist = "any_banlist"
    post = "post"
    message = "msg"
    del_post = "del_post"
    edit_post = "edit_post"
    add_admin = "add_admin"
    del_admin = "del_admin"
    call_cmd = "call_cmd"

class LogModel(Base):

    __tablename__ = "log"

    @hybrid_property
    def moder_name(self):
        session = object_session(self)
        if session:
            moder = session.get(ModerModel, self.moder_id)
            return moder.name if moder else None
        return None

    id: Mapped[int] = mapped_column(primary_key=True)
    moder_id: Mapped[tg_id_f] = mapped_column(ForeignKey("moders.tg_id"))
    action: Mapped[LogAction] = mapped_column(default=LogAction.message)
    payload: Mapped[dict] = mapped_column(JSON)
    banlist_id: Mapped[int | None] = mapped_column(ForeignKey("banlist.id"))
    created_at: Mapped[created_at_f]
    updated_at: Mapped[updated_at_f]
