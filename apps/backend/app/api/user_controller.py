from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.data.user_repository import UserRepository
from app.services.user_service import UserService
from app.domain.user_schema import UserResponse, UserUpdate
from app.domain.user_model import UserModel

router = APIRouter(
    prefix="/users",
    tags=["User Profile"],
)

# Dependency Injection for UserService
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repo = UserRepository(db)
    return UserService(user_repo)

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Retrieve current user profile (Story 1.3a)",
    description="Retrieves the profile of the authenticated user."
)
def get_profile(
    current_user: UserModel = Depends(get_current_user)
):
    """
    GET /api/users/me
    """
    # The user model is already retrieved by the dependency, we just return it.
    return current_user

@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile (Story 1.3a)",
    description="Updates the name and avatarUrl of the authenticated user."
)
def update_profile(
    update_data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    PATCH /api/users/me
    """
    return user_service.update_user_profile(current_user.id, update_data)