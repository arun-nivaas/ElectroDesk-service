from sqlalchemy.orm import Session
from src.backend.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from src.backend.schemas.auth_schema import UserOut
from src.backend.repositeries import product_repo
from typing import Dict, Any


def _require_admin(current_user: UserOut):
    if current_user.role != "admin":
        raise PermissionError("Only admin can perform this action")


# ── Viewer operations (no role restriction) ───────────────

def search_products(db: Session, query: str) -> list[ProductOut]:
    if not query or len(query.strip()) < 1:
        products = product_repo.get_all_products(db)
    else:
        products = product_repo.search_products(db, query.strip())
    return [ProductOut.model_validate(p) for p in products]


def get_product(db: Session, product_id: int) -> ProductOut:
    product = product_repo.get_product_by_id(db, product_id)
    if not product:
        raise ValueError(f"Product with id {product_id} not found")
    return ProductOut.model_validate(product)


# ── Admin only operations ─────────────────────────────────

def add_product(db: Session, data: ProductCreate, current_user: UserOut) -> ProductOut:
    _require_admin(current_user)
    product = product_repo.create_product(db, data)
    return ProductOut.model_validate(product)


def edit_product(db: Session, product_id: int, data: ProductUpdate, current_user: UserOut) -> ProductOut:
    _require_admin(current_user)
    product = product_repo.update_product(db, product_id, data)
    if not product:
        raise ValueError(f"Product with id {product_id} not found")
    return ProductOut.model_validate(product)


def remove_product(db: Session, product_id: int, current_user: UserOut) -> Dict[str,Any]:
    _require_admin(current_user)
    deleted = product_repo.delete_product(db, product_id)
    if not deleted:
        raise ValueError(f"Product with id {product_id} not found")
    return {"message": f"Product {product_id} deleted successfully"}