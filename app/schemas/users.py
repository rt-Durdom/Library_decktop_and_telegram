from typing import Optional
from datetime import date

from fastapi_users import schemas
from pydantic import Field

from app.models.users import GanreBook


class UserRead(schemas.BaseUser[int]):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    birth_date: Optional[date] = Field(None)
    like_ganre: Optional[GanreBook]
    telegram_id: int


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    birth_date: Optional[date] = Field(None)
    like_ganre: Optional[GanreBook]
    telegram_id: int


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    birth_date: Optional[date] = Field(None)
