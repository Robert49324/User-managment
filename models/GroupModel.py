from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    DateTime,
    Integer,
    Text,
    Integer,
)

from models.BaseModel import Base
from sqlalchemy.sql import func


class Group(Base):
    __tablename__ = "group"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(Text, unique=True, nullable=False)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())
