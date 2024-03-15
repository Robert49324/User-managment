from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from models.BaseModel import Base


class Group(Base):
    __tablename__ = "group"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(Text, unique=True, nullable=False)
    created_at = mapped_column(DateTime, nullable=False, default=func.now())
