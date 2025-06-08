from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from app.core.db import Base  # потом через from app.core.base import Base
from sqlalchemy import Column, String, Date


class User(SQLAlchemyBaseUserTable[int], Base):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)

    def __repr__(self):
        pass
