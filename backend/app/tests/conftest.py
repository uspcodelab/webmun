# Environment configuration file for testing

import os
from datetime import datetime
from uuid import UUID

import pytest

# `app.main` builds middleware at import time, which loads Settings before the
# OpenAPI test can run. These are non-secret placeholders; database access is
# mocked in unit tests and no application lifespan is started by that test.
os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/webmun_test"
)
os.environ.setdefault("SUPABASE_URL", "https://supabase.example.test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")


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


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.published: list[tuple[str, str]] = []

    async def get(self, key: str) -> str | None:
        return self.values.get(key)

    async def set(self, key: str, value: str) -> None:
        self.values[key] = value

    async def delete(self, key: str) -> int:
        return int(self.values.pop(key, None) is not None)

    def pipeline(self) -> "FakePipeline":
        return FakePipeline(self)

    def lock(self, *_args: object, **_kwargs: object) -> "FakeLock":
        return FakeLock()


class FakePipeline:
    def __init__(self, client: FakeRedis) -> None:
        self.client = client
        self.commands: list[tuple[str, str, str]] = []

    async def __aenter__(self) -> "FakePipeline":
        return self

    async def __aexit__(self, *args: object) -> None:
        return None

    def set(self, key: str, value: str) -> None:
        self.commands.append(("set", key, value))

    def publish(self, channel: str, message: str) -> None:
        self.commands.append(("publish", channel, message))

    async def execute(self) -> None:
        for command, key, value in self.commands:
            if command == "set":
                self.client.values[key] = value
            else:
                self.client.published.append((key, value))


class FakeLock:
    async def __aenter__(self) -> "FakeLock":
        return self

    async def __aexit__(self, *args: object) -> None:
        return None


@pytest.fixture
def fake_redis() -> FakeRedis:
    return FakeRedis()


@pytest.fixture
def connection_manager():
    return ConnectionManager()
