import { UUID } from '../common';

/**
 * Base interface for User Notification Preferences.
 */
export interface UserPreference {
  user_id: UUID;
  email_enabled: boolean;
  in_app_enabled: boolean;
  preferences: Record<string, unknown>; // JSONB
}

/**
 * DTO for creating or updating User Preferences.
 * user_id is typically derived from the authenticated user, so it's omitted here.
 */
export interface UpdateUserPreferenceDto {
  email_enabled?: boolean;
  in_app_enabled?: boolean;
  preferences?: Record<string, unknown>;
}