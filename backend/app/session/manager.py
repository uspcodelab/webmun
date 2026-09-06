"""
This file describes the overall manager for websocket and states
"""

from fastapi import WebSocket

from app.session.schemas import ServerSessionMessage

from .models import SessionActor


class ConnectionManager:
    def __init__(self):
        # Initialize dictionary with room_name and dict with websocket -> delegation
        self.active_connections: dict[int, dict[WebSocket, SessionActor]] = {}

    async def connect(self, websocket: WebSocket, session_id: int, actor: SessionActor):
        self.active_connections.setdefault(session_id, {})[websocket] = actor

    def disconnect(self, websocket: WebSocket, session_id: int):
        self.active_connections[session_id].pop(websocket)

    def get_actor(self, websocket: WebSocket, session_id: int):
        return self.active_connections.get(session_id, {}).get(websocket)

    def count_connected(self, session_id: int):
        return len(self.active_connections.get(session_id, {}))

    def count_present_delegations(self, session_id: int) -> int:
        """Count unique delegations currently connected to the session."""
        actors = self.active_connections.get(session_id, {}).values()
        return len(
            {actor.delegation.id for actor in actors if actor.delegation is not None}
        )

    async def broadcast_message(self, session_id: int, message: ServerSessionMessage):
        """Sends current state to all clients in the room"""
        for connection in self.active_connections.get(session_id, {}):
            await connection.send_json(message.model_dump(mode="json"))

    async def send_message(
        self, session_id: int, message: ServerSessionMessage, websocket: WebSocket
    ):
        """Sends a ServerSessionMessage to connected socket"""
        if self.active_connections.get(session_id, {}).get(websocket):
            await websocket.send_json(message.model_dump(mode="json"))
