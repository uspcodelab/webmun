"""
This file describes the overall manager for websocket and states
"""
from fastapi import WebSocket
from collections import defaultdict
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

from .schemas import States, DelegateMotionPayload, DelegateQuestionPayload

# Metadata that tracks the voting scheme currently in use
class VotingContext(BaseModel):
    target_type: Literal["PROCEDURAL", "SUBSTANTIVE"] = "PROCEDURAL"
    motion_in_vote: int | None = None # Motion ID to be executed
    voting_registry: dict[str, Literal["FAVOUR", "AGAINST", "ABSTAIN"]] = {}


# Represents the session live state
class SessionLiveState(BaseModel):
    session_id: int
    session_name: str | None = None
    start_time: datetime

    # General state for FSM engine
    current_state: States = States.SETUP
    # gsl_queue_locker?

    # Timer states
    timer_is_running: bool = False
    timer_expiration: datetime | None = None
    timer_duration_seconds: int = 0

    # Speakers
    current_speaker: str | None = None
    gsl_queue: list[str] = []
    can_set_motion: bool = False # Can set motions during speaking time

    # Context Data
    # MotionSchema inherits it's type from Motions
    _motion_id_counter = 0
    _question_id_counter = 0
    submitted_motions: list[DelegateMotionPayload] = []
    submitted_questions: list[DelegateQuestionPayload] = []

    # Agenda
    agenda_topics: list[tuple[str, bool]] = []
    active_topic_index: int | None = None

    # Present delegations
    present_delegations: list[str] = []

    # Voting context
    voting: VotingContext

    # maps to present | present and voting styles
    voting_choice: dict[str, Literal["PRESENT", "VOTING"]]

# to be implemented later
class WebSocketEnvelope(BaseModel):
    pass

class ConnectionManager:
    def __init__(self):
        # Initialize dictionary with room_name and list of connections
        self.active_connections: dict[int, list[WebSocket]] = defaultdict(list)
        # maps committee_id to current committee state 
        self.room_states: dict[int, SessionLiveState] = {}

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

