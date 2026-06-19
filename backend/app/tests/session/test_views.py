import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app.session.manager import manager
from app.session.models import DelegationContext
from app.session.schemas import States


@pytest.fixture(autouse=True)
def clear_global_manager_state() -> None:
    manager.active_connections.clear()
    manager.room_states.clear()


def session_payload(delegations: list[DelegationContext]) -> dict:
    return {
        "session_id": 0,
        "name": "Test Session",
        "delegations": [
            delegation.model_dump(mode="json") for delegation in delegations
        ],
    }


def test_create_session_endpoint_returns_204_and_stores_state(
    client: TestClient,
    delegation_list: list[DelegationContext],
) -> None:
    response = client.post("/committees/", json=session_payload(delegation_list))

    assert response.status_code == 204
    assert manager.room_states[0].current_state == States.ROLL_CALL
    assert manager.room_states[0].delegations == delegation_list
    assert manager.active_connections[0] == {}


def test_create_session_endpoint_rejects_invalid_body(client: TestClient) -> None:
    response = client.post("/committees/", json={"session_id": 0})

    assert response.status_code == 422
    assert manager.room_states == {}


def test_websocket_chair_connect_receives_state_snapshot(
    client: TestClient,
    delegation_list: list[DelegationContext],
) -> None:
    client.post("/committees/", json=session_payload(delegation_list))

    with client.websocket_connect(
        "/committees/ws/0?role=CHAIR&display_name=Chair"
    ) as websocket:
        data = websocket.receive_json()

    assert data["session_id"] == 0
    assert data["current_state"] == States.ROLL_CALL.value
    assert data["delegations"][0]["name"] == "Brazil"


def test_websocket_delegate_connect_receives_state_snapshot(
    client: TestClient,
    delegation_list: list[DelegationContext],
) -> None:
    client.post("/committees/", json=session_payload(delegation_list))

    with client.websocket_connect(
        "/committees/ws/0?role=DELEGATE&delegation_id=1"
    ) as websocket:
        data = websocket.receive_json()

    assert data["session_id"] == 0
    assert data["current_state"] == States.ROLL_CALL.value


def test_websocket_delegate_connect_rejects_unknown_delegation(
    client: TestClient,
    delegation_list: list[DelegationContext],
) -> None:
    client.post("/committees/", json=session_payload(delegation_list))

    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(
            "/committees/ws/0?role=DELEGATE&delegation_id=999"
        ):
            pass

    assert exc_info.value.code == 1008
