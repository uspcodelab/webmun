import pytest

from app.session.manager import ConnectionManager, SessionLiveState
from app.session.models import SessionActor


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

    await connection_manager.connect(websocket, session_id=1, actor=chair_actor)

    assert connection_manager.active_connections[1][websocket] == chair_actor
    assert connection_manager.get_actor(websocket, 1) == chair_actor
    assert connection_manager.count_connected(1) == 1


@pytest.mark.anyio
async def test_connect_sends_existing_room_state(
    connection_manager: ConnectionManager,
    session_state: SessionLiveState,
    chair_actor: SessionActor,
) -> None:
    websocket = FakeWebSocket()
    connection_manager.room_states[session_state.session_id] = session_state

    await connection_manager.connect(
        websocket,
        session_id=session_state.session_id,
        actor=chair_actor,
    )

    assert websocket.sent_json == [session_state.model_dump(mode="json")]


@pytest.mark.anyio
async def test_disconnect_removes_socket(
    connection_manager: ConnectionManager,
    chair_actor: SessionActor,
) -> None:
    websocket = FakeWebSocket()
    await connection_manager.connect(websocket, session_id=1, actor=chair_actor)

    connection_manager.disconnect(websocket, session_id=1)

    assert connection_manager.active_connections[1] == {}
    assert connection_manager.count_connected(1) == 0


@pytest.mark.anyio
async def test_broadcast_state_sends_snapshot_to_all_connections(
    connection_manager: ConnectionManager,
    session_state: SessionLiveState,
    chair_actor: SessionActor,
    delegate_actor: SessionActor,
) -> None:
    chair_socket = FakeWebSocket()
    delegate_socket = FakeWebSocket()
    connection_manager.room_states[session_state.session_id] = session_state
    await connection_manager.connect(
        chair_socket,
        session_state.session_id,
        chair_actor,
    )
    await connection_manager.connect(
        delegate_socket,
        session_state.session_id,
        delegate_actor,
    )

    chair_socket.sent_json.clear()
    delegate_socket.sent_json.clear()

    await connection_manager.broadcast_state(session_state.session_id)

    expected = session_state.model_dump(mode="json")
    assert chair_socket.sent_json == [expected]
    assert delegate_socket.sent_json == [expected]


@pytest.mark.anyio
async def test_broadcast_state_without_room_state_is_noop(
    connection_manager: ConnectionManager,
    chair_actor: SessionActor,
) -> None:
    websocket = FakeWebSocket()
    await connection_manager.connect(websocket, session_id=1, actor=chair_actor)

    await connection_manager.broadcast_state(session_id=1)

    assert websocket.sent_json == []


@pytest.mark.xfail(
    strict=True,
    reason="broadcast_state indexes active_connections when state exists.",
)
@pytest.mark.anyio
async def test_broadcast_state_without_connections_is_noop(
    connection_manager: ConnectionManager,
    session_state: SessionLiveState,
) -> None:
    connection_manager.room_states[session_state.session_id] = session_state

    await connection_manager.broadcast_state(session_state.session_id)
