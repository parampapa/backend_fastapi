from datetime import date

from sqlalchemy import select, func

from src.database import engine
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
    ) -> list[Hotel]:
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location)
                                 .contains(location.lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title)
                                 .contains(title.lower()))
        query = (
            query.offset(offset)
            .limit(limit)
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in
                result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location,
            title,
            limit,
            offset
    ) -> list[Hotel]:

        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))

        if location:
            query = query.filter(func.lower(HotelsOrm.location)
                                 .contains(location.lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title)
                                 .contains(title.lower()))
        query = (
            query.offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in
                result.scalars().all()]
