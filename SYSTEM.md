# WebMUN System Summary

WebMUN is a real-time Model United Nations committee management and simulation system. It is built as a FastAPI backend with a React, TypeScript, Vite, Zustand frontend. The current implementation focuses on live committee session state, WebSocket synchronization, chair/delegate event handling, timers, roll call, queues, motions, voting, and a chair-oriented session interface.

## Repository Layout

- `backend/`: FastAPI application, session domain models, event schemas, WebSocket manager, state-transition engine, service layer, and pytest tests.
- `frontend/`: React SPA using Vite, TypeScript, Zustand, React Router, Tailwind, shadcn-style UI components, and generated OpenAPI TypeScript types.
- `docker-compose.yml`: local two-service development setup for backend and frontend.
- `README.md`, `backend/README.md`, `frontend/README.md`: basic project and setup notes.

## Backend

The backend exposes a FastAPI app titled `WebMUN API` from `backend/app/main.py`. It configures CORS for the Vite dev server at `http://localhost:5173`, constructs one in-memory `ConnectionManager`, one `SessionEngine`, and one `SessionService`, then mounts the session router under `/committees`.

Main backend modules:

- `app/session/views.py`: HTTP and WebSocket adapter layer.
- `app/session/service.py`: orchestration layer between API/websocket input, actor resolution, session creation, engine dispatch, and broadcasting.
- `app/session/manager.py`: in-memory room state and WebSocket connection registry.
- `app/session/engine.py`: finite-state/session event engine.
- `app/session/models.py`: internal live-state models.
- `app/session/schemas.py`: Pydantic request/event schemas used by OpenAPI and frontend type generation.
- `app/session/enums.py`: session states, event names, motion types, debate types, and roll-call values.

### API Surface

Current routes under `/committees`:

- `GET /committees/health`: healthcheck endpoint.
- `POST /committees/`: creates an in-memory session from `SessionCreationSchema`.
- `GET /committees/dummy`: OpenAPI schema exposure workaround for generated frontend types.
- `WS /committees/ws/{session_id}`: realtime session socket.

The WebSocket endpoint requires query parameters:

- `role`: `CHAIR` or `DELEGATE`.
- `delegation_id`: required for delegates.
- `display_name`: accepted, currently only meaningfully used for chair display naming.

On socket connection, the backend resolves the actor and sends the current `SessionLiveState` snapshot if the session exists. On each received message, it validates the JSON as a discriminated `SessionEvent`, dispatches it through the engine, stores the returned state, and broadcasts the full state snapshot to all connected clients in that session.

### Session State Model

`SessionLiveState` is the central live state object. It currently includes:

- `session_id`, `start_time`, and committee `delegations`.
- `current_state`, using the `States` enum.
- Timer fields: `timer_is_running`, `timer_expiration`, `timer_remaining_seconds`.
- Speaker fields: `current_speaker`, `gsl_queue`, `gsl_default_time_seconds`, `can_set_motion`.
- Caucus/debate fields: `caucus_list`, `debate`.
- Submitted procedural data: `submitted_motions`, `submitted_questions`.
- Agenda data: `agenda_topics`, `active_topic_index`.
- Voting data: `voting`, `voting_choice`.
- Roll call data: `roll_call`.

State is currently process-local and in memory. There is no database, persistence layer, auth layer, Redis, or multi-process synchronization yet.

### Session Engine

`SessionEngine.dispatch()` maps incoming event `type` values to handler functions through `EVENT_HANDLERS`. The implemented behavior includes:

- Delegate queue actions for the General Speakers List.
- Delegate voting during an active voting context.
- Delegate roll-call answers.
- Chair timer toggle/increase actions.
- Chair informal voting open/close actions.
- Chair motion resolution into procedural voting.
- Chair procedural voting close flow for some motions.
- Chair speaker selection.
- Chair roll-call marking, bulk marking, and closing.
- Chair queue insertion.
- Session open/close scaffolding.

Important states include:

- `SETUP`
- `ROLL_CALL`
- `INITIAL_DEBATE`
- `OPEN_GSL`
- `CLOSED_GSL`
- `MODERATED_CAUCUS`
- `UNMODERATED_CAUCUS`
- `VOTING_EXECUTION`
- `VOTING_PREPARATION`
- `VOTING_PROCEDURES`
- `BETWEEN_DEBATES`
- `FINISHED`

Motions are filtered by phase through `MOTIONS_ALLOWED`. The engine intends to model parliamentary procedure as a finite state machine, where delegates submit motions/questions and chairs accept, reject, or force transitions.

### Backend Testing

Tests live in `backend/app/tests`. They cover:

