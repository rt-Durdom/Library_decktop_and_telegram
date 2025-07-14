import aiosmtplib
import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from email.message import EmailMessage
import urllib
# from redis.asyncio import Redis

# import redis
from app.core.config import settings, redis_util
from app.core.db import get_async_session, AsyncSessionLocal
from app.crud.books import book_crud

async def send_email():
    book = await get_book()
    msg = EmailMessage()
    msg["From"] = "hubbit@mail.ru"
    msg["To"] = "roman.turskov@yandex.ru"
    msg["Subject"] = "Test from smtplib"
    msg.set_content(f"Hello, {book['name']}")

    await aiosmtplib.send(
        msg,
        hostname="smtp.mail.ru",
        port=465,
        use_tls=True,
        username="hubbit@mail.ru",
        password=settings.email_password
    )

# r = settings.redis_url()
    

async def get_book(session: AsyncSession = AsyncSessionLocal()):
    # session = await get_async_session()
    book_id = int(redis_util.get('book'))
    # print(await book_crud.get_obj_by_id(book_id, session))
    # await session.close()
    redis_util.delete('book')
    responce = (urllib.request.urlopen(f'http://127.0.0.1:8000/books/{book_id}'))

    book = json.loads(responce.read().decode('utf-8'))

    return book

# async def main():
#     book_task = asyncio.create_task(get_book())
    
    # print(book_task.result())


if __name__ == "__main__":
    asyncio.run(send_email())
