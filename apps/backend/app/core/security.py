from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from app.domain.user_model import UserModel
from app.data.user_repository import UserRepository
from app.core.database import get_db
from sqlalchemy.orm import Session
import uuid

# Custom exception for authentication failure (Story 1.2a - 401 Unauthorized)
class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
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

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "sub": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Creates a JWT refresh token (Story 1.2b)."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "sub": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Placeholder for OAuth2 scheme (FastAPI standard)
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")

def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
) -> UserModel:
    """
    Dependency function to retrieve the current authenticated user from the JWT token.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise InvalidCredentialsError()
        
        # Check token type (optional, but good practice)
        if payload.get("sub") != "access":
            raise InvalidCredentialsError()

    except JWTError:
        raise InvalidCredentialsError()

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(uuid.UUID(user_id))
    
    if user is None:
        raise InvalidCredentialsError()
    
    return user