# HTTP API

This is the target API for the conference and committee refactor. It records
what exists today, but target routes are not implemented yet.

Use `/api/v1` for application routes and keep `/health` unversioned. Protected
HTTP requests use `Authorization: Bearer <Supabase JWT>`. The backend resolves
the caller and all permissions; `representation_id` is never client-provided
proof of identity.

Return `201` for creation, `204` for deletion, `401` for missing/invalid
authentication, `403` for insufficient permission, `404` for unavailable
resources, and `409` for invalid lifecycle transitions.

## Current routes

- `GET /health` — health check.
- `POST /sessions` — creates a planned session from `{ committee_id, name }`;
  chair only.
- `POST /sessions/{session_id}/activate` — activates a planned session;
  chair only.
- `GET /access/sessions/{session_id}/me` — returns the caller's role and
  `representation_id`.
- `WS /sessions/{session_id}/ws` — authenticates from its first message and
  exchanges procedure events and `SessionLiveState` snapshots.

## Target routes

### Identity and conferences

- `GET /health` — liveness/readiness probe.
- `GET /api/v1/me` — application profile and conferences visible to the
  current user.
- `GET` / `POST /api/v1/conferences` — list visible conferences / create one.
- `GET` / `PATCH` / `DELETE /api/v1/conferences/{conference_id}` — read,
  update, or delete a conference.

### Committees and assignments

- `GET` / `POST /api/v1/conferences/{conference_id}/committees` — list or
  create conference committees.
- `GET` / `PATCH` / `DELETE /api/v1/committees/{committee_id}` — read, update,
  or delete one committee.
- `GET` / `PUT /api/v1/committees/{committee_id}/seats` — read or atomically
  replace the representation-to-seat map.
- `GET` / `POST /api/v1/committees/{committee_id}/assignments` — list or add
  committee assignments.
- `PATCH` / `DELETE
  /api/v1/committees/{committee_id}/assignments/{user_id}` — change or remove
  an assignment.

Only a conference owner/admin may manage conference data and assignments. A
delegate assignment must reference a representation seated in that committee;
a chair assignment has no `representation_id`.

### Sessions and live procedure

- `GET` / `POST /api/v1/committees/{committee_id}/sessions` — list or create
  planned sessions; creation requires a committee chair.
- `GET` / `PATCH` / `DELETE /api/v1/sessions/{session_id}` — read, rename or
  transition, or delete/cancel a session when its lifecycle allows it.
- `GET /api/v1/sessions/{session_id}/me` — current caller's session access.
- `GET /api/v1/sessions/{session_id}/state` — optional chair-only persisted
  snapshot for recovery/debugging.
- `WS /api/v1/sessions/{session_id}/ws` — live events and authoritative
  snapshots. This is intentionally not REST.

Use `PATCH { "status": "active" }` to request activation. The server must
call the activation service and reject invalid transitions with `409`; it must
not allow status changes to bypass lifecycle rules.

## Before implementation

- Add OpenAPI request/response schemas and regenerate frontend types after
  every backend contract change.
- Implement conference membership/profile data before adding conference-wide
  participant or team endpoints. Do not overload `committee_assignments`.
- Add committee metadata (`acronym`, `type`, `colour`, and optional asset
  reference) before making the committee dashboard fields writable.
- Decide object storage and authorization before adding document upload or
  download endpoints. Store asset IDs/URLs, never browser `data:` URLs.
- Move existing routes behind compatibility aliases only if a released client
  needs them; mark aliases deprecated and remove them at the next version
  boundary.
