# Application orchestration layer. Does things, such as calling functions to create a session, persist/update state, save to database, etc
# The 2nd layer between the API route and inner things such as database, FSM engine, Redis, etc. Should orchestrate everything
# Also calls the manager in order to broadcast states, etc

from dataclasses import replace
import logging
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import EmailStr, TypeAdapter
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.access.models import CommitteeAssignment
import app.session.enums as enums
import app.session.schemas as schemas
import app.session.repository as repository
from app.session.engine import SessionEngine

from .manager import ConnectionManager
from .models import (
    DelegationContext,
    RollCallContext,
    SessionActor,
    SessionLiveState,
    StoredSession,
)


class ActorResolutionError(Exception):
    pass


class SessionCreationError(Exception):
    pass

class SessionFetchError(Exception):
    pass

class SessionUpdateError(Exception):
    pass


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

        delegation = next((d for d in state.delegations if d.id == delegation_id), None)
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
    session_schema: schemas.SessionCreationSchema,
) -> int:
    """Create a planned session"""
    session_id = await repository.create_session(
        session=session, committee_id=session_schema.committee_id, name=session_schema.name
    )

    if session_id is None: 
        raise SessionCreationError("Could not create session with given schema")

    await session.commit()

    return session_id 


async def activate_session(
    session: AsyncSession, 
    manager: ConnectionManager,
    committee_session_id: int,
):
    """Activate a planned session"""
    stored = await repository.get_session_info(
        session=session, committee_session_id=committee_session_id
    )

    if stored is None:
        raise SessionFetchError("Could not fetch session info")
    if stored.status != 'planned':
        raise SessionFetchError("Session already started")

    delegations = await repository.bulk_get_delegation_context(
        session=session, committee_id=stored.committee_id
    )

    if delegations is None:
        raise SessionFetchError("Could not fetch session delegations info")

    live_state = SessionLiveState(
        session_id=stored.id,
        start_time=datetime.now(),
        delegations=delegations,
        current_state=enums.States.SETUP,
        gsl_default_time_seconds=60,
        roll_call=RollCallContext(registry={}),
        voting_choice={},
    )

    updated = replace(
        stored, 
        status='active',
        started_at=datetime.now(),
        state_snapshot=live_state.model_dump(mode='json')
    )
    
    try: 
        await repository.update_session_info(
            session=session, session_info=updated
        )
    except repository.RepositoryError: 
        raise SessionUpdateError("Could not update session info")

    await session.commit()

    manager.room_states[committee_session_id] = live_state
    manager.active_connections.setdefault(committee_session_id, {})

async def pause_session(
    session: AsyncSession, 
    manager: ConnectionManager,
    committee_session_id: int,
) -> None:
    pass

async def close_session(
    session: AsyncSession, 
    manager: ConnectionManager,
    committee_session_id: int,
) -> None:
    pass 

async def prepare_session_connect(
    session: AsyncSession, 
    manager: ConnectionManager, 
    committee_session_id: int,
    assignment: CommitteeAssignment,
) -> SessionActor:
    """Service that prepares for session connect.
    Primarily used as a fallback in case the SessionLiveState is not in manager
    """
    live_state = manager.room_states.get(committee_session_id)

    if live_state is None:
        stored_state = await repository.get_session_info(session, committee_session_id)
        if stored_state is None:
            raise SessionFetchError("Could not fetch session info")
        if stored_state.status != 'active':
            raise SessionFetchError("Session is not active")
        if stored_state.state_snapshot is None:
            raise SessionFetchError("No state snapshot found")
        
        # fetch state_snapshot and validate to be a SessionLiveState
        live_state = SessionLiveState.model_validate(stored_state.state_snapshot)
        
        # put SessionLiveState on ConnectionManager
        manager.room_states[committee_session_id] = live_state
        manager.active_connections.setdefault(committee_session_id, {})

    actor = build_actor(
        manager=manager,
        session_id=committee_session_id,
        role=enums.SessionRole(assignment.role.upper()),
        delegation_id=assignment.representation_id,
    )
        
    return actor


"""
async def old_create_session_service(
    session: AsyncSession,
    session_schema: schemas.SessionCreationSchema,
    creator_uuid: UUID,
):

    # insert into database and return the session id here
    session_id = await create_session(
        session=session, name=session_schema.name or "", delegations=delegations
    )

    if session_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create session with given schema",
        )

    emails_to_uuid_map = await bulk_get_uuids_by_email(
        session, session_schema.delegations
    )
    if len(delegations) != len(emails_to_uuid_map):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Some users were not found"
        )

    final_delegations = [
        CommitteeAssignment(
            user_id=emails_to_uuid_map[d.user_email],
            session_id=session_id,
            delegation_id=i,  # R: I hope this works since I think enumerate is deterministic
            role="DELEGATE",
        )
        for i, d in enumerate(session_schema.delegations)
    ]

    # append this chair at last so we can also retrieve it
    final_delegations.append(
        CommitteeAssignment(
            user_id=creator_uuid,
            session_id=session_id,
            delegation_id=None,
            role="CHAIR",
        )
    )

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
"""


async def handle_client_messages(
    manager: ConnectionManager,
    engine: SessionEngine,
    logger: logging.Logger,
    session_id: int,
    actor: SessionActor,
    data,
):
    adapter = TypeAdapter(schemas.SessionEvent)

    # if schema is None:
    # raise ValueError("Unsupported event type")

    event = adapter.validate_json(data)
    state = manager.room_states[session_id]

    logger.info(event)  # Debugging

    new_state = engine.dispatch(state, event, actor)
    manager.room_states[session_id] = new_state

    await manager.broadcast_state(session_id)
