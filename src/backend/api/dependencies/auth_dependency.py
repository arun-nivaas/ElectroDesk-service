from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.backend.database.database import get_db
from src.backend.schemas.auth_schema import UserOut
from src.backend.services import auth_service
from src.backend.repositeries.database_user_repositary import DatabaseUserRepository
from src.backend.interface.user_repo_interface import UserRepository


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return DatabaseUserRepository(db)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: UserRepository = Depends(get_user_repo)
) -> UserOut:
    try:
        return auth_service.get_current_user(repo, token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )