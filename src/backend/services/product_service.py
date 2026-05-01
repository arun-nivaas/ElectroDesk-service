from src.backend.interface.product_repo_interface import ProductRepository
from src.backend.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from src.backend.schemas.auth_schema import UserOut
from src.backend.core.enums import UserRole
from typing import Dict, Any


def _require_admin(current_user: UserOut):
    if current_user.role != UserRole.ADMIN:
        raise PermissionError("Only admin can perform this action")


# ── Viewer operations (no role restriction) ───────────────

def search_products(repo: ProductRepository, query: str) -> list[ProductOut]:
    if not query or len(query.strip()) < 1:
        products = repo.get_all_products()
    else:
        products = repo.search_products(query.strip())
    return [ProductOut.model_validate(p) for p in products]


def get_product(repo: ProductRepository, product_id: int) -> ProductOut:
    product = repo.get_product_by_id(product_id)
    if not product:
        raise ValueError(f"Product with id {product_id} not found")
    return ProductOut.model_validate(product)


# ── Admin only operations ─────────────────────────────────

def add_product(repo: ProductRepository, data: ProductCreate, current_user: UserOut) -> ProductOut:
    _require_admin(current_user)
    product = repo.create_product(data)
    return ProductOut.model_validate(product)


def edit_product(repo: ProductRepository, product_id: int, data: ProductUpdate, current_user: UserOut) -> ProductOut:
    _require_admin(current_user)
    product = repo.update_product(product_id, data)
    if not product:
        raise ValueError(f"Product with id {product_id} not found")
    return ProductOut.model_validate(product)


def remove_product(repo: ProductRepository, product_id: int, current_user: UserOut) -> Dict[str,Any]:
    _require_admin(current_user)
    deleted = repo.delete_product(product_id)
    if not deleted:
        raise ValueError(f"Product with id {product_id} not found")
    return {"message": f"Product {product_id} deleted successfully"}