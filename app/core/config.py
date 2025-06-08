import sys
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Библиотека'
    database_url: str = None  # 'sqlite+aiosqlite:///./library_test.db'
    secret: str = None

    model_config = SettingsConfigDict(env_file='app/.env')

    # class Conffig:
    #     env_file = '.env'


settings = Settings()
#print(Settings().model_dump())
