# Test suite for service layer
import json
from uuid import UUID

import pytest

from app.access.models import CommitteeAssignment
from app.session import enums
from app.session.manager import ConnectionManager
from app.session.models import SessionActor, SessionLiveState
from app.session.repository import get_session_info
from app.session.enums import SessionRole
from app.session.service import (
    ActorResolutionError,
    SessionFetchError,
    build_actor,
    handle_client_messages,
    prepare_session_connect,
)
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def brazil_assignment():
    return CommitteeAssignment(
        user_id=UUID("44444444-4444-4444-4444-444444444444"),
        committee_id=0,
        role="delegate",
        representation_id=0,
    )


def test_can_build_actor(
    connection_manager: ConnectionManager,
    session_state: SessionLiveState,
) -> None:
    connection_manager.room_states[0] = session_state

    actor = build_actor(
        manager=connection_manager,
        session_id=0,
        role=SessionRole.DELEGATE,
        delegation_id=0,
    )

    assert actor.role == SessionRole.DELEGATE
    assert actor.delegation is not None
    assert actor.delegation.id == connection_manager.room_states[0].delegations[0].id
    assert (
        actor.delegation.name == connection_manager.room_states[0].delegations[0].name
    )


def test_cannot_build_actor_with_nonexistent_state(
    connection_manager: ConnectionManager,
) -> None:
    with pytest.raises(ActorResolutionError, match="session not found"):
        build_actor(
            manager=connection_manager,
            session_id=0,
            role=SessionRole.DELEGATE,
            delegation_id=0,
        )


def test_cannot_build_actor_with_no_delegation_id(
    connection_manager: ConnectionManager,
    session_state: SessionLiveState,
) -> None:
    with pytest.raises(ActorResolutionError, match="needs delegate id"):
        connection_manager.room_states[0] = session_state
        build_actor(
            manager=connection_manager,
            session_id=0,
            role=SessionRole.DELEGATE,
        )


def test_cannot_build_actor_with_nonexistent_delegation(
    connection_manager: ConnectionManager,
    session_state: SessionLiveState,
) -> None:
    with pytest.raises(ActorResolutionError, match="delegation not found"):
        connection_manager.room_states[0] = session_state

        build_actor(
            manager=connection_manager,
            session_id=0,
            role=SessionRole.DELEGATE,
            delegation_id=999,
        )


@pytest.mark.anyio
async def test_prepare_connect_without_db(
    connection_manager: ConnectionManager,
    session_state: SessionLiveState,
    brazil_assignment: CommitteeAssignment,
) -> None:
    connection_manager.room_states[0] = session_state
    mock_session = None

    actor = await prepare_session_connect(
        session=mock_session,  # type: ignore due to mock session not needing to be called. if it is, we fail
        manager=connection_manager,
        committee_session_id=0,
        assignment=brazil_assignment,
    )

    assert actor.role == enums.SessionRole.DELEGATE
    assert actor.delegation is not None
    assert actor.delegation.id == brazil_assignment.representation_id


@pytest.mark.anyio
async def test_prepare_connect_fetches_db(
    connection_manager: ConnectionManager,
    brazil_assignment: CommitteeAssignment,
    monkeypatch,
) -> None:
    mock_session = MagicMock
    mock_stored_state = MagicMock()
    mock_stored_state.status = "active"
    mock_stored_state.state_snapshot = {"session_id": 0}

    mock_get_session_info = AsyncMock(return_value=mock_stored_state)

    monkeypatch.setattr(
        "app.session.repository.get_session_info", mock_get_session_info
    )

    # prevent model_validate from breaking validation
    monkeypatch.setattr(
        SessionLiveState,
        "model_validate",
        MagicMock(return_value=mock_stored_state.state_snapshot),
    )

    monkeypatch.setattr("app.session.service.build_actor", MagicMock())

    await prepare_session_connect(
        session=mock_session,  # type: ignore
        manager=connection_manager,
        committee_session_id=0,
        assignment=brazil_assignment,
    )

    mock_get_session_info.assert_called_once_with(mock_session, 0)


@pytest.mark.anyio
async def test_cant_prepare_connect_storedlive_missing(
    connection_manager: ConnectionManager,
    brazil_assignment: CommitteeAssignment,
    monkeypatch,
) -> None:
    with pytest.raises(SessionFetchError, match="Could not fetch session info"):
        mock_session = MagicMock
        mock_get_session_info = AsyncMock(return_value=None)

        monkeypatch.setattr(
            "app.session.repository.get_session_info", mock_get_session_info
        )

        await prepare_session_connect(
            session=mock_session,  # type: ignore
            manager=connection_manager,
            committee_session_id=0,
            assignment=brazil_assignment,
        )


@pytest.mark.anyio
async def test_handle_client_messages_dispatches_and_broadcasts(
    connection_manager: ConnectionManager,
    fake_engine,
    session_state: SessionLiveState,
    delegate_actor: SessionActor,
) -> None:
    session_state.current_state = enums.States.OPEN_GSL
    connection_manager.room_states[session_state.session_id] = session_state

    broadcasts = []

    async def fake_broadcast_state(session_id: int):
        broadcasts.append(session_id)

    # replaces real broadcast state with this one
    connection_manager.broadcast_state = fake_broadcast_state

    data = json.dumps(
        {
            "type": enums.DelegateEvents.JOIN_QUEUE,
            "payload": {},
        }
    )

    await handle_client_messages(
        manager=connection_manager,
        engine=fake_engine,
        logger=__import__("logging").getLogger("test"),
        session_id=session_state.session_id,
        actor=delegate_actor,
        data=data,
    )

    # tests if engine dispatched the message

    assert fake_engine.dispatched["state"] is session_state
    assert fake_engine.dispatched["event"].type == enums.DelegateEvents.JOIN_QUEUE
    assert fake_engine.dispatched["actor"] is delegate_actor
    assert broadcasts == [session_state.session_id]
