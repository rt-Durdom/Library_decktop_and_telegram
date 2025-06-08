from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    biography: str = Field(..., min_length=3, max_length=100)
    birth_data: date = Field(...,)

    model_config = ConfigDict(from_attributes=True)


class AuthorReadDB(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    biography: Optional[str] = Field(None, min_length=3, max_length=100)
    birth_data: Optional[date] = Field(None,)

