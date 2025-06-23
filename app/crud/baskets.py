from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Basket, User
from app.models.books import Book
from app.crud.base import CRUDBase


class BasketCRUD(CRUDBase):
    async def take_book_on_basket(self, user: User, book_id: int, session: AsyncSession):

        basket = Basket(user_id=user.id, book_id=book_id)
        session.add(basket)
        await session.commit()
        await session.refresh(basket)
        return basket


basket_crud = BasketCRUD(Basket)
