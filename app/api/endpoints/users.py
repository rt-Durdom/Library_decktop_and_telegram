from fastapi import APIRouter

from app.core.users import auth_backend, fastapi_users
from app.schemas.users import UserRead, UserUpdate, UserCreate


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

# @router.post('take_book/{id}', response_model=UserRead)
# async def take_book(
#     id: int,
#     session: AsyncSession = Depends(get_async_session)
# ):
