from typing import Annotated, Literal

from pydantic import BaseModel, Field

import app.session.enums as enums

# --- General Schemas ---


class SessionCreationSchema(BaseModel):
    """Schema to create a session. Follows a DB schema + extra configs format"""

    committee_id: int
    name: str | None = None


class MotionPayload(BaseModel):
    """General motion payload. Used on Delegate and Chair payloads"""

    type: enums.Motions
    debate_type: enums.DebateTypes | None = None
    total_duration_minutes: int | None = None
    per_speaker_seconds: int | None = None
    target_topic: str | None = None
    details: str | None = None


# --- Delegate Payloads ---
class DelegateMotionPayload(MotionPayload):
    pass


class DelegateQuestionPayload(BaseModel):
    type: enums.Questions
    details: str | None = None


class DelegateVotingPayload(BaseModel):
    vote: enums.VotingChoice


# TODO: have a separate AbsentMyselfEvent for this thing here
class AnswerRollCallPayload(BaseModel):
    choice: Literal[
        enums.RollCallChoice.PRESENT, enums.RollCallChoice.PRESENT_AND_VOTING
    ]


# --- Delegate Events ---
class SubmitMotionEvent(BaseModel):
    type: Literal[enums.DelegateEvents.SUBMIT_MOTION]
    payload: DelegateMotionPayload


class SubmitQuestionEvent(BaseModel):
    type: Literal[enums.DelegateEvents.SUBMIT_QUESTION]
    payload: DelegateQuestionPayload


class CastVoteEvent(BaseModel):
    type: Literal[enums.DelegateEvents.CAST_VOTE]
    payload: DelegateVotingPayload


class JoinQueueEvent(BaseModel):
    type: Literal[enums.DelegateEvents.JOIN_QUEUE]
    payload: dict = {}


class LeaveQueueEvent(BaseModel):
    type: Literal[enums.DelegateEvents.LEAVE_QUEUE]
    payload: dict = {}


class AnswerRollCallEvent(BaseModel):
    type: Literal[enums.DelegateEvents.ANSWER_ROLLCALL]
    payload: AnswerRollCallPayload


# --- Chair Payloads ---
class ChairMotionPayload(MotionPayload):
    """Extended payload for motions. Used to log motions"""

    representation_id: int
    decision: enums.MotionDecision


class ChairIncreaseTimerPayload(BaseModel):
    seconds: int = 5


class ChairToggleTimerPayload(BaseModel):
    toggle: bool = True


class ChairOpenInformalVotingPayload(BaseModel):
    # For informal Votings
    title: str | None = None
    majority: enums.MajorityTypes
    veto_power: bool


class ChairResolveMotionPayload(BaseModel):
    motion_id: int  # or motion_id if possible
    action: bool


class ChairForceSpeakerPayload(BaseModel):
    speaker_id: int | None = None  # if none, will pass onto next speaker
    seconds: int | None = None  # if none, will be based on the current seconds


class ChairSetAgendaPayload(BaseModel):
    agenda: list[str]


class ChairSetPhasePayload(BaseModel):
    target_phase: enums.States


class ChairInsertQueuePayload(BaseModel):
    target: int  # Delegate Id


class SetAgendaItemPayload(BaseModel):
    index: str
    topic: str


class MarkAgendaItemPayload(BaseModel):
    index: str  # Agenda Item Id
    indiscussion: bool | None = None
    discussed: bool | None = None


class DeleteAgendaItemPayload(BaseModel):
    index: str  # Agenda Item Id


class EmptyPayload(BaseModel): ...


class MarkRollCallPayload(BaseModel):
    delegation_id: int
    choice: enums.RollCallChoice


class MarkRollCallBulkPayload(BaseModel):
    Rollcalls: dict[int, enums.RollCallChoice]


# --- Chair Events ---
class LogMotionEvent(BaseModel):
    type: Literal[enums.ChairEvents.LOG_MOTION]
    payload: ChairMotionPayload


class OpenSessionEvent(BaseModel):
    type: Literal[enums.ChairEvents.OPEN_SESSION]
    payload: EmptyPayload


