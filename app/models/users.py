from enum import Enum
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from app.core.db import Base  # потом через from app.core.base import Base
from sqlalchemy import Column, String, Date, Integer, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column


class GanreBook(str, Enum):
    ACTION = 1
    COMEDY = 2
    DRAMA = 3
    FANTASY = 4
    HORROR = 5
    ROMANCE = 6
    THRILLER = 7
    DETECTIVE = 8


class User(Base, SQLAlchemyBaseUserTable[int]):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    like_ganre: Mapped[GanreBook] = mapped_column(SQLEnum(GanreBook), nullable=True)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relashionships
    books: Mapped[list['Book']] = relationship(
        'Book',
        secondary='basket',
        back_populates='users'
    )

    def __repr__(self):
        return(
            f"User(first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"birth_date={self.birth_date}"
        )


class Basket(Base):
    date_put_book: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now()
    )
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)

    # # Relationships
    # user: Mapped['User'] = relationship('User', back_populates='books')
    # book: Mapped['Book'] = relationship('Book', back_populates='users')




class AddUserNotification(Base):
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'), primary_key=True)
    date_notification: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
