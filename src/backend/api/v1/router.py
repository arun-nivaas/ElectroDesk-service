from fastapi import APIRouter
from src.backend.api.v1 import auth_router, product_router

v1_router = APIRouter()

v1_router.include_router(auth_router.router,prefix="/auth", tags=["v1 - Auth"])
v1_router.include_router(product_router.router,prefix="/products", tags=["v1 - Products"])