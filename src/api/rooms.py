from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatchRequest, RoomPatch, \
    RoomAddRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms():
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all()


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id,
                                                              hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_rooms(hotel_id: int,
                       room_data: RoomAddRequest = Body(openapi_examples={
                           "1": {
                               "summary": "Сочи",
                               "value": {
                                   "hotel_id": "7",
                                   "title": "2-x местный",
                                   "description": "Отличный отель с расположением у моря",
                                   "price": "5000",
                                   "quantity": "1",
                               }
                           },
                       })):
    async with async_session_maker() as session:
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_hotel(
        room_id: int,
        hotel_id: int,
        room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,
                                            id=room_id,)
        await session.commit()
    return {"status": "OK"}


#
#
@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="<h1>Тут мы частично обновляем данные о номере title</h1>",
)
async def partially_edit_room(
        room_id: int,
        hotel_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data,
                                            exclude_unset=True,
                                            id=room_id,
                                            hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


#
#
@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
        return {"status": "OK"}
