from __future__ import annotations
from typing import List

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship

from app.core.base import Base
from .books import book_author_table


class Author(Base):
    name = Column(String, nullable=False)
    biography = Column(String)
    birth_data = Column(Date, nullable=False)

    #Ralationship
    book: Mapped[List['Book']] = relationship(
        'Book',
        secondary=book_author_table,
        back_populates='authors'
    )

    def __repr__(self):
        return f"Author(name={self.name}, biography={self.biography}, birth_data={self.birth_data})"
