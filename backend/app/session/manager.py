"""
This file describes the overall manager for websocket and states
"""

from fastapi import WebSocket

from .models import SessionActor, SessionLiveState


class ConnectionManager:
    # TODO: refactor additional field 'delegation' when working with auth

    def __init__(self):
        # Initialize dictionary with room_name and dict with websocket -> delegation
        self.active_connections: dict[int, dict[WebSocket, SessionActor]] = {}
        self.room_states: dict[int, SessionLiveState] = {}

    #
    async def connect(self, websocket: WebSocket, session_id: int, actor: SessionActor):
        await websocket.accept()
        self.active_connections.setdefault(session_id, {})[websocket] = actor

        # when someone connects, send current state as SessionLiveState
        if session_id in self.room_states:
            # TODO: check if it's better to create with mode='json' or model_dump_json()
            await websocket.send_json(
                self.room_states[session_id].model_dump(mode="json")
            )

    def disconnect(self, websocket: WebSocket, session_id: int):
        self.active_connections[session_id].pop(websocket)

    def get_actor(self, websocket: WebSocket, session_id: int):
        return self.active_connections.get(session_id, {}).get(websocket)

    def count_connected(self, session_id: int):
        return len(self.active_connections.get(session_id, {}))

    def count_present_delegations(self, session_id: int) -> int:
        """Count unique delegations currently connected to the session."""
        actors = self.active_connections.get(session_id, {}).values()
        return len({actor.delegation.id for actor in actors if actor.delegation is not None})

    # More things from connection manager here 
    async def broadcast_state(self, session_id: int):
        """Sends current state to all clients in the room"""
        state = self.room_states.get(session_id)
        if not state:
            return

        for connection in self.active_connections[session_id]:
            await connection.send_json(state.model_dump(mode="json"))

    # TODO: add broadcast_event so we send only the event + deltas (fields changed)/event only, or keep broadcasting entire state
