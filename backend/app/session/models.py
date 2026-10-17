# This file defines internal models not used as schemas for the application
# Even though it's internal, some things may be sent out to public (TODO:like SessionLiveState)
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
from sre_parse import State
from token import OP
from typing import Any, Literal, Annotated, ClassVar
from uuid import UUID

from pydantic import BaseModel, Field

import app.session.enums as enums
from app.session.enums import States


@dataclass(frozen=True)
class StoredSession:
    id: int
    committee_id: int
    name: str | None
    status: str
    started_at: datetime
    ended_at: datetime
    state_snapshot: dict | None


# TODO: separate this into a DelegationContext with a name/user_id or profile and SeatContext for a map
class DelegationContext(BaseModel):
    id: int
    name: str
    seat: str
    code: str


class SessionActor(BaseModel):
    user_id: UUID
    role: enums.SessionRole
    display_name: str = "Placeholder"
    delegation: DelegationContext | None = None


class MotionContext(BaseModel):
    id: int | None = None
    priority: int = 0
    type: enums.Motions
    delegate_id: int | None = None
    timestamp: datetime
    debate_type: enums.DebateTypes | None = None

    total_duration_minutes: int | None = None
    per_speaker_seconds: int | None = None
    target_topic: str | None = None
    speech_count: int | None = None

    details: str | None = None


class QuestionContext(BaseModel):
    id: int | None = None
    priority: int = 0
    type: enums.Questions
    delegate_id: int | None = None  # Really None?
    details: str | None = None


class VotingContext(BaseModel):
    target_type: enums.VotingType
    title: str | None = None
    return_state: StateTypes
    voting_registry: dict[int, enums.VotingChoice] = {}
    majority: enums.MajorityTypes | None = None

    motion_in_vote: MotionContext | None = None
    # resolution_in_vote: ResolutionContext

    allow_veto_power: bool = False

    def is_choice_allowed(self, choice: enums.VotingChoice) -> bool:
        if self.target_type == enums.VotingType.PROCEDURAL:
            return choice in (enums.VotingChoice.FAVOUR, enums.VotingChoice.AGAINST)

        return True

class DebateContext(BaseModel):
    debate_type: enums.DebateTypes
    return_state: StateTypes | None = None #TEMPORARY

    #unmoderated debate
    total_duration_seconds: int | None = None
    #moderated debate
    total_speeches: int | None = None
    #moderated debate and GSL
    per_speaker_seconds: int | None = None
    #GSL
    closed: bool | None = None


class RollCallContext(BaseModel):
    registry: dict[int, enums.RollCallChoice] = {}  # Delegation Id as key
    return_state: StateTypes | None = None


class AgendaItem(BaseModel):
    index: str
    topic: str
    already_discussed: bool

##SESSION STATES

class SessionState(BaseModel, ABC):

    state_name : ClassVar

    @abstractmethod
    def enterState(self, state : SessionLiveState):
        ...

    @abstractmethod
    def exitState(self, state: SessionLiveState):
        ...

class SetupState(SessionState):
    """Dummy starting State, it's properties are defined when activating a session"""
    state_name : Literal[States.SETUP] = States.SETUP

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        ...

class RollCallState(SessionState):
    state_name : Literal[States.ROLL_CALL] = States.ROLL_CALL
    return_state : StateTypes | None = None

    def enterState(self, state: SessionLiveState):
        state.roll_call = RollCallContext(registry={}, return_state=self.return_state)

    def exitState(self, state: SessionLiveState):
        ...

class OpenGSLState(SessionState):
    state_name : Literal[States.OPEN_GSL] = States.OPEN_GSL
    return_state : StateTypes | None = None
    per_speaker_seconds : int | None = None

    def enterState(self, state: SessionLiveState):
        state.debate = DebateContext(
                        debate_type=enums.DebateTypes.SPEAKERS_LIST,
                        return_state=self.return_state,
                        per_speaker_seconds=self.per_speaker_seconds or state.default_time_seconds,
                        closed=False
                    )

    def exitState(self, state: SessionLiveState):
        state.debate = None

class ClosedGSLState(SessionState):
    state_name : Literal[States.CLOSED_GSL] = States.CLOSED_GSL
    return_state : StateTypes | None = None
    per_speaker_seconds : int | None = None

    def enterState(self, state: SessionLiveState):
        state.debate = DebateContext(
                debate_type=enums.DebateTypes.SPEAKERS_LIST,
                return_state=self.return_state,
                per_speaker_seconds=self.per_speaker_seconds or state.default_time_seconds,
                closed=True
            )

    def exitState(self, state: SessionLiveState):
        state.debate = None

