import asyncio

from client_api import BookClient


async def main():
    client = BookClient()

    print("1. Создаем книгу...")
    new_book = await client.create_book({
        "name": "Война и мир",
        "description": "string",
        "public_data": "2025-10-03",
        "book_genre": 1,
        "book_copies": 5,
        "book_data_ouput": 1,
        "authors": [10]
    })
    print("Создана книга:", new_book)

    print("2. Получаем все книги...")
    books = await client.get_all_books()
    print("Все книги:", books)

    print("3. Получаем конкретную книгу...")
    book = await client.get_book(16)
    print("Книга:", book)

if __name__ == "__main__":
    print("Запускаем клиент...")
    asyncio.run(main())
    print("Клиент завершил работу!")
