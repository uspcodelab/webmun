import pytest

from app.session.manager import ConnectionManager, SessionLiveState
from app.session.models import DispatchOutcome, SessionActor
from app.session.schemas import DispatchResultMessage, StateSnapshotMessage


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
async def test_connect_sends_existing_room_state(
    connection_manager: ConnectionManager,
    session_state: SessionLiveState,
    chair_actor: SessionActor,
) -> None:
    websocket = FakeWebSocket()
    connection_manager.room_states[session_state.session_id] = session_state

    await connection_manager.connect(
        websocket,  # type:ignore
        session_id=session_state.session_id,
        actor=chair_actor,
    )

    expected_json = StateSnapshotMessage(state=session_state).model_dump(mode="json")

    assert websocket.sent_json[-1] == expected_json


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
    session_state: SessionLiveState,
    chair_actor: SessionActor,
    delegate_actor: SessionActor,
) -> None:
    chair_socket = FakeWebSocket()
    delegate_socket = FakeWebSocket()
    connection_manager.room_states[session_state.session_id] = session_state
    await connection_manager.connect(
        chair_socket,  # type:ignore
        session_state.session_id,
        chair_actor,
    )
    await connection_manager.connect(
        delegate_socket,  # type:ignore
        session_state.session_id,
        delegate_actor,
    )

    chair_socket.sent_json.clear()
    delegate_socket.sent_json.clear()

    outcome = DispatchOutcome(state=session_state)
    msg = DispatchResultMessage(state=outcome.state, effect=outcome.effect)

    await connection_manager.broadcast_message(session_state.session_id, msg)

    expected = msg.model_dump(mode="json")
    assert chair_socket.sent_json == [expected]
    assert delegate_socket.sent_json == [expected]


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

    await connection_manager.broadcast_message(session_state.session_id, state=None)  # type:ignore
