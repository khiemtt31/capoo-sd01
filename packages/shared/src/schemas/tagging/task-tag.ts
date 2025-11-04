import { UUID } from '../common';

/**
 * Base interface for a TaskTag entity (link table).
 */
export interface TaskTag {
  task_id: UUID;
  tag_id: UUID;
}

/**
 * DTO for linking a Tag to a Task.
 */
export interface LinkTaskTagDto {
  task_id: UUID;
  tag_id: UUID;
}