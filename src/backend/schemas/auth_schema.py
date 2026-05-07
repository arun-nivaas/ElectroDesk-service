from pydantic import BaseModel, field_validator,Field
from src.backend.core.enums import UserRole
from typing import Any


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1) 
    password: str = Field(..., min_length=4)

    @field_validator("password")
    @classmethod
    def password_length(cls, v: Any) -> Any:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 characters")
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    name: str
    username: str
    role: UserRole

    model_config = {"from_attributes": True}