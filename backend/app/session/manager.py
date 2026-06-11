"""
This file describes the overall manager for websocket and states
"""
from fastapi import WebSocket
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

from .schemas import DebateTypes, RollCallChoice, States, DelegateMotionPayload, DelegateQuestionPayload

class VotingContext(BaseModel):
    target_type: Literal["PROCEDURAL", "SUBSTANTIVE", "INFORMAL"]
    motion_in_vote: DelegateMotionPayload | None = None
    title: str | None = None 
    return_state: States | None = None # If rejected, returns to this state.
    voting_registry: dict[str, Literal["FAVOUR", "AGAINST", "ABSTAIN"]] = {}

    # additional fields
    majority: Literal['SIMPLE', 'QUALIFIED', 'ABSOLUTE']
    veto_power: bool

class DebateContext(BaseModel):
    debate_type: DebateTypes 
    return_state: States 
    total_duration_seconds: int | None = None # TODO: check if this is needed 
    total_speeches: int | None = None # Check if we use total duration or this for calculating overall time, it can also go overtime 
    per_speaker_seconds: int | None = None
    expires_at: datetime | None = None 
    topic: str | None = None

class RollCallContext(BaseModel):
    registry: dict[str, RollCallChoice] = {}
    current_delegation: str | None = None # perhaps not needed

# Represents the session live state
class SessionLiveState(BaseModel):
    session_id: int
    start_time: datetime

    # temporary list of delegations in this committee
    # TODO: validate sender delegation to this list
    delegations: list[str]

    # General state for FSM engine
    current_state: States = States.SETUP

    # Timer states
    timer_is_running: bool = False
    timer_expiration: datetime | None = None
    timer_remaining_seconds: int = 0 # update on pause/increase, can go negative 

    # Speakers 
    current_speaker: str | None = None
    gsl_queue: list[str] = []
    can_set_motion: bool = False # Can set motions during speaking time
    gsl_default_time_seconds: int = 60

    # Caucus variables
    # TODO: how to add a popup placard that fades away after some moment in frontend? related to CHOOSE_SPEAKER
    caucus_list: list[str] = [] # special list that is only used during moderated caucus, has different semantic functionality than gsl queue 
    debate: DebateContext | None = None # used specially for Moderated, unmoderated and possibly tour de table

    # Context Data
    # MotionSchema inherits it's type from Motions
    _motion_id_counter = 0
    _question_id_counter = 0
    submitted_motions: list[DelegateMotionPayload] = []
    submitted_questions: list[DelegateQuestionPayload] = []

    # Agenda
    agenda_topics: list[tuple[str, bool]] = []
    active_topic_index: int | None = None


    # Voting context
    voting: VotingContext | None = None
    
    # present delegations with voting choice
    voting_choice: dict[str, RollCallChoice] | None = None 

    roll_call: RollCallContext | None = None # set to none at first

class ConnectionManager:
    # TODO: refactor additional field 'delegation' when working with auth

    def __init__(self):
        # Initialize dictionary with room_name and dict with websocket -> delegation
        # TODO: needs per room dict initialization. So when a session is created, it needs to create a dict model here
        self.active_connections: dict[int, dict[WebSocket, str]] = {}
        self.room_states: dict[int, SessionLiveState] = {}
    
    async def connect(self, websocket: WebSocket, session_id: int, delegation: str):
        await websocket.accept()
        self.active_connections[session_id][websocket] = delegation

        # when someone connects, send current state as SessionLiveState
        if session_id in self.room_states:
            await websocket.send_json(self.room_states[session_id].model_dump(mode='json'))

    def disconnect(self, websocket: WebSocket, session_id: int):
        self.active_connections[session_id].pop(websocket)

    def get_delegation(self, websocket: WebSocket, session_id: int):
        return self.active_connections[session_id].get(websocket)

    # More things from connection manager here 
    async def broadcast_state(self, session_id: int):
        """Sends current state to all clients in the room"""
        state = self.room_states.get(session_id)
        if not state:
            return

        for connection in self.active_connections[session_id]:
            await connection.send_json(state.dict())

    # TODO: add broadcast_event so we send only the event + deltas (fields changed)/event only, or keep broadcasting entire state

manager = ConnectionManager()

