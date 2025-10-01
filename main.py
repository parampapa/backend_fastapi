import uvicorn
from fastapi import FastAPI, Query, Body, requests

app = FastAPI()


hotels = [{"id": 1, "title": "Sochi"},
          {"id": 2, "title": "Dubai"}]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None),
        title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotels(
        title: str = Body(None, description="Название отеля")
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1 if hotels else 1,
        "title": title,
    })
    return {"Status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"Status": "OK"}


@app.put("/hotels/{hotel_id}")
def put_hotel(
        hotel_id: int,
        title: str = Body(embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] == title
            return {"status": "Created", "hotel": hotel}

    new_hotel = {"id": hotel_id, "title": title}
    hotels.append(new_hotel)
    return {"status": "CREATED", "hotel": new_hotel}


@app.patch("?hotels/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None, embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] == title
            return {"status": "OK", "hotel": hotel}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)




