from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # postgres
    postgres_url: str = Field(default="")

    # redis
    redis_url: str = Field(default="")

    # rabbitmq
    rabbitmq_user: str = Field(default="")
    rabbitmq_password: str = Field(default="")

    # localstack
    localstack_url: str = Field(default="")
    aws_access_key_id: str = Field(default="")
    aws_secret_access_key: str = Field(default="")
    aws_bucket: str = Field(default="")

    secret_key: str = Field(default="")
    algorithm: str = Field(default="")

    host: str = Field(default="")
    port: int = Field(default=0)


# class TestSettings(BaseSettings):
#     model_config = SettingsConfigDict(extra="ignore")
    
#     # postgres
#     postgres_url: str

#     # redis
#     redis_url: str

#     # localstack
#     localstack_url: str
#     aws_access_key_id: str
#     aws_secret_access_key: str
#     aws_bucket: str

#     secret_key: str
#     algorithm: str

#     host: str
#     port: int


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
