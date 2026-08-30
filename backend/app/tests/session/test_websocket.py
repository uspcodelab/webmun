import pytest

from app.session import enums
from app.session.manager import ConnectionManager
from app.session.models import SessionActor
from app.session.schemas import (
    DispatchResultMessage,
    EventRejectedMessage,
)


class FakeWebSocket:
    def __init__(self) -> None:
        self.sent_json: list[dict] = []

    async def send_json(self, data: dict) -> None:
        self.sent_json.append(data)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def connection_manager() -> ConnectionManager:
    return ConnectionManager()


@pytest.mark.anyio
async def test_connect_stores_actor(
    connection_manager: ConnectionManager,
    chair_actor: SessionActor,
) -> None:
    websocket = FakeWebSocket()

    await connection_manager.connect(websocket, session_id=1, actor=chair_actor)  # type:ignore

    assert connection_manager.active_connections[1][websocket] == chair_actor  # type:ignore
    assert connection_manager.get_actor(websocket, 1) == chair_actor  # type:ignore
    assert connection_manager.count_connected(1) == 1


@pytest.mark.anyio
@pytest.mark.anyio
async def test_disconnect_removes_socket(
    connection_manager: ConnectionManager,
    chair_actor: SessionActor,
) -> None:
    websocket = FakeWebSocket()
    await connection_manager.connect(websocket, session_id=1, actor=chair_actor)  # type:ignore

    connection_manager.disconnect(websocket, session_id=1)  # type:ignore

    assert connection_manager.active_connections[1] == {}
    assert connection_manager.count_connected(1) == 0


@pytest.mark.anyio
async def test_broadcast_state_sends_snapshot_to_all_connections(
    connection_manager: ConnectionManager,
    session_state,
    chair_actor: SessionActor,
    delegate_actor: SessionActor,
) -> None:
    chair_socket = FakeWebSocket()
    delegate_socket = FakeWebSocket()
    await connection_manager.connect(
        chair_socket,  # type:ignore
        1,
        chair_actor,
    )
    await connection_manager.connect(
        delegate_socket,  # type:ignore
        1,
        delegate_actor,
    )

    chair_socket.sent_json.clear()
    delegate_socket.sent_json.clear()

    msg = DispatchResultMessage(state=session_state, effect=None)

    await connection_manager.broadcast_message(1, msg)

    expected = msg.model_dump(mode="json")
    assert chair_socket.sent_json == [expected]
    assert delegate_socket.sent_json == [expected]


@pytest.mark.anyio
async def test_send_message_sends_rejection_only_to_originating_connection(
    connection_manager: ConnectionManager,
    chair_actor: SessionActor,
    delegate_actor: SessionActor,
) -> None:
    chair_socket = FakeWebSocket()
    delegate_socket = FakeWebSocket()
    await connection_manager.connect(chair_socket, session_id=1, actor=chair_actor)  # type: ignore[arg-type]
    await connection_manager.connect(
        delegate_socket, session_id=1, actor=delegate_actor
    )  # type: ignore[arg-type]
    message = EventRejectedMessage(
        code=enums.EventErrorCode.INVALID_STATE,
        message="Cannot enter queue right now",
    )

    await connection_manager.send_message(1, message, delegate_socket)  # type: ignore[arg-type]

    assert chair_socket.sent_json == []
    assert delegate_socket.sent_json == [message.model_dump(mode="json")]


@pytest.mark.anyio
@pytest.mark.xfail(
    strict=True,
    reason="broadcast_message indexes active_connections when no clients are connected.",
)
async def test_broadcast_state_without_connections_is_noop(
    connection_manager: ConnectionManager,
) -> None:
    await connection_manager.broadcast_message(
        1,
        message=EventRejectedMessage(
            code=enums.EventErrorCode.INVALID_STATE,
            message="No connected clients",
        ),
    )
