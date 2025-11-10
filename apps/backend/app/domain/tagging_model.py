import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.domain.project_model import TaskModel # Import TaskModel

class TagModel(Base):
    __tablename__ = "tags"

    tag_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    color_hex = Column(String(7), nullable=True)
    description = Column(Text, nullable=True)
    workspace_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    task_tags = relationship("TaskTagModel", back_populates="tag")

    __table_args__ = (UniqueConstraint('workspace_id', 'name', name='_workspace_name_uc'),)

    def __repr__(self):
        return f"<TagModel(tag_id='{self.tag_id}', name='{self.name}')>"

class TaskTagModel(Base):
    __tablename__ = "task_tags"

    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.task_id"), primary_key=True) # References Project Service task_id
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.tag_id"), primary_key=True)

    tag = relationship("TagModel", back_populates="task_tags")
    task = relationship("TaskModel", back_populates="task_tags")

    def __repr__(self):
        return f"<TaskTagModel(task_id='{self.task_id}', tag_id='{self.tag_id}')>"