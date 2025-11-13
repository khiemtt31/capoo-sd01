# Sprint 01: Core User Foundation (Backend)

**Goal:** Establish the foundational user management system, allowing users to register, log in, and manage their basic profile information. This sprint is critical for enabling all subsequent application features.  
**Status:** Done ([DONE])
**Duration:** 10 working days  
**Total Story Points:** 45

## Sprint Scope and Alignment
- Delivers the minimum viable identity layer required by the User Management epic in [planning/1_BUSINESS_REQUIREMENTS.md](capoo-sd01-planning/1_BUSINESS_REQUIREMENTS.md).
- Enables downstream epics (Project Tracking, Notifications, Tagging) by providing authenticated identity, session issuance, and profile context.
- Operates within the modular monolith baseline described in [planning/0_HIGHLEVEL_ARCHITECTURE.md](capoo-sd01-planning/0_HIGHLEVEL_ARCHITECTURE.md), keeping auth, user, and profile concerns modular yet deployable as a single service.
- Details Design should be mapping to schemas [database/] and Developement is about schema-driven architecture (using zod)

## Non-Goals
- OAuth or social login integrations.
- Multi-factor authentication flows.
- Administrative user management UI.
- Production-grade email verification or transactional email delivery.
- Notification channels beyond registration/login confirmation hooks.
- Advanced analytics dashboards beyond auth observability baselines.

## Sprint Backlog Summary
| Story | Description | Story Points |
| --- | --- | --- |
| 1.1a | Registration API foundation (validation, persistence, hashing) | 8 |
| 1.1b | Registration SPA flow and UX integration | 5 |
| 1.2a | Login API and token issuance | 8 |
| 1.2b | Session lifecycle, refresh, and secure key management | 5 |
| 1.3a | Profile API and domain events | 8 |
| 1.3b | Profile UI and avatar pipeline | 6 |
| 1.4 | Observability, audit logging, and alerting | 5 |

_Total Story Points: 45 (all stories sized 5–8 SP to maintain flow and inspectability)._

## Standard Error Response Contract
All endpoints introduced in this sprint return errors using the format:

```json
{
  "error": {
    "code": "HTTP_STATUS",
    "message": "Human readable summary",
    "correlationId": "uuid-v4"
  }
}
```

Error payloads include localized messages at the client layer while keeping codes consistent for monitoring.

## Story Details

### Story 1.1a Registration API Foundation (8 SP)
- **User Story:** As a new user, I want to sign up for an account using my email and password so that I can access the application.
- **Business Value:** Unlocks self-service onboarding and establishes secure identity records.
- **Functions:**
  - Validate incoming payload (name, email, password) against policy.
  - Enforce unique email constraint scoped to workspace.
  - Hash passwords via bcrypt before persistence.
  - Persist user with default role and unverified status.
  - Emit provisional registration event for downstream integrations.
- **Acceptance Tests:**
  - Missing fields and weak passwords return `400 Bad Request`.
  - Duplicate email returns `409 Conflict` with error schema.
  - Successful registration returns `201 Created` and persists hashed password only.
  - Database migration verified via automated test snapshot.
- **Tech Specs:**
  - `POST /api/auth/register` with `{ "name": string, "email": string, "password": string }`.
  - Response `201 Created` with `{ "user": { "id": string, "name": string, "email": string, "role": string, "isVerified": boolean } }`.
  - Error responses conform to standard error contract.
  - Database migration introduces `users` table with audited timestamps.
- **Definition of Done:**
  - Unit and integration tests covering happy/sad paths.
  - OpenAPI documentation updated.
  - Audit log entry created for registration attempts.

### Story 1.1b Registration SPA Flow and UX Integration (5 SP)
- **User Story:** As a new user, I want a clear registration experience so that I can create an account without friction.
- **Business Value:** Converts registration API capability into a usable experience, improving activation rate.
- **Functions:**
  - Build Next.js registration page with client-side validation and error surfacing.
  - Integrate with `POST /api/auth/register`, handling success, 4xx, and 5xx flows.
  - Display success state and redirect to login screen.
  - Implement password strength meter aligning with backend policy.
- **Acceptance Tests:**
  - Cypress e2e test covering complete registration journey.
  - UI prevents submission with invalid data and shows inline errors.
  - Success path navigates to login with confirmation toast.
- **Tech Specs:**
  - Form-level validation mirrors backend rules to reduce round trips.
  - Error contract from API mapped to friendly messaging.
- **Definition of Done:**
  - UI reviewed for accessibility (labels, focus order, contrast).
  - Responsiveness validated on mobile and desktop breakpoints.
  - Analytics event `registration_attempted` emitted with correlation ID.

### Story 1.2a Login API and Token Issuance (8 SP)
- **User Story:** As a returning user, I want to log in with my credentials so that I can access my projects and tasks.
- **Business Value:** Provides secure access control and session establishment.
- **Functions:**
  - Authenticate credentials against stored password hash.
  - Issue JWT access token (RS256) and refresh token pair with role claim.
  - Enforce verified-account flag, with Sprint 01 toggle to bypass if verification incomplete.
  - Record authentication event in audit log.
