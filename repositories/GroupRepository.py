from fastapi import Depends
from configs.database import get_db
from repositories.AbstractRepository import AbstractDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update
from models.GroupModel import Group


class GroupRepository(AbstractDatabase):
    db: AsyncSession

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, group):
        self.db.add(group)
        await self.db.commit()

    async def read(self, group: str):
        group = await self.db.execute(select(Group).where(Group.name == group))
        group = group.scalar()
        return group

    async def read_by_id(self, id: int):
        group = await self.db.execute(select(Group).where(Group.id == id))
        group = group.scalar()
        return group

    async def update(self, group: str, id: int):
        await self.db.execute(update(Group).where(Group.id == id).values(group=group))
        await self.db.execute()

    async def delete(self, id: int):
        await self.db.execute(delete(Group).where(Group.id == id))
        await self.db.commit()

