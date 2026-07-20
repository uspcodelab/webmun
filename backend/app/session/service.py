# Application orchestration layer. Does things, such as calling functions to create a session, persist/update state, save to database, etc
# The 2nd layer between the API route and inner things such as database, FSM engine, Redis, etc. Should orchestrate everything
# Also calls the manager in order to broadcast states, etc

import logging
from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.access.models import CommitteeAssignment
import app.session.enums as enums
from app.session.repository import bulk_get_uuids_by_email, bulk_insert_assignments, create_session
import app.session.schemas as schemas
from app.session.engine import SessionEngine

from .manager import ConnectionManager
from .models import (
    DelegationContext,
    RollCallContext,
    SessionActor,
    SessionLiveState,
)


class ActorResolutionError(Exception):
    pass

class SessionCreationError(Exception):
    pass

# SessionService class defined with Dependency Injection

def build_actor(
    manager: ConnectionManager,
    session_id: int,
    role: enums.SessionRole,
    delegation_id: int | None = None,
) -> SessionActor:

    if role == enums.SessionRole.CHAIR:
        return SessionActor(
            role=enums.SessionRole.CHAIR,
            display_name="Chair",
        )

    if role == enums.SessionRole.DELEGATE:
        if delegation_id is None:
            raise ActorResolutionError("needs delegate id")
        state = manager.room_states.get(session_id)
        if state is None:
            raise ActorResolutionError("session not found")

        delegation = next(
            (d for d in state.delegations if d.id == delegation_id), None
        )
        if delegation is None:
            raise ActorResolutionError("delegation not found")

        return SessionActor(
            role=enums.SessionRole.DELEGATE,
            delegation=DelegationContext(
                id=delegation.id,
                seat=delegation.seat,
                name=delegation.name,
                code=delegation.code,
            ),
            display_name=delegation.name,
        )


async def create_session_service(
        session: AsyncSession,
        manager: ConnectionManager,
        session_schema: schemas.SessionCreationSchema, 
        creator_uuid: UUID):
    # loop through delegationSchema and convert each to DelegationContext
    delegations = [
        # id now begins at 0 instead of 1
        DelegationContext(id=i, name=d.name, seat=d.seat, code=d.code)
        for i, d in enumerate(session_schema.delegations)
    ]

    # insert into database and return the session id here
    session_id = await create_session(session=session, name=session_schema.name or "", delegations=delegations)
    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create session with given schema"
        )
    
    emails_to_uuid_map = await bulk_get_uuids_by_email(session, session_schema.delegations) 
    if len(delegations) != len(emails_to_uuid_map):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some users were not found"
        )

    final_delegations = [
        CommitteeAssignment(
            user_id=emails_to_uuid_map[d.user_email],
            session_id=session_id,
            delegation_id=i, # R: I hope this works since I think enumerate is deterministic
            role="DELEGATE",
        )
        for i, d in enumerate(session_schema.delegations)
    ]
    
    # append this chair at last so we can also retrieve it
    final_delegations.append(CommitteeAssignment(user_id=creator_uuid, session_id=session_id, delegation_id=None,role="CHAIR")) 

    await bulk_insert_assignments(session=session, delegations=final_delegations)


    manager.room_states[session_id] = SessionLiveState(
        session_id=session_id,
        start_time=datetime.now(),
        delegations=delegations,
        current_state=enums.States.SETUP,
        gsl_default_time_seconds=60,
        roll_call=RollCallContext(registry={}),
        voting_choice={},
    )
    manager.active_connections.setdefault(session_id, {})

async def handle_client_messages(
    manager: ConnectionManager,
    engine: SessionEngine,
    logger: logging.Logger,
    session_id: int, 
    actor: SessionActor, 
    data):
    adapter = TypeAdapter(schemas.SessionEvent)

    # if schema is None:
    # raise ValueError("Unsupported event type")

    event = adapter.validate_json(data)
    state = manager.room_states[session_id]

    logger.info(event)  # Debugging

    new_state = engine.dispatch(state, event, actor)
    manager.room_states[session_id] = new_state

    await manager.broadcast_state(session_id)
