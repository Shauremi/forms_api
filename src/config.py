from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    repository_type: str = "memory"
    DB_URL: PostgresDsn | str = "sqlite:///:memory:"

    class Config:
        env_file = ".env"


config = Settings()
