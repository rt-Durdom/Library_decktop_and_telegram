from app.models.users import User
from .base import CRUDBase


class UserCRUD(CRUDBase):
    pass

user_crud = UserCRUD(User)
