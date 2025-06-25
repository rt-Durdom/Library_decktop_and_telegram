from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException


from app.core.users import auth_backend, fastapi_users, current_user
from app.schemas.users import UserRead, UserUpdate, UserCreate
from app.schemas.books import BookRead
from app.core.db import get_async_session
from app.core.config import settings
from app.crud.baskets import basket_crud
from app.crud.books import book_crud
from app.models.users import Basket
from app.crud.users import user_crud
from app.models.users import User

# _______________________________________________________

import aiosmtplib
from email.message import EmailMessage


async def send_email():
    msg = EmailMessage()
    msg["From"] = "hubbit@mail.ru"
    msg["To"] = "roman.turskov@yandex.ru"
    msg["Subject"] = "Test from smtplib"
    msg.set_content("Hello, this is a test email!")

    await aiosmtplib.send(
        msg,
        hostname="smtp.mail.ru",
        port=465,
        use_tls=True,
        username="hubbit@mail.ru",
        password=settings.email_password
    )


    # with aiosmtplib as server:  # или 465-порт 587
    #     server.starttls()
    #     server.login("hubbit@mail.ru", "7zuIL%5g1n")
    #     server.send(msg)
    #print("Email sent!")

# _______________________________________________________


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

@router.post('/take_book/{book_id}', response_model=None)
async def take_book(
    book_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    book = await basket_crud.book_on_basket(user, book_id, session)
    
    user_books = (await session.execute(  #TODO переделать на SQL count
        select(Basket).where(Basket.user_id == user.id)
    )).scalars().all()

    if len(user_books) >= 5:
        raise HTTPException(status_code=400, detail="Больше 5 книг взять нельзя")
    if book:   #  TODO оператор exist() -  найти оператор SQL
        raise HTTPException(status_code=400, detail="Книга уже в корзине")
    send_email()
    return await basket_crud.take_book_on_basket(user, book_id, session)

@router.delete('/delete_book/{book_id}', response_model=None)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    book = await basket_crud.book_on_basket(user, book_id, session)
    if not book:  #  TODO оператор exist() -  найти оператор SQL
        raise HTTPException(status_code=400, detail="Книги в корзине нет")
    return await basket_crud.remove_book_from_basket(user, book_id, session)

@router.get('/get_books_on_basket', response_model=None)
async def get_books_on_basket(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    books_on_basket = await basket_crud.get_books_on_basket(user, session)
    return list(map(lambda x: x.book_id, books_on_basket))
