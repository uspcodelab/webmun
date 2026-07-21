# Test suite for service layer
import json

import pytest

from app.session import enums
from app.session.manager import ConnectionManager
from app.session.models import SessionActor, SessionLiveState
from app.session.enums import SessionRole
from app.session.service import ActorResolutionError, build_actor, handle_client_messages


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
    assert actor.delegation.name == connection_manager.room_states[0].delegations[0].name


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
        session_id=session_state.session_id, actor=delegate_actor, data=data
    )

    # tests if engine dispatched the message

    assert fake_engine.dispatched["state"] is session_state
    assert fake_engine.dispatched["event"].type == enums.DelegateEvents.JOIN_QUEUE
    assert fake_engine.dispatched["actor"] is delegate_actor
    assert broadcasts == [session_state.session_id]
