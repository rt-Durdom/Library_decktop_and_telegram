from typing import List

import aiohttp


class BookClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    async def create_book(self, book_data: dict) -> dict:
        """Cоздание книги."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/books", json=book_data
            ) as resp:
                return await resp.json()

    async def get_all_books(self) -> List[dict]:
        """Получение всех книг."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/books") as resp:
                return await resp.json()

    async def get_book(self, book_id: int) -> dict:
        """Получение указанной книги."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/books/{book_id}") as resp:
                return await resp.json()
