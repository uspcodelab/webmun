# where engine lives
from datetime import timezone, timedelta, datetime
from typing import Callable, Any, TypeAlias

from .schemas import *
from .manager import DebateContext, RollCallContext, SessionLiveState, VotingContext

# placeholder Exception to be used in engine
class InvalidProceduralMove(Exception):
    pass

"""
This will document the flow of states the debates will have. As well as document an initial engine 

Creating a committee should assign a chair as it's admin. Only Secretariats can create a session for a committee

OPEN_SESSION / SETUP: setup state. Websockets are already made, thus possible events are 
- ChooseDelegation: made from Delegates from a list of possible ones (so a list of possible delegations should be present either in server/frontend)
- EditSetup: chair edits setup such as:
    - extends session: (extends an already made session, or unpause session?)
    - speaking_time
    - can_set_motions (during specific debates)
    - default_state (either GSL or Moderated, should be put later)
    - topics
    - may be skipped during initial testings

ChooseDelegation should not be possible anymore (at least not for now)

ROLL_CALL: roll call/ quorum count state. Possible events are:
    - SetVotingChoiceEvent: by Delegate 
    - QuestionEvent
    - Any Chair Event: since most are disruptive

To user, INITIAL_DEBATE and OPEN_GSL should look mostly the same
INITIAL_DEBATE: after roll call, if no agenda is set and/or no speaking time for GSL is set, go to this state. It's an initial speakers list. Possible events are: 
    - Motions: subset - (POSTPONE, END, QUORUM, SETSPEAKINGTIME) 
    - Special action: "Propose Topics"
    - QuestionEvent
    - Any Chair Event
    - CastInformalVoteEvent 
Queue should not be open to speak. Delegates may only speak in motions

OPEN_GSL: default state in general. Queue is open and all motions can be made. The topic is defaulted to the first one in the order of agenda_topics and index_topic.
    - In particular, YieldEvent must be enabled and configured.

Specific Debates: (Moderated, Unmoderated, Tour) Queue not enabled. Each delegation should raise their placard and popups a "selection" on map
    - Motions may only be put if set_motions is enabled.
    - In particular, Unmoderated should not have a queue/motions enabled at all, but this may be implemented later 

BETWEEN_DEBATES: After each speak (From moderated or GSL), this temporary state (for up to 15 seconds) is enabled so chair can ask for new motions and check submitted ones. It should go into OPEN_GSL or MODERATED_CAUCUS, depending on which state is there
-> may not be needed if Chair controls the timer

VOTING_EXECUTION: Voting on a procedural motion.

CLOSED_GSL: after a successfull 'Close Speakers List'. Queue is disabled.

VOTING_PREPARATION: ambiguous state after an "close debate" has either entered as a motion, or "move into voting procedures". Perhaps doesnt need to be added?

VOTING_PROCEDURES: special case of voting on resolutions, etc. Substantive votes.

FINISHED: when topics get empty automatically, or chair decides to close session. may be reverted.

This will give some insight into what should or should not be possible during each event
"""

