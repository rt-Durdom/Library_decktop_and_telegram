from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .base import CRUDBase
from app.models.authors import Author
from app.schemas.authors import AuthorBase, AuthorReadDB, AuthorUpdate
from app.models.books import Book



class AuthorCRUD(CRUDBase):
    pass
    
    # async def add_book_author(
    #     self,
    #     book_id: int,
    #     author_id: int,
    #     session: AsyncSession,
    # ) -> None:
    #     
    #     # author_bd = await CRUDBase(Author).get_obj_by_id(author_id, session)

    #     return book_bd.authors


author_crud = AuthorCRUD(Author)
