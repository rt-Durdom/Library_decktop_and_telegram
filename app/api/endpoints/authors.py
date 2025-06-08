from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.schemas.authors import AuthorBase, AuthorReadDB, AuthorUpdate
from app.crud.authors import author_crud
from app.crud.base import CRUDBase
from app.core.db import get_async_session
from app.models.authors import Author
from app.models.books import Book


router = APIRouter()


@router.post('/', response_model=AuthorBase)
async def create_new_author(
    author: AuthorBase,
    session: AsyncSession = Depends(get_async_session),
):
    new_author = await author_crud.create(
        author, session,
    )
    # session.add(new_author) # раскоменчивать не надо, в функии create есть сессия
    # await session.commit()
    return new_author


@router.get('/', response_model=list[AuthorReadDB])
async def get_all_author(
    session: AsyncSession = Depends(get_async_session)
):
    return await author_crud.get(session)


@router.delete('/{author_id}', response_model=AuthorBase)
async def delete_author(
    author_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    # db_obj = await session.get(Author, id)
    # if not db_obj:
    #     raise HTTPException(status_code=404, detail="Объект не найден")
    return await author_crud.remove(author_id, session)


@router.patch('/{author_id}', response_model=AuthorReadDB)
async def update_author(
    author_in: int,
    author_obj: AuthorUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    author = await session.get(Author, author_in)
    author_data = await author_crud.update(author, author_obj, session)
    return author_data


@router.patch('/{book_id}/add_author/{author_id}', response_model=None)
async def update_book_author(
    book_id: int,
    author_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Добавление только одного автора в книгу"""
    book_db = await CRUDBase(Book).get_obj_by_id(book_id, session)
    if not book_db:
        raise HTTPException(status_code=404, detail="Добавте книгу")
    
    print(author_id)
    author_db = await CRUDBase(Author).get_obj_by_id(author_id, session)
    if not author_db:
        raise HTTPException(
            status_code=404, detail="Добавьте автора")
    
    book_db.authors.append(author_db)

    session.add(book_db)
    await session.commit()
    await session.refresh(book_db)
    return book_db


@router.delete('/{book_id}/delete_author/{author_id}', response_model=None)
async def update_book_for_author(
    book_id: int,
    author_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление автора из книги"""

    book_db = await CRUDBase(Book).get_obj_by_id(book_id, session)
    if not book_db:
        raise HTTPException(
            status_code=404,
            detail="Книги нет, необходимо создать",
        )

    author_db = await CRUDBase(Author).get_obj_by_id(author_id, session)
    if not author_db:
        raise HTTPException(
            status_code=404,
            detail="Автора нет, невозможно удалить",
        )

    if author_db not in book_db.authors:
        raise HTTPException(
            status_code=400,
            detail="Этот автор не связан с данной книгой",
        )

    book_db.authors.remove(author_db)

    session.add(book_db)
    await session.commit()
    await session.refresh(book_db)
    
    return book_db
