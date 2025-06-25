from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.users import Basket, User
from app.models.books import Book
from app.crud.base import CRUDBase


class BasketCRUD(CRUDBase):
    async def book_on_basket(self, user: User, book_id: int, session: AsyncSession):
        book = (await session.execute(
            select(Basket).where(Basket.book_id == book_id, Basket.user_id == user.id)
        )).scalars().first()
        return book

    async def take_book_on_basket(self, user: User, book_id: int, session: AsyncSession):

        basket = Basket(user_id=user.id, book_id=book_id)
        session.add(basket)
        await session.commit()
        await session.refresh(basket)
        return basket

    async def remove_book_from_basket(self, user: User, book_id: int, session: AsyncSession):

        basket = await self.book_on_basket(user, book_id, session)
        await session.delete(basket)
        await session.commit()
        return basket
    
    async def get_books_on_basket(self, user: User, session: AsyncSession):
        return (await session.execute(
            select(Basket).where(Basket.user_id == user.id)
        )).scalars().all()


basket_crud = BasketCRUD(Basket)
