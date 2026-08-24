# Application orchestration layer. Does things, such as calling functions to create a session, persist/update state, save to database, etc
# The 2nd layer between the API route and inner things such as database, FSM engine, Redis, etc. Should orchestrate everything
# Also calls the manager in order to broadcast states, etc

import logging
from dataclasses import replace
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

import app.session.enums as enums
import app.session.repository as repository
import app.session.schemas as schemas
from app.access.models import CommitteeAssignment
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


class SessionFetchError(Exception):
    pass


class SessionUpdateError(Exception):
    pass


def build_actor(
    user_id: UUID,
    manager: ConnectionManager,
    session_id: int,
    role: enums.SessionRole,
    delegation_id: int | None = None,
) -> SessionActor:

    if role == enums.SessionRole.CHAIR:
        return SessionActor(
            user_id=user_id,
            role=enums.SessionRole.CHAIR,
            display_name="Chair",
        )

    if role == enums.SessionRole.DELEGATE:
        if delegation_id is None:
            raise ActorResolutionError("needs delegate id")
        state = manager.room_states.get(session_id)
        if state is None:
            raise ActorResolutionError("session not found")

        delegation = state.delegations.get(delegation_id)
        if delegation is None:
            raise ActorResolutionError("delegation not found")

        return SessionActor(
            user_id=user_id,
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
        session=session,
        committee_id=session_schema.committee_id,
        name=session_schema.name,
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
    if stored.status != "planned":
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
        status="active",
        started_at=datetime.now(),
        state_snapshot=live_state.model_dump(mode="json"),
    )

    try:
        await repository.update_session_info(session=session, session_info=updated)
    except repository.RepositoryError:
        raise SessionUpdateError("Could not update session info") from None

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
        if stored_state.status != "active":
            raise SessionFetchError("Session is not active")
        if stored_state.state_snapshot is None:
            raise SessionFetchError("No state snapshot found")

        # fetch state_snapshot and validate to be a SessionLiveState
        live_state = SessionLiveState.model_validate(stored_state.state_snapshot)

        # put SessionLiveState on ConnectionManager
        manager.room_states[committee_session_id] = live_state
        manager.active_connections.setdefault(committee_session_id, {})

    actor = build_actor(
        user_id=assignment.user_id,
        manager=manager,
        session_id=committee_session_id,
        role=enums.SessionRole(assignment.role.upper()),
        delegation_id=assignment.representation_id,
    )

    return actor


async def handle_client_messages(
    manager: ConnectionManager,
    engine: SessionEngine,
    logger: logging.Logger,
    session_id: int,
    actor: SessionActor,
    data: schemas.EventMessage,
):
    event = data.event
    state = manager.room_states[session_id]

    logger.info(event)  # Debugging

    dispatch_outcome = engine.dispatch(state, event, actor)
    message = schemas.DispatchResultMessage(
        state=dispatch_outcome.state, effect=dispatch_outcome.effect
    )
    manager.room_states[session_id] = dispatch_outcome.state

    await manager.broadcast_message(session_id, message)
