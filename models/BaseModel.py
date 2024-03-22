from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime 
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    created_at = mapped_column(DateTime, default=func.now())