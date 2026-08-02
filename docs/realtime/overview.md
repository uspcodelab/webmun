# Real-time sessions

Active committee sessions use a WebSocket at `/ws/{session_id}`. The server is
authoritative: clients request actions and render the state it sends back.

## Connection and message flow

1. Connect to the session WebSocket.
2. Send `{ "access_token": "<Supabase JWT>" }` as the first message.
3. The backend verifies the token and resolves the user's assignment for that
   session.
4. On success, the server sends the current `SessionLiveState` snapshot.
5. Send event messages in the `{ "type": "...", "payload": { ... } }` form.
6. After a valid event, the server broadcasts the updated full snapshot to all
   connected clients.

The current protocol sends full snapshots, not deltas. Treat a received
snapshot as the current source of truth; do not locally apply an event to the
shared session store first.

## Event envelope

Every event has two fields:

```json
{
  "type": "JoinQueueEvent",
  "payload": {}
}
```

- `type` selects one supported event schema.
- `payload` contains only the data required by that event. It is `{}` for an
  event with no inputs.

The backend validates the envelope, the payload, the caller's role, and the
current session state before changing anything. A client must not supply its
own role or identity as authority.

## Where to look next

- [Events and payloads](events-and-payloads.md) is the searchable event
  reference for frontend and backend development.
- [Session state](session-state.md) describes the snapshot returned by the
  server.
