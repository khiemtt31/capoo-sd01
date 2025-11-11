from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.data.user_repository import UserRepository
from app.services.user_service import UserService
from app.domain.user_schema import UserResponse, UserUpdate
from app.domain.user_model import UserModel
from app.domain.general_schema import GeneralResponse, SuccessResponse, ErrorResponse
from app.core.messages import MessageKeys, get_message

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
    response_model=GeneralResponse[UserResponse],
    summary="Retrieve current user profile (Story 1.3a)",
    description="Retrieves the profile of the authenticated user.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Unauthorized: Authentication required."
        }
    }
)
def get_profile(
    current_user: UserModel = Depends(get_current_user)
) -> GeneralResponse[UserResponse]:
    """
    GET /api/users/me
    """
    # The user model is already retrieved by the dependency, we just return it.
    user_response = UserResponse.model_validate(current_user)
    return SuccessResponse[UserResponse](
        message=get_message(MessageKeys.PROFILE_RETRIEVED_SUCCESS),
        data=user_response
    )

@router.patch(
    "/me",
    response_model=GeneralResponse[UserResponse],
    summary="Update current user profile (Story 1.3a)",
    description="Updates the name and avatarUrl of the authenticated user.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Unauthorized: Authentication required."
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Not Found: User not found (should be rare if authenticated)."
        }
    }
)
def update_profile(
    update_data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> GeneralResponse[UserResponse]:
    """
    PATCH /api/users/me
    """
    updated_user = user_service.update_user_profile(current_user.id, update_data)
    return SuccessResponse[UserResponse](
        message=get_message(MessageKeys.PROFILE_UPDATED_SUCCESS),
        data=updated_user
    )