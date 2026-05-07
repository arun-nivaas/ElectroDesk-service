from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.backend.schemas.auth_schema import TokenResponse, UserOut
from src.backend.services import auth_service
from src.backend.core.enums import UserRole
from src.backend.api.dependencies.auth_dependency import get_user_repo
from src.backend.interface.user_repo_interface import UserRepository

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(get_user_repo)
):
    try:
        return auth_service.login(repo, form_data.username, form_data.password)
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
    role: UserRole = UserRole.USER,
    repo: UserRepository = Depends(get_user_repo)
):
    try:
        return auth_service.register_user(repo, name, username, password, role)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )