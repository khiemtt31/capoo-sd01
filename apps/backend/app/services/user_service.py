from sqlalchemy.orm import Session
from app.data.user_repository import UserRepository
from app.domain.user_schema import UserCreate, UserResponse, UserUpdate, TokenResponse
from app.domain.user_model import UserModel
from app.core.utils import get_password_hash, verify_password
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.exceptions import ConflictException, UnauthorizedException, NotFoundException
from app.core.config import settings
from app.core.messages import MessageKeys
from typing import Optional
import uuid

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
            raise ConflictException(message_key=MessageKeys.EMAIL_ALREADY_REGISTERED)

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
            # Raise 401 Unauthorized using the custom exception
            raise UnauthorizedException(message_key=MessageKeys.INVALID_CREDENTIALS, headers={"WWW-Authenticate": "Bearer"})

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

    def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """
        Handles token refresh (Story 1.2b).
        Validates the refresh token and issues a new access/refresh token pair.
        """
        payload = decode_token(refresh_token)
        
        if payload.get("sub") != "refresh":
            raise UnauthorizedException(message_key=MessageKeys.INVALID_TOKEN)

        user_id_str: str = payload.get("user_id")
        if not user_id_str:
            raise UnauthorizedException(message_key=MessageKeys.INVALID_TOKEN)

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise UnauthorizedException(message_key=MessageKeys.INVALID_TOKEN)

        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedException(message_key=MessageKeys.USER_NOT_FOUND)

        # NOTE: In a real system, we would check if the refresh token is revoked here (Story 1.2b)
        
        # Issue new JWT access token and refresh token pair
        new_access_token = create_access_token(data={"user_id": str(user.id), "role": user.role})
        new_refresh_token = create_refresh_token(data={"user_id": str(user.id)})

        # NOTE: Record token refresh event in audit log (Story 1.2b)

        return TokenResponse(
            accessToken=new_access_token,
            refreshToken=new_refresh_token,
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
            raise NotFoundException(message_key=MessageKeys.USER_NOT_FOUND)
        
        updated_user = self.user_repo.update(user, update_data)
        
        # NOTE: Emit UserProfileUpdated event to event bus (Story 1.3a)
        # Event emission logic placeholder would go here.

        return UserResponse.model_validate(updated_user)