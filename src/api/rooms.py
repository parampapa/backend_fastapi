from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatchRequest, RoomPatch, \
    RoomAddRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int,
                    db: DBDep,
                    date_from: date = Query(example="2026-01-01"),
                    date_to: date = Query(example="2026-01-10"),
                 ):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms")
async def create_rooms(hotel_id: int,
                       db: DBDep,
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(), )
    await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_hotel(
        room_id: int,
        hotel_id: int,
        room_data: RoomAddRequest,
        db: DBDep
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
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
        db: DBDep
):
    _room_data = RoomPatch(hotel_id=hotel_id,
                           **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id)
    await db.commit()
    return {"status": "OK"}


#
#
@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}
