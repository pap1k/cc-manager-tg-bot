from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base, created_at_f, updated_at_f

class DialogModel(Base):

    __tablename__ = "dialogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    moder_id: Mapped[int | None] = mapped_column(ForeignKey("moders.id"))
    created_at: Mapped[created_at_f]
    updated_at: Mapped[updated_at_f]