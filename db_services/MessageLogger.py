from sqlalchemy import update, select, delete, func
from database import db_session
from models import LogMessagesModel

class LogMessageService:

    def __init__(self):
        pass

    @staticmethod
    async def create(message: LogMessagesModel):
        async with db_session() as session:
            session.add(message)
            await session.commit()

    @staticmethod
    async def delete(message: LogMessagesModel):
         async with db_session() as session:
                await session.execute(delete(message))
                await session.commit()

    @staticmethod
    async def get_all():
        async with db_session() as session:
            result = await session.execute(select(LogMessagesModel))
            return result.scalars().all()
        
    @staticmethod
    async def get_count(key, val):
        async with db_session() as session:
            result = await session.execute(select(func.count(LogMessagesModel.id)).filter(key == val))
            return result.scalar() or 0
        
    @staticmethod
    async def get_one(key, val):
        async with db_session() as session:
            result = await session.execute(select(LogMessagesModel).filter(key == val))
            return result.scalar_one_or_none()