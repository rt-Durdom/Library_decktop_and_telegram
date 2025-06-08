from fastapi import APIRouter

from app.api.endpoints import users_router, books_router, author_router

api_router = APIRouter()
api_router.include_router(
    users_router)
api_router.include_router(
    books_router, prefix='/books', tags=['books'])
api_router.include_router(
    author_router, prefix='/authors', tags=['authors'])
