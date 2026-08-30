from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest
from fastapi import WebSocketDisconnect, status

from app.auth.service import AuthUser
from app.session import enums, views
from app.session.engine import EventRejectedError
from app.session.manager import ConnectionManager
from app.session.models import DispatchOutcome, SessionActor, SessionLiveState


class FakeSessionFactory:
    async def __aenter__(self) -> object:
        return object()

    async def __aexit__(self, *args: object) -> None:
        return None

    def __call__(self) -> "FakeSessionFactory":
        return self


class FakeWebSocket:
    def __init__(self, messages: list[dict | WebSocketDisconnect]) -> None:
        self._messages = iter(messages)
        self.app = SimpleNamespace(
            state=SimpleNamespace(db_session_factory=FakeSessionFactory())
        )
        self.accepted = False
        self.closed: tuple[int, str] | None = None
        self.sent_json: list[dict] = []

    async def accept(self) -> None:
        self.accepted = True

    async def receive_json(self) -> dict:
        message = next(self._messages)
        if isinstance(message, WebSocketDisconnect):
            raise message
        return message

    async def send_json(self, message: dict) -> None:
        self.sent_json.append(message)

    async def close(self, code: int, reason: str) -> None:
        self.closed = (code, reason)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def authenticated_websocket_dependencies(monkeypatch, chair_actor: SessionActor):
    monkeypatch.setattr(
        views,
        "verify_jwt_token",
        MagicMock(
            return_value=AuthUser(
                user_id=UUID("11111111-1111-1111-1111-111111111111"),
                email="chair@example.com",
            )
        ),
    )
    monkeypatch.setattr(
        views.access,
        "resolve_session_assignment",
        AsyncMock(return_value=MagicMock()),
    )
    prepare_connect = AsyncMock(return_value=chair_actor)
    monkeypatch.setattr(views.service, "prepare_session_connect", prepare_connect)
    return prepare_connect


def authentication_message() -> dict:
    return {"type": "authenticate", "access_token": "test-token"}


def event_message(request_id: str) -> dict:
    return {
        "type": "event",
        "request_id": request_id,
        "event": {"type": enums.DelegateEvents.JOIN_QUEUE, "payload": {}},
    }


@pytest.mark.anyio
async def test_websocket_endpoint_broadcasts_dispatch_outcome(
    authenticated_websocket_dependencies,
    chair_actor: SessionActor,
    fake_redis,
    session_state: SessionLiveState,
    monkeypatch,
) -> None:
    request_id = str(uuid4())
    websocket = FakeWebSocket(
        [authentication_message(), event_message(request_id), WebSocketDisconnect()]
    )
    manager = ConnectionManager()
    handle_client_messages = AsyncMock(
        return_value=DispatchOutcome(state=session_state)
    )
    monkeypatch.setattr(views.service, "handle_client_messages", handle_client_messages)
    await views.store.save_state(fake_redis, session_state)  # type: ignore[arg-type]

    await views.websocket_endpoint(
        websocket,  # type: ignore[arg-type]
        session_id=session_state.session_id,
        manager=manager,
        engine=MagicMock(),
        logger=MagicMock(),
        settings=MagicMock(),
        redis=fake_redis,  # type: ignore[arg-type]
    )

    assert websocket.accepted is True
    assert websocket.sent_json == [
        {
            "type": "state_snapshot",
            "state": session_state.model_dump(mode="json"),
        },
        {
            "type": "dispatch_result",
            "state": session_state.model_dump(mode="json"),
            "effect": None,
        },
    ]
    handle_client_messages.assert_awaited_once()


@pytest.mark.anyio
async def test_websocket_endpoint_sends_rejection_only_to_sender(
    authenticated_websocket_dependencies,
    chair_actor: SessionActor,
    fake_redis,
    session_state: SessionLiveState,
    monkeypatch,
) -> None:
    request_id = uuid4()
    websocket = FakeWebSocket(
        [
            authentication_message(),
            event_message(str(request_id)),
            WebSocketDisconnect(),
        ]
    )
    rejection = EventRejectedError(
        enums.EventErrorCode.INVALID_STATE,
        "Cannot enter queue right now",
    )
    monkeypatch.setattr(
        views.service,
        "handle_client_messages",
        AsyncMock(return_value=rejection),
    )
    await views.store.save_state(fake_redis, session_state)  # type: ignore[arg-type]

    await views.websocket_endpoint(
        websocket,  # type: ignore[arg-type]
        session_id=session_state.session_id,
        manager=ConnectionManager(),
        engine=MagicMock(),
        logger=MagicMock(),
        settings=MagicMock(),
        redis=fake_redis,  # type: ignore[arg-type]
    )

    assert websocket.sent_json == [
        {
            "type": "state_snapshot",
            "state": session_state.model_dump(mode="json"),
        },
        {
            "type": "event_rejected",
            "request_id": str(request_id),
            "code": enums.EventErrorCode.INVALID_STATE,
            "message": "Cannot enter queue right now",
        },
    ]


@pytest.mark.anyio
async def test_websocket_endpoint_rejects_invalid_event_and_keeps_connection_open(
    authenticated_websocket_dependencies,
    chair_actor: SessionActor,
    fake_redis,
    session_state: SessionLiveState,
    monkeypatch,
) -> None:
    websocket = FakeWebSocket(
        [
            authentication_message(),
            {"type": "event", "event": {"type": "JoinQueueEvent", "payload": {}}},
            WebSocketDisconnect(),
        ]
    )
    handle_client_messages = AsyncMock()
    monkeypatch.setattr(views.service, "handle_client_messages", handle_client_messages)
    await views.store.save_state(fake_redis, session_state)  # type: ignore[arg-type]

    await views.websocket_endpoint(
        websocket,  # type: ignore[arg-type]
        session_id=session_state.session_id,
        manager=ConnectionManager(),
        engine=MagicMock(),
        logger=MagicMock(),
        settings=MagicMock(),
        redis=fake_redis,  # type: ignore[arg-type]
    )

    assert websocket.closed is None
    assert websocket.sent_json[0]["type"] == "state_snapshot"
    assert websocket.sent_json[1]["type"] == "event_rejected"
    assert websocket.sent_json[1]["request_id"] is None
    assert websocket.sent_json[1]["code"] == enums.EventErrorCode.INVALID_MESSAGE
    handle_client_messages.assert_not_awaited()


@pytest.mark.anyio
async def test_websocket_endpoint_closes_when_initial_auth_message_is_invalid(
    chair_actor: SessionActor,
    fake_redis,
) -> None:
    websocket = FakeWebSocket([{"type": "event"}])

    await views.websocket_endpoint(
        websocket,  # type: ignore[arg-type]
        session_id=1,
        manager=ConnectionManager(),
        engine=MagicMock(),
        logger=MagicMock(),
        settings=MagicMock(),
        redis=fake_redis,  # type: ignore[arg-type]
    )

    assert websocket.accepted is True
    assert websocket.closed == (status.WS_1008_POLICY_VIOLATION, "invalid_json")
