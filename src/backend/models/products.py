from sqlalchemy import Column, Integer, String,DateTime, func
from src.backend.database.database import Base

class Product(Base):
    __tablename__ = "products"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False, index=True)
    brand         = Column(String, nullable=False)
    specification = Column(String, nullable=True)
    unit          = Column(String, nullable=False)   # e.g. "per meter", "per piece"
    price         = Column(Integer, nullable=False)
    category      = Column(String, nullable=True)    # e.g. "Wire", "Switch", "MCB"
    created_at    = Column(DateTime, server_default=func.now())
    updated_at    = Column(DateTime, server_default=func.now(), onupdate=func.now())
    