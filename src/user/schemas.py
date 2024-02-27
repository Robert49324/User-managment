from pydantic import BaseModel, EmailStr


class UpdateRequest(BaseModel):
    name: str = None
    surname: str = None
    username: str = None
    phone_number: str = None
    email: str = EmailStr


class ReturnUser(BaseModel):
    name: str = None
    surname: str = None
    username: str = None
    phone_number: str = None
    email: str = EmailStr


class ReturnPagination(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    role: str
    is_blocked: bool