- Connection manager behavior.
- Session service actor resolution, session creation, event dispatch, and broadcast orchestration.
- Engine event behavior for queues, voting, timers, roll call, speaker selection, and selected chair/delegate permissions.
- Route behavior in `test_views.py`.

Some tests are marked `xfail` for known incomplete behavior, such as unimplemented priority functions and edge cases in manager broadcasting.

## Frontend

The frontend is a React SPA in `frontend/` using:

- React 19.
- TypeScript.
- Vite.
- React Router.
- Zustand.
- Tailwind CSS.
- shadcn-style local UI components.
- Lucide icons.
- `@hey-api/openapi-ts` generated types in `src/schemas/types.gen.ts`.

Main frontend entry points:

- `src/main.tsx`: React root mounting.
- `src/App.tsx`: SPA routes.
- `src/store/useCommitteeStore.ts`: Zustand store typed as `SessionLiveState`.
- `src/pages/CreateCommittee.tsx`: hardcoded committee creation flow for session `0`.
- `src/pages/Session.tsx`: chair session page and WebSocket connection.

Current routes:

- `/`: home page.
- `/login`: login page.
- `/create-committee`: committee creation page.
- `/committees/:committeeId/session`: live session page.

### Frontend Data Flow

`Session.tsx` opens a WebSocket to:

```text
ws://localhost:8000/committees/ws/0?role=CHAIR&display_name=Chair
```

When messages arrive, it parses the JSON and calls `UpdateStore(data)`, replacing the Zustand committee store with the latest backend `SessionLiveState`.

`sendMessage(data)` is exported from `Session.tsx`; components can use it to send serialized backend events over the active WebSocket.

Current session UI areas:

- `TopBar`: logo, timer, agenda dialog, active topic display, chair profile placeholder.
- `DelegationMap`: committee seating visualization.
- `SpeakerList`: reads `gsl_queue` and `current_speaker` from Zustand.
- `MotionsList`: currently receives mock motions from `Session.tsx`.
- `BottomBar`: command buttons for exit, vote, motions, speeches, history, session, BRB, incident/help.
- `Timer`, `VotingPopup`, `ManualQuorum`, and bottom-bar button components provide interaction scaffolding.

The frontend is partially wired to live backend state. The store receives full session snapshots, but several UI areas still use hardcoded data or placeholders.

## OpenAPI Type Generation

The frontend generates TypeScript types from the backend OpenAPI schema using `@hey-api/openapi-ts`.

Config:

- `frontend/openapi-ts.config.ts`
- Input: `http://backend:8000/openapi.json`
- Output: `frontend/src/schemas`

`docker-compose.yml` runs `npx @hey-api/openapi-ts` as a frontend `post_start` command, and it watches backend schema/model files for restarts.

## Local Development

Backend:

```bash
cd backend
uv sync
uv run fastapi dev
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Docker Compose:

```bash
docker compose up --build
```

Default exposed ports:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

Useful checks:

```bash
cd backend
uv run pytest
uv run ruff check .
uv run ruff format .
```

```bash
cd frontend
npm run lint
npm run build
```

## Current Caveats

- Session state is in memory only; restarting the backend loses all committees and live state.
- There is no real authentication or authorization yet. Roles are provided by WebSocket query params.
- `Session.tsx` currently connects to hardcoded session `0` as chair, ignoring `committeeId` for the socket URL.
- `CreateCommittee.tsx` uses a hardcoded committee payload.
- Several frontend controls are visual scaffolding and are not fully connected to backend events.
- `MotionsList` currently uses mock data rather than `submitted_motions` from the Zustand store.
- Some engine helpers are stubs, including motion/question priority calculation, vote tallying, agenda setting, and manual phase setting.
- Some backend behavior appears incomplete or inconsistent with tests, including known `xfail` cases.
- The engine's `handle_open_session` references `manager.count_present_delegations(...)`, but `manager` is not in that module's scope.
- `SessionService.create_session()` sets `current_state=States.SETUP`, but `States` is not imported directly in `service.py`; the module imports `app.session.enums as enums`.
- The frontend generated type file `frontend/src/schemas/types.gen.ts` is generated output and currently has uncommitted modifications in the working tree.

## System Direction

The intended architecture is a realtime state-machine backend that owns canonical committee state and broadcasts snapshots to all clients. The frontend should treat Zustand as a local projection of that canonical state and send typed event messages for user actions. As the project matures, the likely next architectural additions are persistence, authentication, role-specific views, fuller procedural rule enforcement, frontend event wiring, and replacing full-state broadcasts with smaller event/delta messages if needed.
