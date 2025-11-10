import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Base Schemas ---

class UserPreferenceBase(BaseModel):
    email_enabled: bool = True
    in_app_enabled: bool = True
    preferences: Optional[Dict[str, Any]] = None

class NotificationBase(BaseModel):
    user_id: uuid.UUID
    source_event: str = Field(max_length=50)
    content: str
    deep_link: Optional[str] = Field(None, max_length=255)
    is_read: bool = False

class EmailDeliveryLogBase(BaseModel):
    recipient_email: str = Field(max_length=255)
    event_type: str = Field(max_length=50)
    status: str = Field(max_length=50)
    failure_reason: Optional[str] = None

# --- Request Schemas (Input DTOs) ---

class UserPreferenceCreate(UserPreferenceBase):
    user_id: uuid.UUID

class UserPreferenceUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    in_app_enabled: Optional[bool] = None
    preferences: Optional[Dict[str, Any]] = None

class NotificationCreate(NotificationBase):
    pass

class EmailDeliveryLogCreate(EmailDeliveryLogBase):
    pass

# --- Response Schemas (Output DTOs) ---

class UserPreferenceResponse(UserPreferenceBase):
    user_id: uuid.UUID

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: str,
        }

class NotificationResponse(NotificationBase):
    notification_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }

class EmailDeliveryLogResponse(EmailDeliveryLogBase):
    log_id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }