from sqlalchemy import update, select, text
from database import db_session
from models import BanlistModel, LogModel, LogAction

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
            action=LogAction.ban, 
            payload={"term": term, "reason": reason, "user_id": user_id},
            )
        banmodel = BanlistModel(moder_id=moder_id, user_id=user_id, term=term)
        await BanlistService._create_records(logmodel, banmodel)

    @staticmethod
    async def kick(moder_id: int, user_id: int, reason: str = ""):
        logmodel = LogModel(
            moder_id=moder_id,
            action=LogAction.kick, 
            payload={"reason": reason, "user_id": user_id},
            )
        await BanlistService._create_records(logmodel)

    @staticmethod
    async def warn(moder_id: int, user_id: int, reason: str = ""):
        logmodel = LogModel(
            moder_id=moder_id,
            action=LogAction.warn, 
            payload={"reason": reason, "user_id": user_id},
            )
        await BanlistService._create_records(logmodel)

    @staticmethod
    async def get(user_id: int):
        async with db_session() as session:
            query = select(LogModel).where(
                text("payload->>'user_id' = :user_id").bindparams(user_id=str(user_id))
            )
            result = await session.execute(query)
            return result.scalars().all()