from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base, created_at_f, updated_at_f, tg_id_f
import enum
from .Moder import ModerModel

class BanAction(enum.Enum):
    ban = "ban"
    mute = "mute"
    tempban = "tempban"

class BanlistModel(Base):

    __tablename__ = "banlist"

    id: Mapped[int] = mapped_column(primary_key=True)
    moder_id: Mapped[tg_id_f] = mapped_column(ForeignKey("moders.tg_id"))
    action: Mapped[BanAction] = mapped_column(default=BanAction.ban)
    user_id: Mapped[tg_id_f]
    term: Mapped[str]
    created_at: Mapped[created_at_f]
    updated_at: Mapped[updated_at_f]

    moder: Mapped["ModerModel"] = relationship("ModerModel", lazy="select")