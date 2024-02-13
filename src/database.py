from abc import ABC, abstractmethod

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

try:
    from config import settings
except ImportError:
    from .config import settings

engine = create_engine(str(settings.database_url))
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
redis_client = redis.Redis(
    host=settings.redis_host, port=settings.redis_port, decode_responses=True
)


class AbstractDatabase(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class PostgresClient(AbstractDatabase):
    def __init__(self, db_session):
        self.db = db_session

    def create(self, user):
        self.db.add(user)
        self.db.commit()

    def read(self, email: str):
        from models import User

        return self.db.query(User).filter_by(email=email).first()

    def read_by_id(self, id: str):
        from models import User

        return self.db.query(User).filter_by(id=id).first()

    def update(self, **kwargs):
        from models import User

        email = kwargs.get("email")
        user = self.read(email)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.db.commit()

    def delete(self, email: str):
        from models import User

        user = self.read(email)
        if user:
            self.db.delete(user)
            self.db.commit()


class RedisClient(AbstractDatabase):
    def __init__(self, redis_client):
        self.redis = redis_client

    def create(self, key, value):
        self.redis.set(key, value)

    def read(self, key):
        return self.redis.get(key)

    def update(self, key, value):
        if self.redis.exists(key):
            self.redis.set(key, value)

    def delete(self, key):
        self.redis.delete(key)


postgres = PostgresClient(SessionLocal())
redis_ = RedisClient(redis_client)
