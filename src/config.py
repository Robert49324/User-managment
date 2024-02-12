from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    # secret_key : str
    # algorithm : str
    
    host: str
    port: int
    
    database_url : str
    
    redis_host : str
    redis_port : int


settings = Settings()
