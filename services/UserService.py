from fastapi import Depends, File, HTTPException, UploadFile
from fastapi_pagination import Page, paginate

from configs.dependencies import get_current_user
from configs.environment import get_settings
from models.UserModel import User
from repositories.AWSClient import S3Client
from repositories.UserRepository import UserRepository
from schemas.UserSchemas import ReturnPagination, ReturnUser, UpdateRequest

settings = get_settings()


class UserService:
    userRepository: UserRepository
    s3: S3Client

    def __init__(
        self,
        userRepository: UserRepository = Depends(),
        s3: S3Client = Depends(),
    ):
        self.userRepository = userRepository
        self.s3 = s3

    async def get_users(
        self,
        filter_by_name: str = None,
        sort_by: str = None,
        order_by: str = None,
    ) -> Page[ReturnPagination]:
        users = await self.userRepository.get_all(filter_by_name, sort_by, order_by)
        return paginate(users)

    async def update(self, update_request: UpdateRequest, token: str) -> ReturnUser:
        user: User = await get_current_user(self, token)
        user: User = await self.userRepository.update(dict(update_request), user.id)
        return ReturnUser(
            name=user.name,
            surname=user.surname,
            username=user.username,
            email=user.email,
            phone_number=user.phone_number if user.phone_number else "",
        )

    async def delete(self, token: str):
        user = await get_current_user(self, token)
        await self.userRepository.delete(user.id)

    async def user_info(self, user_id: str, token: str) -> ReturnUser:
        user_admin: User = await get_current_user(self, token)
        if user_admin.role == "USER":
            raise HTTPException(403, detail="No access")
        user = await self.userRepository.read_by_id(user_id)

        if user_admin.group == user.group:
            return ReturnUser(
                name=user.name,
                surname=user.surname,
                username=user.username,
                email=user.email,
                phone_number=user.phone_number if user.phone_number else "",
            )
        raise HTTPException(403, detail="No access")

    async def update_user(
        self, update_request: UpdateRequest, user_id: str, token: str
    ):
        user_admin: User = await get_current_user(self, token)
        if user_admin.role == "USER":
            raise HTTPException(403, detail="No access")
        user = await self.userRepository.read_by_id(user_id)

        if user_admin.group == user.group:
            user: User = await self.userRepository.update(dict(update_request), user.id)
            return ReturnUser(
                name=user.name,
                surname=user.surname,
                username=user.username,
                email=user.email,
                phone_number=user.phone_number if user.phone_number else "",
            )

        raise HTTPException(403, detail="No access")

    async def add_image(self, token: str, image: UploadFile = File()):
        user: User = await get_current_user(self, token)
        async with self.s3 as s3:
            if await s3.upload_fileobj(image.file, image.filename):
                await self.userRepository.update({"image": image.filename}, user.id)
                return True
            else:
                raise HTTPException(status_code=500, detail="Failed to upload image")
