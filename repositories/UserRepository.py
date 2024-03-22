from fastapi import Depends
from sqlalchemy import asc, delete, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from configs.database import get_db
from models.UserModel import User
from repositories.AbstractRepository import AbstractDatabase
from src.logger import logger

class UserRepository(AbstractDatabase):
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, user: User):
        try:
            self.db.add(user)
            await self.db.commit()
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")

    async def read(self, email: str):
        try:
            user = await self.db.execute(select(User).where(User.email == email))
            user = user.scalar()
            return user
        except Exception as e:
            logger.error(f"Error reading user by email: {str(e)}")

    async def read_by_id(self, id: str):
        try:
            user = await self.db.execute(select(User).where(User.id == id))
            user = user.scalar()
            return user
        except Exception as e:
            logger.error(f"Error reading user by id: {str(e)}")

    async def update(self, request: dict, id: str):
        try:
            request = {key: value for key, value in request.items() if value is not None}
            await self.db.execute(update(User).where(User.id == id).values(**request))
            await self.db.commit()
            user = await self.db.execute(select(User).where(User.id == id))
            user = user.scalar()
            return user
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")

    async def delete(self, id: str):
        try:
            await self.db.execute(delete(User).where(User.id == id))
            await self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")

    async def get_all(
        self,
        filter_by_name: str = None,
        sort_by: str = None,
        order_by: str = None,
    ):
        try:
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
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
