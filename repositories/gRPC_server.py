from grpc import aio
from jose import jwt
from sqlalchemy import select

from configs.database import get_db
from configs.environment import get_settings
from models.UserModel import User
from proto import grpc_pb2, grpc_pb2_grpc
from proto.grpc_pb2 import UserModel

settings = get_settings()


class UserFetcher:
    async def fetch_user(self, user_id: str) -> UserModel:
        db = get_db()
        async for session in db:
            user = await session.execute(select(User).where(User.id == user_id))
            user = user.scalar()
            if user is not None:
                return UserModel(
                    id=str(user.id),
                    name=str(user.name),
                    surname=str(user.surname),
                    username=str(user.username),
                    email=str(user.email),
                    role=str(user.role),
                    group=int(user.group) if user.group is not None else 0,
                    is_blocked=bool(user.is_blocked),
                )
        raise Exception("User not found")


class GRPCServer(grpc_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.user_fetcher = UserFetcher()

    async def GetUser(self, request, context):
        try:
            payload = jwt.decode(
                request.jwt, settings.secret_key, algorithms=settings.algorithm
            )
            user_id: str = payload.get("id")
            if user_id is None:
                raise Exception("User ID not found in JWT")

            user = await self.user_fetcher.fetch_user(user_id)
            return grpc_pb2.GetUserResponse(user=user)
        except Exception as e:
            return grpc_pb2.GetUserResponse()


async def run_grpc_server():
    server = aio.server()
    grpc_pb2_grpc.add_UserServiceServicer_to_server(GRPCServer(), server)
    server.add_insecure_port(f"{settings.rpc_host}:{settings.rpc_port}")
    await server.start()
    await server.wait_for_termination()
