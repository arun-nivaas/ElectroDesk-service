from fastapi import Depends
from sqlalchemy.orm import Session
from src.backend.interface.product_repo_interface import ProductRepository
from src.backend.database.database import get_db
from src.backend.repositeries.database_product_repositary import DatabaseProductRepository

def get_product_repo(db: Session = Depends(get_db)) -> ProductRepository:
    return DatabaseProductRepository(db)