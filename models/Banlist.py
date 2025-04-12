from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base

class BanlistModel(Base):

    __tablename__ = "banlist"

    id: Mapped[int] = mapped_column(primary_key=True)
    moder_id: Mapped[int] = mapped_column(ForeignKey("moders.id"))
    user_id: Mapped[int]
    term: Mapped[int]
