from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Null
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.GroupSchemas import GroupCreate
from services.GroupService import GroupService

group = APIRouter(prefix="/group", tags=["Group module"])

group_service = GroupService()


@group.post("/create", status_code=201)
async def create_group_wrapper(
    group: GroupCreate, groupService: GroupService = Depends()
):
    return await groupService.create_group(group)


@group.delete("/{group_id}")
async def remove_group_wrapper(group_id: int, groupService: GroupService = Depends()):
    return await groupService.remove_group(group_id)


@group.post("/{group_id}/users/{user_id}")
async def add_user_to_group_wrapper(
    group_id: int, user_id: str, groupService: GroupService = Depends()
):
    return await groupService.add_user_to_group(group_id, user_id)


@group.delete("/{group_id}/users/{user_id}")
async def delete_user_from_group_wrapper(
    group_id: int, user_id: str, groupService: GroupService = Depends()
):
    return await groupService.delete_user_from_group(group_id, user_id)
