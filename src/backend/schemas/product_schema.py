from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    brand: str
    specification: Optional[str] = None
    unit: str
    price: float
    category: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    specification: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

class ProductOut(BaseModel):
    id: int
    name: str
    brand: str
    specification: Optional[str]
    unit: str
    price: float
    category: Optional[str]
    updated_at: datetime

    model_config = {"from_attributes": True}