# Dispatch tables: alternative to if else chains
MOTIONS_ALLOWED: dict[States, set[Motions]] = {
    States.INITIAL_DEBATE: { Motions.CUSTOM_MOTION, },
    States.OPEN_GSL: {
        Motions.CHANGE_DEBATE_TYPE,
        Motions.POSTPONE_SESSION,
        Motions.TOUR_DE_TABLE,
        Motions.END_DEBATE,
        Motions.VOTE_AMENDMENT,
        Motions.VOTE_BY_ROLL_CALL,
        Motions.CLOSE_SPEAKERS_LIST,
        Motions.SPLIT_PROPOSAL ,
        Motions.INTRODUCE_RESOLUTION_PROPOSAL,
        Motions.INTRODUCE_AMENDMENT_PROPOSAL,
        Motions.CHANGE_TOPIC,
        Motions.QUORUM ,
        Motions.CUSTOM_MOTION,
    },
    States.CLOSED_GSL: {
        Motions.REOPEN_SPEAKERS_LIST,
        Motions.END_DEBATE,
        Motions.VOTE_AMENDMENT,
        Motions.VOTE_BY_ROLL_CALL,
        Motions.INTRODUCE_RESOLUTION_PROPOSAL,
        Motions.INTRODUCE_AMENDMENT_PROPOSAL,
        Motions.QUORUM,
        Motions.CUSTOM_MOTION,
    },
    States.VOTING_PREPARATION: {
        Motions.VOTE_BY_ROLL_CALL, 
        Motions.SPLIT_PROPOSAL, 
        Motions.CUSTOM_MOTION
    },
    States.MODERATED_CAUCUS: {
        Motions.POSTPONE_SESSION,
        Motions.END_DEBATE,
        Motions.QUORUM,
        Motions.CUSTOM_MOTION,
    },
    States.UNMODERATED_CAUCUS: {
        Motions.POSTPONE_SESSION,
        Motions.END_DEBATE,
        Motions.QUORUM,
    },
} 

# we also need related events or automatic/internal cron job in order to change, for example, caucus to GSL
# TODO: change is_chair boolean flag from handlers to something like a Role class, with "DELEGATE", "OBSERVER", "ADMIN" and "CHAIR" types

# Validations and helpers
def generate_next_motion_id(state: SessionLiveState) -> int:
    if not hasattr(state, "_motion_id_counter"):
        state._motion_id_counter = 0
    state._motion_id_counter += 1
    return state._motion_id_counter

def generate_next_question_id(state: SessionLiveState) -> int:
    if not hasattr(state, "_question_id_counter"):
        state._question_id_counter = 0
    state._question_id_counter += 1
    return state._question_id_counter

# TODO: map more things to be needed here
def validate_motion_payload(payload: DelegateMotionPayload, state: SessionLiveState) -> None:
    """Should validate motion payload and correct it before submitting""" 
    # can correct things
    if payload.target_topic == None:
        payload.target_topic = (
            state.agenda_topics[state.active_topic_index][0] 
            if state.active_topic_index is not None and 0 <= state.active_topic_index < len(state.agenda_topics) 
            else None
        )
    
    # can also raise error if there are missing fields
    if payload.type in {States.MODERATED_CAUCUS} and payload.per_speaker_seconds == None:
        raise InvalidProceduralMove("Cannot submit motion without speaking time")

def validate_question_payload(payload: DelegateQuestionPayload, state: SessionLiveState) -> None:
    ...

def tally_votes(voting: VotingContext) -> bool:
    ...

def get_default_speaker_seconds(state: SessionLiveState) -> int | None:
    if state.current_state == States.MODERATED_CAUCUS and state.debate:
        return state.debate.per_speaker_seconds

    if state.current_state in {States.OPEN_GSL, States.CLOSED_GSL, States.INITIAL_DEBATE}:
        return state.gsl_default_time_seconds

    return None


def reset_timer(state: SessionLiveState, seconds: int = 0) -> None: 
    state.timer_is_running = False
    state.timer_expiration = None 
    state.timer_remaining_seconds = seconds

# -------------- HANDLERS --------------
def handle_submit_motion(state: SessionLiveState, event: SubmitMotionEvent, sender: str, is_chair: bool) -> SessionLiveState:
    """Handles/Maps all possible states through a motion"""
    
    # TODO: change this so Chair can also catalog motions for delegations
    if is_chair:
        raise InvalidProceduralMove("Cannot submit delegate motions as Chair")
    
    # Extract payload (as DelegateMotionSchema)
    payload = event.payload
    current_state = state.current_state

    # check if motion can be made for this state
    if payload.type not in MOTIONS_ALLOWED.get(current_state, set()):
        raise InvalidProceduralMove("Cannot submit this motion at this phase")

    if current_state in {States.MODERATED_CAUCUS, States.UNMODERATED_CAUCUS} and not state.can_set_motion:
        raise InvalidProceduralMove("Submitting motions during caucuses is disabled")
    
    validate_motion_payload(payload, state)

    payload.id = generate_next_motion_id(state)
    payload.delegate.name = sender #TODO: FIX
    state.submitted_motions.append(payload)
    
    return state

