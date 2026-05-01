from abc import ABC, abstractmethod
from typing import List, Optional
from src.backend.models.products import Product
from src.backend.schemas.product_schema import ProductCreate, ProductUpdate

class ProductRepository(ABC):

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def search_products(self, query: str) -> List[Product]:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def create_product(self, data: ProductCreate) -> Product:
        pass

    @abstractmethod
    def update_product(self, product_id: int, data: ProductUpdate) -> Optional[Product]:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        pass