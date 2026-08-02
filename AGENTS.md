# AGENTS root guide

## Architecture

- WebMUN is a FastAPI + React/Vite app for real-time MUNs over WebSockets.
- Supabase is used for durable data as direct PostgreSQL. Supabase Auth is used for signup/login.
- PostgreSQL stores durable committee/session data; `SessionLiveState` is the in-memory/persisted FSM state for an active session.
- The backend is authoritative: clients receive state snapshots and send events; authorization is resolved server-side from the websocket JWT and committee assignment.
- `representation_id` identifies a committee representation across backend state and frontend views.

## contributor guidance

- Read the nearest `AGENTS.md` before changing files; the backend and frontend have additional scoped rules.
- Keep changes focused. Preserve unrelated working-tree changes and do not mix refactors, dependency updates, and feature work in one commit.
- Treat `representation_id` as the delegation identity everywhere.
- For cross-boundary changes, verify the backend tests and the frontend build/typecheck. Report pre-existing failures separately.
- Inspect security advisories before changing dependencies. Do not run `npm audit fix --force` without approval and a review of the resulting version changes.
