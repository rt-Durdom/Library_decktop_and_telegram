from typing import Optional
from datetime import date

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    birth_date: Optional[date] = Field(None)


class UserCreate(schemas.BaseUserCreate):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    birth_date: Optional[date] = Field(None)


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    birth_date: Optional[date] = Field(None)
