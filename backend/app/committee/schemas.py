from pydantic import BaseModel, Field
from typing import Literal, Annotated
from datetime import datetime 
from enum import Enum

# Schema to be sent to create Session
class SessionCreationSchema(BaseModel):
    committee_id: int
    name: str

# Schema to be sent to update newcomers (or perhaps send entire SessionLiveState?)
class SessionStateSchema(BaseModel):
    committee_id: int 
    name: str
    current_speaker: int | None 
    timer_end: datetime | None 

SessionCreationSchema.model_rebuild()

# The idea here is to send States to the clients using the States Enum, plus
# their corresponding Schema, for exemple to open a session you would send
# {"type"= States.OPEN_SESSION, "payload"= session.model_dump(mode='json')}
# with session being a SessionSchema.
# R: Enum idea seems good. But further research indicates a mix of States + Events is a better option

# We'll separate into two: Events indicate actions to be taken, whereas States/Phases indicate the current
# Phase of the Session (Debate (Moderated/Unmoderated), General Speakers List, More if needed)
#
class States(str, Enum):
    # Normal flow of states
    SETUP = 'Setup Room'

    ROLL_CALL = 'Roll Call'
    INITIAL_DEBATE = 'Initial Debate' # or INITIAL_GSL
    OPEN_GSL = 'Open GSL'
    CLOSED_GSL = 'Closed GSL'
    VOTING_PROCEDURES = 'Voting Procedures' # Voting on resolutions
    FINISHED = 'Finished'

    # States based on motions, resolutions, etc
    MODERATED_CAUCUS = 'Moderated Caucus'
    UNMODERATED_CAUCUS = 'Unmoderated Caucus'
    VOTING_EXECUTION = 'Voting Execution' # this handles either "motion to moderated caucus" or "motion to voting procedures", for example
    PRE_VOTING = 'Pre-voting' # Special case when someone wants to close debate/move into voting procedures

# ----------------------------- EVENTS
# Events like this will also enable "Discriminated Unions" in Typescript
class DelegateEvents(str, Enum):
    SUBMIT_MOTION = 'Submit Motion'
    SUBMIT_QUESTION = 'Submit Question'
    JOIN_QUEUE = 'Join Speakers Queue'
    LEAVE_QUEUE = 'Leave Speakers Queue'
    CAST_VOTE = 'Cast Substantive Vote'
    CHOOSE_DELEGATION = 'Choose Delegation'
    YIELD_SPEAKING = 'Yield Speaking'

class DebateTypes(str, Enum):
    SPEAKERS_LIST = 'Speakers List'
    MODERATED_DEBATE = 'Moderated Debate' # During this type, the queue to speak should not be automatic
    UNMODERATED_DEBATE = 'Unmoderated Debate'

class Motions(str, Enum):
    CHANGE_DEBATE_TYPE = 'Change Debate Type'
    POSTPONE_SESSION = 'Postpone Session'
    REOPEN_SESSION = 'Reopen Session'
    TOUR_DE_TABLE = 'Tour de Table'
    END_DEBATE  = 'End Debate'
    VOTE_AMENDMENT = 'Vote Amendment'
    VOTE_BY_ROLL_CALL = 'Vote by Roll Call'
    CLOSE_SPEAKERS_LIST  = 'Close Speakers list'
    REOPEN_SPEAKERS_LIST = 'Reopen Speakers list'
    SPLIT_PROPOSAL = 'Split Proposal'
    INTRODUCE_RESOLUTION_PROPOSAL = 'Introduce Resolution Proposal'
    INTRODUCE_AMENDMENT_PROPOSAL = 'Introduce Amendment Proposal'
    CHANGE_TOPIC = 'Change Topic'
    QUORUM = 'Quorum'
    CUSTOM_MOTION = ''

class DelegateMotionPayload(BaseModel):
    id: int | None = None # When Delegate Sends it, it's None
    priority: int = 0
    type: Motions
    delegate: int | None = None

    total_duration_minutes: int | None = None
    total_speaking_seconds: int | None = None
    target_topic: str | None = None

    details: str | None = None

class Questions(str, Enum):
    ORDER = 'Order'
    QUESTION = 'Question'
    PERSONAL_PRIVILEGE = 'Personal Privilege'

class DelegateQuestionPayload(BaseModel):
    id: int | None = None
    priority: int = 0
    type: Questions
    delegate: int | None = None
    details: str

class DelegateVotingPayload(BaseModel):
    motion_id: int
    vote: Literal["FAVOUR", "AGAINST", "ABSTAIN"]

# Specific class to choose a country when first entering session
class ChooseDelegatePayload(BaseModel):
    choice: str

# Yields speaking time to Chair, to a country, or to questions (open for everyone)
class DelegateYieldPayload(BaseModel):
    choice: str | Literal['CHAIR'] = 'CHAIR'

