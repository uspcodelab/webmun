# This file defines internal models not used as schemas for the application
# Even though it's internal, some things may be sent out to public (TODO:like SessionLiveState)
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Literal

from .schemas import DebateTypes, RollCallChoice, States, DelegateMotionPayload, DelegateQuestionPayload #We'll probably remove or move some of these

# This may be used for SessionLiveState as well, but mainly used in SessionActor
class DelegationContext(BaseModel):
    id: int
    seat: str
    name: str
    code: str

class SessionRole(str, Enum):
    CHAIR = "CHAIR"
    DELEGATE = "DELEGATE"
    # further roles are put here

class SessionActor(BaseModel):
    role: SessionRole
    display_name: str = "Placeholder"
    delegation: DelegationContext | None = None

#Most likely there will be substantial changes to models down here
# TODO: separate this in relation to Schema and Model 
# Current

class VotingContext(BaseModel):
    target_type: Literal["PROCEDURAL", "SUBSTANTIVE", "INFORMAL"]
    motion_in_vote: DelegateMotionPayload | None = None
    title: str | None = None 
    return_state: States 
    voting_registry: dict[int, Literal["FAVOUR", "AGAINST", "ABSTAIN"]] = {}

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
    registry: dict[int, RollCallChoice] = {} #Delegation Id as key
    current_delegation: int | None = None # perhaps not needed

# Represents the session live state
class SessionLiveState(BaseModel):
    session_id: int
    start_time: datetime

    # temporary list of delegations in this committee
    delegations: list[DelegationContext]

    # General state for FSM engine
    current_state: States = States.SETUP

    # Timer states
    timer_is_running: bool = False
    timer_expiration: datetime | None = None
    timer_remaining_seconds: int = 0 # update on pause/increase, can go negative 

    # Speakers 
    current_speaker: int | None = None
    gsl_queue: list[int] = []
    can_set_motion: bool = False # Can set motions during speaking time
    gsl_default_time_seconds: int = 60

    # Caucus variables
    # TODO: how to add a popup placard that fades away after some moment in frontend? related to CHOOSE_SPEAKER
    caucus_list: list[int] = [] # special list that is only used during moderated caucus, has different semantic functionality than gsl queue 
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
    voting_choice: dict[int, RollCallChoice] | None = None # DelegationId as key

    roll_call: RollCallContext #Not None, even if registry is empty