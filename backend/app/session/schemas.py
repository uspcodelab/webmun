from typing import Annotated, Literal

from pydantic import BaseModel, Field

import app.session.enums as enums

# --- General Schemas ---


# should be used to create list of delegations.
class DelegationSchema(BaseModel):
    name: str
    seat: str  # TODO: check if its better to use an int here on the frontend
    code: str  # TODO: check if this is needed


class SessionCreationSchema(BaseModel):
    session_id: int
    name: str | None = None
    delegations: list[DelegationSchema]  # useful for now


# --- Delegate Payloads ---
# TODO: refactor this to only reflect the payload received by delegates, with MotionModel being a separated entity
class DelegateMotionPayload(BaseModel):
    type: enums.Motions
    delegate: int
    debate_type: enums.DebateTypes | None = None

    total_duration_minutes: int | None = None
    per_speaker_seconds: int | None = None
    target_topic: str | None = None

    details: str | None = None


class DelegateQuestionPayload(BaseModel):
    type: enums.Questions
    delegate: int
    details: str | None = None


class DelegateVotingPayload(BaseModel):
    # other types of voting must be put in here
    type: Literal[
        "FORMAL",
        "INFORMAL",
    ]  # perhaps not needed
    motion_id: int | None = (
        None  # perhaps not needed, unless we pass the voting context to UI to validate?
    )
    title: str | None = None  # perhaps not needed
    vote: Literal["FAVOUR", "AGAINST", "ABSTAIN"]


# TODO: should be better implemented
class ChooseDelegatePayload(BaseModel):
    choice: str


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


# TODO: should be better implemented
class ChooseDelegateEvent(BaseModel):
    type: Literal[enums.DelegateEvents.CHOOSE_DELEGATION]
    payload: ChooseDelegatePayload


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
class ChairIncreaseTimerPayload(BaseModel):
    seconds: int = 5


class ChairToggleTimerPayload(BaseModel):
    toggle: bool = True


class ChairOpenInformalVotingPayload(BaseModel):
    # For informal Votings
    title: str | None = None
    majority: Literal["SIMPLE", "QUALIFIED", "ABSOLUTE"]
    veto_power: bool


class ChairResolveMotionPayload(BaseModel):
    motion_id: int  # or motion_id if possible
    action: Literal["ACCEPT", "DENY"]


class ChairForceSpeakerPayload(BaseModel):
    speaker_id: int | None = None  # if none, will pass onto next speaker
    seconds: int | None = None  # if none, will be based on the current seconds


class ChairSetAgendaPayload(BaseModel):
    agenda: list[str]


class ChairSetPhasePayload(BaseModel):
    target_phase: enums.States


class ChairInsertQueuePayload(BaseModel):
    target: int  # Delegate Id


# These two normally don't need to have an id
class ChairCloseInformalVotingPayload(BaseModel):
    voting_id: int | None = None


class EmptyPayload(BaseModel): ...


class MarkRollCallPayload(BaseModel):
    delegation_id: int
    choice: enums.RollCallChoice


class MarkRollCallBulkPayload(BaseModel):
    Rollcalls: dict[int, enums.RollCallChoice]


# --- Chair Events ---
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
    payload: ChairCloseInformalVotingPayload


class CloseProceduralVotingEvent(BaseModel):
    type: Literal[enums.ChairEvents.CLOSE_PROCEDURAL_VOTING]
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


# --- Discriminated Union ---
SessionEvent = Annotated[
    SubmitMotionEvent
    | SubmitQuestionEvent
    | CastVoteEvent
    | ChooseDelegateEvent
    | AnswerRollCallEvent
    | JoinQueueEvent
    | LeaveQueueEvent
    | OpenSessionEvent
    | CloseSessionEvent
    | IncreaseTimerEvent
    | ToggleTimerEvent
    | OpenInformalVotingEvent
    | CloseProceduralVotingEvent
    | CloseInformalVotingEvent
    | ResolveMotionEvent
    | SpeakerEvent
    | SetAgendaEvent
    | SetPhaseEvent
    | MarkRollCallEvent
    | CloseRollCallEvent
    | ChairInsertQueueEvent
    | MarkRollCallBulkEvent,
    Field(discriminator="type"),
]
