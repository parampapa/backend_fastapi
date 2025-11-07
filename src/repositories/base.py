from sqlalchemy import select, func

from src.database import async_session_maker
from src.models.hotels import HotelsOrm


class BaseRepositories:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one(self, hotel_id):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().first()
