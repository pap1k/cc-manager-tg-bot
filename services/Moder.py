from sqlalchemy import update, select
from database import db_session
from models import ModerModel

class ModerService:

    def __init__(self):
        pass
    
    @staticmethod
    async def update(moder: ModerModel, **new_data):
        async with db_session() as session:
            stmt = update(ModerModel).where(ModerModel.tg_id == moder.tg_id).values(new_data)
            await session.execute(stmt)
            await session.commit()
            stmt = select(ModerModel).where(ModerModel.tg_id == moder.tg_id)
            updated = await session.execute(stmt)
            return updated.scalar_one_or_none()

    @staticmethod
    async def create(moder: ModerModel):
        async with db_session() as session:
            session.add(moder)
            await session.commit()