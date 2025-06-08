from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.schemas.books import BookDB, BookRead
from app.schemas.authors import AuthorBase
from app.models.books import Book
from app.models.authors import Author


class BookCRUD(CRUDBase):

    async def create_book(
        self,
        object_b: BookDB,
        session: AsyncSession,
    ):
        # Извлекаем данные книги (исключая авторов)
        book_data = object_b.model_dump(exclude={'authors'})
        #print('1',book_data)
        # Получаем список ID авторов
        author_ids = object_b.authors
        #print('2', author_ids)
        # Проверяем, что указаны авторы
        if not author_ids:
            raise ValueError("Необходимо указать хотя бы одного автора")
        
        # Получаем объекты авторов из БД
        authors = []
        for author_id in author_ids:
            result = await session.execute(select(Author).where(Author.id == author_id))
            author = result.scalar_one_or_none()
            if author is None:
                raise HTTPException(status_code=404, detail=f"Автор с ID {author_id} не найден")
            authors.append(author)
        # Создаем новую книгу
        new_book = self.model(**book_data)
        #print('3', new_book)
        session.add(new_book)
        
        # Устанавливаем связь с авторами
        new_book.authors = authors
        
        try:
            await session.commit()
            await session.refresh(new_book)
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Ошибка при создании книги: {str(e)}")
        
        # Преобразуем в Pydantic модель для возврата
        return new_book
    

    async def update_book(
            self,
            db_obj,  # объект базы данных
            obj_in,  # входящий объект
            session: AsyncSession,
):
        obj_data = jsonable_encoder(db_obj)  # получаем словарь объекта БД
        #  Получаем словарь данных котрые необхомо занести в БД, кроме авторов
        update_data = obj_in.model_dump(exclude={'authors'})
        # операция по авторам
        author_ids = obj_in.authors

        if not author_ids:
            raise ValueError("Необходимо указать хотя бы одного автора")
        
        # Получаем объекты авторов из БД
        authors = []
        for author_id in author_ids:
            result = await session.execute(select(Author).where(Author.id == author_id))
            author = result.scalar_one_or_none()
            if author is None:
                raise HTTPException(status_code=404, detail=f"Автор с ID {author_id} не найден")
            authors.append(author)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        # db_obj = self.model(**update_data)
        session.add(db_obj)
        
        # Устанавливаем связь с авторами
        db_obj.authors = authors
        await session.commit()
        await session.refresh(db_obj)

        return db_obj



    async def get_all_books(  
        self,
        session: AsyncSession
    ) -> list[BookRead]:
        # Загружаем книги с авторами за один запрос
        books = (await session.execute(
            select(Book).where(self.model.authors) # попросить пояснить Леонида self.model.authors
        )).scalars().all()
    
        return books


book_crud = BookCRUD(Book)
