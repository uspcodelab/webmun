# Application orchestration layer. Does things, such as calling functions to create a session, persist/update state, save to database, etc
# The 2nd layer between the API route and inner things such as database, FSM engine, Redis, etc. Should orchestrate everything
# Also calls the manager in order to broadcast states, etc

from datetime import datetime

from pydantic import TypeAdapter
from app.session.engine import SessionEngine
from .manager import manager
from .schemas import *
from .models import SessionActor, SessionRole, DelegationContext, SessionLiveState, RollCallContext
import logging

engine = SessionEngine()

class ActorResolutionError(Exception):
    pass

def build_actor(
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
        state = manager.room_states.get(session_id)
        if state is None:
            raise ActorResolutionError("session not found")

        delegation = next(
                  (d for d in state.delegations if d.id == delegation_id), None)
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


def create_session(session_schema: SessionCreationSchema):
    session_id = session_schema.session_id
    
    manager.room_states[session_id] = SessionLiveState(
            session_id=session_id,
            start_time=datetime.now(),
            delegations=session_schema.delegations,
            current_state=States.ROLL_CALL,
            gsl_default_time_seconds=60,
            roll_call=RollCallContext(registry={}),
            voting_choice={},
    )
    manager.active_connections.setdefault(session_id, {})

uvicorn_logger = logging.getLogger("uvicorn.error")

async def handle_client_messages(session_id: int, actor: SessionActor, data):
    adapter = TypeAdapter(SessionEvent)

    #if schema is None:
        #raise ValueError("Unsupported event type")
    
    event = adapter.validate_json(data)
    state = manager.room_states[session_id]


    uvicorn_logger.info(event) #Debugging
    
    new_state = engine.dispatch(state, event, actor)
    manager.room_states[session_id] = new_state

    await manager.broadcast_state(session_id)
