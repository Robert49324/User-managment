import uuid

from sqlalchemy import UUID, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from models.BaseModel import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name = mapped_column(Text, nullable=False)
    surname = mapped_column(Text, nullable=False)
    username = mapped_column(Text, nullable=False)
    password = mapped_column(Text, nullable=False)
    phone_number = mapped_column(Text, unique=True)
    email = mapped_column(Text, unique=True, nullable=False)
    role = mapped_column(
        Enum("USER", "ADMIN", "MODERATOR", name="Role"), nullable=False, default="USER"
    )
    group = mapped_column(ForeignKey("group.id"))
    image = mapped_column(Text, unique=True)
    is_blocked = mapped_column(Boolean, default=False)
    modified_at = mapped_column(DateTime, default=func.now())
