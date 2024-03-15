from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Null
from sqlalchemy.ext.asyncio import AsyncSession

from models.GroupModel import Group
from repositories.GroupRepository import GroupRepository
from repositories.UserRepository import UserRepository
from schemas.GroupSchemas import GroupCreate


class GroupService:
    groupRepository: GroupRepository
    userRepository: UserRepository

    def __init__(
        self,
        groupRepository: GroupRepository = Depends(),
        userRepository: UserRepository = Depends(),
    ):
        self.groupRepository = groupRepository
        self.userRepository = userRepository

    async def create_group(self, group: GroupCreate):
        if await self.groupRepository.read(group.name):
            raise HTTPException(status_code=400, detail="Group already exists")
        group = Group(**group.dict())
        await self.groupRepository.create(group)
        group = await self.groupRepository.read(group.name)
        return {"message": "Group created", "id": group.id}

    async def remove_group(self, group_id: int):
        if not await self.groupRepository.read_by_id(group_id):
            raise HTTPException(status_code=404, detail="Group not found")
        group = await self.groupRepository.delete(group_id)
        return {"message": "Group deleted"}

    async def add_user_to_group(self, group_id: int, user_id: str):
        group = await self.groupRepository.read_by_id(group_id)
        user = await self.userRepository.read_by_id(user_id)
        if group and user:
            await self.userRepository.update({"group": group.id}, user_id)
            return {"message": "User added to group"}

    async def delete_user_from_group(self, group_id: int, user_id: str):
        group = await self.groupRepository.read_by_id(group_id)
        user = await self.userRepository.read_by_id(user_id)
        if not group and not user:
            raise HTTPException(status_code=404, detail="Group or user not found")
        await self.userRepository.update({"group": Null()}, user_id)
