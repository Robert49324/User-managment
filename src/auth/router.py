from fastapi import APIRouter, Depends

auth = APIRouter()


@auth.post("auth/signup")
def signup():
    pass


@auth.post("auth/login")
def login():
    pass


@auth.post("auth/refresh_token")
def refresh_token():
    pass


@auth.post("auth/reset_password")
def reset_password():
    pass
