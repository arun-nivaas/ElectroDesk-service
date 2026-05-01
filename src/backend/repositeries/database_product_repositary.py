from sqlalchemy.orm import Session
from src.backend.models.products import Product
from src.backend.schemas.product_schema import ProductCreate, ProductUpdate
from src.backend.interface.product_repo_interface import ProductRepository

class DatabaseProductRepository(ProductRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self):
        return self.db.query(Product).order_by(Product.name).all()


    def search_products(self, query: str) -> list[Product]:
        search_term = f"%{query}%"
        return (
            self.db.query(Product)
            .filter(
                Product.name.ilike(search_term)
                | Product.brand.ilike(search_term)
                | Product.specification.ilike(search_term)
                | Product.category.ilike(search_term)
            )
            .order_by(Product.name)
            .all()
        )


    def get_product_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()


    def create_product(self, data: ProductCreate) -> Product:
        product = Product(**data.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product


    def update_product(self, product_id: int, data: ProductUpdate) -> Product | None:
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        updated_fields = data.model_dump(exclude_unset=True)
        for field, value in updated_fields.items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product


    def delete_product(self, product_id: int) -> bool:
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.commit()
        return True