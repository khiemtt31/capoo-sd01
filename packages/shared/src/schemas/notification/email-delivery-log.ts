import { Timestamp } from '../common';

/**
 * Base interface for Email Delivery Log entries.
 */
export interface EmailDeliveryLog {
  log_id: number; // BIGSERIAL
  recipient_email: string;
  event_type: string;
  status: string; // e.g., 'SENT', 'FAILED', 'RETRYING'
  failure_reason: string | null;
  timestamp: Timestamp;
}