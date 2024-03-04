from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env", extra="чgnore")

    # postgres
    postgres_user: str
    postgres_password: str
    postgres_database: str

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


settings = Settings()
