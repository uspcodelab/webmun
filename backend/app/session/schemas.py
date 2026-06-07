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
    VOTING_PREPARATION = 'Voting Preparation'
    VOTING_PROCEDURES = 'Voting Procedures' # Voting on resolutions
    FINISHED = 'Finished'

    # States based on motions, resolutions, etc
    MODERATED_CAUCUS = 'Moderated Caucus'
    UNMODERATED_CAUCUS = 'Unmoderated Caucus'
    VOTING_EXECUTION = 'Voting Execution' # this handles either "motion to moderated caucus" or "motion to voting procedures", for example
    BETWEEN_DEBATES = 'Between Debates'

# ----------------------------- EVENTS
# Events like this will also enable "Discriminated Unions" in Typescript
class DelegateEvents(str, Enum):
    SUBMIT_MOTION = 'SubmitMotionEvent'
    SUBMIT_QUESTION = 'SubmitQuestionEvent'
    JOIN_QUEUE = 'JoinQueueEvent' #doesn't work anymore
    LEAVE_QUEUE = 'LeaveQueueEvent' #doesn't work anymore
    CAST_VOTE = 'CastVoteEvent'
    CHOOSE_DELEGATION = 'ChooseDelegateEvent'
    YIELD_SPEAKING = 'YieldEvent'

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
    CUSTOM_MOTION = '' #not implemented

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
    # other types of voting must be put in here
    type: Literal['FORMAL', 'INFORMAL',]
    motion_id: int | None = None
    title: str | None = None # For informal votes, put custom string
    vote: Literal["FAVOUR", "AGAINST", "ABSTAIN"]

# Specific class to choose a country when first entering session
class ChooseDelegatePayload(BaseModel):
    choice: str

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

# We can use a ternary operator / UI state to check if it's in queue in order to check things
class JoinQueueEvent(BaseModel):
    # no need to track what delegate it is since it should already be captured by websocket
    type: Literal[DelegateEvents.JOIN_QUEUE]
    payload: dict = {}

class LeaveQueueEvent(BaseModel):
    type: Literal[DelegateEvents.LEAVE_QUEUE] 
    payload: dict = {}

# -----------------------------------------------------------------------

class ChairEvents(str, Enum):
    OPEN_SESSION = 'OpenSessionEvent' # Defines Session to be opened, doesnt work anymore
    TOGGLE_TIMER = 'ToggleTimerEvent'
    INCREASE_TIMER = 'IncreaseTimerEvent'
    OPEN_INFORMAL_VOTING = 'OpenInformalVotingEvent'
    RESOLVE_MOTION = 'ResolveMotionEvent'
    CLOSE_PROCEDURAL_VOTING = 'CloseProceduralVotingEvent'
    CLOSE_INFORMAL_VOTING = 'CloseInformalVotingEvent'

    # Disruptive events (i.e manual override events)
    SET_AGENDA = 'SetAgendaEvent'
    MANUAL_PHASE_SET = 'SetPhaseEvent'
    CLOSE_SESSION = 'CloseSessionEvent' # doesnt work anymore

    # Manual actions 
    CHOOSE_SPEAKER = 'Choose Speaker'
    
class ChairIncreaseTimerPayload(BaseModel):
    duration_seconds: int = 5

class ChairToggleTimerPayload(BaseModel):
    toggle: bool = True

class ChairOpenInformalVotingPayload(BaseModel):
    # For informal Votings
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

# These two normally don't need to have an id 
class ChairCloseInformalVotingPayload(BaseModel):
    voting_id: int | None = None

class ChairCloseProceduralVotingPayload(BaseModel):
    ... 


class EmptyPayload(BaseModel):
    ...

# Related Events
class OpenSessionEvent(BaseModel): 
    type: Literal[ChairEvents.OPEN_SESSION]
    payload: EmptyPayload

class CloseSessionEvent(BaseModel):
    type: Literal[ChairEvents.CLOSE_SESSION]
    payload: EmptyPayload

class IncreaseTimerEvent(BaseModel):
    type: Literal[ChairEvents.INCREASE_TIMER]
    payload: ChairIncreaseTimerPayload

class ToggleTimerEvent(BaseModel):
    type: Literal[ChairEvents.TOGGLE_TIMER]
    payload: ChairToggleTimerPayload

class OpenInformalVotingEvent(BaseModel):
    type: Literal[ChairEvents.OPEN_INFORMAL_VOTING]
    payload: ChairOpenInformalVotingPayload

class ResolveMotionEvent(BaseModel):
    type: Literal[ChairEvents.RESOLVE_MOTION]
    payload: ChairResolveMotionPayload

class SpeakerEvent(BaseModel):
    type: Literal[ChairEvents.CHOOSE_SPEAKER]
    payload: ChairForceSpeakerPayload

class SetAgendaEvent(BaseModel):
    type: Literal[ChairEvents.SET_AGENDA]
    payload: ChairSetAgendaPayload

class SetPhaseEvent(BaseModel):
    type: Literal[ChairEvents.MANUAL_PHASE_SET]
    payload: ChairSetPhasePayload

class CloseInformalVotingEvent(BaseModel):
    type: Literal[ChairEvents.CLOSE_INFORMAL_VOTING]
    payload: ChairCloseInformalVotingPayload

class CloseProceduralVotingEvent(BaseModel):
    type: Literal[ChairEvents.CLOSE_PROCEDURAL_VOTING]
    payload: ChairCloseProceduralVotingPayload

# -----------------------------------------------------------------------
# Event envelope model / Discriminated Union

SessionEvent = Annotated[ 
    SubmitMotionEvent | SubmitQuestionEvent | CastVoteEvent | ChooseDelegateEvent
    | JoinQueueEvent | LeaveQueueEvent | OpenSessionEvent | CloseSessionEvent | IncreaseTimerEvent | ToggleTimerEvent | OpenInformalVotingEvent
    | CloseProceduralVotingEvent | CloseInformalVotingEvent | ResolveMotionEvent | SpeakerEvent 
    | SetAgendaEvent | SetPhaseEvent,
    Field(discriminator="type")]

