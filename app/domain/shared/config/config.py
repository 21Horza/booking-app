from typing import Literal
from pydantic import BaseSettings, root_validator

class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_NAME: str
    DB_PWD: str
    DB_USER: str
    DB_PORT: int
    DB_HOST: str

    @root_validator
    def get_db_url(cls, v): # - settings values
        v["DATABASE_URL"] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PWD']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        return v

    TEST_DB_NAME: str
    TEST_DB_PWD: str
    TEST_DB_USER: str
    TEST_DB_PORT: int
    TEST_DB_HOST: str

    @root_validator
    def get_test_db_url(cls, v): # - settings values
        v["TEST_DATABASE_URL"] = f"postgresql+asyncpg://{v['TEST_DB_USER']}:{v['TEST_DB_PWD']}@{v['TEST_DB_HOST']}:{v['TEST_DB_PORT']}/{v['TEST_DB_NAME']}"
        return v
    
    SECRET_KEY: str
    ALGORITHM: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PWD: str

    REDIS_HOST: str
    REDIS_PORT: int
        
    class Config:
        env_file = ".env"

settings = Settings()

print(settings.DATABASE_URL)