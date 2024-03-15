from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_pagination import Page

from configs.dependencies import authorize
from schemas.UserSchemas import ReturnPagination, ReturnUser, UpdateRequest
from services.UserService import UserService

user = APIRouter(prefix="/user", tags=["User module"])
users = APIRouter(prefix="/users", tags=["User module"])


@users.get("/", response_model=Page[ReturnPagination])
async def get_users(
    filter_by_name: str = None,
    sort_by: str = None,
    order_by: str = None,
    token: str = Depends(authorize),
    userService: UserService = Depends(),
) -> Page[ReturnPagination]:
    return await userService.get_users(token, filter_by_name, sort_by, order_by)


@user.patch("/me", response_model=ReturnUser)
async def update(
    update_request: UpdateRequest,
    token: str = Depends(authorize),
    userService: UserService = Depends(),
):
    return await userService.update(update_request, token)


@user.delete("/me")
async def delete_user(
    token: str = Depends(authorize),
    userService: UserService = Depends(),
):
    await userService.delete(token)


@user.get("/{user_id}", response_model=ReturnUser)
async def user_info(
    user_id: str,
    token: str = Depends(authorize),
    userService: UserService = Depends(),
):
    return await userService.user_info(user_id, token)


@user.patch("/{user_id}", response_model=ReturnUser)
async def update_user(
    update_request: UpdateRequest,
    user_id: str,
    token: str = Depends(authorize),
    userService: UserService = Depends(),
):
    return await userService.update_user(update_request, user_id, token)


@user.post("/add_image")
async def add_image(
    image: UploadFile = File(),
    token: str = Depends(authorize),
    userService: UserService = Depends(),
):
    await userService.add_image(token, image)
