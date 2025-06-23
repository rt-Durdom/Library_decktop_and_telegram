import sys
from redis import Redis

from pydantic_settings import BaseSettings, SettingsConfigDict


r = Redis(host='localhost', port=6379)

class Settings(BaseSettings):
    app_title: str = 'Библиотека'
    database_url: str = None  # 'sqlite+aiosqlite:///./library_test.db'
    secret: str = None
    #templates_dir: str = "templates"

    # # Mail settings
    # mail_host: str  
    # email_port: int  
    # email_username: str  
    # email_password: SecretStr 

    # # Redis settings
    # redis_host: str  
    # redis_port: int  
    # redis_db: int

    # @property  
    # def redis_url(self):  
    #     return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # config
    model_config = SettingsConfigDict(env_file='app/.env')



settings = Settings()

