from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict, BaseSettings


class Config(BaseSettings):
    DB_URL: PostgresDsn
    model_config = SettingsConfigDict()

config = Config(
    DB_URL="postgresql+psycopg2://postgres:\u0020@localhost:5432/forms"
)
