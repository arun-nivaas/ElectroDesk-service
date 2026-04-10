from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
from src.backend.schemas.auth_schema import  TokenResponse, UserOut
from src.backend.core.config import settings
from src.backend.repositeries import user_repo


# ── Password validation ───────────────────────────────────

def _validate_password_length(password: str):
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must not exceed 72 characters")


# ── Password helpers ──────────────────────────────────────

def hash_password(plain_password: str) -> str:
    _validate_password_length(plain_password)
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(
        plain_password.encode("utf-8"), salt
    ).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    _validate_password_length(plain_password)
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ── JWT helpers ───────────────────────────────────────────

def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": expire})
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return None



# ── Core auth logic ───────────────────────────────────────

def login(db: Session, username: str, password: str) -> TokenResponse:
    user = user_repo.get_user_by_username(db, username)

    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid username or password")

    token = create_access_token(data={
        "sub": str(user.id),
        "username": user.username,
        "role": user.role
    })

    return TokenResponse(access_token=token)


def get_current_user(db: Session, token: str) -> UserOut:
    payload = decode_access_token(token)

    if not payload:
        raise ValueError("Invalid or expired token")

    user = user_repo.get_user_by_id(db, int(payload["sub"]))

    if not user:
        raise ValueError("User not found")

    return UserOut.model_validate(user)


def register_user(db: Session, name: str, username: str, password: str, role: str = "viewer") -> UserOut:
    existing = user_repo.get_user_by_username(db, username)

    if existing:
        raise ValueError("Username already exists")

    hashed = hash_password(password)
    user = user_repo.create_user(db, name=name, username=username, hashed_password=hashed, role=role)

    return UserOut.model_validate(user)