class CloseSessionEvent(BaseModel):
    type: Literal[enums.ChairEvents.CLOSE_SESSION]
    payload: EmptyPayload


class IncreaseTimerEvent(BaseModel):
    type: Literal[enums.ChairEvents.INCREASE_TIMER]
    payload: ChairIncreaseTimerPayload


class ToggleTimerEvent(BaseModel):
    type: Literal[enums.ChairEvents.TOGGLE_TIMER]
    payload: ChairToggleTimerPayload


class OpenInformalVotingEvent(BaseModel):
    type: Literal[enums.ChairEvents.OPEN_INFORMAL_VOTING]
    payload: ChairOpenInformalVotingPayload


class ResolveMotionEvent(BaseModel):
    type: Literal[enums.ChairEvents.RESOLVE_MOTION]
    payload: ChairResolveMotionPayload


class SpeakerEvent(BaseModel):
    type: Literal[enums.ChairEvents.CHOOSE_SPEAKER]
    payload: ChairForceSpeakerPayload


class SetAgendaEvent(BaseModel):
    type: Literal[enums.ChairEvents.SET_AGENDA]
    payload: ChairSetAgendaPayload


class SetPhaseEvent(BaseModel):
    type: Literal[enums.ChairEvents.MANUAL_PHASE_SET]
    payload: ChairSetPhasePayload


class CloseInformalVotingEvent(BaseModel):
    type: Literal[enums.ChairEvents.CLOSE_INFORMAL_VOTING]
    payload: EmptyPayload


class CloseProceduralVotingEvent(BaseModel):
    type: Literal[enums.ChairEvents.CLOSE_PROCEDURAL_VOTING]
    payload: EmptyPayload


class FinishCaucusEvent(BaseModel):
    type: Literal[enums.ChairEvents.FINISH_CAUCUS]
    payload: EmptyPayload


class MarkRollCallEvent(BaseModel):
    type: Literal[enums.ChairEvents.MARK_ROLLCALL]
    payload: MarkRollCallPayload


class MarkRollCallBulkEvent(BaseModel):
    type: Literal[enums.ChairEvents.MARK_ROLLCALL_BULK]
    payload: MarkRollCallBulkPayload


class CloseRollCallEvent(BaseModel):
    type: Literal[enums.ChairEvents.CLOSE_ROLLCALL]
    payload: EmptyPayload


class ChairInsertQueueEvent(BaseModel):
    type: Literal[enums.ChairEvents.INSERT_QUEUE]
    payload: ChairInsertQueuePayload


class MarkAgendaItemEvent(BaseModel):
    type: Literal[enums.ChairEvents.MARK_AGENDA_ITEM]
    payload: MarkAgendaItemPayload


class SetAgendaItemEvent(BaseModel):
    type: Literal[enums.ChairEvents.SET_AGENDA_ITEM]
    payload: SetAgendaItemPayload


class DeleteAgendaItemEvent(BaseModel):
    type: Literal[enums.ChairEvents.DELETE_AGENDA_ITEM]
    payload: DeleteAgendaItemPayload


# --- Discriminated Union ---
SessionEvent = Annotated[
    SubmitMotionEvent
    | SubmitQuestionEvent
    | CastVoteEvent
    | AnswerRollCallEvent
    | JoinQueueEvent
    | LeaveQueueEvent
    | LogMotionEvent
    | OpenSessionEvent
    | CloseSessionEvent
    | IncreaseTimerEvent
    | ToggleTimerEvent
    | OpenInformalVotingEvent
    | CloseProceduralVotingEvent
    | CloseInformalVotingEvent
    | FinishCaucusEvent
    | ResolveMotionEvent
    | SpeakerEvent
    | SetAgendaEvent
    | SetAgendaItemEvent
    | MarkAgendaItemEvent
    | DeleteAgendaItemEvent
    | SetPhaseEvent
    | MarkRollCallEvent
    | CloseRollCallEvent
    | ChairInsertQueueEvent
    | MarkRollCallBulkEvent,
    Field(discriminator="type"),
]
