import pytest

from app.session import store
from app.session.models import SessionLiveState


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_save_and_get_state(fake_redis, session_state: SessionLiveState) -> None:
    await store.save_state(fake_redis, session_state)  # type: ignore[arg-type]

    state = await store.get_state(fake_redis, session_state.session_id)  # type: ignore[arg-type]

    assert state == session_state


@pytest.mark.anyio
async def test_get_missing_state_returns_none(fake_redis) -> None:
    assert await store.get_state(fake_redis, 404) is None  # type: ignore[arg-type]


@pytest.mark.anyio
async def test_delete_state_removes_saved_state(
    fake_redis, session_state: SessionLiveState
) -> None:
    await store.save_state(fake_redis, session_state)  # type: ignore[arg-type]
    await store.delete_state(fake_redis, session_state.session_id)  # type: ignore[arg-type]

    assert await store.get_state(fake_redis, session_state.session_id) is None  # type: ignore[arg-type]
