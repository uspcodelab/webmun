from enum import Enum


# --- States ---
class States(str, Enum):
    # Normal flow of states
    SETUP = "Setup Room"

    ROLL_CALL = "Roll Call"
    INITIAL_DEBATE = (
        "Initial Debate"  # currently unused, gsl speaking time is set by the chair
    )
    OPEN_GSL = "Open GSL"
    CLOSED_GSL = "Closed GSL"
    VOTING_PREPARATION = "Voting Preparation"
    VOTING_PROCEDURES = "Voting Procedures"  # Voting on resolutions
    FINISHED = "Finished"

    # States based on motions, resolutions, etc
    MODERATED_CAUCUS = "Moderated Caucus"
    UNMODERATED_CAUCUS = "Unmoderated Caucus"
    VOTING_EXECUTION = "Voting Execution"  # this handles either "motion to moderated caucus" or "motion to voting procedures", for example
    BETWEEN_DEBATES = "Between Debates"


# --- Events ---
class DelegateEvents(str, Enum):
    SUBMIT_MOTION = "SubmitMotionEvent"
    SUBMIT_QUESTION = "SubmitQuestionEvent"
    JOIN_QUEUE = "JoinQueueEvent"
    LEAVE_QUEUE = "LeaveQueueEvent"
    CAST_VOTE = "CastVoteEvent"
    CHOOSE_DELEGATION = "ChooseDelegateEvent"
    YIELD_SPEAKING = "YieldEvent"
    ANSWER_ROLLCALL = "AnswerRollCallEvent"


class ChairEvents(str, Enum):
    OPEN_SESSION = "OpenSessionEvent"
    TOGGLE_TIMER = "ToggleTimerEvent"
    INCREASE_TIMER = "IncreaseTimerEvent"
    OPEN_INFORMAL_VOTING = "OpenInformalVotingEvent"
    RESOLVE_MOTION = "ResolveMotionEvent"
    CLOSE_PROCEDURAL_VOTING = "CloseProceduralVotingEvent"
    CLOSE_INFORMAL_VOTING = "CloseInformalVotingEvent"

    # Disruptive events (i.e manual override events)
    SET_AGENDA = "SetAgendaEvent"
    MANUAL_PHASE_SET = "SetPhaseEvent"
    CLOSE_SESSION = "CloseSessionEvent"

    # Manual actions
    CHOOSE_SPEAKER = "SpeakerEvent"
    MARK_ROLLCALL = "MarkRollCallEvent"
    MARK_ROLLCALL_BULK = "Mark Roll Call Bulk Event"
    CLOSE_ROLLCALL = "CloseRollCallEvent"
    INSERT_QUEUE = "InsertQueueEvent"


# --- Additional Info ---
class DebateTypes(str, Enum):
    SPEAKERS_LIST = "Speakers List"
    MODERATED_DEBATE = "Moderated Debate"  # During this type, the queue to speak should not be automatic
    UNMODERATED_DEBATE = "Unmoderated Debate"


class Motions(str, Enum):
    CHANGE_DEBATE_TYPE = "Mudar Tipo de Debate"
    POSTPONE_SESSION = "Adiaamento de Sessão"
    REOPEN_SESSION = "Reabrir Sessão"
    TOUR_DE_TABLE = "Tour de Table"
    END_DEBATE = "Encerramento de Debate"  # TODO: map this out since "motion to close debate" means clear GSL and go to voting procedures in modeldiplomat and can also mean the same as "motion to move into voting procedures"
    VOTE_AMENDMENT = "Votação de Emenda"  # TODO: check the way this is used, since amendments MUST be voted if they're present during VOTING_PROCEDURES
    VOTE_BY_ROLL_CALL = "Votação por Chamada"  # TODO: check the way this is used
    CLOSE_SPEAKERS_LIST = "Fechamento da Lista de Discursos"
    REOPEN_SPEAKERS_LIST = "Reabrir a Lista de Discursos"
    SPLIT_PROPOSAL = "Divisão de Proposta"
    INTRODUCE_RESOLUTION_PROPOSAL = "Introdução de Proposta de Resolução"
    INTRODUCE_AMENDMENT_PROPOSAL = "Introdução de Proposta de Emenda"
    CHANGE_TOPIC = "Mudança de Tópico"
    QUORUM = "Quórum"
    CUSTOM_MOTION = ""  # not implemented


class Questions(str, Enum):
    ORDER = "Order"
    QUESTION = "Question"
    PERSONAL_PRIVILEGE = "Personal Privilege"


class RollCallChoice(str, Enum):
    PRESENT = "Present"
    PRESENT_AND_VOTING = "Present and Voting"
    ABSENT = "Absent"

class SessionRole(str, Enum):
    CHAIR = "CHAIR"
    DELEGATE = "DELEGATE"
    # further roles are put here
