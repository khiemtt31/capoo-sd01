from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.data.user_repository import UserRepository
from app.domain.user_schema import UserCreate, UserResponse, UserUpdate, TokenResponse
from app.domain.user_model import UserModel
from app.core.utils import get_password_hash, verify_password
from app.core.security import create_access_token, create_refresh_token
from typing import Optional
import uuid

# Custom exception for duplicate email (Story 1.1a - 409 Conflict)
class DuplicateEmailError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "409_CONFLICT",
                    "message": "Email already registered.",
                    "correlationId": str(uuid.uuid4())
                }
            }
        )

class UserService:
    """
    Business Logic Layer for User operations.
    Handles registration, login, and profile management.
    """
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Handles user registration (Story 1.1a).
        - Enforce unique email constraint.
        - Hash password via bcrypt.
        - Persist user.
        """
        if self.user_repo.get_by_email(user_data.email):
            raise DuplicateEmailError()

        hashed_password = get_password_hash(user_data.password)
        
        # Persist user with default role and unverified status
        db_user = self.user_repo.create(user_data, hashed_password)
        
        # NOTE: Emit provisional registration event for downstream integrations (Story 1.1a)
        # Event emission logic placeholder would go here.

        return UserResponse.model_validate(db_user)

    def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
        """
        Authenticates user credentials (Story 1.2a).
        Returns UserModel if successful, None otherwise.
        """
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        
        # NOTE: Enforce verified-account flag check would go here (Story 1.2a)
        # For now, we allow login regardless of verification status.

        return user

    def login_user(self, email: str, password: str) -> TokenResponse:
        """
        Handles user login and token issuance (Story 1.2a).
        """
        user = self.authenticate_user(email, password)
        if not user:
            # Raise 401 Unauthorized using the standard error contract
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": {
                        "code": "401_UNAUTHORIZED",
                        "message": "Invalid credentials.",
                        "correlationId": str(uuid.uuid4())
                    }
                },
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Issue JWT access token and refresh token pair (Story 1.2a)
        access_token = create_access_token(data={"user_id": str(user.id), "role": user.role})
        refresh_token = create_refresh_token(data={"user_id": str(user.id)})
        
        # NOTE: Record authentication event in audit log (Story 1.2a)
        # Audit log logic placeholder would go here.

        return TokenResponse(
            accessToken=access_token,
            refreshToken=refresh_token,
            expiresIn=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 # seconds
        )

    def get_user_profile(self, user_id: uuid.UUID) -> Optional[UserModel]:
        """Retrieves a user profile by ID (Story 1.3a)."""
        return self.user_repo.get_by_id(user_id)

    def update_user_profile(self, user_id: uuid.UUID, update_data: UserUpdate) -> UserResponse:
        """
        Updates a user's profile (Story 1.3a).
        - Enforce email immutability (handled by schema not including email).
        """
        user = self.user_repo.get_by_id(user_id)
        if not user:
            # This should ideally be caught by authentication dependency, but included for robustness
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": "404_NOT_FOUND",
                        "message": "User not found.",
                        "correlationId": str(uuid.uuid4())
                    }
                }
            )
        
        updated_user = self.user_repo.update(user, update_data)
        
        # NOTE: Emit UserProfileUpdated event to event bus (Story 1.3a)
        # Event emission logic placeholder would go here.

        return UserResponse.model_validate(updated_user)