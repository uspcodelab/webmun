# Consuming the application API

Supabase provides authentication. FastAPI owns WebMUN data, permissions, and
business rules. The target route map is in
[HTTP API](../backend/http-api.md).

## HTTP

- Use `apiFetch` from `src/lib/api.ts` for protected requests. It supplies the
  bearer token from the current Supabase session.
- Do not hard-code `http://localhost:8000`; use `VITE_API_URL` through the
  shared client.
- Check `response.ok`. A `fetch` promise resolves even for HTTP error
  responses; show server validation messages where possible.
- Generate frontend API types after backend OpenAPI changes:

  ```sh
  npm run generate:schema
  ```

- Do not edit `src/schemas/types.gen.ts` manually. Keep UI-only state separate
  from API models.

The dashboard should use the target conference, committee, assignment, and
session routes in the backend API document rather than page-local data.

## Live sessions

- Open the session WebSocket with `VITE_WS_URL`.
- Send `{ "access_token": "<Supabase JWT>" }` as the first message.
- Replace the Zustand store with every received `SessionLiveState` snapshot.
- Send live procedure actions—motions, votes, queues, and roll call—only over
  the WebSocket, never HTTP.
- The current implementation uses `/sessions/{session_id}/ws`.

`representation_id` comes from server access/state data. It may identify a
target when an event requires one, but it is not frontend-authenticated
identity and must not be inferred from display order.
