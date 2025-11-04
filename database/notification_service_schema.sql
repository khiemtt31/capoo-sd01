-- Schema for Notification Service (PostgreSQL)

-- User Notification Preferences (Story 4.1, AC 4; Story 4.2, AC 2)
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY, -- References User Service user_id
    email_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    in_app_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    preferences JSONB -- Stores granular preferences per event type
);

-- In-App Notifications (Story 4.1)
CREATE TABLE notifications (
    notification_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL, -- Recipient (References User Service user_id)
    source_event VARCHAR(50) NOT NULL, -- e.g., 'TaskAssigned', 'CommentAdded'
    content TEXT NOT NULL,
    deep_link VARCHAR(255), -- Actionable link (Story 4.2, AC 4)
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Email Delivery Log (Story 4.2, AC 3)
CREATE TABLE email_delivery_log (
    log_id BIGSERIAL PRIMARY KEY,
    recipient_email VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL, -- e.g., 'SENT', 'FAILED', 'RETRYING'
    failure_reason TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);