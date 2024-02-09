import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = "postgresql://admin:admin@localhost:5432/user_managment"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

redis = redis.Redis(host="localhost", port=6379, decode_responses=True)
