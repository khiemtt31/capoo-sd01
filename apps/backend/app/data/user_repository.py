from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.domain.user_model import UserModel
from app.domain.user_schema import UserCreate, UserUpdate

class UserRepository:
    """
    Data Access Layer (Repository) for User operations.
    Handles persistence logic and mapping between models and database.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[UserModel]:
        """Retrieve a user by their email address."""
        return self.db.scalar(
            select(UserModel).where(UserModel.email == email)
        )

    def create(self, user_data: UserCreate, password_hash: str) -> UserModel:
        """Create a new user record."""
        db_user = UserModel(
            email=user_data.email,
            name=user_data.name,
            password_hash=password_hash,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user: UserModel, update_data: UserUpdate) -> UserModel:
        """Update an existing user record."""
        if update_data.name is not None:
            user.name = update_data.name
        if update_data.avatar_url is not None:
            user.avatar_url = update_data.avatar_url
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: uuid.UUID) -> Optional[UserModel]:
        """Retrieve a user by their ID."""
        return self.db.scalar(
            select(UserModel).where(UserModel.id == user_id)
        )