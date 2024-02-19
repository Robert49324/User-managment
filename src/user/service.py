from typing import Annotated

from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from config import settings
from database import postgres

from .dependencies import bcrypt_context, oauth2_bearer


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("id")
        if id is None:
            raise HTTPException(status_code=401, detail="Could not validate the user.")
        user = postgres.read_by_id(id)

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate the user.")


async def authorize(token: str = Depends(oauth2_bearer)):
    return token
