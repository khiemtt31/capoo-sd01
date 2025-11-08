import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# --- Base Schemas ---

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1)

# --- Request Schemas (Input DTOs) ---

class UserCreate(UserBase):
    """Schema for POST /api/auth/register (Story 1.1a)"""
    password: str = Field(min_length=8) # Assuming a minimum password length policy

class UserLogin(BaseModel):
    """Schema for POST /api/auth/login (Story 1.2a)"""
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """Schema for PATCH /api/users/me (Story 1.3a)"""
    name: Optional[str] = Field(None, min_length=1)
    avatar_url: Optional[str] = None # Placeholder for avatar pipeline

# --- Response Schemas (Output DTOs) ---

class UserResponse(UserBase):
    """Schema for successful registration response (Story 1.1a) and profile retrieval (Story 1.3a)"""
    id: uuid.UUID
    role: str
    is_verified: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Enable ORM mode for SQLAlchemy models
        json_encoders = {
            uuid.UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }

class TokenResponse(BaseModel):
    """Schema for successful login response (Story 1.2a)"""
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")
    expires_in: int

    class Config:
        populate_by_name = True # Allow field names to be populated by their aliases