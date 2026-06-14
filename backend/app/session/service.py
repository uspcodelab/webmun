# Application orchestration layer. Does things, such as calling functions to create a session, persist/update state, save to database, etc
# The 2nd layer between the API route and inner things such as database, FSM engine, Redis, etc. Should orchestrate everything
# Also calls the manager in order to broadcast states, etc

from datetime import datetime

from pydantic import TypeAdapter
from app.session.engine import SessionEngine
from .manager import manager, SessionLiveState,RollCallContext
from .schemas import *
import logging
import json

engine = SessionEngine()

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

async def handle_client_messages(session_id: int, sender: str, data):
    is_chair = False if sender != "CHAIR" else True

    adapter = TypeAdapter(SessionEvent)

    #if schema is None:
        #raise ValueError("Unsupported event type")
    
    event = adapter.validate_json(data)
    state = manager.room_states[session_id]


    uvicorn_logger.info(event) #Debugging
    
    new_state = engine.dispatch(state, event, sender, is_chair)
    manager.room_states[session_id] = new_state

    await manager.broadcast_state(session_id)
