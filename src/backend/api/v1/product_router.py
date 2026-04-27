from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.backend.database.database import get_db
from src.backend.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from src.backend.schemas.auth_schema import UserOut
from src.backend.services import product_service
from src.backend.api.dependencies.auth_dependency import get_current_user
from src.backend.api.dependencies.role_dependency import require_admin

router = APIRouter()


@router.get("/", response_model=list[ProductOut])
def search_products(
    query: str = "",
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return product_service.search_products(db, query)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        return product_service.get_product(db, product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def add_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(require_admin)
):
    try:
        return product_service.add_product(db, data, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.put("/{product_id}", response_model=ProductOut)
def edit_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(require_admin)
):
    try:
        return product_service.edit_product(db, product_id, data, current_user)
    except (ValueError, PermissionError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{product_id}")
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(require_admin)
):
    try:
        return product_service.remove_product(db, product_id, current_user)
    except (ValueError, PermissionError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )