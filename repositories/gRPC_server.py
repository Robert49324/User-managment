import logging
from grpc import aio
from jose import jwt
from sqlalchemy import select

from configs.database import get_db
from configs.environment import get_settings
from models.UserModel import User
from proto import grpc_pb2, grpc_pb2_grpc
from proto.grpc_pb2 import UserModel

settings = get_settings()

logger = logging.getLogger("user_managment")


class GRPCServer(grpc_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.db = get_db()

    async def GetUser(self, request, context):
        try:
            payload = jwt.decode(
                request.jwt, settings.secret_key, algorithms=settings.algorithm
            )
            id: str = payload.get("id")
            if id is None:
                raise Exception("User ID not found in JWT")

            async def fetch_user():
                async for session in self.db:
                    user_query = await session.execute(select(User).where(User.id == id))
                    user = user_query.scalar()
                    if user is not None:
                        return user
                return None

            user = await fetch_user()

            if user is not None:
                user_data = UserModel(
                    id=str(user.id),
                    name=str(user.name),
                    surname=str(user.surname),
                    username=str(user.username),
                    email=str(user.email),
                    role=str(user.role),
                    group=int(user.group) if user.group is not None else 0,
                    is_blocked=bool(user.is_blocked),
                )
                print(user_data.group)
                return grpc_pb2.GetUserResponse(
                    user=user_data
                )
            else:
                raise Exception("User not found")

        except Exception as e:
            print(e)
            logger.error(f"Error getting user: {str(e)}")
            return grpc_pb2.GetUserResponse()



async def run_grpc_server():
    server = aio.server()
    grpc_pb2_grpc.add_UserServiceServicer_to_server(GRPCServer(), server)
    server.add_insecure_port(f"{settings.rpc_host}:{settings.rpc_port}")
    await server.start()
    await server.wait_for_termination()
