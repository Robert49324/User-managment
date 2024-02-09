import sys
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

sys.path.append("..")

from auth.constants import *
from auth.service import (authenticate_user, create_access_token,
                          create_refresh_token, is_blocked, authorize)
from models import User

from .dependencies import bcrypt_context, get_db, oauth2_bearer
from .schemas import LoginRequest, SignUpRequest, Token

auth = APIRouter(prefix="/auth", tags=["Auth module"])


@auth.post("/signup", status_code=201)
def signup(db: Annotated[Session, Depends(get_db)], user: SignUpRequest):
    if db.query(User).filter_by(email=user.email).first() == None:
        user = User(
            name=user.name,
            surname=user.surname,
            username=user.username,
            password=bcrypt_context.hash(user.password),
            email=user.email,
        )
        db.add(user)
        db.commit()
        return {"detail": "User successfully registered."}
    else:
        raise HTTPException(status_code=409, detail="User already exists.")


@auth.post("/login")
def login(db: Annotated[Session, Depends(get_db)], form_data: LoginRequest):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate user.")
    return {
        "access_token": create_access_token(
            {"id": str(user.id), "email": user.email, "role": str(user.role)}
        ),
        "refresh_token": create_refresh_token({"id": str(user.id)}),
        "token_type": "bearer",
    }


@auth.post("/refresh_token")
def refresh_token(
    db: Annotated[Session, Depends(get_db)],
    refresh_token: dict=Depends(authorize)
):
    if is_blocked(str(refresh_token)):
        return HTTPException(status_code=403, detail="User is blocked")
    return refresh_token


@auth.post("/reset_password")
def reset_password():
    pass
