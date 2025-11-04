import { UUID } from '../common';

/**
 * Base interface for a Project Member entity (link table).
 */
export interface ProjectMember {
  project_id: UUID;
  user_id: UUID;
  member_role: string; // 'owner', 'contributor', 'viewer'
}

/**
 * DTO for adding a new Project Member.
 */
export interface AddProjectMemberDto {
  project_id: UUID;
  user_id: UUID;
  member_role: string;
}

/**
 * DTO for updating a Project Member's role.
 */
export interface UpdateProjectMemberDto {
  member_role: string;
}