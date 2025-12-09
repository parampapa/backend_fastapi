from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="локация"),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.post("",
             summary="Добавление отеля",)
async def create_hotel(db: DBDep,
                       hotel_data: HotelAdd = Body(openapi_examples={
                           "1": {
                               "summary": "Сочи",
                               "value": {
                                   "title": "Отель Сочи 5 звезд у моря",
                                   "location": "ул. Моря, 1",
                               }
                           },
                           "2": {
                               "summary": "Дубай",
                               "value": {
                                   "title": "Отель Дубай У фонтана",
                                   "location": "ул. Шейха, 2",
                               }
                           }
                       })):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return hotel


@router.put("/{hotel_id}",
            summary="полное обновление данных об отеле",
            description="<h1 class=color:red>Тут полностью обновляем данные об отеле</h1>",
            )
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep,
):
    hotel = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return hotel


@router.patch(
    "/{hotel_id}",
    summary="### 🔧 Частичное обновление отеля",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep
):
    hotel = await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return hotel


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    hotel = await db.hotels.delete(id=hotel_id)
    db.commit()
    return {"status": "ok"}
