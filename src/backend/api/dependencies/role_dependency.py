from fastapi import Depends, HTTPException, status
from src.backend.schemas.auth_schema import UserOut
from src.backend.api.dependencies.auth_dependency import get_current_user


def require_admin(
    current_user: UserOut = Depends(get_current_user)
) -> UserOut:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_viewer(
    current_user: UserOut = Depends(get_current_user)
) -> UserOut:
    if current_user.role not in ["admin", "viewer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    return current_user