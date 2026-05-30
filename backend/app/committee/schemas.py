from pydantic import BaseModel
from datetime import datetime 
from enum import Enum

class CommitteeCreationSchema(BaseModel):
    committee_id: int
    name: str

class CommitteeStateSchema(BaseModel):
    committee_id: int 
    name: str
    current_speaker: int | None 
    timer_end: datetime | None 

CommitteeCreationSchema.model_rebuild()

# The idea here is to send States to the clients using the States Enum, plus
# their corresponding Schema, for exemple to open a session you would send
# {"type"= States.OPEN_SESSION, "payload"= session.model_dump(mode='json')}
# with session being a SessionSchema.
class States(str, Enum):
    OPEN_SESSION = 'Open Session'
    CREATE_AGENDA_START = 'Create Agenda Start'
    CREATE_AGENDA_END = 'Create Agenda End'
    DEBATE_START = 'Debate Start'
    DEBATE_END = 'Debate End'
    TIMER_START = 'Timer Start'
    TIMER_CHANGE = 'Timer Change'
    TIMER_END = 'Timer End'
    VOTING_START = 'Voting Start'
    VOTING_END = 'Voting End'
    MOTION_CREATED = 'Motion Created'
    QUESTION_CREATED = 'Question Created'

class SessionSchema(BaseModel):
    delegates: list[str]
    theme: str

class AgendaSchema(BaseModel):
    topics: list[str]

class DebateTypes(str, Enum):
    DISCOURSE_LIST = 'Discourse List'
    MODERATED_DEBATE = 'Moderated Debate'
    UNMODERATED_DEBATE = 'Unmoderated Debate'

class DebateSchema(BaseModel):
    topic: str
    type: DebateTypes

class TimerSchema(BaseModel):
    start_time: int
    end_time: int

class VotingSchema(BaseModel):
    topic: str
    majority_needed: int

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

class MotionSchema(BaseModel):
    id: int
    priority: int
    type: Motions
    delegate: int | None
    details: str

class Questions(str, Enum):
    ORDER = 'Order'
    QUESTION = 'Question'
    PERSONAL_PRIVILEGE = 'Personal Privilege'

class QuestionSchema(BaseModel):
    id: int
    priority: int
    type: Questions
    delegate: int | None
    details: str