- **Acceptance Tests:**
  - Valid credentials return `200 OK` with tokens.
  - Invalid password returns `401 Unauthorized` using standard error contract.
  - Locked or unverified accounts return appropriate `403 Forbidden`.
- **Tech Specs:**
  - `POST /api/auth/login` payload `{ "email": string, "password": string }`.
  - Success response `{ "accessToken": string, "refreshToken": string, "expiresIn": number }`.
  - JWT signed with RS256 using private key stored in HashiCorp Vault.
- **Definition of Done:**
  - Contract tests verifying token structure and claims.
  - API gateway routes configured.
  - Observability dashboard includes login latency and failure metrics.

### Story 1.2b Session Lifecycle and Secure Key Management (5 SP)
- **User Story:** As a platform administrator, I want secure token refresh and rotation so that user sessions remain reliable and safe.
- **Business Value:** Reduces security risk by handling session renewal and secret governance.
- **Functions:**
  - Implement `POST /api/auth/refresh` to issue new token pair.
  - Store refresh tokens with ability to revoke (e.g., Redis or database flag).
  - Provision HashiCorp Vault namespace for auth service secrets.
  - Generate RS256 key pair and document rotation cadence.
- **Acceptance Tests:**
  - Valid refresh token returns new pair (`200 OK`).
  - Revoked or expired token returns `401 Unauthorized`.
  - Vault integration confirmed via integration test hitting mock Vault.
- **Tech Specs:**
  - Secrets retrieved from Vault using service account identity.
  - Rotation playbook captured in README.
  - Refresh endpoint includes correlation ID in responses.
- **Definition of Done:**
  - Manual rotation rehearsal executed and logged.
  - Monitoring alert configured for refresh failure spikes.

### Story 1.3a Profile API and Domain Events (8 SP)
- **User Story:** As a user, I want to manage my profile so my teammates can identify me correctly.
- **Business Value:** Ensures collaboration surfaces display accurate user data.
- **Functions:**
  - `GET /api/users/me` to retrieve profile.
  - `PATCH /api/users/me` to update name and `avatarUrl`.
  - Enforce email immutability; route change requests to admin workflow.
  - Emit `UserProfileUpdated` event to event bus.
- **Acceptance Tests:**
  - Authenticated requests succeed; unauthenticated return `401 Unauthorized`.
  - Invalid avatar URLs return `400 Bad Request`.
  - Event emitted with correct payload verified via contract test.
- **Tech Specs:**
  - DTO includes `id`, `name`, `email`, `role`, `avatarUrl`, timestamps.
  - Error responses follow standard schema.
  - Event published to RabbitMQ topic `user.profile.updated`.
- **Definition of Done:**
  - API docs updated with request/response schemas.
  - Backwards compatibility reviewed for future service extraction.
  - Audit trail records profile updates.

### Story 1.3b Profile UI and Avatar Pipeline (6 SP)
- **User Story:** As a user, I want an intuitive profile page so that I can view and update my personal details effortlessly.
- **Business Value:** Converts profile API capability into UX, reinforcing user trust and recognition.
- **Functions:**
  - Build Next.js profile page displaying current data and avatar preview.
  - Implement avatar upload component with client-side size/type validation.
  - Integrate with object storage stub (local filesystem) for Sprint 01.
  - Provide optimistic UI updates with rollback on failure.
- **Acceptance Tests:**
  - e2e test covering profile view and update flows.
  - Avatar uploads exceeding size limit produce UI error without hitting API.
  - Updated display name appears in task assignments (regression check).
- **Tech Specs:**
  - Utilize signed URL workflow placeholder for future storage provider.
  - Store avatar metadata referencing object storage location.
- **Definition of Done:**
  - Accessibility checks (keyboard navigation, alt text) complete.
  - Responsive layout verified.
  - Release notes include user-facing summary.

### Story 1.4 Observability, Audit Logging, and Alerting (5 SP)
- **User Story:** As an operator, I need insight into authentication health so that I can respond to issues quickly.
- **Business Value:** Provides operational guardrails and compliance trail from first release.
- **Functions:**
  - Instrument registration, login, refresh, and profile endpoints with OpenTelemetry traces, metrics, and structured logs.
  - Build Grafana dashboard visualizing success rates, latency, error codes.
  - Configure alerts for authentication failure spikes and refresh error rates.
  - Ensure all auth events generate audit log entries with correlation IDs.
- **Acceptance Tests:**
  - Observability smoke test confirms metrics exposed.
  - Alert configurations tested via simulated failures.
  - Audit log entries sampled for completeness.
- **Tech Specs:**
  - Metrics exported to Prometheus (`auth_request_total`, `auth_request_duration_seconds`).
  - Logs ingested into centralized observability stack with correlation ID passthrough.
- **Definition of Done:**
  - Dashboard link included in runbook.
  - On-call playbook drafted for major auth incidents.
  - Compliance checklist for logging signed off.

