import enum
import uuid

from sqlalchemy import (UUID, Boolean, Column, DateTime, Enum, ForeignKey,
                        Index, Integer, Table, Text)
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.sql import func

from config import settings

engine = create_async_engine(
    settings.postgres_url,
)
Base = declarative_base()
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


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
    is_blocked = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=func.now())
    modified_at = mapped_column(DateTime, default=func.now())


class Group(Base):
    __tablename__ = "group"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(Text, unique=True, nullable=False)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())
