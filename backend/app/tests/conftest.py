# Environment configuration file for testing

from datetime import datetime
from uuid import UUID

import pytest

from app.session.engine import SessionEngine
from app.session.enums import (
    SessionRole,
    States,
)
from app.session.manager import ConnectionManager
from app.session.models import (
    DelegationContext,
    DispatchOutcome,
    RollCallContext,
    SessionActor,
    SessionLiveState,
)


@pytest.fixture
def delegation_dict():
    brazil = DelegationContext(id=0, seat="1-2", name="Brazil", code="br")
    usa = DelegationContext(id=1, seat="3-4", name="USA", code="us")
    russia = DelegationContext(id=2, seat="5-6", name="Russia", code="ru")

    return {0: brazil, 1: usa, 2: russia}


@pytest.fixture
def roll_call():
    return RollCallContext()


@pytest.fixture
def session_state(delegation_dict, roll_call):
    return SessionLiveState(
        session_id=0,
        start_time=datetime.now(),
        delegations=delegation_dict,
        roll_call=roll_call,
    )


@pytest.fixture
def chair_actor():
    return SessionActor(
        user_id=UUID("11111111-1111-1111-1111-111111111111"),
        role=SessionRole.CHAIR,
        display_name="Chair",
    )


@pytest.fixture
def delegate_actor(delegation_dict):
    return SessionActor(
        user_id=UUID("22222222-2222-2222-2222-222222222222"),
        role=SessionRole.DELEGATE,
        delegation=delegation_dict.get(0),
    )


@pytest.fixture
def engine():
    return SessionEngine()


class FakeEngine:
    def __init__(self):
        self.dispatched = None

    def dispatch(self, state, event, actor):
        self.dispatched = {
            "state": state,
            "event": event,
            "actor": actor,
        }
        state.current_state = States.OPEN_GSL
        return DispatchOutcome(state=state, effect=None)


@pytest.fixture
def fake_engine():
    return FakeEngine()


@pytest.fixture
def connection_manager():
    return ConnectionManager()
