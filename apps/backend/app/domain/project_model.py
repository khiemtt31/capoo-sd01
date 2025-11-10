import uuid
from datetime import datetime, date, timezone
from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProjectModel(Base):
    __tablename__ = "projects"

    project_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False, default='Draft')
    workspace_id = Column(UUID(as_uuid=True), nullable=False) # Assuming multi-tenant workspace scoping
    created_by = Column(UUID(as_uuid=True), nullable=False) # References User Service user_id
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    tasks = relationship("TaskModel", back_populates="project")
    members = relationship("ProjectMemberModel", back_populates="project")

    def __repr__(self):
        return f"<ProjectModel(project_id='{self.project_id}', name='{self.name}')>"

class TaskModel(Base):
    __tablename__ = "tasks"

    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.project_id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), nullable=False, default='Medium')
    due_date = Column(Date, nullable=True)
    assignee_id = Column(UUID(as_uuid=True), nullable=True) # References User Service user_id
    status = Column(String(50), nullable=False, default='To Do') # (To Do, In Progress, Blocked, Done)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    project = relationship("ProjectModel", back_populates="tasks")
    history = relationship("TaskHistoryModel", back_populates="task")
    task_tags = relationship("TaskTagModel", back_populates="task")

    def __repr__(self):
        return f"<TaskModel(task_id='{self.task_id}', title='{self.title}')>"

class TaskHistoryModel(Base):
    __tablename__ = "task_history"

    history_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # Changed from BIGSERIAL to UUID
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.task_id"), nullable=False)
    changed_by = Column(UUID(as_uuid=True), nullable=False) # References User Service user_id
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    reason = Column(Text, nullable=True) # Required for 'Blocked' status (Story 2.3, AC 4)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    task = relationship("TaskModel", back_populates="history")

    def __repr__(self):
        return f"<TaskHistoryModel(history_id='{self.history_id}', task_id='{self.task_id}')>"

class ProjectMemberModel(Base):
    __tablename__ = "project_members"

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.project_id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), primary_key=True) # References User Service user_id
    member_role = Column(String(50), nullable=False) # 'owner', 'contributor', 'viewer'

    project = relationship("ProjectModel", back_populates="members")

    def __repr__(self):
        return f"<ProjectMemberModel(project_id='{self.project_id}', user_id='{self.user_id}')>"