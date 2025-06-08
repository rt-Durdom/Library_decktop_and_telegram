from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from app.models.books import Book
from app.models.authors import Author
from app.core.db import Base


ModelType = TypeVar('ModelType', bound=Base)

class CRUDBase():
    def __init__(self, model):
        self.model = model

    async def retrive(self, obj_id: int, session: AsyncSession):
        return (await session.execute(select(self.model).where(self.model.id == obj_id))
                .scalars().first())
    
    async def get(self, session: AsyncSession) -> list[ModelType]:
        return (await session.execute(select(self.model))).scalars().all()

    async def create(
        self,
        object_in,
        session: AsyncSession,
        # commit: bool = True
    ):
        object_data = object_in.dict()
        db_object = self.model(**object_data)
        session.add(db_object)
        # if commit:
        await session.commit()
        await session.refresh(db_object)
        return db_object
    
    async def update(
            self,
            db_object,
            object_in,
            session: AsyncSession,
            # commit: bool = True
    ):
        obj_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_object, field, update_data[field])
    
        session.add(db_object)
        # if commit:
        await session.commit()
        await session.refresh(db_object)
        return db_object
    
    # async def remove(
    #         self,
    #         db_obj,
    #         session: AsyncSession,
    # ) -> ModelType:
    #     await session.delete(db_obj)
    #     await session.commit()
    #     return db_obj

    async def remove(
        self,
        id: int,  # Принимаем ID вместо объекта
        session: AsyncSession,
    ):
        # Находим объект в базе
        db_obj = await session.get(self.model, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Объект не найден")
        # Удаляем объект
        await session.delete(db_obj)
        await session.commit()
        return db_obj
    
    async def get_obj_by_id(self, obj_id: int, session: AsyncSession):
        return (await session.execute(
            select(self.model).where(self.model.id == obj_id)
            )).scalars().first()

