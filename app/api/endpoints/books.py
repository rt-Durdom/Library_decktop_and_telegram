from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.books import BookBase, BookDB, BookRead
from app.crud.books import book_crud
from app.core.db import get_async_session
from app.models.books import Book
from app.core.config import settings, redis_util  # import redis


router = APIRouter()
#redis_util = settings.redis_url()


@router.post('/', response_model=BookRead)
async def create_new_book(
    book: BookDB,
    session: AsyncSession = Depends(get_async_session),
):
    new_book = await book_crud.create_book(
        book, session,
    )

    redis_util.set('book', f'{new_book.id}')

    # session.add(new_book)
    # await session.commit()
    return new_book


@router.get('/', response_model=list[BookRead])  # list[BookRead]
async def get_all_books(
    session: AsyncSession = Depends(get_async_session)
):
    return await book_crud.get(session)


@router.get('/{book_id}', response_model=BookRead)  # list[BookRead]
async def get_all_books(
    book_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return await book_crud.get_obj_by_id(book_id,session)


@router.delete('/{book_id}', response_model=BookRead)
async def delete_books(
    book: int,
    session: AsyncSession = Depends(get_async_session)
):
    return await book_crud.remove(book, session)


@router.patch('/{book_id}', response_model=None)
async def update_book(
    book_id: int,
    book_obj: BookDB,
    session: AsyncSession = Depends(get_async_session)
):
    data_book = await session.get(Book, book_id)
    updating_book = await book_crud.update_book(data_book, book_obj, session)

    return updating_book

