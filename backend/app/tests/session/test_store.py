import pytest

from app.session import store
from app.session.models import DispatchOutcome, SessionLiveState


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_save_and_get_outcome(
    fake_redis, session_state: SessionLiveState
) -> None:
    outcome = DispatchOutcome(state=session_state)
    await store.save_outcome(fake_redis, outcome)  # type: ignore[arg-type]

    saved = await store.get_outcome(fake_redis, session_state.session_id)  # type: ignore[arg-type]

    assert saved == outcome


@pytest.mark.anyio
async def test_get_missing_outcome_returns_none(fake_redis) -> None:
    assert await store.get_outcome(fake_redis, 404) is None  # type: ignore[arg-type]


@pytest.mark.anyio
async def test_delete_outcome_removes_saved_outcome(
    fake_redis, session_state: SessionLiveState
) -> None:
    await store.save_outcome(fake_redis, DispatchOutcome(state=session_state))  # type: ignore[arg-type]
    await store.delete_outcome(fake_redis, session_state.session_id)  # type: ignore[arg-type]

    assert await store.get_outcome(fake_redis, session_state.session_id) is None  # type: ignore[arg-type]


@pytest.mark.anyio
async def test_save_publish_outcome_updates_cache_and_publishes(
    fake_redis, session_state: SessionLiveState
) -> None:
    outcome = DispatchOutcome(state=session_state)

    await store.save_publish_outcome(fake_redis, outcome)  # type: ignore[arg-type]

    assert await store.get_outcome(fake_redis, session_state.session_id) == outcome  # type: ignore[arg-type]
    assert fake_redis.published == [
        (store.SESSION_STATE_CHANNEL, outcome.model_dump_json())
    ]
