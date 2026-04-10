from sqlalchemy import Column, Integer, String, DateTime, func
from src.backend.database import Base

class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False)
    username      = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role          = Column(String, nullable=False, default="viewer")  # "admin" or "viewer"
    created_at    = Column(DateTime, server_default=func.now())