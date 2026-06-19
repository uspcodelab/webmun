# Test suite for service layer
import json

import pytest

from app.session import enums
from app.session.models import SessionActor, SessionLiveState, SessionRole
from app.session.schemas import DelegationSchema, SessionCreationSchema
from app.session.service import ActorResolutionError, SessionService


@pytest.fixture
def delegation_schema_list():
    brazil = DelegationSchema(seat="1-2", name="Brazil", code="br")
    usa = DelegationSchema(seat="3-4", name="USA", code="us")
    russia = DelegationSchema(seat="5-6", name="Russia", code="ru")
    return [brazil, usa, russia]


@pytest.fixture 
def session_test_schema(delegation_schema_list: list[DelegationSchema]):
    return SessionCreationSchema(
        session_id=0,
        delegations=delegation_schema_list
    )


def test_can_build_actor(
    service: SessionService, 
    session_state: SessionLiveState,
) -> None:
    service.manager.room_states[0] = session_state

    actor = service.build_actor(
        session_id=0,
        role=SessionRole.DELEGATE,
        delegation_id=0,
    )

    assert actor.role == SessionRole.DELEGATE
    assert actor.delegation is not None
    assert actor.delegation.id == service.manager.room_states[0].delegations[0].id
    assert actor.delegation.name == service.manager.room_states[0].delegations[0].name


def test_cannot_build_actor_with_nonexistent_state(
    service: SessionService, 
) -> None:
    with pytest.raises(ActorResolutionError, match="session not found"):
            service.build_actor(
                session_id=0,
                role=SessionRole.DELEGATE,
                delegation_id=0,
            )


def test_cannot_build_actor_with_no_delegation_id(
    service: SessionService, 
    session_state: SessionLiveState,
) -> None:
    with pytest.raises(ActorResolutionError, match="needs delegate id"):
            service.manager.room_states[0] = session_state
            service.build_actor(
                session_id=0,
                role=SessionRole.DELEGATE,
            )


def test_cannot_build_actor_with_nonexistent_delegation(
    service: SessionService, 
    session_state: SessionLiveState,
) -> None:
    with pytest.raises(ActorResolutionError, match="delegation not found"):
            service.manager.room_states[0] = session_state

            service.build_actor(
                session_id=0,
                role=SessionRole.DELEGATE,
                delegation_id=999,
            )

def test_can_create_session(
    service: SessionService,
    session_test_schema: SessionCreationSchema,
) -> None:
    service.create_session(session_test_schema)

    assert len(service.manager.room_states) == 1
    assert len(service.manager.room_states[0].delegations) == 3
    assert service.manager.room_states[0].delegations[0].name == "Brazil"
    assert service.manager.room_states[0].delegations[1].id == 1


@pytest.mark.anyio
async def test_handle_client_messages_dispatches_and_broadcasts(
    service: SessionService, 
    session_state: SessionLiveState,
    delegate_actor: SessionActor, 
) -> None:
    session_state.current_state = enums.States.OPEN_GSL
    service.manager.room_states[session_state.session_id] = session_state

    broadcasts = []

    async def fake_broadcast_state(session_id: int):
        broadcasts.append(session_id)
    
    # replaces real broadcast state with this one
    service.manager.broadcast_state = fake_broadcast_state

    data = json.dumps({
        "type": enums.DelegateEvents.JOIN_QUEUE,
        "payload": {},
    })

    await service.handle_client_messages(
        session_id=session_state.session_id,
        actor=delegate_actor, 
        data=data
    )

    # tests if engine dispatched the message 

    assert service.engine.dispatched["state"] is session_state # type: ignore
    assert service.engine.dispatched["event"].type == enums.DelegateEvents.JOIN_QUEUE # type: ignore
    assert service.engine.dispatched["actor"] is delegate_actor # type: ignore
    assert broadcasts == [session_state.session_id]