class ModeratedCaucusState(SessionState):
    state_name : Literal[States.MODERATED_CAUCUS] = States.MODERATED_CAUCUS
    return_state : StateTypes | None = None
    per_speaker_seconds : int | None = None
    total_speeches : int | None = None

    def enterState(self, state: SessionLiveState):
        state.debate = DebateContext(
            debate_type=enums.DebateTypes.MODERATED_DEBATE,
            return_state=self.return_state,
            per_speaker_seconds=self.per_speaker_seconds or state.default_time_seconds,
            total_speeches= self.total_speeches,
        )

    def exitState(self, state: SessionLiveState):
        state.debate = None

class UnmoderatedCaucusState(SessionState):
    state_name : Literal[States.UNMODERATED_CAUCUS] = States.UNMODERATED_CAUCUS
    return_state : StateTypes | None = None
    total_duration_minutes : int | None

    def enterState(self, state: SessionLiveState):
        duration = (self.total_duration_minutes or 5) * 60
        state.debate = DebateContext(
            debate_type=enums.DebateTypes.UNMODERATED_DEBATE,
            return_state=self.return_state,
            total_duration_seconds=duration,
        )
        state.reset_timer(duration)

    def exitState(self, state: SessionLiveState):
        state.debate = None

class TourDeTableState(SessionState):
    """To be implemented"""
    state_name : Literal[States.TOUR_DE_TABLE] = States.TOUR_DE_TABLE

    def enterState(self, state: SessionLiveState):
        ...

    def exitState(self, state: SessionLiveState):
        state.debate = None


class VotingExecutionState(SessionState):
    state_name : Literal[States.VOTING_EXECUTION] = States.VOTING_EXECUTION

    context : VotingContext
    def enterState(self, state: SessionLiveState):
        state.voting = self.context
    def exitState(self, state: SessionLiveState):
        state.voting = None

class FinishedState(SessionState):
    state_name : Literal[States.FINISHED] = States.FINISHED

    def enterState(self, state: SessionLiveState):
        state.current_speaker = None
        state.gsl_queue = []  # I'm supposing this queue has the first element popped when someone speaks,
        # so it should be empty when session is closed. In case this list is to be kept,
        # we can remove this line.
        state.can_set_motion = False
        state.debate = None  # Same as queue
        state.timer_is_running = False
        state.timer_expiration = None
        state.timer_remaining_seconds = 0

    def exitState(self, state: SessionLiveState):
        ...

StateTypes = Annotated[ 
    SetupState | 
    RollCallState | 
    OpenGSLState | 
    ClosedGSLState | 
    ModeratedCaucusState | 
    UnmoderatedCaucusState |
    TourDeTableState |
    VotingExecutionState |
    FinishedState, Field(discriminator="state_name") ]

# Represents the session live state
class SessionLiveState(BaseModel):
    session_id: int
    start_time: datetime

    # list of present representations (rep_id)
    delegations: dict[int, DelegationContext]

    #private state object for FSM engine
    state_obj : StateTypes
    # General state for FSM engine
    current_state: enums.States = enums.States.SETUP

    # Timer states
    timer_is_running: bool = False
    timer_expiration: datetime | None = None
    timer_remaining_seconds: int = 0  # update on pause/increase, can go negative

    # Speakers
    current_speaker: int | None = None
    gsl_queue: list[int] = [] #Never resets, so it's in global context
    can_set_motion: bool = False  # Can set motions during speaking time
    default_time_seconds: int = 60

    # Caucus variables
    debate: DebateContext | None = (
        None  # used specially for Moderated, unmoderated and possibly tour de table
    )

    # Context Data
    # MotionSchema inherits it's type from Motions
    _motion_id_counter = 0
    _question_id_counter = 0
    submitted_motions: list[MotionContext] = []
    submitted_questions: list[QuestionContext] = []

    # Agenda
    agenda_topics: dict[str, AgendaItem] = {}
    active_topic_index: str | None = None

    # Voting context
    voting: VotingContext | None = None

    # present delegations with voting choice
    roll_call: RollCallContext = RollCallContext() # Not None, even if registry is empty

    #Temporary Speaker History
    previous_speakers: list[int] = [] #temporary list for now

    # Additional config
    has_veto_power: bool = False

    default_debate: OpenGSLState | ModeratedCaucusState | UnmoderatedCaucusState = Field(discriminator="state_name")

    def transition_to(self: SessionLiveState, state: StateTypes) -> None:
        self.state_obj.exitState(self)
        state.enterState(self)
        self.current_state = state.state_name
        self.state_obj = state

    def reset_timer(self: SessionLiveState, seconds: int = 0) -> None:
        self.timer_is_running = False
        self.timer_expiration = None
        self.timer_remaining_seconds = seconds


#Add more for other effects (Possibly change the Voting context, when doing that change frontend too)
EffectPayloads = VotingContext | None

class SessionEffect(BaseModel):
    type: enums.SessionEffectType
    data: EffectPayloads = None


class DispatchOutcome(BaseModel):
    state: SessionLiveState
    effect: SessionEffect | None = None
