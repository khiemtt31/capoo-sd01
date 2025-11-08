from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.data.user_repository import UserRepository
from app.services.user_service import UserService
from app.domain.user_schema import UserCreate, UserResponse, UserLogin, TokenResponse
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
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="User Registration (Story 1.1a)",
    description="Creates a new user account, hashes the password, and persists the record."
)
def register(
    user_data: UserCreate, 
    user_service: UserService = Depends(get_user_service)
):
    """
    POST /api/auth/register
    Successful registration returns 201 Created.
    """
    return user_service.register_user(user_data)

@router.post(
    "/login", 
    response_model=TokenResponse,
    summary="User Login and Token Issuance (Story 1.2a)",
    description="Authenticates user credentials and returns JWT access and refresh tokens."
)
def login(
    user_data: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """
    POST /api/auth/login
    Successful login returns 200 OK with tokens.
    """
    return user_service.login_user(user_data.email, user_data.password)

# NOTE: Refresh endpoint (Story 1.2b) and Profile endpoints (Story 1.3a) will be added next.