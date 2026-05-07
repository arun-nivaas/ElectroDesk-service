from sqlalchemy.orm import Session
from src.backend.models.user import User
from src.backend.core.enums import UserRole
from src.backend.interface.user_repo_interface import UserRepository


class DatabaseUserRepository(UserRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self,username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()


    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()


    def create_user(self, name: str, username: str, hashed_password: str, role: UserRole = UserRole.USER) -> User:
        user = User(
            name=name,
            username=username,
            hashed_password=hashed_password,
            role=role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()