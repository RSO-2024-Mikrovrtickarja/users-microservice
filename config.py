from pydantic_settings import BaseSettings, SettingsConfigDict
import os


DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding="utf-8")


settings = Settings()
