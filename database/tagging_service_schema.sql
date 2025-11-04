-- Schema for Tagging Service (PostgreSQL)

-- Tags table (Story 5.1)
CREATE TABLE tags (
    tag_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    color_hex VARCHAR(7),
    description TEXT,
    workspace_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (workspace_id, name) -- Prevents duplicates within a workspace (Story 5.1, AC 1)
);

-- Link table for tasks and tags (Story 5.1)
CREATE TABLE task_tags (
    task_id UUID NOT NULL, -- References Project Service task_id
    tag_id UUID REFERENCES tags(tag_id) NOT NULL,
    PRIMARY KEY (task_id, tag_id)
);