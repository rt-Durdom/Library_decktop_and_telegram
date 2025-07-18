import sys
from redis import Redis

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Библиотека'
    database_url: str = None  # 'sqlite+aiosqlite:///./library_test.db'
    secret: str = None
    #templates_dir: str = "templates"

    # # Mail settings
    # mail_host: str  
    # email_port: int  
    # email_username: str  
    email_password: str

    # Redis settings
    redis_host: str  
    redis_port: int  
    # redis_db: int

    # @property  
    # def email_url(self):  
    #     return f"smtps://{self.email_username}:{self.email_password}@{self.mail_host}:{self.email_port}"

    # @property  
    # def redis_url(self):
    #     return f"redis://{self.redis_host}:{self.redis_port}"  # /{self.redis_db}"

    # config
    model_config = SettingsConfigDict(env_file='app/.env')


settings = Settings()
redis_util = Redis(host=settings.redis_host, port=settings.redis_port)
