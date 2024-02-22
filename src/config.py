from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_user: str
    postgres_password: str
    postgres_database: str

    secret_key: str
    algorithm: str

    host: str
    port: int

    redis_url: str


settings = Settings()
