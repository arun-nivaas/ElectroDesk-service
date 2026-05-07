from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1)
    brand: str = Field(..., min_length=1)
    specification: Optional[str] = None
    unit: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    brand: Optional[str] = Field(None, min_length=1)
    specification: Optional[str] = None
    unit: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
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