from abc import ABC, abstractmethod
from typing import Optional, List
from src.backend.models.user import User
from src.backend.core.enums import UserRole

class UserRepository(ABC):

    @abstractmethod
    def get_user_by_username(self,username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(
        self,
        name: str,
        username: str,
        hashed_password: str,
        role: UserRole = UserRole.USER
    ) -> User:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass