from __future__ import annotations
from typing import List

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship

from app.core.db import Base  # потом через from app.core.base import Base


book_author_table = Table(
    'book_author_table',
    Base.metadata,
    Column('book_id', ForeignKey('book.id')),
    Column('author_id', ForeignKey('author.id'))
)


class Book(Base):
    name = Column(String, nullable=False)
    description = Column(String)
    public_data = Column(Date, nullable=False)
    # author = Column(Integer, ForeignKey('author.id'), nullable=False)
    book_genre = Column(String, nullable=False)
    book_copies = Column(Integer, nullable=False)

    # Ralationship
    authors: Mapped[List['Author']] = relationship(
        'Author',
        secondary=book_author_table,
        back_populates='book',
        lazy="selectin")

    def __repr__(self):
        return (
        f'name={self.name}'
        f'description={self.description}'
        f'author={self.authors}'
        )
