from fastapi import Depends
from repositories.AbstractRepository import AbstractDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, delete, desc, select, update
from models.UserModel import User
from sqlalchemy.sql import func
from configs.database import get_db
from models.UserModel import User

class UserRepository(AbstractDatabase):
    db : AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, user : User):
        self.db.add(user)
        await self.db.commit()

    async def read(self, email: str):
        user = await self.db.execute(select(User).where(User.email == email))
        user = user.scalar()
        return user

    async def read_by_id(self, id: str):

        user = await self.db.execute(select(User).where(User.id == id))
        user = user.scalar()
        return user

    async def update(self, request: dict, id: str):
        request = {key: value for key, value in request.items() if value is not None}
        request["modified_at"] = func.now()
        await self.db.execute(update(User).where(User.id == id).values(**request))
        await self.db.commit()
        user = await self.db.execute(select(User).where(User.id == id))
        user = user.scalar()
        return user

    async def delete(self, id: str):
        await self.db.execute(delete(User).where(User.id == id))
        await self.db.commit()

    async def get_all(
        self,
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
        users = await self.db.execute(query)
        users = users.scalars().all()
        return users

