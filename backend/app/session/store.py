import asyncio
import logging

import redis.asyncio as redis

from app.session.manager import ConnectionManager
from app.session.models import DispatchOutcome
from app.session.schemas import DispatchResultMessage

SESSION_STATE_CHANNEL = "webmun:session:updates"


def state_key(session_id: int) -> str:
    return f"webmun:session:{session_id}"


async def get_outcome(client: redis.Redis, session_id: int) -> DispatchOutcome | None:
    """Get the current state for a session"""
    res = await client.get(state_key(session_id))
    if res is None:
        return None

    return DispatchOutcome.model_validate_json(res)


async def save_outcome(client: redis.Redis, result: DispatchOutcome) -> None:
    """Only save outcome in the client cache"""
    await client.set(state_key(result.state.session_id), result.model_dump_json())


async def save_publish_outcome(client: redis.Redis, result: DispatchOutcome) -> None:
    """Save outcome and publish to the channel"""
    serialized_outcome = result.model_dump_json()
    async with client.pipeline() as pipe:
        pipe.set(state_key(result.state.session_id), serialized_outcome)
        pipe.publish(SESSION_STATE_CHANNEL, result.model_dump_json())
        await pipe.execute()


async def delete_outcome(client: redis.Redis, session_id: int) -> None:
    await client.delete(state_key(session_id))


async def subscriber_worker(
    client: redis.Redis, connection_manager: ConnectionManager, logger: logging.Logger
) -> None:
    async with client.pubsub() as pubsub:
        try:
            await pubsub.subscribe(SESSION_STATE_CHANNEL)
            logger.info("Subscribed to Redis channel %s", SESSION_STATE_CHANNEL)

            async for message in pubsub.listen():
                if message and message["type"] == "message":
                    try:
                        outcome = DispatchOutcome.model_validate_json(message["data"])
                        result = DispatchResultMessage(
                            state=outcome.state, effect=outcome.effect
                        )
                        await connection_manager.broadcast_message(
                            session_id=outcome.state.session_id, message=result
                        )
                    except Exception:
                        logger.exception("Failed to relay Redis session update")
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Redis Pub/Sub worker stopped")
            raise
