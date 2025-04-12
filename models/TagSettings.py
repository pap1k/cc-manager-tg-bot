from sqlalchemy.orm import Mapped, mapped_column
from database import Base, created_at_f, updated_at_f

class TagSettingsModel(Base):

    __tablename__ = "tag_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str]
    channel: Mapped[str]
    created_at: Mapped[created_at_f]
    updated_at: Mapped[updated_at_f]
