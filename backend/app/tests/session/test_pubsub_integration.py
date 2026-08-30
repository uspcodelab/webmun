"""Integration coverage for Redis fan-out across independent backend nodes."""

import asyncio
import logging
import os

import pytest
from redis.asyncio import Redis

from app.session import store
from app.session.manager import ConnectionManager
from app.session.models import DispatchOutcome, SessionActor, SessionLiveState


class RecordingWebSocket:
    def __init__(self) -> None:
        self.messages: list[dict] = []
        self.message_received = asyncio.Event()

    async def send_json(self, message: dict) -> None:
        self.messages.append(message)
        self.message_received.set()


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def redis_test_url() -> str:
    url = os.environ.get("REDIS_TEST_URL")
    if url is None:
        pytest.skip("set REDIS_TEST_URL to run Redis integration tests")
    return url


@pytest.mark.anyio
async def test_publish_relays_outcome_to_connections_on_two_nodes(
    redis_test_url: str,
    chair_actor: SessionActor,
    session_state: SessionLiveState,
) -> None:
    publisher = Redis.from_url(redis_test_url)
    node_one_client = Redis.from_url(redis_test_url)
    node_two_client = Redis.from_url(redis_test_url)
    node_one_manager = ConnectionManager()
    node_two_manager = ConnectionManager()
    node_one_socket = RecordingWebSocket()
    node_two_socket = RecordingWebSocket()
    node_one_ready = asyncio.Event()
    node_two_ready = asyncio.Event()
    logger = logging.getLogger("test.redis_pubsub")

    try:
        await publisher.ping()
        await publisher.flushdb()
        await node_one_manager.connect(
            node_one_socket, session_state.session_id, chair_actor
        )  # type: ignore[arg-type]
        await node_two_manager.connect(
            node_two_socket, session_state.session_id, chair_actor
        )  # type: ignore[arg-type]
        node_one_task = asyncio.create_task(
            store.subscriber_worker(
                node_one_client, node_one_manager, logger, ready=node_one_ready
            )
        )
        node_two_task = asyncio.create_task(
            store.subscriber_worker(
                node_two_client, node_two_manager, logger, ready=node_two_ready
            )
        )
        await asyncio.wait_for(
            asyncio.gather(node_one_ready.wait(), node_two_ready.wait()), timeout=5
        )

        outcome = DispatchOutcome(state=session_state)
        await store.save_publish_outcome(publisher, outcome)

        await asyncio.wait_for(node_one_socket.message_received.wait(), timeout=5)
        await asyncio.wait_for(node_two_socket.message_received.wait(), timeout=5)

        expected = {
            "type": "dispatch_result",
            "state": session_state.model_dump(mode="json"),
            "effect": None,
        }
        assert node_one_socket.messages == [expected]
        assert node_two_socket.messages == [expected]
        assert await store.get_outcome(publisher, session_state.session_id) == outcome
    finally:
        for task in (locals().get("node_one_task"), locals().get("node_two_task")):
            if task is not None:
                task.cancel()
        await asyncio.gather(
            *(
                task
                for task in (
                    locals().get("node_one_task"),
                    locals().get("node_two_task"),
                )
                if task is not None
            ),
            return_exceptions=True,
        )
        await publisher.flushdb()
        await asyncio.gather(
            publisher.aclose(), node_one_client.aclose(), node_two_client.aclose()
        )
