from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import bcrypt
from fastapi import HTTPException, status
from src.backend.schemas.auth_schema import TokenResponse, UserOut
from src.backend.core.config import settings
from src.backend.core.enums import UserRole
from src.backend.interface.user_repo_interface import UserRepository
from typing import Dict, Any


# ── Password helpers ──────────────────────────────────────

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(
        plain_password.encode("utf-8"), salt
    ).decode("utf-8")


def verify_password(plain_password: str, hashed_password: Any) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ── JWT helpers ───────────────────────────────────────────

def create_access_token(data: Dict[str, Any]) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": expire})
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


# ── Core auth logic ───────────────────────────────────────

def login(repo: UserRepository, username: str, password: str) -> TokenResponse:
    user = repo.get_user_by_username(username)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(data={
        "sub": str(user.id),
        "username": user.username,
        "role": user.role.value
    })

    return TokenResponse(access_token=token)


def get_current_user(repo: UserRepository, token: str) -> UserOut:
    payload = decode_access_token(token)

    user = repo.get_user_by_id(int(payload["sub"]))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserOut.model_validate(user)


def register_user(repo: UserRepository, name: str, username: str, password: str, role: UserRole = UserRole.USER) -> UserOut:
    existing = repo.get_user_by_username(username)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    hashed = hash_password(password)
    user = repo.create_user(name=name, username=username, hashed_password=hashed, role = role)

    return UserOut.model_validate(user)