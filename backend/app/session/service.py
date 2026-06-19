# Application orchestration layer. Does things, such as calling functions to create a session, persist/update state, save to database, etc
# The 2nd layer between the API route and inner things such as database, FSM engine, Redis, etc. Should orchestrate everything
# Also calls the manager in order to broadcast states, etc

import logging
from datetime import datetime

from pydantic import TypeAdapter

import app.session.enums as enums
import app.session.schemas as schemas
from app.session.engine import SessionEngine

from .manager import ConnectionManager
from .models import (
    DelegationContext,
    RollCallContext,
    SessionActor,
    SessionLiveState,
    SessionRole,
)


class ActorResolutionError(Exception):
    pass


# SessionService class defined with Dependency Injection
class SessionService:
    def __init__(self, manager: ConnectionManager, engine: SessionEngine):
        self.manager = manager
        self.engine = engine
        self.uvicorn_logger = logging.getLogger("uvicorn.error")

    def build_actor(
        self,
        session_id: int,
        role: SessionRole,
        delegation_id: int | None = None,
        display_name: str | None = None,
    ) -> SessionActor:

        if role == SessionRole.CHAIR:
            return SessionActor(
                role=SessionRole.CHAIR,
                display_name="Chair",
            )

        if role == SessionRole.DELEGATE:
            if delegation_id is None:
                raise ActorResolutionError("needs delegate id")
            state = self.manager.room_states.get(session_id)
            if state is None:
                raise ActorResolutionError("session not found")

            delegation = next(
                (d for d in state.delegations if d.id == delegation_id), None
            )
            if delegation is None:
                raise ActorResolutionError("delegation not found")

            return SessionActor(
                role=SessionRole.DELEGATE,
                delegation=DelegationContext(
                    id=delegation.id,
                    seat=delegation.seat,
                    name=delegation.name,
                    code=delegation.code,
                ),
                display_name=delegation.name,
            )

    def create_session(self, session_schema: schemas.SessionCreationSchema):
        session_id = session_schema.session_id

        # loop through delegationSchema and convert each to DelegationContext
        delegations = [
            # id now begins at 0 instead of 1
            DelegationContext(id=i, name=d.name, seat=d.seat, code=d.code)
            for i, d in enumerate(session_schema.delegations)
        ]

        self.manager.room_states[session_id] = SessionLiveState(
            session_id=session_id,
            start_time=datetime.now(),
            delegations=delegations,
            current_state=enums.States.ROLL_CALL,
            gsl_default_time_seconds=60,
            roll_call=RollCallContext(registry={}),
            voting_choice={},
        )
        self.manager.active_connections.setdefault(session_id, {})

    async def handle_client_messages(self, session_id: int, actor: SessionActor, data):
        adapter = TypeAdapter(schemas.SessionEvent)

        # if schema is None:
        # raise ValueError("Unsupported event type")

        event = adapter.validate_json(data)
        state = self.manager.room_states[session_id]

        self.uvicorn_logger.info(event)  # Debugging

        new_state = self.engine.dispatch(state, event, actor)
        self.manager.room_states[session_id] = new_state

        await self.manager.broadcast_state(session_id)
