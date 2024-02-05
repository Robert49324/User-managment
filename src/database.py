from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgres://localhost:5433@admin:admin/user_managment"

engine = create_engine(DATABASE_URL)

base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)