from sqlalchemy.orm import Mapped, mapped_column
from database import Base, created_at_f, updated_at_f, tg_id_f


class LogMessagesModel(Base):

    __tablename__ = "log_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[tg_id_f]
    message: Mapped[str]
    link: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[created_at_f]
    updated_at: Mapped[updated_at_f]