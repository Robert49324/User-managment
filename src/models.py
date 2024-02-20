import enum
import uuid

from sqlalchemy import (UUID, Boolean, DateTime, Enum, ForeignKey, Index,
                        Integer, Text)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, sessionmaker
from sqlalchemy.sql import func

from config import settings

engine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@postgres:5432/{settings.postgres_database}"
)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


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
    role = mapped_column(
        Enum("USER", "ADMIN", "MODERATOR", name="Role"), nullable=False, default="USER"
    )
    group = mapped_column(ForeignKey("group.id"))
    image = mapped_column(Text, unique=True)
    is_blocked = mapped_column(Boolean)
    created_at = mapped_column(DateTime, default=func.now())
    modified_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    __table_args__ = (Index("ix_users_email", email),)


class Group(Base):
    __tablename__ = "group"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(Text, unique=True, nullable=False)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())
