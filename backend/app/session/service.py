# Application orchestration layer. Does things, such as calling functions to create a session, persist/update state, save to database, etc
# The 2nd layer between the API route and inner things such as database, FSM engine, Redis, etc. Should orchestrate everything
# Also calls the manager in order to broadcast states, etc

import logging
from dataclasses import replace
from datetime import datetime
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

import app.session.enums as enums
import app.session.repository as repository
import app.session.schemas as schemas
import app.session.store as store
from app.access.models import CommitteeAssignment
from app.core.exceptions import (
    BadRequest,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from app.session.engine import EventRejectedError, SessionEngine

from .manager import ConnectionManager
from .models import (
    DelegationContext,
    DispatchOutcome,
    RollCallContext,
    SessionActor,
    SessionLiveState,
)


class ActorResolutionError(Exception):
    pass


class SessionFetchError(Exception):
    pass


async def build_actor(
    user_id: UUID,
    session_id: int,
    role: enums.SessionRole,
    redis: Redis,
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
        res = await store.get_outcome(client=redis, session_id=session_id)
        if res is None:
            raise ActorResolutionError("session not found")

        delegation = res.state.delegations.get(delegation_id)
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
        raise BadRequest("Could not create session with given schema")

    await session.commit()

    return session_id


async def get_session_for_activation(session: AsyncSession, committee_session_id: int):
    stored = await repository.get_session_info(
        session=session, committee_session_id=committee_session_id
    )
    if stored is None:
        raise NotFoundError("Session not found")
    return stored


async def activate_session(
    session: AsyncSession,
    manager: ConnectionManager,
    committee_session_id: int,
    redis: Redis,
):
    """Activate a planned session"""
    stored = await get_session_for_activation(session, committee_session_id)
    if stored.status != "planned":
        raise ConflictError("Session already started")

    delegations = await repository.bulk_get_delegation_context(
        session=session, committee_id=stored.committee_id
    )

    if delegations is None:
        raise ConflictError("Session delegations are unavailable")

    live_state = SessionLiveState(
        session_id=stored.id,
        start_time=datetime.now(),
        delegations=delegations,
        current_state=enums.States.SETUP,
        gsl_default_time_seconds=60,
        roll_call=RollCallContext(registry={}),
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
        raise InternalServerError("Could not update session info") from None

    await session.commit()

    manager.active_connections.setdefault(committee_session_id, {})
    await store.save_outcome(client=redis, result=DispatchOutcome(state=live_state))


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
    redis: Redis,
) -> SessionActor:
    """Service that prepares for session connect.
    Used as a fallback if redis/backend does not have the session_id
    """
    res = await store.get_outcome(client=redis, session_id=committee_session_id)

    if res is None:
        stored_state = await repository.get_session_info(session, committee_session_id)
        if stored_state is None:
            raise SessionFetchError("Could not fetch session info")
        if stored_state.status != "active":
            raise SessionFetchError("Session is not active")
        if stored_state.state_snapshot is None:
            raise SessionFetchError("No state snapshot found")

        # fetch state_snapshot and validate to be a SessionLiveState
        live_state = SessionLiveState.model_validate(stored_state.state_snapshot)

        # put SessionLiveState on Cache
        await store.save_outcome(client=redis, result=DispatchOutcome(state=live_state))

    if manager.active_connections.get(committee_session_id) is None:
        manager.active_connections.setdefault(committee_session_id, {})

    actor = await build_actor(
        user_id=assignment.user_id,
        session_id=committee_session_id,
        role=enums.SessionRole(assignment.role.upper()),
        delegation_id=assignment.representation_id,
        redis=redis,
    )

    return actor


async def handle_client_messages(
    engine: SessionEngine,
    logger: logging.Logger,
    session_id: int,
    actor: SessionActor,
    data: schemas.EventMessage,
    redis: Redis,
):
    lock = redis.lock(
        f"webmun:session:{session_id}:lock",
        timeout=5,
        blocking_timeout=2,
    )

    # Lock for calculating in FSM without another worker overriding
    async with lock:
        event = data.event
        outcome = await store.get_outcome(client=redis, session_id=session_id)
        if outcome is None:
            raise NotFoundError("Session state has not been found")

        logger.info("Processing %s for session %s", event.type, session_id)

        try:
            result = engine.dispatch(outcome.state, event, actor)
            await store.save_publish_outcome(client=redis, result=result)
            return result
        except EventRejectedError as exc:
            return exc
