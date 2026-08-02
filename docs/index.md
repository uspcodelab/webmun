# WebMUN Developer's Handbook

Welcome to WebMUN!

WebMUN is a web application designed to manage MUNs, from general conferences, data and access up to real-time sessions and actions for committees. This app was born in the USPCodeLab group, at IME-USP.

Our stack is currently composed of:
- React 19 as our frontend framework
- Vite 8 as our general frontend builder
- TailwindCSS and Shadcn for UI style and design 
- FastAPI as our backend
- Pytest for backend testing
- Ruff for backend formatting
- Supabase for database management (PostgreSQL) and Supabase Auth for user signup and login
- (Planned) Redis for in-memory kv store
- (Planned) Terraform for infra setup and management

## What's next?

Use the following items to guide yourself through these docs.

TODO
# WebMUN developer documentation

WebMUN is a real-time web application for running Model United Nations
committees. It uses a React/Vite frontend, a FastAPI backend, Supabase Auth,
and PostgreSQL.

## Start here

If you are new to the project, read [Getting started](getting-started.md) to
run the application locally, then read [Architecture](architecture.md) for the
main application boundaries.

If you are working on an active committee session, continue with the
[real-time overview](realtime/overview.md). The backend is authoritative: the
client sends requested actions and renders the session state returned by the
server.

## Documentation

- [Getting started](getting-started.md)
- [Architecture](architecture.md)
- Real-time sessions
  - [Overview](realtime/overview.md)
  - [Events and payloads](realtime/events-and-payloads.md)
  - [Session state](realtime/session-state.md)
- Backend
  - [Database](backend/database.md)
  - [Authentication and authorization](backend/authentication-and-authorization.md)
  - [Testing](backend/testing.md)
- Frontend
  - [State management](frontend/state-management.md)
  - [Authentication](frontend/authentication.md)
- [Testing overview](testing/overview.md)
