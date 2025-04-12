from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base, created_at_f, updated_at_f

class ChatModel(Base):

    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    dialog_id: Mapped[int] = mapped_column(ForeignKey("dialogs.id"))
    message: Mapped[str]
    moder_id: Mapped[int | None] = mapped_column(ForeignKey("moders.id"))
    user_id: Mapped[int | None]
    created_at: Mapped[created_at_f]
    updated_at: Mapped[updated_at_f]
    
    
