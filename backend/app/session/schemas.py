from pydantic import BaseModel, Field
from typing import Literal, Annotated
from enum import Enum

#TODO: Separate models and schemas more cleanly, this is only here to stop circular imports
#TEMPORARY SOLUTION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class DelegationContext(BaseModel):
    id: int
    seat: str
    name: str
    code: str

# Schema to be sent to create Session
class SessionCreationSchema(BaseModel):
    session_id: int
    name: str | None = None
    delegations: list[DelegationContext] # useful for now

# {"type"= States.OPEN_SESSION, "payload"= session.model_dump(mode='json')}
# We'll separate into two: Events indicate actions to be taken, whereas States/Phases indicate the current phase

class States(str, Enum):
    # Normal flow of states
    SETUP = 'Setup Room'

    ROLL_CALL = 'Roll Call'
    INITIAL_DEBATE = 'Initial Debate' # currently unused, gsl speaking time is set by the chair
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

class RollCallChoice(str, Enum):
    PRESENT = 'Present'
    PRESENT_AND_VOTING = 'Present and Voting'
    ABSENT = 'Absent'

# ----------------------------- EVENTS
# Events like this will also enable "Discriminated Unions" in Typescript
class DelegateEvents(str, Enum):
    SUBMIT_MOTION = 'SubmitMotionEvent'
    SUBMIT_QUESTION = 'SubmitQuestionEvent'
    JOIN_QUEUE = 'JoinQueueEvent' 
    LEAVE_QUEUE = 'LeaveQueueEvent' 
    CAST_VOTE = 'CastVoteEvent'
    CHOOSE_DELEGATION = 'ChooseDelegateEvent'
    YIELD_SPEAKING = 'YieldEvent'
    ANSWER_ROLLCALL = 'AnswerRollCallEvent'

class DebateTypes(str, Enum):
    SPEAKERS_LIST = 'Speakers List'
    MODERATED_DEBATE = 'Moderated Debate' # During this type, the queue to speak should not be automatic
    UNMODERATED_DEBATE = 'Unmoderated Debate'

class Motions(str, Enum):
    CHANGE_DEBATE_TYPE = 'Mudar Tipo de Debate'
    POSTPONE_SESSION = 'Adiaamento de Sessão'
    REOPEN_SESSION = 'Reabrir Sessão'
    TOUR_DE_TABLE = 'Tour de Table'
    END_DEBATE  = 'Encerramento de Debate' # TODO: map this out since "motion to close debate" means clear GSL and go to voting procedures in modeldiplomat and can also mean the same as "motion to move into voting procedures"
    VOTE_AMENDMENT = 'Votação de Emenda' # TODO: check the way this is used, since amendments MUST be voted if they're present during VOTING_PROCEDURES
    VOTE_BY_ROLL_CALL = 'Votação por Chamada' # TODO: check the way this is used
    CLOSE_SPEAKERS_LIST  = 'Fechamento da Lista de Discursos' 
    REOPEN_SPEAKERS_LIST = 'Reabrir a Lista de Discursos'
    SPLIT_PROPOSAL = 'Divisão de Proposta'
    INTRODUCE_RESOLUTION_PROPOSAL = 'Introdução de Proposta de Resolução'
    INTRODUCE_AMENDMENT_PROPOSAL = 'Introdução de Proposta de Emenda'
    CHANGE_TOPIC = 'Mudança de Tópico'
    QUORUM = 'Quórum'
    CUSTOM_MOTION = '' #not implemented

# TODO: refactor this to only reflect the payload received by delegates, with MotionModel being a separated entity
class DelegateMotionPayload(BaseModel):
    id: int | None = None # When Delegate Sends it, it's None
    priority: int = 0 # TODO: priority must be set on the backend unless Chair sends with custom priority? also check if chair motions automatically pass
    type: Motions
    delegate: DelegationContext
    debate_type: DebateTypes | None = None

    total_duration_minutes: int | None = None
    per_speaker_seconds: int | None = None
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
    delegate: DelegationContext
    details: str

class DelegateVotingPayload(BaseModel):
    # other types of voting must be put in here
    type: Literal['FORMAL', 'INFORMAL',] #perhaps not needed
    motion_id: int | None = None # perhaps not needed, unless we pass the voting context to UI to validate?
    title: str | None = None # perhaps not needed
    vote: Literal["FAVOUR", "AGAINST", "ABSTAIN"]

