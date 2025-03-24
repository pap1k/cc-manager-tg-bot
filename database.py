from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import URL, create_engine, text
import asyncio
from config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
    # pool_size=5
)

async def test():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT 1,2,3"))
        print(f"{res.all()=}")

# asyncio.run(test())