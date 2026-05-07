from src.backend.schemas.auth_schema import TokenResponse, UserOut
from src.backend.core.enums import UserRole
from src.backend.interface.user_repo_interface import UserRepository
from src.backend.utilis.jwt_helper import (hash_password, verify_password, create_access_token, decode_access_token)


def login(repo: UserRepository, username: str, password: str) -> TokenResponse:
    user = repo.get_user_by_username(username)

    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid username or password")

    token = create_access_token({
        "sub": str(user.id),
        "username": user.username,
        "role": user.role.value
    })

    return TokenResponse(access_token=token)


def get_current_user(repo: UserRepository, token: str) -> UserOut:
    payload = decode_access_token(token)

    user = repo.get_user_by_id(int(payload["sub"]))

    if not user:
        raise ValueError("User not found")

    return UserOut.model_validate(user)


def register_user(repo: UserRepository, name: str, username: str, password: str, role: UserRole = UserRole.USER) -> UserOut:
    existing = repo.get_user_by_username(username)

    if existing:
        raise ValueError("Username already exists")

    hashed = hash_password(password)
    user = repo.create_user(name=name, username=username, hashed_password=hashed, role = role)

    return UserOut.model_validate(user)