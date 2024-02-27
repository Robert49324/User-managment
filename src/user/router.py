import io
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi_pagination import Page
from fastapi_pagination.async_paginator import paginate
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from aws import s3
from database import get_db, postgres
from models import Group, User
from user.service import get_current_user

from .schemas import ReturnPagination, ReturnUser, UpdateRequest

user = APIRouter(prefix="/user", tags=["User module"])
users = APIRouter(prefix="/users", tags=["User module"])


@users.get("/", response_model=Page[ReturnPagination])
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    filter_by_name: str = None,
    sort_by: str = None,
    order_by: str = None,
) -> Page[ReturnPagination]:
    users = await postgres.get_all(db, filter_by_name, sort_by, order_by)
    return await paginate(users)


@user.patch("/me", response_model=ReturnUser)
async def update(
    db: Annotated[AsyncSession, Depends(get_db)],
    update_request: UpdateRequest,
    user: User = Depends(get_current_user),
):
    user: User = await postgres.update(dict(update_request), db, user.id)
    return ReturnUser(
        name=user.name,
        surname=user.surname,
        username=user.username,
        email=user.email,
        phone_number=user.phone_number if user.phone_number else "",
    )


@user.delete("/me")
async def delete_user(
    db: Annotated[AsyncSession, Depends(get_db)], user: User = Depends(get_current_user)
):
    await postgres.delete(user.id, db)


@user.get("/{user_id}", response_model=ReturnUser)
async def user_info(
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: User = Depends(get_current_user),
):

    if user.role == "USER":
        raise HTTPException(403, detail="No access")
    user = await postgres.read_by_id(user_id, db)

    if user.group == user.group:
        return ReturnUser(
            name=user.name,
            surname=user.surname,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number if user.phone_number else "",
        )
    raise HTTPException(403, detail="No access")


@user.patch("/{user_id}", response_model=ReturnUser)
async def update_user(
    update_request: UpdateRequest,
    user_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: User = Depends(get_current_user),
):
    if user.role == "USER":
        raise HTTPException(403, detail="No access")
    user = await postgres.read_by_id(user_id, db)

    if user.group == user.group:
        user: User = await postgres.update(dict(update_request), db, user.id)
        return ReturnUser(
            name=user.name,
            surname=user.surname,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number if user.phone_number else "",
        )


@user.post("/add_image")
async def add_image(
    db: Annotated[AsyncSession, Depends(get_db)],
    image: UploadFile = File(),
    user: User = Depends(get_current_user),
):
    if await s3.upload_fileobj(image, image.filename):
        await postgres.update({"image": image.filename}, db, user.id)
        return {"message": "File uploaded successfully to S3"}
    else:
        raise HTTPException(status_code=500, detail="Failed to upload image")
