import sys
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from auth.constants import *
from database import get_db
from ..models import User

from .schemas import SignUpRequest

auth = APIRouter(prefix="/auth", tags=["Auth module"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


@auth.post("/signup")
def signup(db: Annotated[Session, Depends(get_db)], user: SignUpRequest):
    print(db.query(User).filter_by(email=user.email).first())
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
    else:
        return {"error":"User already exists"}


@auth.post("/login")
def login():
    pass


@auth.post("/refresh_token")
def refresh_token():
    pass


@auth.post("/reset_password")
def reset_password():
    pass
