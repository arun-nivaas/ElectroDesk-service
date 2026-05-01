from fastapi import APIRouter, Depends, HTTPException, status
from src.backend.api.dependencies.product_dependency import get_product_repo
from src.backend.interface.product_repo_interface import ProductRepository
from src.backend.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from src.backend.schemas.auth_schema import UserOut
from src.backend.services import product_service
from src.backend.api.dependencies.auth_dependency import get_current_user
from src.backend.api.dependencies.role_dependency import require_admin

router = APIRouter()


@router.get("/", response_model=list[ProductOut])
def search_products(
    query: str = "",
    repo: ProductRepository = Depends(get_product_repo),
    current_user: UserOut = Depends(get_current_user)
):
    return product_service.search_products(repo, query)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    repo: ProductRepository = Depends(get_product_repo),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        return product_service.get_product(repo, product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def add_product(
    data: ProductCreate,
    repo: ProductRepository = Depends(get_product_repo),
    current_user: UserOut = Depends(require_admin)
):
    try:
        return product_service.add_product(repo, data, current_user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.put("/{product_id}", response_model=ProductOut)
def edit_product(
    product_id: int,
    data: ProductUpdate,
    repo: ProductRepository = Depends(get_product_repo),
    current_user: UserOut = Depends(require_admin)
):
    try:
        return product_service.edit_product(repo, product_id, data, current_user)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.delete("/{product_id}")
def remove_product(
    product_id: int,
    repo: ProductRepository = Depends(get_product_repo),
    current_user: UserOut = Depends(require_admin)
):
   
    try:
        return product_service.remove_product(repo, product_id, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )