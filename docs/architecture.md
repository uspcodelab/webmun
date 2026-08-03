# Architecture overview

> Quick note: this overview was generated with the help of AI and curated by one of the devs.

Our architecture is composed of three main parts:

- A React application that people use in their browser.
- A FastAPI backend that applies the application's rules and coordinates live sessions.
- Supabase, which provides authentication and PostgreSQL storage.

The browser is responsible for presenting information and requesting actions.
The backend is responsible for deciding whether those actions are allowed and for updating the committee state. This division keeps the rules in one place and means that clients cannot grant themselves permissions by changing their own UI. In short, backend is **authoritative**.

## At a glance

TODO: Change this to a sketch/diagram

```text
Browser (React / Vite)
        |
        | HTTP requests and WebSocket events
        v
Backend (FastAPI)
        |
        +-- Supabase Auth: verifies who the user is
        |
        +-- PostgreSQL: durable application data
        |
        +-- SessionLiveState: active, real-time session state
```

HTTP is used for ordinary request/response work. WebSockets are used while a committee is active (so, real-time actions), because every connected participant needs to receive changes without repeatedly asking the server for updates.

## The frontend

The frontend is a React application built with Vite. It renders the screens that delegates and committee staff use, manages browser-side interaction, and communicates with the backend.

It should be thought of as a client of the application rules, not the owner of them. For example, it can hide a control when a user appears not to have a role, but the backend must still enforce that role when it receives the corresponding request or WebSocket event.

Supabase Auth is used in the frontend for sign-up and sign-in. After a user has signed in, the frontend uses that authenticated session when calling the backend and connecting to a live session. The backend uses the authentication information to identify the caller; it does not trust an identity supplied in an arbitrary client payload.

### Frontend development conventions

The active session view has one shared Zustand store:
`useCommitteeStore`. Its shape is the generated `SessionLiveState` type, and a complete state snapshot received over the WebSocket replaces the store's state.
Session components should select only the fields they render from this store; they send event requests to the backend rather than editing the shared session state themselves. Component-local state remains appropriate for temporary UI concerns such as an open dialog or an unsubmitted form value.

The schema types in `src/schemas/types.gen.ts` are generated from the backend OpenAPI definition. Do not edit them by hand; regenerate them with
`npm run generate:schema` whenever an applicable backend schema changes.

Authentication state is provided application-wide by `AuthProvider`, which uses the Supabase client to restore, refresh, and observe the browser session.
Components use `useAuth()` for the current user, session, and access token.
Authenticated HTTP requests use that token as a Bearer token, while the
session WebSocket sends it after connecting. Route guards improve navigation, but the backend is still responsible for authorization.

For a fuller guide on these conventions, see
[Frontend state management](frontend/state-management.md) and
[Frontend authentication](frontend/authentication.md).

## The backend

The backend is a FastAPI application. It is the authoritative place for
application rules: it validates input, resolves the current user's permissions and committee assignment, changes state, and sends the result back to clients.

To keep this work understandable, backend code is divided into layers. A
request normally moves through them in this order:

TODO: Change this to a sketch?

```text
view  ->  service  ->  repository
```

### Views

Views are the entry points to the backend. In FastAPI, these are normally HTTP route handlers or WebSocket handlers. A view should be small and focused:

- receive and parse input;
- obtain the authenticated user and required request context;
- **call the appropriate service**;
- translate the result into an HTTP response or WebSocket message.

A view should not contain the core business rules or direct database queries. This is important. Do not mix responsibilities unless absolutely needed.
Keeping it thin makes the external API easier to change without moving the application's logic around.

### Services

Services contain the use cases of the application: the actions that make sense in WebMUN. They coordinate rules, authorization, state changes, and any data that must be read or written to complete an action.

For example, a service might determine whether a participant may perform an action in the current phase of a committee, update the live session state, and request persistence where appropriate. Services are where different sources of data come together; they should not be concerned with HTTP status codes or React components.

### Repositories

Repositories isolate database access. They retrieve and persist durable data in PostgreSQL without exposing SQL or Supabase-specific details to the rest of the application.

This boundary gives the service layer a small, meaningful interface—for
example, "get this committee" or "save this assignment"—and keeps storage decisions out of views. It also makes services simpler to test, since a test can substitute a repository with a controlled implementation.

## Durable data and live session state

PostgreSQL holds information that must survive application restarts, such as users, committees, assignments, and session-related records. Supabase is used as the managed PostgreSQL and authentication platform.

An active committee session also has changing, real-time state. This is managed as `SessionLiveState`, an in-memory state machine that is persisted as needed (Planned to be moved into a Redis service). A state machine represents the session's current phase and the changes that are valid from that phase. This is useful because the rules of a live committee depend on what is happening now, not only on records stored in the database.

## Real-time session flow

During an active session, the server shares state snapshots with connected clients (Planned to use only deltas - snippets of real changes). A client sends an event describing the action it wants to take; it does not directly change the session's state.

```text
1. The client sends an event with its payload.
2. The WebSocket view identifies the authenticated user.
3. A service validates the action against permissions and current session state.
4. The service updates SessionLiveState and persists required durable changes.
5. The backend broadcasts an updated state snapshot to connected clients.
6. Clients render the new snapshot.
```

The backend performs the validation in step 3 for every event. The frontend may use the latest snapshot to make the interface pleasant to use, but it must be ready for the backend to reject an action when the state has changed or the user is not allowed to perform it.

## Why the separation matters

The layers are a practical way to decide where new code belongs:

| If you are changing... | Start in... |
| --- | --- |
| An HTTP or WebSocket message shape | a view, then its service |
| A business rule or committee action | a service |
| A database query or persistence detail | a repository |
| A page, component, or browser interaction | the frontend |
| The phases or transitions of a live committee | the session-state logic and its services |

When in doubt, follow the direction of dependencies: views call services, and services call repositories. Repositories should not call views, and business rules should not depend on a particular frontend screen.

## Related documentation

- [Getting started](getting-started.md) explains how to run the application
  locally.
- [Authentication and authorization](backend/authentication-and-authorization.md)
  covers Supabase Auth and backend identity checks.
- [MUN committee flow and technical approach](realtime/mun-flow.md) maps the
  committee procedure to the state machine, events, and snapshots.
