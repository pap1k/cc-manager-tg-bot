from sqlalchemy import update, select, text, func
from sqlalchemy.orm import selectinload
from database import db_session
from models import BanlistModel, LogModel, LogAction, BanAction

class BanlistService:
    
    @staticmethod
    async def _create_records(logmodel: LogModel, banmodel: BanlistModel = None):
        async with db_session() as session:
            async with session.begin():
                if banmodel:
                    session.add(banmodel)
                    await session.flush()
                    logmodel.banlist_id = banmodel.id

                session.add(logmodel)
                await session.commit()

    @staticmethod
    async def ban(moder_id: int, user_id: int, term: int = 7, reason: str = ""):
        logmodel = LogModel(
            moder_id=moder_id,
            action=LogAction.banlist, 
            payload={"term": term, "reason": reason, "user_id": user_id},
        )
        banmodel = BanlistModel(moder_id=moder_id, user_id=user_id, term=term, action=BanAction.ban)
        await BanlistService._create_records(logmodel, banmodel)

    @staticmethod
    async def tempban(moder_id: int, user_id: int, term: int = 7, reason: str = ""):
        logmodel = LogModel(
            moder_id=moder_id,
            action=LogAction.banlist, 
            payload={"term": term, "reason": reason, "user_id": user_id},
        )
        banmodel = BanlistModel(moder_id=moder_id, user_id=user_id, term=term, action=BanAction.tempban)
        await BanlistService._create_records(logmodel, banmodel)

    @staticmethod
    async def mute(moder_id: int, user_id: int, term: int = 7, reason: str = ""):
        logmodel = LogModel(
            moder_id=moder_id,
            action=LogAction.banlist, 
            payload={"term": term, "reason": reason, "user_id": user_id},
        )
        banmodel = BanlistModel(moder_id=moder_id, user_id=user_id, term=term, action=BanAction.mute)
        await BanlistService._create_records(logmodel, banmodel)

    @staticmethod
    async def kick(moder_id: int, user_id: int, reason: str = ""):
        logmodel = LogModel(
            moder_id=moder_id,
            action=LogAction.banlist, 
            payload={"reason": reason, "user_id": user_id},
        )
        await BanlistService._create_records(logmodel)

    @staticmethod
    async def warn(moder_id: int, user_id: int, reason: str = ""):
        logmodel = LogModel(
            moder_id=moder_id,
            action=LogAction.banlist, 
            payload={"reason": reason, "user_id": user_id},
        )
        await BanlistService._create_records(logmodel)

    @staticmethod
    async def get_count():
        async with db_session() as session:
            query = select(func.count(BanlistModel.id))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def get_all(offset = 0, limit = 10):
        async with db_session() as session:
            query = (
                select(BanlistModel)
                .order_by(BanlistModel.id.desc())
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            return result.scalars().all()
        
    @staticmethod
    async def get_one(id: int):
        async with db_session() as session:
            query = (
                select(BanlistModel)
                .options(selectinload(BanlistModel.moder))
                .where(BanlistModel.id == id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()