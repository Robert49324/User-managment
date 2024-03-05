from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # postgres
    postgres_url: str

    # redis
    redis_url: str

    # rabbitmq
    rabbitmq_user: str
    rabbitmq_password: str

    # localstack
    localstack_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bucket: str

    secret_key: str
    algorithm: str

    host: str
    port: int


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    
    # postgres
    postgres_url: str

    # redis
    redis_url: str

    # rabbitmq
    # rabbitmq_user: str
    # rabbitmq_password: str

    # localstack
    localstack_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_bucket: str

    secret_key: str
    algorithm: str

    host: str
    port: int


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
