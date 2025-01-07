from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    redis_url: RedisDsn = RedisDsn("redis://localhost")
    secrets_encryption_key: bytes


def get_settings() -> Settings:
    return Settings()
