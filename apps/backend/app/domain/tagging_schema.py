import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# --- Base Schemas ---

class TagBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    color_hex: Optional[str] = Field(None, max_length=7)
    description: Optional[str] = None
    workspace_id: uuid.UUID

class TaskTagBase(BaseModel):
    task_id: uuid.UUID
    tag_id: uuid.UUID

# --- Request Schemas (Input DTOs) ---

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color_hex: Optional[str] = Field(None, max_length=7)
    description: Optional[str] = None

class TaskTagCreate(TaskTagBase):
    pass

# --- Response Schemas (Output DTOs) ---

class TagResponse(TagBase):
    tag_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }

class TaskTagResponse(TaskTagBase):
    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: str,
        }