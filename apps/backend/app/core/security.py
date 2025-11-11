from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt, JWTError
from fastapi import Depends, status
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.domain.user_model import UserModel
from app.data.user_repository import UserRepository
from app.core.database import get_db
from sqlalchemy.orm import Session
import uuid

def decode_token(token: str) -> dict[str, Any]:
    """Decodes a JWT token and returns the payload, raising UnauthorizedException on failure."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise UnauthorizedException(detail="Invalid token or token expired.")

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
    payload = decode_token(token)
    user_id: str = payload.get("user_id")
    
    if user_id is None or payload.get("sub") != "access":
        raise UnauthorizedException(detail="Invalid access token payload.")

    user_repo = UserRepository(db)
    try:
        user = user_repo.get_by_id(uuid.UUID(user_id))
    except ValueError:
        # Handle case where user_id is not a valid UUID
        raise UnauthorizedException(detail="Invalid user ID in token.")
    
    if user is None:
        raise UnauthorizedException(detail="User not found.")
    
    return user