# -------
# Respective "type" + "payload" compositions that enable deep documentation
class SubmitMotionEvent(BaseModel):
    type: Literal[DelegateEvents.SUBMIT_MOTION]
    payload: DelegateMotionPayload

class SubmitQuestionEvent(BaseModel):
    type: Literal[DelegateEvents.SUBMIT_QUESTION]
    payload: DelegateQuestionPayload

class CastVoteEvent(BaseModel):
    type: Literal[DelegateEvents.CAST_VOTE]
    payload: DelegateVotingPayload

class ChooseDelegateEvent(BaseModel):
    type: Literal[DelegateEvents.CHOOSE_DELEGATION]
    payload: ChooseDelegatePayload

class SetQueueEvent(BaseModel):
    # no need to track what delegate it is since it should already be captured by websocket
    type: Literal[DelegateEvents.JOIN_QUEUE, DelegateEvents.LEAVE_QUEUE]
    payload: dict = {}

class YieldEvent(BaseModel):
    type: Literal[DelegateEvents.YIELD_SPEAKING]
    payload: DelegateYieldPayload

# -----------------------------------------------------------------------

class ChairEvents(str, Enum):
    OPEN_SESSION = 'Open Session' # Defines Session to be opened
    TOGGLE_TIMER = 'Toggle Timer'
    INCREASE_TIMER = 'Increase Timer'
    SET_VOTING_STATE = 'Set Voting State'
    RESOLVE_MOTION = 'Resolve Motion'

    # Disruptive events (i.e manual override events)
    FORCE_SPEAKER = 'Force Speaker'
    SET_AGENDA = 'Set Agenda'
    MANUAL_PHASE_SET = 'Manual Phase Set'
    CLOSE_SESSION = 'Close Session'

# either close or open session
class ChairSetSessionPayload(BaseModel):
    open_session: bool = True

class ChairToggleTimerPayload(BaseModel):
    toggle: bool = True # toggle is 1, that is, execute toggle

class ChairIncreaseTimerPayload(BaseModel):
    duration_seconds: int = 5

class ChairSetVotingPayload(BaseModel):
    title: str | None = None
    majority: Literal['SIMPLE', 'QUALIFIED', 'ABSOLUTE']
    veto_power: bool

class ChairResolveMotionPayload(BaseModel):
    motion_id: int # or motion_id if possible
    action: Literal['ACCEPT', "DENY"]

class ChairForceSpeakerPayload(BaseModel):
    speaker: str | None = None # if none, will pass onto next speaker
    seconds: int | None = None # if none, will be based on the current seconds

class ChairSetAgendaPayload(BaseModel):
    agenda: list[str]

class ChairSetPhasePayload(BaseModel):
    target_phase: States

class EmptyPayload():
    ...

# Related Events
class SetSessionEvent(BaseModel):
    type: Literal[ChairEvents.OPEN_SESSION, ChairEvents.CLOSE_SESSION]
    payload: EmptyPayload

class ToggleTimerEvent(BaseModel):
    type: Literal[ChairEvents.TOGGLE_TIMER]
    payload: ChairToggleTimerPayload

class IncreaseTimerEvent(BaseModel):
    type: Literal[ChairEvents.INCREASE_TIMER]
    payload: ChairIncreaseTimerPayload

class SetVotingEvent(BaseModel):
    type: Literal[ChairEvents.SET_VOTING_STATE]
    payload: ChairSetVotingPayload

class ResolveMotionEvent(BaseModel):
    type: Literal[ChairEvents.RESOLVE_MOTION]
    payload: ChairResolveMotionPayload

class SpeakerEvent(BaseModel):
    type: Literal[ChairEvents.FORCE_SPEAKER]
    payload: ChairForceSpeakerPayload

class SetAgendaEvent(BaseModel):
    type: Literal[ChairEvents.SET_AGENDA]
    payload: ChairSetAgendaPayload

class SetPhaseEvent(BaseModel):
    type: Literal[ChairEvents.MANUAL_PHASE_SET]
    payload: ChairSetPhasePayload

# -----------------------------------------------------------------------
# Event envelope model / Discriminated Union

SessionEvent = Annotated[ 
    SubmitMotionEvent | SubmitQuestionEvent | CastVoteEvent | ChooseDelegateEvent
    | SetQueueEvent | YieldEvent | SetSessionEvent | ToggleTimerEvent 
    | IncreaseTimerEvent | SetVotingEvent | ResolveMotionEvent | SpeakerEvent 
    | SetAgendaEvent | SetPhaseEvent,
    Field(discriminator="type")]


# To be cleaned -----------------------------------------------
# Metadata associated to an Event
"""
class SessionSchema(BaseModel):
    delegates: list[str]
    theme: str

class AgendaSchema(BaseModel):
    topics: list[str]


class DebateSchema(BaseModel):
    topic: str
    type: DebateTypes

class TimerSchema(BaseModel):
    start_time: int
    end_time: int

class VotingSchema(BaseModel):
    topic: str
    majority_needed: int

"""
