from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from app.schemas.authors import AuthorBase


class BookBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=5, max_length=100)
    public_data: Optional[date] = Field(None)
    book_genre: str = Field(...)
    book_copies: int = Field(..., ge=0, le=5)


class BookRead(BookBase):
    id: int
    authors: list[AuthorBase]

    model_config = ConfigDict(from_attributes=True)


class BookDB(BookBase):
    authors: list[int] = Field(...)

    model_config = ConfigDict(from_attributes=True)

class AddAuthor(BaseModel):
    author: int = Field(...)
