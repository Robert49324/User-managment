from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_url: str = Field(default="")

    redis_url: str = Field(default="")

    rabbitmq_user: str = Field(default="")
    rabbitmq_password: str = Field(default="")

    localstack_url: str = Field(default="")
    aws_access_key_id: str = Field(default="")
    aws_secret_access_key: str = Field(default="")
    aws_bucket: str = Field(default="")

    secret_key: str = Field(default="")
    algorithm: str = Field(default="")

    host: str = Field(default="")
    port: int = Field(default=0)


@lru_cache
def get_settings() -> Settings:
    return Settings()
