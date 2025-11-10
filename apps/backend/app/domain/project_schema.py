import uuid
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field

# --- Base Schemas ---

class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = Field('Draft', max_length=50)
    workspace_id: uuid.UUID

class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    priority: str = Field('Medium', max_length=20)
    due_date: Optional[date] = None
    assignee_id: Optional[uuid.UUID] = None
    status: str = Field('To Do', max_length=50)

class TaskHistoryBase(BaseModel):
    changed_by: uuid.UUID
    old_status: Optional[str] = None
    new_status: str = Field(max_length=50)
    reason: Optional[str] = None

class ProjectMemberBase(BaseModel):
    user_id: uuid.UUID
    member_role: str = Field(max_length=50)

# --- Request Schemas (Input DTOs) ---

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = Field(None, max_length=50)
    workspace_id: Optional[uuid.UUID] = None # Should not be updated after creation

class TaskCreate(TaskBase):
    project_id: uuid.UUID

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, max_length=20)
    due_date: Optional[date] = None
    assignee_id: Optional[uuid.UUID] = None
    status: Optional[str] = Field(None, max_length=50)

class TaskHistoryCreate(TaskHistoryBase):
    task_id: uuid.UUID

class ProjectMemberCreate(ProjectMemberBase):
    project_id: uuid.UUID

# --- Response Schemas (Output DTOs) ---

class TaskHistoryResponse(TaskHistoryBase):
    history_id: uuid.UUID
    task_id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }

class TaskResponse(TaskBase):
    task_id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    history: List[TaskHistoryResponse] = [] # Nested history

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }

class ProjectMemberResponse(ProjectMemberBase):
    project_id: uuid.UUID

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: str,
        }

class ProjectResponse(ProjectBase):
    project_id: uuid.UUID
    created_by: uuid.UUID
    created_at: datetime
    tasks: List[TaskResponse] = [] # Nested tasks
    members: List[ProjectMemberResponse] = [] # Nested members

    class Config:
        from_attributes = True
        json_encoders = {
            uuid.UUID: str,
            datetime: lambda dt: dt.isoformat(),
        }