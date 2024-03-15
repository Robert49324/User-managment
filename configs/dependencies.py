from aio_pika import Message, connect
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
import redis
from configs.environment import get_settings
import asyncio

import aioboto3

settings = get_settings()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")


async def get_current_user(
    self,
    token: str = Depends(oauth2_bearer),
):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("id")
        print(id)
        if id is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        user = await self.userRepository.read_by_id(id)
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user.")

def authorize(token: str = Depends(oauth2_bearer)):
    return token

class S3Client:
    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket = settings.aws_bucket

    async def __aenter__(self):
        self.client = self.session.client(
            "s3",
            endpoint_url=settings.localstack_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self.s3 = await self.client.__aenter__()
        try:
            await self.s3.head_bucket(Bucket=self.bucket)
        except Exception as e:
            await self.s3.create_bucket(Bucket=self.bucket)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.__aexit__(exc_type, exc, tb)

    async def upload_fileobj(self, file, filename):
        try:
            await self.s3.upload_fileobj(Fileobj=file, Bucket=self.bucket, Key=filename)
            return True
        except Exception as e:
            print(e)  # or use your preferred logging method
            return False




def get_s3_client():
    return S3Client()

class RedisClient():
    def __init__(self):
        self.redis = redis.from_url(settings.redis_url)

    async def create(self, key, value):
        print(f"Creating {key} : {value}")
        self.redis.set(key, value)

    async def read(self, key):
        return self.redis.get(key)

    async def update(self, key, value):
        if await self.redis.exists(key):
            await self.redis.set(key, value)

    async def delete(self, key):
        await self.redis.delete(key)


async def get_redis_client():
    return RedisClient()

class RabbitMQ:
    def __init__(self):
        self.address = (
            f"amqp://{settings.rabbitmq_user}:{settings.rabbitmq_password}@rabbitmq/"
        )

    async def __aenter__(self):
        self.connection = await connect(self.address)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.connection.close()

    async def publish(self, message: str, routing_key: str):
        channel = await self.connection.channel()
        await channel.default_exchange.publish(
            Message(message.encode("utf-8")), routing_key=routing_key
        )


def get_rabbitmq():
    return RabbitMQ()
