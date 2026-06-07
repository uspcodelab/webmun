# where engine lives
from typing import Callable, Any

from .schemas import *
from .manager import SessionLiveState

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

ChooseDelegation should not be possible anymore (at least not for now)

ROLL_CALL: roll call/ quorum count state. Possible events are:
    - SetVotingChoiceEvent: by Delegate 
    - QuestionEvent
    - Any Chair Event: since most are disruptive

To user, INITIAL_DEBATE and OPEN_GSL should look mostly the same
INITIAL_DEBATE: after roll call, if no agenda is set and/or no speaking time for GSL is set, go to this state. It's an initial speakers list. Possible events are: 
    - Motions: subset - (POSTPONE, END, QUORUM, SETAGEND, SETSPEAKINGTIME) 
    - QuestionEvent
    - Any Chair Event
    - CastVoteEvent 
Queue should not be open to speak. Delegates may only speak in motions

OPEN_GSL: default state in general. Queue is open and automatic and all motions can be made. The topic is defaulted to the first one in the order of agenda_topics and index_topic.
    - In particular, YieldEvent must be enabled and configured.

Specific Debates: (Moderated, Unmoderated, Tour) Queue is not automatic, rather, it now serves as a list that Chair can accept someone.
    - Motions may only be set if set_motions is enabled.
    - In particular, Unmoderated should not have a queue/motions enabled at all, but this may be implemented later 

VOTIING_EXECUTION: may be to vote on a motion or on a specific resolution. Only after the chair enables voting on a motion. 

CLOSED_GSL: after a successfull 'Close Speakers List'. Queue is disabled.

PRE_VOTING: ambiguous state after an "close debate" has either entered as a motion, or "move into voting procedures"

VOTING_PROCEDURES: special case of voting on specific resolution

FINISHED: when topics get empty automatically, or chair decides to close session. may be reverted.

This will give some insight into what should or should not be possible during each event
"""

# Dispatch tables: alternative to if else chains
MOTIONS_ALLOWED: dict[States, set[Motions]] = {
    States.INITIAL_DEBATE: {
        Motions.CUSTOM_MOTION,
    },
    States.OPEN_GSL: {
        Motions.CHANGE_DEBATE_TYPE,
        Motions.POSTPONE_SESSION,
        Motions.REOPEN_SESSION,
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

# Validations and helpers
def generate_next_motion_id(state: SessionLiveState) -> int:
    if not hasattr(state, "_motion_id_counter"):
        state._motion_id_counter = 0
    state._motion_id_counter += 1
    return state._motion_id_counter

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
    if payload.type in {States.MODERATED_CAUCUS} and payload.total_speaking_seconds == None:
        raise InvalidProceduralMove("Cannot submit motion without speaking time")


# -------------- HANDLERS --------------
def handle_submit_motion(state: SessionLiveState, event: SubmitMotionEvent, sender: str, is_chair: bool) -> SessionLiveState:
    """Handles/Maps all possible states through a motion"""
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
    payload.delegate = sender
    state.submitted_motions.append(payload)
    
    return state


# defines the overall "interface" (as in golang?) for a function to be an EventHandler 
# Iremos ignorar o Event dado ao SessionEvent, assumindo que ele está sendo feito. 
# Podemos também remover o SessionEvent depois
type EventHandler = Callable[
        [SessionLiveState, Any, str, bool], # overall signature
        SessionLiveState # Return type
        ]

# TODO: check if list has all events, since it's generated by codex
EVENT_HANDLERS: dict[DelegateEvents | ChairEvents, EventHandler] = {
      DelegateEvents.SUBMIT_MOTION: handle_submit_motion,
      #DelegateEvents.SUBMIT_QUESTION: handle_submit_question,
      #DelegateEvents.JOIN_QUEUE: handle_join_queue,
      #DelegateEvents.LEAVE_QUEUE: handle_leave_queue,
      #DelegateEvents.CAST_VOTE: handle_cast_vote,
      #DelegateEvents.CHOOSE_DELEGATION: handle_choose_delegation,

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
         
