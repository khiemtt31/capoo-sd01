-- Schema for User Service (PostgreSQL)

-- Table for user roles (Admin, Project Manager, Team Member)
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL -- 'Admin', 'PM', 'TM'
);

-- Users table (Story 1.1, 1.3)
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(255),
    role_id INTEGER REFERENCES roles(role_id) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE, -- For deactivation (Story 1.2)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit trail for role changes and deactivations (Story 1.2, AC 4)
CREATE TABLE user_audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) NOT NULL,
    actor_id UUID NOT NULL, -- User who performed the action
    action_type VARCHAR(50) NOT NULL, -- e.g., 'ROLE_CHANGE', 'DEACTIVATION'
    details JSONB, -- Stores old_role, new_role, reason, etc.
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);