## Checkpoints and Milestones
| Code | Target Day | Scope | Exit Criteria | Progress Target |
| --- | --- | --- | --- | --- |
| CP-1 | Day 2 | Registration foundations | Stories 1.1a + 1.1b development complete and merged; registration e2e happy path green. | ≥ 25% (11 SP) |
| CP-2 | Day 5 | Auth flows solidified | Stories 1.2a + 1.2b complete; login and refresh journeys passing automated suites; Vault integrated. | ≥ 55% (25 SP) |
| CP-3 | Day 8 | Profile experience delivered | Stories 1.3a + 1.3b complete; profile UI validated; avatar pipeline working with stub storage. | ≥ 85% (38 SP) |
| CP-4 | Day 10 | Operational readiness | Story 1.4 complete; dashboards live; alert rehearsal executed; release artifacts finalized. | 100% (45 SP) |

## Task Checklist (No Story Points)
**Backend**
- [x] Implement user entity, repository, migrations, and password policy utilities.
- [x] Develop registration, login, refresh, profile endpoints with validation.
- [x] Integrate HashiCorp Vault for RS256 key pair storage and retrieval.
- [x] Emit domain events and audit logs for registration and profile updates.

**Frontend**
- [x] Create user context with zod for authentication and others.
- [x] Auth must seperate auth / un-auth path.
- [x] Create proxy to handle route checking for public/private paths.
- [x] Enhance UI for signup, login and dashboard.
- [x] Build registration page with form validation and success/error states.
- [x] Implement login page with session handling and token storage strategy.
- [x] Create profile page with editable fields, avatar upload, and optimistic updates.
- [x] Connect UI flows to telemetry (analytics events, correlation IDs).

**Infrastructure & QA**
- [x] Configure automated test suites (unit, integration, e2e) for new flows.
- [x] Set up Grafana dashboards, Prometheus metrics, and alert rules.
- [x] Document secret rotation playbook and incident response steps.
- [x] Update release notes and developer onboarding guides.

## Progress Tracking Guidance
1. Track progress by completed story points; each story completion releases its assigned SP.  
   `Progress % = (Completed Story Points ÷ 45) × 100`
2. Update progress summaries at each checkpoint, noting blockers, owner, and mitigation.
3. Maintain daily burndown by remaining story points.
4. Use task checklist for coordination without affecting SP metrics.

## Metrics and Monitoring
- Registration completion rate ≥ 90% without manual intervention.
- Authentication latency ≤ 500 ms p95.
- Token refresh success rate ≥ 98%.
- Profile update latency ≤ 400 ms p95.
- Audit log coverage 100% for auth-related events.
- Alert response time: initial acknowledgement within 15 minutes during support hours.

## Dependencies and Assumptions
- HashiCorp Vault (or AWS Secrets Manager equivalent) accessible for secret storage.
- Feature flag controls email verification enforcement until email provider integration lands.
- Object storage stub available (local filesystem or MinIO) with clear swap interface.
- CI/CD pipeline runs lint, unit, integration, and e2e suites on merge.
- API gateway routing rules updated in tandem with backend deployments.

## Risks and Mitigations
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Vault provisioning delay | Blocks token issuance | Coordinate with platform team ahead of Sprint start; temporarily use local Vault dev server with manual approval gate. |
| Avatar storage complexity | Slows profile delivery | Start with stub provider and abstract storage interface for future swap; scope creep flagged in Non-Goals. |
| Password policy changes mid-sprint | Rework UI and backend validation | Lock policy with security team in Sprint planning; document in shared configuration. |
| Insufficient frontend resourcing | UI stories slip | Pair backend/frontend teams on each story; pull in additional UI support if CP-2 misses target. |

## System Flow Reference
```mermaid
graph TD
    subgraph Client
        RegistrationSPA[Registration SPA]
        LoginSPA[Login SPA]
        ProfileSPA[Profile SPA]
    end
    subgraph API
        AuthRegister[POST /api/auth/register]
        AuthLogin[POST /api/auth/login]
        AuthRefresh[POST /api/auth/refresh]
        ProfileGet[GET /api/users/me]
        ProfilePatch[PATCH /api/users/me]
    end
    subgraph Services
        UserService[User Service]
        Vault[Vault Keys]
        AuditLog[Audit Log]
        EventBus[Event Bus]
        Storage[Avatar Storage Stub]
    end
    RegistrationSPA --> AuthRegister
    AuthRegister --> UserService
    AuthRegister --> AuditLog
    AuthRegister --> EventBus
    LoginSPA --> AuthLogin
    AuthLogin --> Vault
    AuthLogin --> UserService
    AuthLogin --> AuditLog
    LoginSPA --> AuthRefresh
    AuthRefresh --> Vault
    AuthRefresh --> UserService
    AuthRefresh --> AuditLog
    ProfileSPA --> ProfileGet
    ProfileSPA --> ProfilePatch
    ProfileGet --> UserService
    ProfilePatch --> UserService
    ProfilePatch --> Storage
    ProfilePatch --> EventBus
    ProfilePatch --> AuditLog