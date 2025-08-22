from sqlalchemy import update, select, delete
from database import db_session
from models import TagSettingsModel

class TagService:

    def __init__(self):
        pass
    
    @staticmethod
    async def update(updatetag: TagSettingsModel, **new_data):
        async with db_session() as session:
            stmt = update(TagSettingsModel).where(TagSettingsModel.id == updatetag.id).values(new_data)
            await session.execute(stmt)
            await session.commit()
            stmt = select(TagSettingsModel).where(TagSettingsModel.id == updatetag.id)
            updated = await session.execute(stmt)
            return updated.scalar_one_or_none()

    @staticmethod
    async def create(tag: TagSettingsModel):
        async with db_session() as session:
            session.add(tag)
            await session.commit()

    @staticmethod
    async def delete(tag: TagSettingsModel):
         async with db_session() as session:
                await session.execute(delete(tag))
                await session.commit()

    @staticmethod
    async def get_all():
        async with db_session() as session:
            result = await session.execute(select(TagSettingsModel))
            return result.scalars().all()
        
    @staticmethod
    async def get_one(key, val):
        async with db_session() as session:
            result = await session.execute(select(TagSettingsModel).filter(key == val))
            return result.scalar_one_or_none()