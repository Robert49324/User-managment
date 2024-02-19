from abc import ABC, abstractmethod
from typing import Any

import redis.asyncio as redis
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@postgres:5432/{settings.postgres_database}"
)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


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


class PostgresUser(AbstractDatabase):
    async def create(self, user, db: AsyncSession):
        db.add(user)
        await db.commit()

    async def read(self, email: str, db: AsyncSession):
        from models import User

        user = await db.execute(select(User).where(User.email == email))
        user = user.scalar()
        return user

    async def read_by_id(self, id: str, db: AsyncSession):
        from models import User

        user = await db.execute(select(User).where(User.id == id))
        user = user.scalar()
        return user

    async def update(self, request: dict, db: AsyncSession):
        from models import User

        id = request.get("id")
        user = await db.query(User).filter_by(id=id).first()
        if user:
            for key, value in request.items():
                if key in user.__dict__ and key != None:
                    await setattr(user, key, value)
            await db.commit()

    async def delete(self, email: str, db: AsyncSession):
        from models import User

        user = await db.query(User).filter_by(email=email).first()
        if user:
            await db.delete(user)
            await db.commit()


class RedisClient(AbstractDatabase):
    def __init__(self):
        self.redis = redis.from_url(settings.redis_url)

    async def create(self, key, value):
        print(f"Creating {key} : {value}")
        await self.redis.set(key, value)

    async def read(self, key):
        return await self.redis.get(key)

    async def update(self, key, value):
        if await self.redis.exists(key):
            await self.redis.set(key, value)

    async def delete(self, key):
        await self.redis.delete(key)


postgres = PostgresUser()
redis_ = RedisClient()
