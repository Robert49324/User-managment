import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

try:
    from config import settings
except:
    from .config import settings


engine = create_engine(str(settings.database_url))

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

redis = redis.Redis(
    host=settings.redis_host, port=settings.redis_port, decode_responses=True
)
