from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import BigInteger
import datetime
from config import settings
from typing import Annotated

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
    # pool_size=5
)

created_at_f = Annotated[datetime.datetime, mapped_column(server_default=text("now()"))]
updated_at_f = Annotated[datetime.datetime, mapped_column(server_default=text("now()"), onupdate=datetime.datetime.now)]
tg_id_f_unique = Annotated[int, mapped_column(BigInteger, unique=True)]
tg_id_f = Annotated[int, mapped_column(BigInteger)]

db_session = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass