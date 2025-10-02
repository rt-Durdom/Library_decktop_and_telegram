from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.schemas.authors import AuthorBase


class BookBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=5, max_length=100)
    public_data: Optional[date] = Field(None)
    book_genre: int = Field(..., ge=1, le=8)
    book_copies: int = Field(..., ge=0, le=5)
    book_data_ouput: int = Field(None, ge=1, le=60)

    # @field_validator('book_genre')
    # def check_book_genre(cls, value):

    #     isinstance()

    #     try:
    #         int_value = int(value)
    #     except ValueError:
    #         raise ValueError("Значение должно быть числом в кавычках")
    

    #     if int_value not in range(1, 9):
    #         print('Jib,rf', int_value)
    #         raise ValueError("Значение должно быть числом в кавычках от 1 до 8")
    #     return str(int_value)
    


class BookRead(BookBase):
    id: int
    authors: list[AuthorBase]

    model_config = ConfigDict(from_attributes=True)


class BookDB(BookBase):
    authors: list[int] = Field(...)

    model_config = ConfigDict(from_attributes=True)

class AddAuthor(BaseModel):
    author: int = Field(...)
