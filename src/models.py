import enum
import uuid

from sqlalchemy import UUID, Boolean, Column, DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from src.database import Base


class Role(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class User(Base):
    __tablename__ = "users"

    id = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name = mapped_column(Text, nullable=False)
    surname = mapped_column(Text, nullable=False)
    username = mapped_column(Text, nullable=False)
    password = mapped_column(Text, nullable=False)
    phone_number = mapped_column(Text, unique=True)
    email = mapped_column(Text, unique=True, nullable=False)
    role = mapped_column(Enum(Role), nullable=False, default=Role.USER)
    group = mapped_column(ForeignKey("group.id"))
    image = mapped_column(Text, unique=True)
    is_blocked = mapped_column(Boolean)
    created_at = mapped_column(DateTime, default=func.now())
    modified_at = mapped_column(DateTime)


class Group(Base):
    __tablename__ = "group"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(Text, unique=True, nullable=False)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())
