from dataclasses import Field
from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
