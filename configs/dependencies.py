from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from configs.environment import get_settings

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
