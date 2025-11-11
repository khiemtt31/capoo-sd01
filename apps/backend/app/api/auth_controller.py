from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.data.user_repository import UserRepository
from app.services.user_service import UserService
from app.domain.user_schema import UserCreate, UserResponse, UserLogin, TokenResponse, TokenRefreshRequest
from app.domain.general_schema import GeneralResponse, SuccessResponse, ErrorResponse
from app.core.security import oauth2_scheme # Used for documentation purposes

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# Dependency Injection for UserService
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)

@router.post(
    "/register",
    response_model=GeneralResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="User Registration (Story 1.1a)",
    description="Creates a new user account, hashes the password, and persists the record.",
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "Conflict: Email already registered."
        }
    }
)
def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> GeneralResponse[UserResponse]:
    """
    POST /api/auth/register
    Successful registration returns 201 Created.
    """
    user = user_service.register_user(user_data)
    return SuccessResponse[UserResponse](
        message="User registered successfully.",
        data=user
    )

@router.post(
    "/login",
    response_model=GeneralResponse[TokenResponse],
    summary="User Login and Token Issuance (Story 1.2a)",
    description="Authenticates user credentials and returns JWT access and refresh tokens.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Unauthorized: Invalid credentials."
        }
    }
)
def login(
    user_data: UserLogin,
    user_service: UserService = Depends(get_user_service)
) -> GeneralResponse[TokenResponse]:
    """
    POST /api/auth/login
    Successful login returns 200 OK with tokens.
    """
    tokens = user_service.login_user(user_data.email, user_data.password)
    return SuccessResponse[TokenResponse](
        message="Login successful.",
        data=tokens
    )

@router.post(
    "/refresh",
    response_model=GeneralResponse[TokenResponse],
    summary="Token Refresh (Story 1.2b)",
    description="Exchanges a valid refresh token for a new access token and refresh token pair.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Unauthorized: Invalid or expired refresh token."
        }
    }
)
def refresh(
    refresh_request: TokenRefreshRequest,
    user_service: UserService = Depends(get_user_service)
) -> GeneralResponse[TokenResponse]:
    """
    POST /api/auth/refresh
    Successful refresh returns 200 OK with new tokens.
    """
    tokens = user_service.refresh_tokens(refresh_request.refresh_token)
    return SuccessResponse[TokenResponse](
        message="Token refresh successful.",
        data=tokens
    )