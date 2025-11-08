import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False) # Default role as per 1.1a
    is_verified = Column(Boolean, default=False, nullable=False) # Default unverified status as per 1.1a
    avatar_url = Column(String, nullable=True) # Added for Story 1.3a
    
    # Audited timestamps as per 1.1a Tech Specs
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<UserModel(id='{self.id}', email='{self.email}', role='{self.role}')>"