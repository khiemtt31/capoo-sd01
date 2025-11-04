import { UUID, Timestamp } from '../common';

/**
 * Base interface for In-App Notifications.
 */
export interface Notification {
  notification_id: number; // BIGSERIAL
  user_id: UUID; // Recipient
  source_event: string; // e.g., 'TaskAssigned', 'CommentAdded'
  content: string;
  deep_link: string | null;
  is_read: boolean;
  created_at: Timestamp;
}

/**
 * DTO for updating a Notification (e.g., marking as read).
 */
export interface UpdateNotificationDto {
  is_read?: boolean;
}