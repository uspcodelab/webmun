import redis.asyncio as redis

from app.session.models import SessionLiveState


async def get_state(session: redis.Redis, session_id: int) -> SessionLiveState | None:
    res = await session.get(f"webmun:session:{session_id}")
    if res is None:
        return None

    return SessionLiveState.model_validate_json(res)


async def save_state(session: redis.Redis, state: SessionLiveState) -> None:
    await session.set(f"webmun:session:{state.session_id}", state.model_dump_json())


async def delete_state(session: redis.Redis, session_id: int) -> None:
    await session.delete(f"webmun:session:{session_id}")
