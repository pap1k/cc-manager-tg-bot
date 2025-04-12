from sqlalchemy.orm import Mapped, mapped_column
from database import Base, created_at_f, updated_at_f
import enum

class Level(enum.Enum):
    junior=1
    middle=2
    senior=3
    admin=4
    
class ModerModel(Base):

    __tablename__ = "moders"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column()
    level: Mapped[Level] = mapped_column(default=Level.junior)
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[created_at_f]
    updated_at: Mapped[updated_at_f]

