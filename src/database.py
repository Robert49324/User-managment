from abc import ABC, abstractmethod
from typing import Any

import redis.asyncio as redis
from sqlalchemy import asc, delete, desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from config import settings
from models import Group, User, async_session


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

        user = await db.execute(select(User).where(User.email == email))
        user = user.scalar()
        return user

    async def read_by_id(self, id: str, db: AsyncSession):

        user = await db.execute(select(User).where(User.id == id))
        user = user.scalar()
        return user

    async def update(self, request: dict, db: AsyncSession, id: str):
        request = {key: value for key, value in request.items() if value is not None}
        request["modified_at"] = func.now()
        await db.execute(update(User).where(User.id == id).values(**request))
        await db.commit()
        user = await db.execute(select(User).where(User.id == id))
        user = user.scalar()
        return user

    async def delete(self, id: str, db: AsyncSession):
        await db.execute(delete(User).where(User.id == id))
        await db.commit()

    async def get_all(
        self,
        db: AsyncSession,
        filter_by_name: str = None,
        sort_by: str = None,
        order_by: str = None,
    ):
        query = (
            select(User).where(User.name.contains(filter_by_name))
            if filter_by_name
            else select(User)
        )
        if sort_by and order_by:
            if order_by == "asc":
                query = query.order_by(asc(sort_by))
            elif order_by == "desc":
                query = query.order_by(desc(sort_by))
        users = await db.execute(query)
        users = users.scalars().all()
        return users


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


async def get_db():
    async with async_session() as session:
        yield session
