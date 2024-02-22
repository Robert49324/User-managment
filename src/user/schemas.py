from pydantic import BaseModel


class UpdateRequest(BaseModel):
    name: str = None
    surname: str = None
    username: str = None
    phone_number: str = None
    email: str = None


class ReturnUser(BaseModel):
    name: str = None
    surname: str = None
    username: str = None
    phone_number: str = None
    email: str = None
