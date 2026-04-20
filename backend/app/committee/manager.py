"""
This file describes the overall manager for websocket and states
"""
from fastapi import WebSocket
from collections import defaultdict
from pydantic import BaseModel
from datetime import datetime 

# Represents the committee live state 
class CommitteeLiveState(BaseModel):
    committee_id: int
    committee_name: str
    start_time: datetime = None

class ConnectionManager:
    def __init__(self):
        # Initialize dictionary with room_name and list of connections
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)
        # maps committee_id to current committee state 
        self.room_states: dict[int, CommitteeLiveState] = {}

    async def connect(self, websocket: WebSocket, committee_id: int):
        await websocket.accept()
        self.active_connections[committee_id].append(websocket)

        # when someone connects, send current state 
        if committee_id in self.room_states:
            await websocket.send_json({
                "type": "INITIAL_STATE",
                "payload": self.room_states[committee_id].model_dump(mode='json'),
                })

    def disconnect(self, websocket: WebSocket, committee_id: int):
        self.active_connections[committee_id].remove(websocket)

    # More things from connection manager here 
    async def broadcast_state(self, committee_id: int):
        """Sends current state to all clients in the room"""
        state = self.room_states.get(committee_id)
        if not state:
            return
        
        message = {
                "type": "STATE_UPDATE",
                "payload": state.dict()
        }

        for connection in self.active_connections[committee_id]:
            await connection.send_json(message)

manager = ConnectionManager()

