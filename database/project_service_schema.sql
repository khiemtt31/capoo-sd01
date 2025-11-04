-- Schema for Project Service (PostgreSQL)

-- Projects table (Story 2.1)
CREATE TABLE projects (
    project_id UUID PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'Draft',
    workspace_id UUID NOT NULL, -- Assuming multi-tenant workspace scoping
    created_by UUID NOT NULL, -- References User Service user_id
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table (Story 2.2, 2.3)
CREATE TABLE tasks (
    task_id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(project_id) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL DEFAULT 'Medium',
    due_date DATE,
    assignee_id UUID, -- References User Service user_id
    status VARCHAR(50) NOT NULL DEFAULT 'To Do', -- (To Do, In Progress, Blocked, Done)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Task Status History (Story 2.3, AC 2)
CREATE TABLE task_history (
    history_id BIGSERIAL PRIMARY KEY,
    task_id UUID REFERENCES tasks(task_id) NOT NULL,
    changed_by UUID NOT NULL, -- References User Service user_id
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    reason TEXT, -- Required for 'Blocked' status (Story 2.3, AC 4)
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Project Membership (Story 2.1, AC 3)
CREATE TABLE project_members (
    project_id UUID REFERENCES projects(project_id) NOT NULL,
    user_id UUID NOT NULL, -- References User Service user_id
    member_role VARCHAR(50) NOT NULL, -- 'owner', 'contributor', 'viewer'
    PRIMARY KEY (project_id, user_id)
);