def handle_submit_question(state: SessionLiveState, event: SubmitQuestionEvent, sender: str, is_chair: bool) -> SessionLiveState:
    # TODO: change this so Chair can also catalog motions for delegations
    if is_chair:
        raise InvalidProceduralMove("Cannot submit delegate motions as Chair")
    
    payload = event.payload

    validate_question_payload(payload, state)
    payload.id = generate_next_question_id(state)
    payload.delegate.name = sender #TODO: FIX
    state.submitted_questions.append(payload)

    return state

def handle_join_queue(state: SessionLiveState, event: JoinQueueEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if is_chair:
        raise InvalidProceduralMove("Cannot submit delegate motions as Chair")
    
    if state.current_state != States.OPEN_GSL:
        raise InvalidProceduralMove("Cannot enter queue right now")

    # if already in queue, return error, else remove from queue and return state 
    if sender in state.gsl_queue:
        raise InvalidProceduralMove("Already in Queue")
    
    state.gsl_queue.append(sender)
    return state
    

def handle_leave_queue(state: SessionLiveState, event: LeaveQueueEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if is_chair:
        raise InvalidProceduralMove("Cannot submit delegate motions as Chair")

    if state.current_state != States.OPEN_GSL:
        raise InvalidProceduralMove("Cannot enter queue right now")

    if sender not in state.gsl_queue:
        raise InvalidProceduralMove("Not in Queue")

    state.gsl_queue.remove(sender)
    return state
    

def handle_cast_vote(state: SessionLiveState, event: CastVoteEvent, sender: str, is_chair: bool) -> SessionLiveState:
    # review copy structuring here
    if is_chair:
        raise InvalidProceduralMove("Cannot cast vote as Chair")
    
    voting_context = state.voting 
    if voting_context == None:
        raise InvalidProceduralMove("Cannot vote during this stage")
    
    # initial voting workflow, may be reviewed later
    # TODO: perhaps allow casting another vote if first one fails
    if sender in voting_context.voting_registry:
        raise InvalidProceduralMove("Already cast vote")
   
    # register vote on voting context
    voting_context.voting_registry[sender] = event.payload.vote

    return state

# TODO: remove this
def handle_choose_delegation(state: SessionLiveState, event: ChooseDelegateEvent, sender: str, is_chair: bool) -> SessionLiveState:
    ...

def handle_answer_roll_call(state: SessionLiveState, event: AnswerRollCallEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if state.current_state != States.ROLL_CALL or state.roll_call is None:
        raise InvalidProceduralMove("Roll call not available now")

    state.roll_call.registry[sender] = event.payload.choice 
    return state
     
# Chair events
def handle_open_session(state: SessionLiveState, event: OpenSessionEvent, sender: str, is_chair: bool) -> SessionLiveState:
    ...
    # should go into rollcall and modify RollCallContext

def handle_close_session(state: SessionLiveState, event: CloseSessionEvent, sender: str, is_chair: bool) -> SessionLiveState:
    ...

# TODO: create helpers for timers -> stop_timer, set_timer, pause_timer, etc
def handle_toggle_timer(state: SessionLiveState, event: ToggleTimerEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if not is_chair:
        raise InvalidProceduralMove("Invalid move")
    
    # uses utc for now
    now = datetime.now(timezone.utc)
    if state.timer_is_running:
        # timer currently running 
        if state.timer_expiration is not None and now > state.timer_expiration:
            # currently overtime, act as stop button

            state.timer_is_running = False 
            state.timer_remaining_seconds = 0
    
        elif state.timer_expiration is not None:
            state.timer_is_running = False 
            elapsed = state.timer_expiration - now 
            state.timer_remaining_seconds = int(elapsed.total_seconds())
            state.timer_expiration = None
    else:
        # timer currently stopped 
        state.timer_is_running = True 
        state.timer_expiration = now + timedelta(seconds=state.timer_remaining_seconds)
    
    return state

def handle_increase_timer(state: SessionLiveState, event: IncreaseTimerEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if not is_chair:
        raise InvalidProceduralMove("Invalid move")

    now = datetime.now(timezone.utc)

    if state.timer_is_running and state.timer_expiration is not None:
        state.timer_expiration += timedelta(seconds=event.payload.seconds)
        state.timer_remaining_seconds = int((state.timer_expiration - now).total_seconds())
    else:
        state.timer_remaining_seconds += event.payload.seconds 

    return state

def handle_open_informal_voting(state: SessionLiveState, event: OpenInformalVotingEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if not is_chair:
        raise InvalidProceduralMove("Invalid move")

    if state.current_state == States.VOTING_EXECUTION:
        raise InvalidProceduralMove("Can't open voting while another voting is in course")
    
    state.voting = VotingContext(
            target_type="INFORMAL",
            title=event.payload.title,
            return_state=state.current_state,
            voting_registry= {},
            majority=event.payload.majority,
            veto_power=event.payload.veto_power,
    ) 

    state.current_state = States.VOTING_EXECUTION

    return state
     

def handle_close_informal_voting(state: SessionLiveState, event: CloseInformalVotingEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if not is_chair:
        raise InvalidProceduralMove("Invalid move")

    if state.voting is None:
        raise InvalidProceduralMove("No voting present")
    
    if state.current_state != States.VOTING_EXECUTION or state.voting.target_type != "INFORMAL":
        raise InvalidProceduralMove("Can't close voting")
    
    # extract last state 
    state.current_state = state.voting.return_state

    state.voting = None

    return state


def handle_close_procedural_voting(state: SessionLiveState, event: CloseProceduralVotingEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if not is_chair:
        raise InvalidProceduralMove("Invalid move")

    if state.voting is None:
        raise InvalidProceduralMove("No voting present")

    if state.current_state != States.VOTING_EXECUTION or state.voting.target_type != "PROCEDURAL": 
        raise InvalidProceduralMove("Can't close voting")

    motion = state.voting.motion_in_vote
    
    if motion is None:
        raise InvalidProceduralMove("Can't close voting if motion is None")

    passed = tally_votes(state.voting)
    
    # TODO: pass everything here into a helper "apply_passed_motion" and "apply_change_debate"
    if passed:
        next_state = state.current_state # as fallback
        state.current_speaker = None 
        state.timer_is_running = False 
        state.timer_expiration = None 
        
        # 1st block: change of debate motions
        if motion.type == Motions.CHANGE_DEBATE_TYPE and motion.debate_type is not None: 

            state.caucus_list = []
            state.current_speaker = None 
            duration_seconds = (motion.total_duration_minutes * 60) if motion.total_duration_minutes is not None else 600 # defaults to 10 minutes as fallback

            match motion.debate_type:
                case DebateTypes.MODERATED_DEBATE:
                    next_state = States.MODERATED_CAUCUS 
                    state.debate = DebateContext(
                        debate_type=DebateTypes.MODERATED_DEBATE, 
                        return_state = state.current_state, 
                        total_duration_seconds = duration_seconds,
                        per_speaker_seconds = motion.per_speaker_seconds,
                        expires_at = datetime.now(timezone.utc) + timedelta(seconds=duration_seconds),
                    ) 
                    reset_timer(state, motion.per_speaker_seconds if motion.per_speaker_seconds is not None else 60)

                case DebateTypes.UNMODERATED_DEBATE:
                    next_state = States.UNMODERATED_CAUCUS
                    state.debate = DebateContext(
                        debate_type=DebateTypes.UNMODERATED_DEBATE, 
                        return_state = state.current_state, 
                        total_duration_seconds = duration_seconds,
                        per_speaker_seconds = None,
                        expires_at = datetime.now(timezone.utc) + timedelta(seconds=duration_seconds),
                    ) 
                    reset_timer(state) # should not display per_speaker timer

                case DebateTypes.SPEAKERS_LIST:
                    next_state = States.OPEN_GSL
                    state.debate = None
                    reset_timer(state, state.gsl_default_time_seconds)

                case _:
                    raise InvalidProceduralMove("Undefined debate type")
    
        match motion.type:
            case Motions.POSTPONE_SESSION: 
                # TODO: create a type of force_to_database function here? or query if it's a postpone session on service.py 
                pass
            case Motions.REOPEN_SESSION:
                # TODO: same as above
                pass
            case Motions.TOUR_DE_TABLE:
                # note: seems like belongs to debate type
                pass 
            case Motions.END_DEBATE:
                # clean gsl list
                state.gsl_queue = []
                state.debate = None
                reset_timer(state)
                next_state = States.VOTING_PROCEDURES # or VOTING_PREPARATION
                
            case Motions.VOTE_AMENDMENT:
                # note: seems more like an informal consultation
                pass 
            case Motions.VOTE_BY_ROLL_CALL:
                # will define the VotingContext for resolutions
                pass 
            case Motions.CLOSE_SPEAKERS_LIST: 
                next_state = States.CLOSED_GSL

            case Motions.REOPEN_SPEAKERS_LIST: 
                next_state = States.OPEN_GSL

            case Motions.SPLIT_PROPOSAL:
                # note: seems more like an informal consultation
                pass 
            case Motions.CHANGE_TOPIC:
                # note: seems more like an informal consultation
                pass
            case Motions.QUORUM:
                state.roll_call = RollCallContext(registry={})
                next_state = States.ROLL_CALL
            case _:
                raise InvalidProceduralMove("Undefined motion type")

        # additional case: if we went from GSL to something, save gsl structures
        state.current_state = next_state
    else:
        # motion failed, so return to last state 
        state.current_state = state.voting.return_state
    
    # clear state voting 
    state.voting = None
    return state


# handles setting state into VOTING_EXECUTION or rejecting the motion
def handle_resolve_motion(state: SessionLiveState, event: ResolveMotionEvent, sender: str, is_chair: bool) -> SessionLiveState:
    # TODO: check how to resolve INTRODUCE_RESOLUTION_PROPOSAL and INTRODUCE_AMENDMENT_PROPOSAL motions separately from procedural motions
    if not is_chair:
        raise InvalidProceduralMove("Not authorized")

    payload = event.payload 
    # next() function with generator expression
    motion = next((m for m in state.submitted_motions if m.id == payload.motion_id), None) 

    if motion is None:
        raise InvalidProceduralMove("Motion not found")
    
    if payload.action == "ACCEPT":
        state.voting = VotingContext(
                target_type="PROCEDURAL",
                motion_in_vote=motion,
                return_state=state.current_state,
                voting_registry={},
                majority='QUALIFIED', # TODO: change depending on type of motion
                veto_power=True
        )

        state.current_state = States.VOTING_EXECUTION
    
    state.submitted_motions.remove(motion)

    return state
    

def handle_set_agenda(state: SessionLiveState, event: SetAgendaEvent, sender: str, is_chair: bool) -> SessionLiveState:
    ...

def handle_manual_phase_set(state: SessionLiveState, event: SetPhaseEvent, sender: str, is_chair: bool) -> SessionLiveState:
    ...

def handle_choose_speaker(state: SessionLiveState, event: SpeakerEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if not is_chair:
        raise InvalidProceduralMove("Cannot choose speaker as delegate")

    seconds = event.payload.seconds or get_default_speaker_seconds(state)
    state.current_speaker = event.payload.speaker
    
    state.timer_is_running = False
    state.timer_expiration = None # will be calculated when timer is toggled 
    state.timer_remaining_seconds = seconds or 60 # default to something

    return state

def handle_mark_roll_call(state: SessionLiveState, event: MarkRollCallEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if not is_chair:
        raise InvalidProceduralMove("cannot mark roll call as delegate")
    if state.current_state != States.ROLL_CALL or state.roll_call is None:
        raise InvalidProceduralMove("Cannot mark roll call right now")

    
    state.roll_call.registry[event.payload.delegation_id] = event.payload.choice

    return state

def handle_close_roll_call(state: SessionLiveState, event: CloseRollCallEvent, sender: str, is_chair: bool) -> SessionLiveState:
    if not is_chair:
        raise InvalidProceduralMove("cannot close roll call as delegate")
    if state.current_state != States.ROLL_CALL or state.roll_call is None:
        raise InvalidProceduralMove("Cannot close roll call right now")

    # may also empty roll call if needed, to avoid loading stale values 
    state.current_state = States.OPEN_GSL
    state.voting_choice = {
            delegation: RollCallChoice.PRESENT_AND_VOTING if choice == RollCallChoice.PRESENT_AND_VOTING else RollCallChoice.PRESENT
            for delegation, choice in state.roll_call.registry.items() 
            if choice in {RollCallChoice.PRESENT, RollCallChoice.PRESENT_AND_VOTING}
    }
    state.roll_call = None
    return state

def handle_insert_queue(state: SessionLiveState, event: ChairInsertQueueEvent, sender: str, is_chair: bool)-> SessionLiveState:
    if not is_chair:
        raise InvalidProceduralMove("cannot insert someone on queue as delegate")
    delegate = state.delegations[event.payload.target]
    state.gsl_queue.append(delegate)
    return state

# Signature for events/handlers, uses legacy(ish) 3.11 TypeAlias
EventHandler: TypeAlias = Callable[
        [SessionLiveState, Any, str, bool], # overall signature
        SessionLiveState # Return type
        ]

# TODO: check if list has all events, since it's generated by codex
EVENT_HANDLERS: dict[DelegateEvents | ChairEvents, EventHandler] = {
      DelegateEvents.SUBMIT_MOTION: handle_submit_motion,
      DelegateEvents.SUBMIT_QUESTION: handle_submit_question,
      DelegateEvents.JOIN_QUEUE: handle_join_queue,
      DelegateEvents.LEAVE_QUEUE: handle_leave_queue,
      DelegateEvents.CAST_VOTE: handle_cast_vote,
      DelegateEvents.CHOOSE_DELEGATION: handle_choose_delegation,
      DelegateEvents.ANSWER_ROLLCALL: handle_answer_roll_call,

      ChairEvents.OPEN_SESSION: handle_open_session,
      ChairEvents.INCREASE_TIMER: handle_increase_timer,
      ChairEvents.TOGGLE_TIMER: handle_toggle_timer,
      ChairEvents.OPEN_INFORMAL_VOTING: handle_open_informal_voting,
      ChairEvents.CLOSE_INFORMAL_VOTING: handle_close_informal_voting,
      ChairEvents.CLOSE_PROCEDURAL_VOTING: handle_close_procedural_voting,
      ChairEvents.RESOLVE_MOTION: handle_resolve_motion,
      ChairEvents.SET_AGENDA: handle_set_agenda, 
      ChairEvents.MANUAL_PHASE_SET: handle_manual_phase_set,
      ChairEvents.CLOSE_SESSION: handle_close_session,
      ChairEvents.CHOOSE_SPEAKER: handle_choose_speaker,
      ChairEvents.MARK_ROLLCALL: handle_mark_roll_call,
      ChairEvents.CLOSE_ROLLCALL: handle_close_roll_call,
      ChairEvents.INSERT_QUEUE: handle_insert_queue
}

class SessionEngine:
    # function to calculate new state over old one
    def dispatch(self, 
                 state: SessionLiveState,
                 event: SessionEvent,
                 sender: str, 
                 is_chair: bool) -> SessionLiveState:

        handler = EVENT_HANDLERS.get(event.type)
        if handler is None:
            raise InvalidProceduralMove(f"Unsupported Type: {event.type}")
        
        return handler(state, event, sender, is_chair)
         
