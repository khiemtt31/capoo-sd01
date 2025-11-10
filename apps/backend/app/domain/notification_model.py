import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class UserPreferenceModel(Base):
    __tablename__ = "user_preferences"

    user_id = Column(UUID(as_uuid=True), primary_key=True) # References User Service user_id
    email_enabled = Column(Boolean, nullable=False, default=True)
    in_app_enabled = Column(Boolean, nullable=False, default=True)
    preferences = Column(JSON, nullable=True) # Stores granular preferences per event type

    def __repr__(self):
        return f"<UserPreferenceModel(user_id='{self.user_id}')>"

class NotificationModel(Base):
    __tablename__ = "notifications"

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # Changed from BIGSERIAL to UUID
    user_id = Column(UUID(as_uuid=True), nullable=False) # Recipient (References User Service user_id)
    source_event = Column(String(50), nullable=False) # e.g., 'TaskAssigned', 'CommentAdded'
    content = Column(Text, nullable=False)
    deep_link = Column(String(255), nullable=True) # Actionable link (Story 4.2, AC 4)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<NotificationModel(notification_id='{self.notification_id}', user_id='{self.user_id}')>"

class EmailDeliveryLogModel(Base):
    __tablename__ = "email_delivery_log"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # Changed from BIGSERIAL to UUID
    recipient_email = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False) # e.g., 'SENT', 'FAILED', 'RETRYING'
    failure_reason = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<EmailDeliveryLogModel(log_id='{self.log_id}', recipient_email='{self.recipient_email}')>"