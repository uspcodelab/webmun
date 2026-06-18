# Environment configuration file for testing

from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.session.engine import SessionEngine
from app.session.models import SessionActor, SessionRole, DelegationContext
from app.session.manager import (
        RollCallContext,  
        SessionLiveState
        )

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def delegation_list():
    brazil = DelegationContext(id=1, seat="1-2", name="Brazil", code="br")
    usa = DelegationContext(id=2, seat="3-4", name="USA", code="us")
    russia = DelegationContext(id=3, seat="5-6", name="Russia", code="ru")
    return [brazil, usa, russia]

@pytest.fixture 
def roll_call():
    return RollCallContext()

@pytest.fixture
def session_state(delegation_list: list[DelegationContext], roll_call: RollCallContext):
    return SessionLiveState(
        session_id=0,
        start_time=datetime.now(),
        delegations=delegation_list,
        roll_call=roll_call,
    )

@pytest.fixture
def chair_actor():
    return SessionActor(role=SessionRole.CHAIR, display_name="Chair")

@pytest.fixture
def delegate_actor(delegation_list: list[DelegationContext]):
    return SessionActor(role=SessionRole.DELEGATE, delegation=delegation_list[0])

@pytest.fixture 
def engine():
    return SessionEngine()
