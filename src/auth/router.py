from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from auth.constants import *
from auth.service import (authenticate_user, authorize, create_access_token,
                          create_refresh_token, get_current_user, handle_login,
                          is_blocked)
from database import postgres, redis_
from logger import logger
from models import User

from .dependencies import bcrypt_context, get_db, oauth2_bearer
from .schemas import LoginRequest, SignUpRequest, Token

auth = APIRouter(prefix="/auth", tags=["Auth module"])


@auth.post("/signup", status_code=201)
def signup(user: SignUpRequest):
    if postgres.read(user.email) is None:
        logger.info(f"User {user.email} has been registrated")
        user = User(
            name=user.name,
            surname=user.surname,
            username=user.username,
            password=bcrypt_context.hash(user.password),
            email=user.email,
        )
        postgres.create(user)
        return {"detail": "User successfully registered."}
    else:
        raise HTTPException(status_code=409, detail="User already exists.")


@auth.post("/login")
def login(form_data: LoginRequest):
    user = authenticate_user(form_data.email, form_data.password)
    logger.info(f"Logging in {form_data.email}")
    return handle_login(user)


@auth.post("/refresh_token")
def refresh_token(refresh_token: dict = Depends(authorize)):
    refresh_token: str = refresh_token.pop()
    if is_blocked(refresh_token):
        return HTTPException(status_code=403, detail="User is blocked")

    user = get_current_user(refresh_token)
    logger.info(f"Refreshing token: {refresh_token}")
    return handle_login(user)


@auth.post("/reset_password")
def reset_password():
    pass
