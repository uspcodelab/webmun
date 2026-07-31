# Backend guidance

- `SessionLiveState` is the authoritative engine state. IDs in queues, speakers, votes, roll calls, motions, and questions are `representation_id` values.
- Authenticate websocket users into a server-built `SessionActor`; never trust a client-supplied delegation identity. Validate chair-selected target IDs against `state.delegations`.
- Keep `delegations` keyed by representation ID. Iterate with `.values()` only when context data is needed.
- State snapshots are persisted and reloaded. Make state-model changes deliberately and provide a migration/versioning path when stored snapshots would become incompatible.
- Run `cd backend && pytest -q` after backend behavior changes.