# TODO: should be removed
class ChooseDelegatePayload(BaseModel):
    choice: str

# TODO: have a separate AbsentMyselfEvent for this thing here
class AnswerRollCallPayload(BaseModel):
    choice: Literal[RollCallChoice.PRESENT, RollCallChoice.PRESENT_AND_VOTING]

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

# TODO: should be removed
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

class AnswerRollCallEvent(BaseModel):
    type: Literal[DelegateEvents.ANSWER_ROLLCALL]
    payload: AnswerRollCallPayload

# -----------------------------------------------------------------------

class ChairEvents(str, Enum):
    OPEN_SESSION = 'OpenSessionEvent'
    TOGGLE_TIMER = 'ToggleTimerEvent'
    INCREASE_TIMER = 'IncreaseTimerEvent'
    OPEN_INFORMAL_VOTING = 'OpenInformalVotingEvent'
    RESOLVE_MOTION = 'ResolveMotionEvent'
    CLOSE_PROCEDURAL_VOTING = 'CloseProceduralVotingEvent'
    CLOSE_INFORMAL_VOTING = 'CloseInformalVotingEvent'

    # Disruptive events (i.e manual override events)
    SET_AGENDA = 'SetAgendaEvent'
    MANUAL_PHASE_SET = 'SetPhaseEvent'
    CLOSE_SESSION = 'CloseSessionEvent'

    # Manual actions 
    CHOOSE_SPEAKER = 'SpeakerEvent'
    MARK_ROLLCALL = 'MarkRollCallEvent'
    MARK_ROLLCALL_BULK = 'Mark Roll Call Bulk Event'
    CLOSE_ROLLCALL = 'CloseRollCallEvent'
    INSERT_QUEUE = 'InsertQueueEvent'
    
class ChairIncreaseTimerPayload(BaseModel):
    seconds: int = 5

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
    speaker_id: int | None = None # if none, will pass onto next speaker
    seconds: int | None = None # if none, will be based on the current seconds

class ChairSetAgendaPayload(BaseModel):
    agenda: list[str]

class ChairSetPhasePayload(BaseModel):
    target_phase: States

class ChairInsertQueuePayload(BaseModel):
    target: int #Delegate Id 

# These two normally don't need to have an id 
class ChairCloseInformalVotingPayload(BaseModel):
    voting_id: int | None = None

class EmptyPayload(BaseModel):
    ...

class MarkRollCallPayload(BaseModel):
    delegation_id: int
    choice: RollCallChoice

class MarkRollCallBulkPayload(BaseModel):
    Rollcalls: dict[int, RollCallChoice]

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
    payload: EmptyPayload

class MarkRollCallEvent(BaseModel):
    type: Literal[ChairEvents.MARK_ROLLCALL]
    payload: MarkRollCallPayload

class MarkRollCallBulkEvent(BaseModel):
    type: Literal[ChairEvents.MARK_ROLLCALL_BULK]
    payload: MarkRollCallBulkPayload

class CloseRollCallEvent(BaseModel):
    type: Literal[ChairEvents.CLOSE_ROLLCALL]
    payload: EmptyPayload

class ChairInsertQueueEvent(BaseModel):
    type: Literal[ChairEvents.INSERT_QUEUE]
    payload: ChairInsertQueuePayload
# -----------------------------------------------------------------------
# Event envelope model / Discriminated Union

SessionEvent = Annotated[ 
    SubmitMotionEvent | SubmitQuestionEvent | CastVoteEvent | ChooseDelegateEvent | AnswerRollCallEvent
    | JoinQueueEvent | LeaveQueueEvent | OpenSessionEvent | CloseSessionEvent | IncreaseTimerEvent | ToggleTimerEvent | OpenInformalVotingEvent
    | CloseProceduralVotingEvent | CloseInformalVotingEvent | ResolveMotionEvent | SpeakerEvent 
    | SetAgendaEvent | SetPhaseEvent | MarkRollCallEvent | CloseRollCallEvent | ChairInsertQueueEvent | MarkRollCallBulkEvent,
    Field(discriminator="type")]

