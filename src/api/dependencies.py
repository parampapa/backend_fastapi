from typing import Annotated

from fastapi import Depends, Query, Response, Request, HTTPException
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(3, ge=1, le=100)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(status_code=401,
                            detail="Токен доступа не был предоставлен")
    return access_token


def get_current_user_id(
        token: str = Depends(get_token),
) -> int:
    data = AuthService().decode_token(token)
    user_id = data.get("user_id", None)
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]
