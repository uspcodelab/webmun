from enum import StrEnum


# --- States ---
class States(StrEnum):
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
class DelegateEvents(StrEnum):
    SUBMIT_MOTION = "SubmitMotionEvent"
    SUBMIT_QUESTION = "SubmitQuestionEvent"
    JOIN_QUEUE = "JoinQueueEvent"
    LEAVE_QUEUE = "LeaveQueueEvent"
    CAST_VOTE = "CastVoteEvent"
    YIELD_SPEAKING = "YieldEvent"
    ANSWER_ROLLCALL = "AnswerRollCallEvent"


class ChairEvents(StrEnum):
    OPEN_SESSION = "OpenSessionEvent"
    TOGGLE_TIMER = "ToggleTimerEvent"
    INCREASE_TIMER = "IncreaseTimerEvent"
    OPEN_INFORMAL_VOTING = "OpenInformalVotingEvent"
    RESOLVE_MOTION = "ResolveMotionEvent"
    CLOSE_PROCEDURAL_VOTING = "CloseProceduralVotingEvent"
    CLOSE_INFORMAL_VOTING = "CloseInformalVotingEvent"

    # Disruptive events (i.e manual override events)
    MANUAL_PHASE_SET = "SetPhaseEvent"
    CLOSE_SESSION = "CloseSessionEvent"

    # Manual actions
    SET_AGENDA_ITEM = "SetAgendaItemEvent"
    MARK_AGENDA_ITEM = "MarkAgendaItemEvent"
    DELETE_AGENDA_ITEM = "DeleteAgendaItemEvent"
    SET_AGENDA = "SetAgenda"
    CHOOSE_SPEAKER = "SpeakerEvent"
    MARK_ROLLCALL = "MarkRollCallEvent"
    MARK_ROLLCALL_BULK = "MarkRollCallBulkEvent"
    CLOSE_ROLLCALL = "CloseRollCallEvent"
    INSERT_QUEUE = "InsertQueueEvent"


# --- Additional Info ---
class DebateTypes(StrEnum):
    SPEAKERS_LIST = "Lista de Discursos"
    MODERATED_DEBATE = "Debate Moderado"  # During this type, the queue to speak should not be automatic
    UNMODERATED_DEBATE = "Debate não Moderado"


class Motions(StrEnum):
    CHANGE_DEBATE_TYPE = "Mudar Tipo de Debate"
    POSTPONE_SESSION = "Adiamento de Sessão"
    REOPEN_SESSION = "Reabertura de Sessão"
    TOUR_DE_TABLE = "Tour de Table"
    END_DEBATE = "Encerramento de Debate"  # TODO: map this out since "motion to close debate" means clear GSL and go to voting procedures in modeldiplomat and can also mean the same as "motion to move into voting procedures"
    VOTE_AMENDMENT = "Votação de Emenda"  # TODO: check the way this is used, since amendments MUST be voted if they're present during VOTING_PROCEDURES
    VOTE_BY_ROLL_CALL = "Votação por Chamada"  # TODO: check the way this is used
    CLOSE_SPEAKERS_LIST = "Fechamento da Lista de Discursos"
    REOPEN_SPEAKERS_LIST = "Reabertura de Lista de Discursos"
    SPLIT_PROPOSAL = "Divisão da Proposta"
    INTRODUCE_RESOLUTION_PROPOSAL = "Introdução da Proposta de Resolução"
    INTRODUCE_AMENDMENT_PROPOSAL = "Introdução da Proposta de Emenda"
    CHANGE_TOPIC = "Mudança de Tópico"
    QUORUM = "Contagem de Quórum"
    CUSTOM_MOTION = ""  # not implemented


class Questions(StrEnum):
    ORDER = "Ordem"
    QUESTION = "Questão"
    PERSONAL_PRIVILEGE = "Privilégio Pessoal"


class RollCallChoice(StrEnum):
    PRESENT = "Present"
    PRESENT_AND_VOTING = "Present and Voting"
    ABSENT = "Absent"


class MajorityTypes(StrEnum):
    SIMPLE = "Maioria Simples"
    QUALIFIED = "Maioria Qualificada"
    ABSOLUTE = "Consenso"


class SessionRole(StrEnum):
    CHAIR = "CHAIR"
    DELEGATE = "DELEGATE"
    # further roles are put here


class VotingChoice(StrEnum):
    FAVOUR = "Favour"
    AGAINST = "Against"
    ABSTAIN = "Abstain"


class VotingType(StrEnum):
    INFORMAL = "Informal"
    PROCEDURAL = "Procedural"
    SUBSTANTIVE = "Substantive"
