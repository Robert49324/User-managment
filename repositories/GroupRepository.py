from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from configs.database import get_db
from models.GroupModel import Group
from repositories.AbstractRepository import AbstractDatabase
from src.logger import logger


class GroupRepository(AbstractDatabase):
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, group):
        try:
            self.db.add(group)
            await self.db.commit()
        except Exception as e:
            logger.error(f"Error creating group: {str(e)}")
            await self.db.rollback()

    async def read(self, group: str):
        try:
            group = await self.db.execute(select(Group).where(Group.name == group))
            group = group.scalar()
            return group
        except Exception as e:
            logger.error(f"Error reading group: {str(e)}")

    async def read_by_id(self, id: int):
        try:
            group = await self.db.execute(select(Group).where(Group.id == id))
            group = group.scalar()
            return group
        except Exception as e:
            logger.error(f"Error reading group by id: {str(e)}")

    async def update(self, group: str, id: int):
        try:
            await self.db.execute(
                update(Group).where(Group.id == id).values(group=group)
            )
            await self.db.commit()
        except Exception as e:
            logger.error(f"Error updating group: {str(e)}")
            await self.db.rollback()

    async def delete(self, id: int):
        try:
            await self.db.execute(delete(Group).where(Group.id == id))
            await self.db.commit()
        except Exception as e:
            logger.error(f"Error deleting group: {str(e)}")
            await self.db.rollback()
