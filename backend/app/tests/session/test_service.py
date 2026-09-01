from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest

from app.access.enums import SessionRoles
from app.access.models import CommitteeAssignment
from app.session import enums, store
from app.session.engine import EventRejectedError
from app.session.enums import SessionRole
from app.session.models import SessionActor, SessionLiveState
from app.session.schemas import EventMessage, JoinQueueEvent
from app.session.service import (
    ActorResolutionError,
    SessionFetchError,
    build_actor,
    handle_client_messages,
    prepare_session_connect,
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def brazil_assignment() -> CommitteeAssignment:
    return CommitteeAssignment(
        user_id=UUID("44444444-4444-4444-4444-444444444444"),
        committee_id=0,
        role=SessionRoles.DELEGATION,
        representation_id=0,
    )


@pytest.mark.anyio
async def test_builds_delegate_actor_from_redis(
    fake_redis, session_state: SessionLiveState
) -> None:
    await store.save_state(fake_redis, session_state)  # type: ignore[arg-type]

    actor = await build_actor(
        user_id=UUID("11111111-1111-1111-1111-111111111111"),
        session_id=session_state.session_id,
        role=SessionRole.DELEGATE,
        delegation_id=0,
        redis=fake_redis,  # type: ignore[arg-type]
    )

    assert actor.role == SessionRole.DELEGATE
    assert actor.delegation is not None
    assert actor.delegation.id == session_state.delegations[0].id
    assert actor.delegation.name == session_state.delegations[0].name


@pytest.mark.anyio
async def test_cannot_build_actor_with_missing_redis_state(fake_redis) -> None:
    with pytest.raises(ActorResolutionError, match="session not found"):
        await build_actor(
            user_id=UUID("11111111-1111-1111-1111-111111111111"),
            session_id=0,
            role=SessionRole.DELEGATE,
            delegation_id=0,
            redis=fake_redis,  # type: ignore[arg-type]
        )


@pytest.mark.anyio
async def test_cannot_build_actor_with_no_delegation_id(fake_redis) -> None:
    with pytest.raises(ActorResolutionError, match="needs delegate id"):
        await build_actor(
            user_id=UUID("11111111-1111-1111-1111-111111111111"),
            session_id=0,
            role=SessionRole.DELEGATE,
            redis=fake_redis,  # type: ignore[arg-type]
        )


@pytest.mark.anyio
async def test_cannot_build_actor_with_nonexistent_delegation(
    fake_redis, session_state: SessionLiveState
) -> None:
    await store.save_state(fake_redis, session_state)  # type: ignore[arg-type]

    with pytest.raises(ActorResolutionError, match="delegation not found"):
        await build_actor(
            user_id=UUID("11111111-1111-1111-1111-111111111111"),
            session_id=session_state.session_id,
            role=SessionRole.DELEGATE,
            delegation_id=999,
            redis=fake_redis,  # type: ignore[arg-type]
        )


@pytest.mark.anyio
async def test_prepare_connect_uses_redis_without_database(
    connection_manager, fake_redis, session_state: SessionLiveState, brazil_assignment
) -> None:
    await store.save_state(fake_redis, session_state)  # type: ignore[arg-type]

    actor = await prepare_session_connect(
        session=None,  # type: ignore[arg-type]
        manager=connection_manager,
        committee_session_id=session_state.session_id,
        assignment=brazil_assignment,
        redis=fake_redis,  # type: ignore[arg-type]
    )

    assert actor.role == enums.SessionRole.DELEGATE
    assert actor.delegation is not None
    assert actor.delegation.id == brazil_assignment.representation_id


@pytest.mark.anyio
async def test_prepare_connect_hydrates_redis_from_database(
    connection_manager,
    fake_redis,
    session_state: SessionLiveState,
    brazil_assignment,
    monkeypatch,
) -> None:
    mock_stored_state = MagicMock(
        status="active", state_snapshot=session_state.model_dump(mode="json")
    )
    mock_get_session_info = AsyncMock(return_value=mock_stored_state)
    monkeypatch.setattr(
        "app.session.repository.get_session_info", mock_get_session_info
    )

    actor = await prepare_session_connect(
        session=MagicMock(),
        manager=connection_manager,
        committee_session_id=session_state.session_id,
        assignment=brazil_assignment,
        redis=fake_redis,  # type: ignore[arg-type]
    )

    assert actor.delegation is not None
    assert await store.get_state(fake_redis, session_state.session_id) == session_state  # type: ignore[arg-type]
    mock_get_session_info.assert_awaited_once()


@pytest.mark.anyio
async def test_prepare_connect_rejects_missing_durable_session(
    connection_manager, fake_redis, brazil_assignment, monkeypatch
) -> None:
    monkeypatch.setattr(
        "app.session.repository.get_session_info", AsyncMock(return_value=None)
    )

    with pytest.raises(SessionFetchError, match="Could not fetch session info"):
        await prepare_session_connect(
            session=MagicMock(),
            manager=connection_manager,
            committee_session_id=0,
            assignment=brazil_assignment,
            redis=fake_redis,  # type: ignore[arg-type]
        )


@pytest.mark.anyio
async def test_handle_client_messages_persists_dispatch_outcome(
    fake_redis,
    fake_engine,
    session_state: SessionLiveState,
    delegate_actor: SessionActor,
) -> None:
    session_state.current_state = enums.States.OPEN_GSL
    await store.save_state(fake_redis, session_state)  # type: ignore[arg-type]
    client_message = EventMessage(
        request_id=uuid4(),
        event=JoinQueueEvent(type=enums.DelegateEvents.JOIN_QUEUE, payload={}),
    )

    result = await handle_client_messages(
        engine=fake_engine,
        logger=__import__("logging").getLogger("test"),
        session_id=session_state.session_id,
        actor=delegate_actor,
        data=client_message,
        redis=fake_redis,  # type: ignore[arg-type]
    )

    assert fake_engine.dispatched["state"] is not None
    assert result.state is not None
    assert (await store.get_state(fake_redis, session_state.session_id)) is not None  # type: ignore[arg-type]


@pytest.mark.anyio
async def test_handle_client_messages_does_not_persist_rejection(
    fake_redis, session_state: SessionLiveState, delegate_actor: SessionActor
) -> None:
    await store.save_state(fake_redis, session_state)  # type: ignore[arg-type]
    rejection = EventRejectedError(
        enums.EventErrorCode.INVALID_STATE, "Cannot enter queue right now"
    )
    rejecting_engine = MagicMock()
    rejecting_engine.dispatch.side_effect = rejection
    event = EventMessage(
        request_id=uuid4(),
        event=JoinQueueEvent(type=enums.DelegateEvents.JOIN_QUEUE, payload={}),
    )

    result = await handle_client_messages(
        engine=rejecting_engine,
        logger=__import__("logging").getLogger("test"),
        session_id=session_state.session_id,
        actor=delegate_actor,
        data=event,
        redis=fake_redis,  # type: ignore[arg-type]
    )

    assert result is rejection
    assert await store.get_state(fake_redis, session_state.session_id) == session_state  # type: ignore[arg-type]
