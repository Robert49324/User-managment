
import datetime
from fastapi import Depends, HTTPException
from configs.dependencies import RabbitMQ, RedisClient, authorize, bcrypt_context, get_current_user, get_rabbitmq, get_redis_client, oauth2_bearer
from repositories.GroupRepository import GroupRepository
from repositories.UserRepository import UserRepository
from schemas.AuthSchemas import LoginRequest, ResetPasswordRequest, SignUpRequest
from models.UserModel import User
from configs.environment import get_settings
from jose import jwt
from src.logger import logger


settings = get_settings()

class AuthService:
    userRepository : UserRepository
    redis : RedisClient
    rabbit : RabbitMQ
    
    def __init__(
        self,
        userRepository: UserRepository = Depends(),
        redis : RedisClient = Depends(get_redis_client),
        rabbit : RabbitMQ = Depends(get_rabbitmq)
    ):
        self.userRepository = userRepository
        self.redis = redis
        self.rabbit = rabbit
    
    async def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.datetime.now() + datetime.timedelta(hours=1)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt


    async def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.datetime.now() + datetime.timedelta(days=1)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )
        return encoded_jwt


    async def generate_tokens(self, user: User):
        access_token = await self.create_access_token(
            {"id": str(user.id), "email": user.email, "role": str(user.role)}
        )
        refresh_token = await self.create_refresh_token({"id": str(user.id)})
        return access_token, refresh_token


    async def handle_login(self, user: User):
        if not user:
            raise HTTPException(status_code=401, detail="Could not validate user.")
        access_token, refresh_token = await self.generate_tokens(user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def authenticate_user(self, email: str, password: str):
        user: User = await self.userRepository.read(email)
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        if not bcrypt_context.verify(password, user.password):
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        return user


    async def verify_password(self, user: User, password: str):
        if not bcrypt_context.verify(password, user.password):
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        return True


    async def is_blocked(self, token: str = Depends(oauth2_bearer)):
        if await self.redis.read(token):
            return True
        return False


    async def block_token(self, token: str = Depends(oauth2_bearer)):
        await self.redis.create(token, "blocked")

    async def send_email(self, email: str):
        async with self.rabbit:
            await self.rabbit.publish(email, "change_email")
    
    async def signup(self, user: SignUpRequest):
        if await self.userRepository.read(user.email) is None:
            logger.info(f"User {user.email} has been registrated")
            user = User(
                name=user.name,
                surname=user.surname,
                username=user.username,
                password=bcrypt_context.hash(user.password),
                email=user.email,
            )
            await self.userRepository.create(user)
            return {"detail": "User successfully registered."}
        else:
            raise HTTPException(status_code=409, detail="User already exists.")

    async def login(self, form_data: LoginRequest):
        user = await self.authenticate_user(form_data.email, form_data.password)
        logger.info(f"Logging in {form_data.email}")
        return await self.handle_login(user)

    async def refresh_token(
        self, refresh_token: str = Depends(authorize)
    ):
        if await self.is_blocked(refresh_token):
            return HTTPException(status_code=403, detail="Token is blocked")
        await self.block_token(refresh_token)
        user = await get_current_user(self, token=refresh_token)
        logger.info(f"Refreshing token: {refresh_token}")
        return await self.handle_login(user)
    
    async def reset_password(
        self, 
        request: ResetPasswordRequest,
        token : str = Depends(authorize),
    ):
        user = await get_current_user(self, token)
        if await self.verify_password(user, request.password):
            await self.userRepository.update(
                {"password": bcrypt_context.hash(request.new_password)}, user.id
            )
            await self.send_email(request.email)
        return {"detail": "Password successfully reset."}
    