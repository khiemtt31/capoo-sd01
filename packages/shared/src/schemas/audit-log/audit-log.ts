import { UUID, Timestamp } from '../common';

/**
 * Complex type for detailed log information, modeled as a generic key-value map.
 */
export type AuditLogDetails = Record<string, unknown>;

/**
 * Represents a read-only entry in the Audit Log.
 */
export interface AuditLogEntry {
  Timestamp: Timestamp;
  Service: string;
  EventType: string;
  Severity: string;
  Message: string;
  ActorId?: UUID;
  TargetId?: UUID;
  Details?: AuditLogDetails;
}