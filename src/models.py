from sqlalchemy import Column, Integer, DateTime, Boolean, Enum, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column
from database import Base
import datetime

class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"

class User(Base):
    __tablename__ = "users"
    
    id = mapped_column(Text,primary_key=True)
    name = mapped_column(Text, nullable=False)
    surname = mapped_column(Text, nullable=False)
    username = mapped_column(Text, nullable=False)
    password = mapped_column(Text,nullable=False)
    phone_number = mapped_column(Text, unique=True)
    email = mapped_column(Text, unique=True, nullable=False)
    role = mapped_column(Role)
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

    
    