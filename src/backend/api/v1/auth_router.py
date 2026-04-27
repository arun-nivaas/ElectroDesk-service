from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.backend.database.database import get_db
from src.backend.schemas.auth_schema import TokenResponse, UserOut
from src.backend.services import auth_service

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        return auth_service.login(db, form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/register", response_model=UserOut)
def register(
    name: str,
    username: str,
    password: str,
    role: str = "viewer",
    db: Session = Depends(get_db)
):
    try:
        return auth_service.register_user(db, name, username, password, role)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )