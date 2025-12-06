from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def add_bookings(user_id: UserIdDep,
                       db: DBDep,
                       booking_data: BookingAddRequest = Body(openapi_examples={
                           "1": {
                               "summary": "пример добавления",
                               "value": {
                                   "room_id": "5",
                                   "data_from": "2025-12-7",
                                   "data_to": "2025-12-10",
                               }
                           },
                       })):

    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(user_id=user_id,
                               price=room_price,
                               **booking_data.model_dump())

    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
