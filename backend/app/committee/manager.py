"""
This file describes the overall manager for websocket and states
"""
from fastapi import WebSocket
from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        # Initialize dictionary with room_name and list of connections
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, committee_id: int):
        await websocket.accept()
        self.active_connections[committee_id].append(websocket)

    def disconnect(self, websocket: WebSocket, committee_id: int):
        self.active_connections[committee_id].remove(websocket)

    # More things from connection manager here 

manager = ConnectionManager()

