from sqlalchemy.orm import Session
from src.backend.models.products import Product
from src.backend.schemas.product_schema import ProductCreate, ProductUpdate


def get_all_products(db: Session) -> list[Product]:
    return db.query(Product).order_by(Product.name).all()


def search_products(db: Session, query: str) -> list[Product]:
    search_term = f"%{query}%"
    return (
        db.query(Product)
        .filter(
            Product.name.ilike(search_term)
            | Product.brand.ilike(search_term)
            | Product.specification.ilike(search_term)
            | Product.category.ilike(search_term)
        )
        .order_by(Product.name)
        .all()
    )


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, data: ProductUpdate) -> Product | None:
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    updated_fields = data.model_dump(exclude_unset=True)
    for field, value in updated_fields.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    product = get_product_by_id(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True